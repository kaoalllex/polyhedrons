"""Owner-run conquer stage using the existing checkpoint, identity and budget helpers."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prep
from prep import HERE, ROOT, pilot, formula
import tranche


def run(args):
    shard, shards = args.shard, args.shards
    out = Path(args.results_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    root = out.parent
    summary = HERE / 'results/prep/summary.json'
    data = json.loads(summary.read_text()); assert data['PASS']
    for path, digest in data['inputs_sha256'].items():
        assert pilot.sha(ROOT / path) == digest, path
    identity = dict(prep_sha256=pilot.sha(summary), sources={str(p.relative_to(ROOT)):pilot.sha(p) for p in
                    (Path(__file__), Path(prep.__file__), Path(tranche.__file__), Path(pilot.__file__))},
                    solver_sha256=pilot.sha(Path(pilot.CADICAL)))
    tranche.check_identity(root, identity)
    with tranche.locked(root/'budget.lock'):
        if not (root/'budget.json').exists():
            tranche.atomic(root/'budget.json', dict(mono1=3660, mono2=3660,
                           prep=sum(r['seconds'] for r in data['rows'])))
    tranche.BUDGET_SECONDS = 28800
    targets = [r for r in data['rows'] if r.get('job') in ('lutz1','lutz2')]
    maps = json.loads((ROOT/'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json').read_text())['maps']
    tasks = [(r['job'],None) for r in targets] + [(r['job'],i) for i in range(128) for r in targets]
    assert all(len(r['cubes']) == 128 for r in targets)
    done = {r['task'] for p in root.glob('[0-9]*/results.jsonl') for r in tranche.records(p)}
    limit = int(os.environ.get('S6CUBE_SMOKE_LIMIT', len(tasks)))
    started = time.monotonic(); count = 0
    for j,(name,i) in enumerate(tasks):
        task = name + ('_mono' if i is None else f'_cube{i}')
        if j % shards != shard or task in done:
            continue
        if tranche.stopped(root) or count >= limit:
            break
        count += 1
        cap = 3600 if i is None else 600
        try:
            if i is None:
                key = 'mono'+name[-1]
                with tranche.locked(root/'dispatch.lock'):
                    claim = root / (key+'.claimed')
                    first = not claim.exists()
                    if first:
                        tranche.atomic(claim, dict(shard=shard))
                if not first:
                    key = tranche.reserve(root, cap+60, shard)
            else:
                key = tranche.reserve(root, cap+60, shard)
        except RuntimeError:
            break
        before = time.monotonic()
        dest = out / f'attempt_{time.time_ns()}'; dest.mkdir()
        print(f'{task} started cap={cap}', flush=True)
        try:
            c = formula(next(m['links'] for m in maps if 'lutz'+str(m['lutz']) == name))
            if i is not None:
                cube = next(r['cubes'][i] for r in targets if r['job'] == name)
                c.clauses.extend([[v] for v in cube])
            pilot.SOLVER_OPTS = ['--sat'] if i is None else []
            with tranche.dispatch_gate(root):
                pass
            r = pilot.solve(c, dest, task, cap, solver_gate=lambda: tranche.dispatch_gate(root))
            r.update(task=task, target='S6 (10,3)', cube=i, map=name, solver_opts=pilot.SOLVER_OPTS,
                     unit=str(dest.relative_to(ROOT)), total_seconds=time.monotonic()-before)
            pilot.dump(dest/'result.json',r)
            tranche.append_checkpoint(out/'results.jsonl',r)
            tranche.finish_reservation(root,key,r['total_seconds'])
            print(task,r['status'],flush=True)
            if r['status'] == 'SAT':
                tranche.latch_sat(root,r)
                break
            if r['status'] == 'ERROR':
                tranche.atomic(root/'stop.json',r)
                break
        except tranche.DispatchStopped:
            tranche.finish_reservation(root,key,time.monotonic()-before)
            break
    pilot.dump(out/f'manifest-{time.time_ns()}.json', dict(wall_seconds=time.monotonic()-started,
               commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
               python=sys.version, identity=identity, shard=shard, shards=shards))
