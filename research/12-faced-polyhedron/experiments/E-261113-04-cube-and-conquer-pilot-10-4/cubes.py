"""Shard runner of PLAN.md: python3 cubes.py SHARD SHARDS OUT [LIMIT]   (NO_PROOF=1, SAT_SOLVER=kissat, via run.sh).

Controls first (any failure exits non-zero before a unit): c1 the plain formulas of (10, 4) maps 96, 85 and 845 rebuild
to their recorded CNF SHA-256 (E-261108-03); c2 the nine cube literals of maps 96 and 85 are existing, distinct, unfixed
variables of the plain formula and the 512 cubes are all their sign vectors; c3 the pinned Roest-Vigh chirotope with the
eight cubes of its first doubled pair: exactly one SAT, the cube read off the pinned model, seven UNSAT-SOLVER; the same
cube on the unpinned Roest-Vigh formula SAT. Then the units of this shard: unit 0 the monolithic speed calibration on
map 845, then the 512 cubes of map 96, then of map 85 (unit j on shard j % SHARDS). A cube of an arm whose recorded
solver seconds already reach 0.7x its monolithic time is recorded as SKIPPED-ARM-CAP. Recorded units are skipped.
LIMIT (pilot only): stop after that many units of this shard."""
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
sys.path.insert(0, str(ROOT / 'experiments/E-261110-05-immersion-only-s5-formulas'))
import pilot  # noqa: E402
from units import cnf_sha, pinned  # noqa: E402

# Monolithic kissat rel-4.0.4 solver seconds and CNF SHA-256 of the plain formula, E-261108-03 results/run/kissat-B
# (10 simultaneous shards, NO_PROOF=1), with the DIMACS comments of pilot.solve.
MONO = {96: (1073.4878988749697, '859f21a94e6d9b02888a98059a96d643d9a7460f3b86f64f12291b4c08e29df0'),
        85: (2748.8595722500468, 'd89b0f3d42407482c58a5c15a9c0382b0f84cde1c3d5f5214dce696b6472aed0'),
        845: (188.38137454201933, '7b125e1c3862dd80209e5725a1e096cc6b4c38802d9dd45b63c9911a5aedd025')}
ARMS, CALIBRATION = (96, 85), 845
ARM_CAP, CUBE_CAP, CALIBRATION_CAP, CONTROL_CAP = 0.7, 0.1, 600, 60


def formula(links):
    t = pilot.from_links(links)
    c = pilot.CNF(len(links)); P = pilot.build(c, t, pilot.ALL_OPTS)
    return c, P, t


def order_literals(c, P, t, pairs=None):
    """Three segment-order literals per doubled pair (X < Y, segments (A, C), (D, E) as T.segments lists them):
    lt(X,Y,A,C), lt(X,Y,D,E), lt(X,Y,A,D). They must already be variables of the formula (no new definitions)."""
    nv, nc, lits = c.nv, len(c.clauses), []
    multi = sorted(tuple(sorted(k)) for k, s in t._segments.items() if len(s) > 1)
    for X, Y in multi[:pairs]:
        (A, C), (D, E) = t.segments(X, Y)
        lits += [P.lt(X, Y, A, C), P.lt(X, Y, D, E), P.lt(X, Y, A, D)]
    assert (c.nv, len(c.clauses)) == (nv, nc), 'a cube literal is not a variable of the plain formula'
    return lits, multi[:pairs]


def cube(lits, k):
    return [l if k >> b & 1 else -l for b, l in enumerate(lits)]


def solve_with(c, units, out, name, cap):
    c.clauses.extend([[l] for l in units])
    try:
        return pilot.solve(c, out, name, cap)
    finally:
        del c.clauses[len(c.clauses) - len(units):]


def controls(out):
    census = pilot.census(10, 4)['maps']
    report, ok = {}, True
    for i, (_, digest) in MONO.items():
        c, P, t = formula(census[i]['links'])
        c1 = cnf_sha(c, f'map{i}_plain') == digest
        report[f'c1_map{i}_plain_hash'] = c1; ok &= c1
        if i in ARMS:
            lits, pairs = order_literals(c, P, t)
            units = {abs(cl[0]) for cl in c.clauses if len(cl) == 1}
            cubes = {tuple(cube(lits, k)) for k in range(2 ** len(lits))}
            c2 = (len(pairs) == 3 and len({abs(l) for l in lits}) == 9 and not units & {abs(l) for l in lits}
                  and cubes == set(itertools.product(*[(-l, l) for l in lits])) and len(cubes) == 512)
            report[f'c2_map{i}'] = dict(ok=c2, pairs=pairs, literals=lits); ok &= c2
    name, planes, t = pilot.controls()[0]
    assert name == 'roest_vigh'
    c = pilot.CNF(t.n); P = pilot.build(c, t, pilot.ALL_OPTS)
    lits, pairs = order_literals(c, P, t, pairs=1)
    free = pilot.solve(c, out, 'c3_rv_unpinned_nocube', CONTROL_CAP)['status']
    pinned(c, planes)
    r = pilot.solve(c, out, 'c3_rv_pinned_nocube', CONTROL_CAP)
    model = set(json.loads((out / 'c3_rv_pinned_nocube.model.json').read_text())) if r['status'] == 'SAT' else set()
    want = sum(1 << b for b, l in enumerate(lits) if l in model)
    got = {k: solve_with(c, cube(lits, k), out, f'c3_rv_pinned_cube{k}', CONTROL_CAP)['status'] for k in range(8)}
    c3 = (r['status'] == 'SAT' and got[want] == 'SAT'
          and all(s == pilot.UNSAT_OK for k, s in got.items() if k != want))
    del c.clauses[-len(pilot.chirotope_from_planes(planes)):]
    unp = solve_with(c, cube(lits, want), out, f'c3_rv_unpinned_cube{want}', CONTROL_CAP)['status']
    c3 &= unp == 'SAT'
    report['c3_roest_vigh'] = dict(ok=c3, pair=pairs, literals=lits, expected_cube=want, pinned=got,
                                   unpinned_expected_cube=unp, unpinned_no_cube=free)
    ok &= c3
    report['status'] = 'CONTROLS-PASS' if ok else 'CONTROLS-FAIL'
    pilot.dump(out / 'controls.json', report)
    return ok


def recorded(root):
    return [json.loads(l) for p in root.glob('*/results.jsonl') for l in p.read_text().splitlines() if l.strip()]


def main(shard, shards, out, limit=None):
    assert pilot.NO_PROOF and 'kissat' in pilot.CADICAL, 'run through run.sh (kissat, NO_PROOF=1)'
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    if not controls(out):
        sys.exit('controls failed: no unit run')
    census = pilot.census(10, 4)['maps']
    units = [(CALIBRATION, None)] + [(i, k) for i in ARMS for k in range(512)]
    built, ran = {}, 0
    for j, (i, k) in enumerate(units):
        name = f'map{i}_monolithic' if k is None else f'map{i}_cube{k:03d}'
        if j % shards != shard or (out.parent / 'stop.requested').exists():
            continue
        rows = recorded(out.parent)
        if name in {r['task'] for r in rows}:
            continue
        if limit is not None and ran >= limit:
            break
        ran += 1
        if i not in built:
            built[i] = formula(census[i]['links'])
        c, P, t = built[i]
        mono = MONO[i][0]
        if k is None:
            r = pilot.solve(c, out, name, CALIBRATION_CAP)
            r.update(cube=None, reference_seconds=mono)
        else:
            spent = sum(r['seconds'] for r in rows if r.get('map_index') == i and r.get('cube') is not None)
            lits = order_literals(c, P, t)[0]
            if spent >= ARM_CAP * mono:
                r = dict(status='SKIPPED-ARM-CAP', seconds=0.0, arm_seconds_at_skip=spent)
            else:
                r = solve_with(c, cube(lits, k), out, name, CUBE_CAP * mono)
            r.update(cube=k, cube_literals=cube(lits, k), monolithic_seconds=mono)
        r.update(task=name, case=[10, 4], map_index=i, solver=pilot.CADICAL,
                 scope='plain uniform embedding formula (E-261103-02 encoder) plus the cube units; UNSAT is UNSAT-SOLVER')
        with open(out / 'results.jsonl', 'a') as fh:
            fh.write(json.dumps(r) + '\n')
        print(name, r['status'], round(r['seconds'], 1), flush=True)


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else None)
