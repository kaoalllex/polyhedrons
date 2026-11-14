"""Re-gauged positive controls, with one registered reorientation-only retry."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
import itertools
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ['NO_PROOF'] = '1'
os.environ['SAT_SOLVER'] = str(Path.home() / 'bin/kissat')
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot
from test_encoder import controls, perturb


def topology(links):
    links = {int(k): v for k, v in links.items()} if isinstance(links, dict) else dict(enumerate(links))
    tris = sorted({tuple(sorted((x, a, b))) for x, l in links.items() for a, b in zip(l, l[1:] + l[:1])})
    return pilot.Triangulation(len(links), tris, links=links, submap=True)


def gauge(chi, n, mirror):
    units = [(0, 1, k, n) for k in range(2, n)] + [(0, 2, 3, n), (1, 2, 3, n)]
    if mirror:
        units.append((0, 1, 2, 3))
    for sign in ((1, -1) if mirror else (1,)):
        for eps in itertools.product((1, -1), repeat=n):
            def value(q):
                v = sign * chi[q]
                for i in q:
                    if i < n:
                        v *= eps[i]
                return v
            if all(value(q) == 1 for q in units):
                return {q: value(q) for q in chi}, dict(mirror=sign == -1, reorientation=list(eps))
    raise AssertionError('normalisation unreachable')


def jobs():
    result = [(name, h, t) for name, h, t in controls()]
    for name, path in [(f'convex_f{n}', Path(pilot.HERE) / f'control_f{n}.json') for n in (9, 10)] + [
            ('grooved_k2', ROOT / 'experiments/E-261109-01-grooved-box-multiplicity-control/control_k2.json'),
            ('grooved_k3', ROOT / 'experiments/E-261109-01-grooved-box-multiplicity-control/control_k3.json')]:
        d = json.loads(path.read_text()); result.append((name, d['planes'], topology(d['links'])))
    run = ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/results/run'
    realized = []
    for p in sorted(run.glob('*/results.jsonl')):
        for line in p.read_text().splitlines():
            d = json.loads(line)
            if d.get('candidate') and d.get('candidate_verify_rc') == 0:
                path = ROOT.parents[1] / d['candidate']
                if not path.exists():
                    path = ROOT.parents[2] / 'polyhedrons-data' / d['candidate']
                data = json.loads(path.read_text())
                h = [[int(round(float(v) * 10**9)) for v in row] for row in data['planes']]
                realized.append((f"realized_{d['map_index']}", h, topology(data['links'])))
    assert len(realized) == 16, len(realized)
    result.extend(realized)
    p = ROOT / 'experiments/E-261113-02-s6-10-2-calibration-rung/maps/seeded_formulas.json'
    seen = set()
    for m in json.loads(p.read_text())['maps']:
        if m['lutz'] not in seen and m['lutz'] != 739:
            seen.add(m['lutz']); result.append((f"unpinned_{m['lutz']}", None, topology(m['links'])))
    assert len(seen) == 50, len(seen)
    return result


def shard(args):
    k, out, work = args
    dest = out / str(k); dest.mkdir(parents=True)
    rows = []
    start = time.monotonic()
    for name, planes, t in work:
        row = dict(name=name, faces=t.n, attempts=[])
        if planes is not None:
            # Preserve exact decimal input; known symmetric controls need a uniform perturbation.
            h = [[Fraction(str(v)) for v in p] for p in planes]
            chi = pilot.chirotope_from_planes(h)
            if not all(chi.values()):
                h = perturb(h); chi = pilot.chirotope_from_planes(h)
            row['planes'] = [[str(v) for v in p] for p in h]
            e = pilot.CNF(t.n); pilot.build(e, t, pilot.ALL_OPTS)
        for mirror in (True, False):
            c = pilot.CNF(t.n)
            pilot.build(c, t, dict(pilot.ALL_OPTS, symbreak=True, mirror=mirror))
            if planes is not None:
                normalized, transform = gauge(chi, t.n, mirror)
                c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in normalized.items()])
                row['transform'] = transform
            r = pilot.solve(c, dest, name + ('_mirror' if mirror else '_reorient'), 60)
            row['attempts'].append(dict(mirror=mirror, **r))
            if r['status'] == 'SAT':
                break
        rows.append(row)
        pilot.dump(dest / 'controls.json', rows)
        if rows[-1]['attempts'][-1]['status'] != 'SAT':
            break
    usage = resource.getrusage(resource.RUSAGE_SELF); children = resource.getrusage(resource.RUSAGE_CHILDREN)
    pilot.dump(dest / 'manifest.json', dict(shard=k, seconds=time.monotonic()-start,
               cpu_seconds=usage.ru_utime+usage.ru_stime+children.ru_utime+children.ru_stime,
               python=sys.version, platform=platform.platform(), solver_sha256=pilot.sha(Path(pilot.CADICAL)),
               commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(), dirty=True))
    return rows


def main(out):
    work = jobs(); out.mkdir(parents=True, exist_ok=False)
    with ProcessPoolExecutor(10) as pool:
        rows = sum(pool.map(shard, [(k, out, work[k::10]) for k in range(10)]), [])
    report = dict(PASS=len(rows)==len(work) and all(r['attempts'][-1]['status']=='SAT' for r in rows),
                  expected=len(work), completed=len(rows), retries=[r['name'] for r in rows if len(r['attempts'])>1],
                  inputs_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in
                                 (Path(__file__), ROOT/'code/omsat.py', Path(pilot.__file__))})
    pilot.dump(out/'summary.json', report); print(json.dumps(report))
    return 0 if report['PASS'] else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1])))
