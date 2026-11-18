"""Bounded ten-shard lookahead partition and cover gate; no target conquer run."""
from concurrent.futures import ProcessPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['NO_PROOF'] = '1'
os.environ['SAT_SOLVER'] = shutil.which('kissat') or str(Path.home() / 'bin/kissat')
sys.path.insert(0, str(HERE.parent / 'E-261114-01-normalised-s6-10-3'))
from controls import pilot, topology


def formula(links):
    t = topology(links)
    c = pilot.CNF(t.n)
    pilot.build(c, t, dict(pilot.ALL_OPTS, symbreak=True, mirror=True))
    return c


def parse(path, nv):
    cubes = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('c '):
            continue
        fields = line.split()
        assert fields[0] == 'a' and fields[-1] == '0', line
        cube = list(map(int, fields[1:-1]))
        assert all(0 < abs(v) <= nv for v in cube), line
        assert len(set(map(abs, cube))) == len(cube), line
        cubes.append(cube)
    assert cubes, 'no complete cubes'
    return cubes


def shard(args):
    k, job, out = args
    dest = out / str(k); dest.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    report = dict(shard=k, job=job[0] if job else None, PASS=False, attempts=[])
    try:
        if job is None:
            report['PASS'] = True
            return report
        name, links, positive = job
        c = formula(links)
        cnf = dest / 'source.cnf'; c.dimacs(cnf)
        report.update(cnf_sha256=pilot.sha(cnf), variables=c.nv, clauses=len(c.clauses))
        cuber = shutil.which('march_cu') or str(Path.home() / 'bin/march_cu')
        report['cuber_sha256'] = pilot.sha(Path(cuber))
        for depth in (7, 8, 9, 10):
            path = dest / f'depth{depth}.cubes'
            before = time.monotonic()
            rc = pilot.command([cuber, str(cnf), '-d', str(depth), '-o', str(path)],
                               dest / f'depth{depth}.log', 60)
            attempt = dict(depth=depth, rc=rc, seconds=time.monotonic()-before,
                           ended_by='timeout' if rc is None else 'completed')
            report['attempts'].append(attempt)
            assert rc == 0, f'cuber unsuccessful exit {rc}'
            cubes = parse(path, c.nv)
            attempt.update(cubes=len(cubes), sha256=pilot.sha(path))
            if not 100 <= len(cubes) <= 500:
                continue
            report.update(depth=depth, cubes=cubes)
            original = len(c.clauses)
            c.clauses.extend([[-v for v in cube] for cube in cubes])
            cover = pilot.solve(c, dest, 'cover', 60)
            del c.clauses[original:]
            report['cover'] = cover
            assert cover['status'] == 'UNSAT-SOLVER', 'cover failed or unresolved'
            if positive:
                report['conquer'] = []
                remaining = 120
                for i, cube in enumerate(cubes):
                    if remaining <= 0:
                        break
                    c.clauses.extend([[v] for v in cube])
                    r = pilot.solve(c, dest, f'cube{i}', min(60, remaining))
                    del c.clauses[original:]
                    remaining -= r['seconds']
                    report['conquer'].append(r)
                    if r['status'] == 'SAT':
                        model = json.loads((dest / f'cube{i}.model.json').read_text())
                        assert pilot.model_valid(c.clauses, model)
                        break
                assert any(r['status'] == 'SAT' for r in report['conquer']), 'positive pipeline failed'
            report['PASS'] = True
            break
        assert report['PASS'], 'no eligible completed partition at depths 7..10'
    except Exception as exc:
        report['error'] = str(exc)
    finally:
        report.update(seconds=time.monotonic()-started, python=sys.version,
                      solver_sha256=pilot.sha(Path(pilot.CADICAL)),
                      commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
        pilot.dump(dest / 'result.json', report)
    return report


def main():
    out = HERE / 'results/prep'
    out.mkdir(parents=True, exist_ok=False)
    target = ROOT / 'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json'
    control = ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/maps/seeded_formulas.json'
    jobs = [(f"lutz{m['lutz']}",m['links'],False) for m in json.loads(target.read_text())['maps'][:2]]
    m = next(m for m in json.loads(control.read_text())['maps'] if m['lutz'] == 739)
    jobs.insert(0, ('control739',m['links'],True))
    with ProcessPoolExecutor(10) as pool:
        rows = list(pool.map(shard, [(k,jobs[k] if k<len(jobs) else None,out) for k in range(10)]))
    result = dict(PASS=all(r['PASS'] for r in rows), rows=rows,
                  inputs_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in
                                 (Path(__file__), target, control, Path(pilot.__file__), ROOT/'code/omsat.py')})
    pilot.dump(out/'summary.json',result)
    print(json.dumps(dict(PASS=result['PASS'], rows=[{k:r[k] for k in ('job','PASS','seconds','error') if k in r} for r in rows])))


if __name__ == '__main__':
    main()
