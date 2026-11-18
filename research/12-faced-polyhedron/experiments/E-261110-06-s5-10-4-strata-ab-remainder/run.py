"""Normalised A+B night using the existing checkpoint, budget and solver primitives."""
import gzip
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

import prep
from prep import HERE, ROOT, pilot, tranche


def run(args):
    invocation_start = time.monotonic(); invocation_epoch = time.time()
    def cpu():
        a = resource.getrusage(resource.RUSAGE_SELF); b = resource.getrusage(resource.RUSAGE_CHILDREN)
        return a.ru_utime+a.ru_stime+b.ru_utime+b.ru_stime
    invocation_cpu = cpu()
    out = Path(args.results_dir).resolve(); root = out.parent
    shard, shards = args.shard, args.shards
    if args.workers != 1 or not 8 <= shards <= 10 or not 0 <= shard < shards or out.name != str(shard):
        raise ValueError('requires 8..10 single-worker shards and numeric results directory')
    out.mkdir(parents=True, exist_ok=True)
    queue_path = Path(args.s5_queue or HERE / 'queue.json')
    queue = json.loads(queue_path.read_text())
    topology = pilot.from_links
    if queue.get('submap'):
        sys.path.insert(0, str(ROOT / 'experiments/E-261114-01-normalised-s6-10-3'))
        from controls import topology
    provenance = prep.controls()
    if queue.get('controls_file'):
        assert json.loads((ROOT / queue['controls_file']).read_text())['PASS'], 'size controls failed'
    for name, digest in queue['inputs_sha256'].items():
        assert pilot.sha(ROOT / name) == digest, name
    identity = dict(queue=pilot.sha(queue_path), controls=provenance,
                    sources={p.name: pilot.sha(p) for p in (Path(__file__), HERE/'prep.py', HERE/'run.sh')})
    case = queue.get('case', [10, 4])
    if queue.get('census_file'):
        path = ROOT / queue['census_file']
        with (gzip.open(path, 'rt') if path.suffix == '.gz' else path.open()) as stream:
            maps = json.load(stream)
    else:
        maps = pilot.census(*case)
    tranche.BUDGET_SECONDS = args.s5_budget_seconds
    tranche.BRIDGE = dict(submap=False, restarts=6)
    with tranche.locked(root / f'shard{shard}.lock', blocking=False):
        tranche.check_identity(root, identity)
        start = invocation_start if queue.get('truncate_to_budget') else time.monotonic()
        epoch = invocation_epoch if queue.get('truncate_to_budget') else time.time()
        initial = invocation_cpu if queue.get('truncate_to_budget') else cpu()
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
                        branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],text=True)),
                        python=sys.version, platform=platform.platform(), workers=1,
                        started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(epoch)),
                        solver_sha256=pilot.sha(Path(pilot.CADICAL)),
                        shard=shard, shards=shards, controls=provenance, allowance_seconds=allowance)
        try:
            for entry in queue['maps'][shard::shards]:
                if tranche.stopped(root):
                    break
                index = entry['index']
                records = [r for p in root.glob('[0-9]*/results.jsonl') for r in tranche.records(p)]
                if any(r['map_index'] == index for r in records):
                    continue
                if deadline-time.monotonic() < (1 if queue.get('truncate_to_budget') and not queue.get('full_cap') else entry['solver_cap']+10):
                    break
                dest = out / f'map{index}'; dest.mkdir(exist_ok=True)
                tranche.append_checkpoint(out/'progress.jsonl', dict(map_index=index, event='START'))
                print(f'map {index} start', flush=True)
                build_start = time.monotonic()
                t = topology(maps['maps'][index]['links'])
                assert t.n == case[0]
                c = pilot.CNF(t.n); pilot.build(c,t,dict(pilot.ALL_OPTS,symbreak=True,mirror=True))
                build_seconds = time.monotonic()-build_start
                rows = tranche.records(dest/'models.jsonl')
                for seed in range(30):
                    if rows and rows[0]['status'] != 'SAT':
                        break
                    if tranche.stopped(root):
                        break
                    if any(r['seed'] == seed for r in rows):
                        continue
                    pilot.SOLVER_OPTS = queue.get('solver_opts', []) + ([] if queue.get('stop_on_sat') else [f'--seed={seed}'])
                    name = f'map{index}_seed{seed}'
                    state = dest / (name + '.json')
                    cap = min(entry['solver_cap'], deadline-time.monotonic()-1) if queue.get('truncate_to_budget') else entry['solver_cap']
                    if cap <= 0:
                        break
                    gate = dict(solver_gate=lambda: tranche.dispatch_gate(root)) if queue.get('stop_on_sat') else {}
                    r = json.loads(state.read_text()) if state.exists() else dict(seed=seed, **pilot.solve(c,dest,name,cap,**gate))
                    r['solver_opts'] = pilot.SOLVER_OPTS
                    tranche.atomic(state,r)
                    if r['status'] == 'SAT' and queue.get('stop_on_sat'):
                        tranche.latch_sat(root, dict(r, map_index=index, unit=str(dest.relative_to(ROOT.resolve()))))
                        tranche.append_checkpoint(dest/'models.jsonl',r); rows.append(r)
                        break
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
                              build_seconds=build_seconds, price_seconds=build_seconds+rows[0]['seconds'],
                              bridge_complete=rows[0]['status'] != 'SAT' or sum(r['status']=='SAT' for r in rows)>=30)
                tranche.append_checkpoint(out/'results.jsonl',result)
                print(f"map {index} {result['status']}",flush=True)
        except tranche.DispatchStopped:
            manifest['dispatch_stopped'] = True
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
