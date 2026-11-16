"""Normalised A+B night using the existing checkpoint, budget and solver primitives."""
import json
from pathlib import Path
import resource
import subprocess
import time

import prep
from prep import HERE, ROOT, pilot, tranche


def run(args):
    out = Path(args.results_dir).resolve(); root = out.parent
    shard, shards = args.shard, args.shards
    if args.workers != 1 or not 8 <= shards <= 10 or not 0 <= shard < shards or out.name != str(shard):
        raise ValueError('requires 8..10 single-worker shards and numeric results directory')
    out.mkdir(parents=True, exist_ok=True)
    queue_path = Path(args.s5_queue or HERE / 'queue.json')
    queue = json.loads(queue_path.read_text())
    provenance = prep.controls()
    for name, digest in queue['inputs_sha256'].items():
        assert pilot.sha(ROOT / name) == digest, name
    identity = dict(queue=pilot.sha(queue_path), controls=provenance,
                    sources={p.name: pilot.sha(p) for p in (Path(__file__), HERE/'prep.py', HERE/'run.sh')})
    tranche.BUDGET_SECONDS = args.s5_budget_seconds
    tranche.BRIDGE = dict(submap=False, restarts=6)
    with tranche.locked(root / f'shard{shard}.lock', blocking=False):
        tranche.check_identity(root, identity)
        start = time.monotonic(); epoch = time.time()
        def cpu():
            a = resource.getrusage(resource.RUSAGE_SELF); b = resource.getrusage(resource.RUSAGE_CHILDREN)
            return a.ru_utime+a.ru_stime+b.ru_utime+b.ru_stime
        initial = cpu()
        allowance = min(args.hours*3600, tranche.BUDGET_SECONDS/shards-tranche.shard_charged(root, shard))
        if allowance <= 0:
            return
        key = tranche.reserve(root, allowance, shard)
        deadline = start + allowance
        command = pilot.command
        def bounded(argv, log, timeout, gate=None):
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise TimeoutError('shard deadline exhausted')
            return command(argv, log, min(timeout, remaining), gate)
        pilot.command = bounded
        manifest = dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
                        shard=shard, shards=shards, controls=provenance, allowance_seconds=allowance)
        try:
            for entry in queue['maps'][shard::shards]:
                if tranche.stopped(root):
                    break
                index = entry['index']
                records = [r for p in root.glob('[0-9]*/results.jsonl') for r in tranche.records(p)]
                if any(r['map_index'] == index for r in records):
                    continue
                if deadline-time.monotonic() < entry['solver_cap']+10:
                    break
                dest = out / f'map{index}'; dest.mkdir(exist_ok=True)
                tranche.append_checkpoint(out/'progress.jsonl', dict(map_index=index, event='START'))
                print(f'map {index} start', flush=True)
                t = pilot.from_links(pilot.census(10,4)['maps'][index]['links'])
                c = pilot.CNF(t.n); pilot.build(c,t,dict(pilot.ALL_OPTS,symbreak=True,mirror=True))
                rows = tranche.records(dest/'models.jsonl')
                for seed in range(30):
                    if rows and rows[0]['status'] != 'SAT':
                        break
                    if tranche.stopped(root):
                        break
                    if any(r['seed'] == seed for r in rows):
                        continue
                    pilot.SOLVER_OPTS = [f'--seed={seed}']
                    name = f'map{index}_seed{seed}'
                    state = dest / (name + '.json')
                    r = json.loads(state.read_text()) if state.exists() else dict(seed=seed, **pilot.solve(c,dest,name,entry['solver_cap']))
                    tranche.atomic(state,r)
                    if r['status'] == 'SAT' and 'processing' not in r:
                        r.update(tranche.bridge(dest,name,c,t.link,'S5'))
                        tranche.atomic(state,r)
                    tranche.append_checkpoint(dest/'models.jsonl',r); rows.append(r)
                    if r.get('candidate_verify_rc') == 0:
                        tranche.atomic(root/'stop.json',dict(reason='CANDIDATE-NEEDS-REVIEW',map_index=index))
                        break
                    if r['status'] == 'ERROR':
                        raise RuntimeError(f'map {index}, seed {seed}: ERROR')
                    if seed == 0 and r['status'] != 'SAT':
                        break
                if not rows:
                    break
                result = dict(map_index=index, status=rows[0]['status'], models=rows,
                              seconds=sum(r['seconds'] for r in rows), pattern=entry['pattern'],
                              bridge_complete=rows[0]['status'] != 'SAT' or sum(r['status']=='SAT' for r in rows)>=30)
                tranche.append_checkpoint(out/'results.jsonl',result)
                print(f"map {index} {result['status']}",flush=True)
        except TimeoutError:
            manifest['deadline_stop'] = True
        except (KeyboardInterrupt, InterruptedError):
            manifest['interrupted'] = True
            raise
        except BaseException as exc:
            manifest['error'] = repr(exc)
            tranche.atomic(root/'stop.json',dict(error=repr(exc)))
            raise
        finally:
            pilot.command = command
            manifest.update(wall_seconds=time.monotonic()-start,cpu_seconds=cpu()-initial,
                            endpoint_clock_gap=time.time()-epoch-(time.monotonic()-start))
            tranche.atomic(out/f'manifest-{time.time_ns()}.json',manifest)
            tranche.finish_reservation(root,key,manifest['wall_seconds'])
