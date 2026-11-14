"""Exact re-charting controls and bounded vertex-cube pilot; see PLAN.md."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPO = ROOT.parents[1]
PREVIOUS = HERE.parent / 'E-261114-01-normalised-s6-10-3'
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMBA_NUM_THREADS'):
    os.environ[key] = '1'
spec = importlib.util.spec_from_file_location('normalised_controls', PREVIOUS / 'controls.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
pilot = previous.pilot
from omsat import Eval, Predicates, det4
from ladder_exact import solve3
import numpy as np
from scipy.optimize import linprog
import sympy as sp

OPTS = dict(pilot.ALL_OPTS, symbreak=True, mirror=True)


def selector(b, t, vertex, reverse=False):
    """One selected vertex, not a partition of the abstract OM models."""
    p = Predicates(b, t)
    inward_negative = {}
    for a in vertex:
        x, y = [i for i in vertex if i != a]
        d = t.other_partner(x, y, a)
        inward_negative[a] = p.sd(x, y, d, a)
        if reverse:
            inward_negative[a] = b.NOT(inward_negative[a])
        b.clause([b.NOT(p.REFLEX(a, x, y))], 'HULL_CONVEX')
    for q in itertools.combinations(range(t.n), 3):
        terms = [b.xor([b.chi_neg((*q, a)), inward_negative[a]]) for a in vertex if a not in q]
        if not terms:
            continue
        inf = b.chi_neg((*q, t.n))
        b.clause(terms + [b.NOT(inf)], 'HULL_POSITIVE')
        b.clause([b.NOT(v) for v in terms] + [inf], 'HULL_NEGATIVE')


def integer_rows(rows):
    result = []
    for row in rows:
        denominator = math.lcm(*(x.denominator for x in row))
        values = [int(x * denominator) for x in row]
        divisor = math.gcd(*values)
        result.append([x // divisor for x in values])
    return result


def value(h, p):
    return sum(a * b for a, b in zip(h[:3], p)) + h[3]


def support(h, t, vertex, points):
    """An exact exposing plane, or an exact nonextreme-point certificate; LP only proposes."""
    inward = []
    for a in vertex:
        x, y = [i for i in vertex if i != a]
        d = t.other_partner(x, y, a)
        scale = value(h[a], points[tuple(sorted((x, y, d)))])
        assert scale
        inward.append([x / scale for x in h[a]])
    others = [q for q in points if q != vertex]
    matrix = [[value(row, points[q]) for row in inward] for q in others]
    proposal = linprog(np.zeros(3), A_ub=-np.array(matrix, dtype=float),
                       b_ub=-np.ones(len(others)), bounds=[(1, None)] * 3,
                       method='highs', options={'time_limit': 5})
    if proposal.success:
        weights = [F(float(x)).limit_denominator(10**9) for x in proposal.x]
        plane = [sum(w * row[k] for w, row in zip(weights, inward)) for k in range(4)]
        if all(w > 0 for w in weights) and all(value(plane, points[q]) > 0 for q in others):
            assert value(plane, points[vertex]) == 0
            return plane, dict(kind='hull', weights=list(map(str, weights)),
                               inward=[[str(x) for x in row] for row in inward])
    # Never classify a numerical infeasibility as a non-hull vertex.
    a = [[*points[q], F(1)] for q in others]
    target = [*points[vertex], F(1)]
    combination = linprog(np.zeros(len(others)), A_eq=np.array(a, dtype=float).T,
                          b_eq=np.array(target, dtype=float), bounds=(0, None),
                          method='highs', options={'time_limit': 5})
    assert combination.success, ('hull classification unresolved', vertex, proposal.message)
    active = [i for i, x in enumerate(combination.x) if x > 0]
    exact, parameters = sp.Matrix([a[i] for i in active]).T.gauss_jordan_solve(sp.Matrix(target))
    assert not parameters.rows
    weights = [F(x) for x in exact]
    assert all(w >= 0 for w in weights) and sum(weights) == 1
    assert all(sum(w * a[i][k] for w, i in zip(weights, active)) == target[k] for k in range(4))
    return None, dict(kind='nonhull', vertices=[others[i] for i in active], weights=list(map(str, weights)))


def rechart(h, vertex, point, plane):
    e = (0, 0, 0, 1)
    bounds = [F(1)]
    for q in itertools.combinations(range(len(h)), 3):
        d0 = det4([h[i] for i in q] + [plane])
        di = det4([h[i] for i in q] + [e])
        assert di
        if d0:
            bounds.append(abs(d0 / (2 * di)))
    epsilon = min(bounds)
    # Coordinates y=(x-v)/(h_0(x)+epsilon); det of this homogeneous map is epsilon>0.
    transformed = []
    for row in h:
        at_vertex = value(row, point)
        transformed.append([epsilon * row[k] - at_vertex * plane[k] for k in range(3)] + [at_vertex])
    result = integer_rows(transformed)
    assert all(pilot.chirotope_from_planes(result).values())
    return result, epsilon


def cpu_seconds():
    return sum(u.ru_utime + u.ru_stime for u in
               (resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)))


def pin(c, chi):
    c.clauses.extend([[c.qvar[q] if s > 0 else -c.qvar[q]] for q, s in chi.items()])


def control(name, h, t, out, deadline):
    points = {tuple(sorted(v)): solve3([h[i] for i in sorted(v)]) for v in t.tris}
    records = []
    negative_done = False
    for vertex, point in sorted(points.items()):
        assert time.monotonic() < deadline, 'control shard budget exhausted'
        plane, certificate = support(h, t, vertex, points)
        row = dict(vertex=vertex, certificate=certificate)
        if plane is not None:
            transformed, epsilon = rechart(h, vertex, point, plane)
            assert all(value(plane, q) + epsilon > 0 for q in points.values())
            stem = name + '_' + '_'.join(map(str, vertex))
            path = out / (stem + '.json')
            pilot.dump(path, dict(planes=transformed, links=t.link))
            log = out / (stem + '.checker.log')
            rc = pilot.command([sys.executable, str(ROOT / 'verification/verify_candidate.py'), str(path)],
                               log, min(30, deadline - time.monotonic()))
            assert rc == 0, ('rechart verifier failed', stem, rc, log.read_text())
            chi = pilot.chirotope_from_planes(transformed)
            chi, gauge = previous.gauge(chi, t.n, True)
            direct = Eval(t.n, chi)
            pilot.build(direct, t, OPTS)
            selector(direct, t, vertex)
            assert not direct.violations, (stem, direct.violations)
            c = pilot.CNF(t.n)
            pilot.build(c, t, OPTS)
            selector(c, t, vertex)
            pin(c, chi)
            solved = pilot.solve(c, out, stem, min(10, deadline - time.monotonic()))
            assert solved['status'] == 'SAT', (stem, solved)
            row.update(epsilon=str(epsilon), support_plane=list(map(str, plane)), gauge=gauge,
                       candidate=path.name, candidate_sha256=pilot.sha(path), verifier_rc=rc,
                       checker_sha256=pilot.sha(log), formula=solved)
            if not negative_done:
                wrong = Eval(t.n, chi)
                selector(wrong, t, vertex, reverse=True)
                assert wrong.violations, 'outward sign mutation undetected'
                c = pilot.CNF(t.n)
                selector(c, t, vertex, reverse=True)
                pin(c, chi)
                negative = pilot.solve(c, out, stem + '_wrong_orientation', min(10, deadline - time.monotonic()))
                assert negative['status'] == 'UNSAT-SOLVER', negative
                row['negative'] = dict(violations=wrong.violations, formula=negative)
                negative_done = True
        records.append(row)
        pilot.dump(out / (name + '.controls.json'), records)
    assert negative_done
    return dict(name=name, hull=sum(r['certificate']['kind'] == 'hull' for r in records),
                nonhull=sum(r['certificate']['kind'] == 'nonhull' for r in records), PASS=True)


def shard(args):
    k, out, jobs, mode = args
    dest = out / str(k)
    dest.mkdir(parents=True)
    start, wall, cpu = time.monotonic(), time.time(), cpu_seconds()
    cap = 144 if mode == 'controls' else 36
    rows = []
    manifest = dict(shard=k, shards=10, started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                    commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                    dirty=subprocess.check_output(['git', 'status', '--porcelain'], text=True),
                    python=sys.version, host=platform.node(), platform=platform.platform(),
                    solver_sha256=pilot.sha(Path(pilot.CADICAL)), budget_seconds=cap, mode=mode)
    pilot.dump(dest / 'manifest.json', manifest)
    def expired(signum, frame):
        raise TimeoutError('shard wall budget exhausted')
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, cap)
    try:
        for job in jobs:
            if mode == 'controls':
                name, h, t = job
                print(f'shard {k}: {name}', flush=True)
                rows.append(control(name, h, t, dest, start + cap))
            else:
                name, t, vertex = job
                c = pilot.CNF(t.n)
                pilot.build(c, t, OPTS)
                selector(c, t, vertex)
                r = pilot.solve(c, dest, name, min(10, start + cap - time.monotonic()))
                rows.append(dict(name=name, vertex=vertex, **r))
                assert r['status'] != 'ERROR', r
            pilot.dump(dest / 'results.json', rows)
        manifest['PASS'] = True
    except Exception as exc:
        manifest.update(PASS=False, error=repr(exc))
        print(f'shard {k}: ERROR {exc!r}', flush=True)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        elapsed = time.monotonic() - start
        manifest.update(wall_seconds=elapsed, core_hours=elapsed / 3600,
                        cpu_seconds=cpu_seconds() - cpu, sleep_gap_seconds=time.time() - wall - elapsed,
                        outputs_sha256={p.name: pilot.sha(p) for p in dest.iterdir()
                                        if p.is_file() and p.name != 'manifest.json'})
        pilot.dump(dest / 'manifest.json', manifest)
    return rows, manifest


def reuse():
    environment = json.loads((PREVIOUS / 'results/environment.json').read_text())
    for path, digest in environment['inputs_sha256'].items():
        assert pilot.sha(REPO / path) == digest, ('changed baseline dependency', path)
    assert pilot.sha(Path(pilot.CADICAL)) == environment['solver_sha256']
    dependencies = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True).splitlines()
    assert dependencies == environment['dependencies'], 'changed Python environment'
    for gate in ('invariance', 'positive', 'negative'):
        assert json.loads((PREVIOUS / f'results/{gate}/summary.json').read_text())['PASS']
    return dict(environment_sha256=pilot.sha(PREVIOUS / 'results/environment.json'),
                gates={g: pilot.sha(PREVIOUS / f'results/{g}/summary.json')
                       for g in ('invariance', 'positive', 'negative')})


def main(mode, out):
    assert mode in ('controls', 'small')
    reused = reuse()
    jobs = []
    if mode == 'controls':
        topology = {name: t for name, h, t in previous.jobs() if h is not None}
        for path in sorted((PREVIOUS / 'results/positive').glob('*/controls.json')):
            for record in json.loads(path.read_text()):
                if 'planes' in record:
                    h = [[F(v) for v in row] for row in record['planes']]
                    jobs.append((record['name'], h, topology[record['name']]))
        assert len(jobs) == 23
    else:
        gate = HERE / 'results/controls/summary.json'
        assert json.loads(gate.read_text())['PASS'], 'rechart gate failed'
        maps = json.loads((ROOT / 'experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json').read_text())['maps'][:2]
        for m in maps:
            t = previous.topology(m['links'])
            c = pilot.CNF(t.n)
            pilot.build(c, t, OPTS)
            name = f"lutz{m['lutz']}"
            old = json.loads((PREVIOUS / f"results/pilot/{m['lutz'] - 1}/results.json").read_text())[0]
            baseline = HERE / f'.{name}.cnf'
            c.dimacs(baseline, comments=[name, 'S5 pilot; interpret symmetry and model scope separately'])
            assert pilot.sha(baseline) == old['cnf_sha256'], 'baseline formula changed'
            baseline.unlink()
            for j, vertex in enumerate(sorted(tuple(sorted(v)) for v in t.tris)[:5]):
                jobs.append((f'{name}_v{j}', t, vertex))
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    with ProcessPoolExecutor(10) as pool:
        answers = list(pool.map(shard, [(k, out, jobs[k::10], mode) for k in range(10)]))
    rows = [r for part, _ in answers for r in part]
    report = dict(mode=mode, PASS=len(rows) == len(jobs) and all(m['PASS'] for _, m in answers),
                  completed=len(rows), expected=len(jobs), reused=reused, wall_seconds=time.monotonic() - started,
                  worker_core_hours=sum(m['core_hours'] for _, m in answers),
                  cpu_seconds=sum(m['cpu_seconds'] for _, m in answers),
                  inputs_sha256={str(p.relative_to(REPO)): pilot.sha(p) for p in
                                 (Path(__file__), HERE / 'SOUNDNESS.md', HERE / 'PLAN.md', PREVIOUS / 'controls.py')})
    if mode == 'controls':
        report.update(hull=sum(r['hull'] for r in rows), nonhull=sum(r['nonhull'] for r in rows))
    else:
        report['statuses'] = {s: sum(r['status'] == s for r in rows) for s in ('SAT', 'UNSAT-SOLVER', 'TIMEOUT', 'ERROR')}
        report['full_pilot_gate'] = report['PASS'] and any(r['status'] == 'UNSAT-SOLVER' for r in rows) and not any(r['status'] == 'SAT' for r in rows)
    pilot.dump(out / 'summary.json', report)
    print(json.dumps(report), flush=True)
    return 0 if report['PASS'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], Path(sys.argv[2])))
