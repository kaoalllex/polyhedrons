"""Exhaustive face-group restrictions of normalised V1; PLAN.md owns the scope."""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import itertools
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
os.environ['NO_PROOF'] = '1'
os.environ['SAT_SOLVER'] = str(Path.home() / 'bin/kissat')
sys.path.insert(0, str(ROOT / 'experiments/E-261114-01-normalised-s6-10-3'))
from controls import gauge, pilot

OPTS = dict(pilot.ALL_OPTS, triples=False, symbreak=True, mirror=True)


def grouped(t):
    c = pilot.CNF(t.n)
    c.defs_only = True
    p = pilot.build(c, t, OPTS)
    c.defs_only = False
    groups = []

    def add(faces, fn):
        start = len(c.clauses)
        fn()
        groups.extend((frozenset(faces), cl) for cl in c.clauses[start:])
        del c.clauses[start:]

    for x, y, z in t.nontriangles():
        for a, b, d in ((x, y, z), (y, z, x), (z, x, y)):
            add([a], lambda: c.equiv(p.IN(a, b, d), p.IN(a, d, b), 'INCONS'))
    for x in range(t.n):
        for a, b in t.corners(x):
            add([x], lambda: c.equiv(p.REFLEX(x, a, b), p.REFLEX(x, b, a), 'RFCONS'))
    for x, y, z in t.tris:
        faces = [x, y, z]
        refs = [p.REFLEX(x, y, z), p.REFLEX(y, z, x), p.REFLEX(z, x, y)]
        for i, j in itertools.combinations(range(3), 2):
            add([faces[i], faces[j]], lambda: c.clause([-refs[i], -refs[j]], 'REFLEX1'))
    for x in range(t.n):
        w = [c.xor([p.RTURN(x, a, b), p.REFLEX(x, a, b)]) for a, b in t.corners(x)]
        for i in range(1, len(w)):
            add([x], lambda: c.equiv(w[0], w[i], 'POC'))
    fixed = [(0, 1, k, t.n) for k in range(2, t.n)] + [(0, 2, 3, t.n), (1, 2, 3, t.n), (0, 1, 2, 3)]
    c.clauses.extend([[-c.chi_neg(q)] for q in fixed])
    plain = pilot.CNF(t.n)
    pilot.build(plain, t, OPTS)
    assert c.nv == plain.nv
    assert Counter(map(tuple, c.clauses + [cl for _, cl in groups])) == Counter(map(tuple, plain.clauses))
    return c, groups


def restriction(t, faces):
    c, groups = grouped(t)
    c.clauses.extend(cl for owners, cl in groups if owners <= set(faces))
    return c


def shard(args):
    k, out = args
    dest = out / str(k)
    dest.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    name, planes, t = pilot.controls()[0]
    c = restriction(t, range(t.n))
    chi, _ = gauge(pilot.chirotope_from_planes(planes), t.n, True)
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chi.items()])
    pos = pilot.solve(c, dest, 'positive', 5)
    c.clauses.extend([[1], [-1]])
    neg = pilot.solve(c, dest, 'negative', 5)
    census = pilot.census(8, 2)['maps']
    empty = pilot.solve(restriction(pilot.from_links(census[0]['links']), []), dest, 'empty', 5)
    assert [pos['status'], neg['status'], empty['status']] == ['SAT', 'UNSAT-SOLVER', 'SAT']
    pilot.dump(dest / 'controls.json', dict(positive=pos, negative=neg, empty=empty, PASS=True))
    tasks = [(m, mask) for m in (0, 1) for mask in range(256)]
    rows = []
    for m, mask in tasks[k::10]:
        faces = [i for i in range(8) if mask & (1 << i)]
        c = restriction(pilot.from_links(census[m]['links']), faces)
        r = pilot.solve(c, dest, f'map{m}_mask{mask}', 5)
        r.update(map=m, mask=mask, faces=faces)
        rows.append(r)
        with (dest / 'results.jsonl').open('a') as stream:
            stream.write(json.dumps(r) + '\n')
    usage = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    pilot.dump(dest / 'manifest.json', dict(shard=k, seconds=time.monotonic()-start,
        cpu_seconds=usage.ru_utime+usage.ru_stime+children.ru_utime+children.ru_stime,
        commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        python=sys.version, solver_sha256=pilot.sha(Path(pilot.CADICAL)),
        sources_sha256={str(p.relative_to(ROOT)):pilot.sha(p) for p in
            (Path(__file__), ROOT/'code/omsat.py', Path(pilot.__file__))}))
    return rows


def main(out, pilot_only=False):
    out.mkdir(parents=True, exist_ok=True)
    if pilot_only:
        shard((0, out))
        return
    with ProcessPoolExecutor(9) as pool:
        list(pool.map(shard, [(k, out) for k in range(1, 10)]))
    rows = [json.loads(line) for path in out.glob('*/results.jsonl') for line in path.read_text().splitlines()]
    report = dict(completed=len(rows), maps={})
    for m in (0, 1):
        rs = {r['mask']:r for r in rows if r['map']==m}
        cores = []
        for mask, r in rs.items():
            if r['status']=='UNSAT-SOLVER' and all(rs[mask ^ (1 << i)]['status']=='SAT' for i in r['faces']):
                cores.append(r['faces'])
        report['maps'][m] = dict(counts=dict(Counter(r['status'] for r in rs.values())),
            minimal_cores=cores, six_face_statuses=dict(Counter(r['status'] for r in rs.values() if len(r['faces'])==6)))
    pilot.dump(out/'summary.json', report)
    print(json.dumps(report))


if __name__ == '__main__':
    main(Path(sys.argv[1]), '--pilot' in sys.argv)
