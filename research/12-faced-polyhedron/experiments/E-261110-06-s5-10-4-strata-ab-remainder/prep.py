"""Bounded normalised cost probe; reuse unchanged controls and completed timing units."""
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPO = ROOT.parents[1]
SOURCE = HERE.parent / 'E-261114-01-normalised-s6-10-3'
os.environ['NO_PROOF'] = '1'
os.environ['SAT_SOLVER'] = shutil.which('kissat') or str(Path.home() / 'bin/kissat')
os.environ['SOLVER_OPTS'] = '--seed=0'
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS'):
    os.environ[key] = '1'
sys.path.insert(0, str(HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot
import tranche


def controls():
    env = json.loads((SOURCE / 'results/environment.json').read_text())
    assert env['python'] == sys.version, 'Python changed'
    deps = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True).splitlines()
    assert sorted(deps) == sorted(env['dependencies']), 'dependencies changed'
    assert pilot.sha(Path(pilot.CADICAL)) == env['solver_sha256'], 'solver changed'
    for name, digest in env['inputs_sha256'].items():
        assert pilot.sha(REPO / name) == digest, name
    report = dict(environment_sha256=pilot.sha(SOURCE / 'results/environment.json'), gates={})
    for gate in ('invariance', 'positive', 'negative'):
        path = SOURCE / 'results' / gate / 'summary.json'
        data = json.loads(path.read_text()); assert data['PASS'], gate
        for name, digest in data['inputs_sha256'].items():
            # pilot.py gained the already-checked optimizer_seed option after these gates.
            if name.endswith('/pilot.py'):
                assert pilot.sha(ROOT / name) == env['inputs_sha256'][str((ROOT / name).relative_to(REPO))]
            else:
                assert pilot.sha(ROOT / name) == digest, name
        report['gates'][gate] = pilot.sha(path)
    return report


def cached():
    result = {}
    for path in (SOURCE / 'results/negative').glob('[0-9]*/results.json'):
        for row in json.loads(path.read_text()):
            if row['name'] in ('f10_map845', 'f10_map96', 'f10_map85'):
                assert row['status'] == 'UNSAT-SOLVER'
                log = path.parent / (row['name'] + '.solver.log')
                assert 's UNSATISFIABLE' in log.read_text()
                result[int(row['name'].split('map')[1])] = dict(row, reused_from=str(path.relative_to(ROOT)),
                                                              solver_log_sha256=pilot.sha(log))
    assert len(result) == 3
    return result


def shard(args):
    k, out, entries, reuse = args
    dest = out / str(k); dest.mkdir(parents=True, exist_ok=True)
    start = time.monotonic(); wall = time.time()
    def cpu():
        a = resource.getrusage(resource.RUSAGE_SELF); b = resource.getrusage(resource.RUSAGE_CHILDREN)
        return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime
    initial = cpu()
    done = {r['map_index'] for r in tranche.records(dest / 'results.jsonl')}
    for entry in entries:
        index = entry['index']
        if index in done:
            continue
        before = time.monotonic()
        if index in reuse:
            row = dict(reuse[index])
            row['total_seconds'] = row['seconds']  # original build time was not measured per unit
            row['total_is_solver_lower_bound'] = True
        else:
            t = pilot.from_links(pilot.census(10, 4)['maps'][index]['links'])
            c = pilot.CNF(t.n); pilot.build(c, t, dict(pilot.ALL_OPTS, symbreak=True, mirror=True))
            row = pilot.solve(c, dest, f'map{index}', 1800)
            row['total_seconds'] = time.monotonic() - before
        row.update(map_index=index, pattern=entry['pattern'])
        tranche.append_checkpoint(dest / 'results.jsonl', row)
        print(f"shard {k} map {index}: {row['status']} {row['seconds']:.3f}s", flush=True)
        if row['status'] in ('SAT', 'ERROR'):
            # Save the initial checked model first; the registered 30-model bridge is a separate stage.
            break
    pilot.dump(dest / f'manifest-{time.time_ns()}.json', dict(shard=k, cpu_seconds=cpu()-initial,
               wall_seconds=time.monotonic()-start, endpoint_clock_gap=time.time()-wall-(time.monotonic()-start),
               commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
               python=sys.version, solver_sha256=pilot.sha(Path(pilot.CADICAL))))


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    provenance = controls()
    queue = HERE.parent / 'E-261103-07-s5-10-4-census-symmetry/queue_probe.json'
    entries = [r for r in json.loads(queue.read_text())['maps'] if isinstance(r['index'], int)]
    assert len(entries) == 10
    identity = dict(controls=provenance, queue_sha256=pilot.sha(queue), source_sha256=pilot.sha(Path(__file__)))
    path = out / 'identity.json'
    if path.exists():
        assert json.loads(path.read_text()) == identity, 'resume identity changed'
    pilot.dump(path, identity)
    reuse = cached()
    with ProcessPoolExecutor(10) as pool:
        list(pool.map(shard, [(k, out, entries[k::10], reuse) for k in range(10)]))
    rows = [r for p in out.glob('[0-9]*/results.jsonl') for r in tranche.records(p)]
    by_id = {r['map_index']: r for r in rows}
    assert len(rows) == len(by_id) == 10
    summary = dict(statuses={s: sum(r['status'] == s for r in rows) for s in ('SAT','UNSAT-SOLVER','TIMEOUT','ERROR')},
                   rows=rows, control_reuse=provenance)
    samples = [by_id[i] for i in (96,926,85,852)]
    summary['projection_censored'] = any(r['status'] == 'TIMEOUT' for r in samples)
    for field in ('seconds', 'total_seconds'):
        summary['projected_' + field + '_core_hours'] = (520 * sum(by_id[i][field] for i in (96,926)) / 2 +
                                                         237 * sum(by_id[i][field] for i in (85,852)) / 2) / 3600
    summary['night_gate'] = (not summary['projection_censored'] and not summary['statuses']['ERROR'] and
                             not summary['statuses']['SAT'] and summary['statuses']['TIMEOUT'] < 10)
    pilot.dump(out / 'summary.json', summary)
    print(json.dumps({k:v for k,v in summary.items() if k != 'rows'}), flush=True)


if __name__ == '__main__':
    main(Path(sys.argv[1]))
