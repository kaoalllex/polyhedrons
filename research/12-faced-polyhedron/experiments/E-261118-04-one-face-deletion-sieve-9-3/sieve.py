"""E-261118-04: the S5 formula of a map with the own conditions of one face S dropped (PLAN.md).

build_deleted mirrors omsat.build for ALL_OPTS family by family and splits every clause into two phases:
'kept' (conditions of the other faces, among themselves and along their edges with S) and 'own' (the conditions of
the polygon F_S: TRIPLE on non-triangles containing S, INCONS with S as the in-face, RFCONS and POC of S, REFLEX1 on
triangles containing S). The plane of S stays an element, so the edges e_XS of the other faces stay on the lines
L_XS. The deleted formula is the 'kept' phase alone; 'kept' then 'own' on one backend is the full formula reordered,
so the deleted CNF is a prefix of it (monotonicity by construction, test_sieve.py).

Usage: python3 sieve.py --shard K --shards N --cap SECONDS --budget SECONDS --out DIR   (one shard)
       python3 sieve.py --controls --cap SECONDS --out NEW_DIR
"""
import argparse
import itertools
import json
import os
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'code'))
sys.path.insert(0, str(ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'))
import pilot  # noqa: E402  (E-261103-03: solve(), census(), from_links(); SAT_SOLVER and NO_PROOF from the environment)
from omsat import Predicates, chirotope_from_planes  # noqa: E402
import control_rost_vigh  # noqa: E402
from omsat_validate import ALL_OPTS  # noqa: E402

FULL_CONTROLS = (29, 66, 20)  # the fastest full UNSAT-VERIFIED (9, 3) maps of E-261103-03 (29-31 s, CaDiCaL)


def build_deleted(B, T, S, phases=('kept',)):
    """ALL_OPTS families of omsat.build, emitted in the order of `phases`; S = None deletes nothing."""
    assert set(ALL_OPTS) == {'gp', 'triples', 'inconsist', 'reflex', 'reflexconsist', 'poc'} and all(ALL_OPTS.values())
    P = Predicates(B, T)
    n = T.n
    nt = T.nontriangles()
    for phase in phases:
        own = phase == 'own'
        if not own:
            B.gp()
        if T.multi and not own:
            for X, Y in itertools.combinations(range(n), 2):   # boundary runs of the faces X, Y on L_XY
                for (A, C), (D, E) in itertools.combinations(T.segments(X, Y), 2):
                    for V in (D, E):
                        B.clause([B.NOT(P.segment(X, Y, A, C, V))], 'SEGMENT_DISJOINT')
                    for V in (A, C):
                        B.clause([B.NOT(P.segment(X, Y, D, E, V))], 'SEGMENT_DISJOINT')
        for X, Y, Z in nt:
            if (S in (X, Y, Z)) == own:
                a = B.name(('IN', X, Y, Z), P.IN(X, Y, Z))
                b = B.name(('IN', Y, Z, X), P.IN(Y, Z, X))
                c = B.name(('IN', Z, X, Y), P.IN(Z, X, Y))
                B.clause([B.NOT(a), B.NOT(b), B.NOT(c)], 'TRIPLE')
        for X, Y, Z in nt:
            for (p, q, r) in ((X, Y, Z), (Y, Z, X), (Z, X, Y)):
                if (p == S) == own:
                    B.equiv(B.name(('IN', p, q, r), P.IN(p, q, r)), B.name(('IN', p, r, q), P.IN(p, r, q)), 'INCONS')
        for X in range(n):
            if (X == S) == own:
                for A, Bv in T.corners(X):
                    B.name(('RF', X, A, Bv), P.REFLEX(X, A, Bv))
                    B.name(('RF', X, Bv, A), P.REFLEX(X, Bv, A))
                    B.name(('RT', X, A, Bv), P.RTURN(X, A, Bv))
        for X in range(n):
            if (X == S) == own:
                for A, Bv in T.corners(X):
                    B.equiv(P.REFLEX(X, A, Bv), P.REFLEX(X, Bv, A), 'RFCONS')
        for t in T.tris:
            if (S in t) == own:
                X, Y, Z = t
                r = [P.REFLEX(X, Y, Z), P.REFLEX(Y, Z, X), P.REFLEX(Z, X, Y)]
                for i, j in itertools.combinations(range(3), 2):
                    B.clause([B.NOT(r[i]), B.NOT(r[j])], 'REFLEX1')
        for X in range(n):
            if (X == S) == own:
                w = [B.xor([P.RTURN(X, A, Bv), P.REFLEX(X, A, Bv)]) for A, Bv in T.corners(X)]
                for i in range(1, len(w)):
                    B.equiv(w[0], w[i], 'POC')
    return P


def deleted_cnf(T, S):
    c = pilot.CNF(T.n)
    build_deleted(c, T, S)
    return c


def roest_vigh(shifted=False):
    """Roest-Vigh's (8, 3) planes and map; shifted: plane 0 moved off its place (every deleted formula violated)."""
    h, links = control_rost_vigh.build()
    if shifted:
        h = [[100 * v for v in row] for row in h]
        h[0][3] += 259
    return h, pilot.from_links(links)


def pinned(c, planes):
    c.clauses.extend([[c.qvar[q] if v > 0 else -c.qvar[q]] for q, v in chirotope_from_planes(planes).items()])
    return c


def controls(out, cap):
    """Positive: Roest-Vigh's planes pinned, every deleted face SAT. Negative: the shifted planes pinned, every deleted
    face UNSAT; the full formulas (no deletion) of three (9, 3) maps UNSAT within the cap."""
    out.mkdir(parents=True, exist_ok=False)
    maps = pilot.census(9, 3)['maps']
    jobs = [(f'rv_del{S}', 'SAT', pinned(deleted_cnf(roest_vigh()[1], S), roest_vigh()[0])) for S in range(8)]
    jobs += [(f'rv_shifted_del{S}', pilot.UNSAT_OK, pinned(deleted_cnf(roest_vigh(True)[1], S), roest_vigh(True)[0]))
             for S in range(8)]
    jobs += [(f'map{i}_full', pilot.UNSAT_OK, deleted_cnf(pilot.from_links(maps[i]['links']), None)) for i in FULL_CONTROLS]
    summary = {}
    for name, expected, c in jobs:
        r = pilot.solve(c, out, name, cap)
        r.update(expected=expected, passed=r['status'] == expected)
        summary[name] = r
        print(f'{name}: {r["status"]} {r["seconds"]:.1f} s (expected {expected})', flush=True)
    summary = dict(passed=all(r['passed'] for r in summary.values()), solver=os.path.basename(pilot.CADICAL),
                   cap=cap, controls=summary)
    pilot.dump(out / 'controls.json', summary)
    return summary['passed']


def units():
    """Every admissible (9, 3) census map x every face, map-major, in census order."""
    maps = pilot.census(9, 3)['maps']
    return [(i, S) for i, rec in enumerate(maps) if rec['admissible'] for S in range(9)]


def done_keys(out):
    keys = set()
    for path in out.parent.glob('*/results.jsonl'):
        for line in path.read_text().splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue  # a torn last line: that unit reruns
            keys.add((r['map_index'], r['deleted_face']))
    return keys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shard', type=int, default=0)
    ap.add_argument('--shards', type=int, default=1)
    ap.add_argument('--cap', type=float, default=300)
    ap.add_argument('--budget', type=float, default=0, help='solver seconds of this shard over all restarts')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--limit', type=int, default=0, help='pilot: at most this many units of the shard (0 = all)')
    ap.add_argument('--controls', action='store_true', help='run the controls into --out instead of the shard')
    a = ap.parse_args()
    if a.controls:
        sys.exit(0 if controls(a.out, a.cap) else 1)
    a.out.mkdir(parents=True, exist_ok=True)
    maps = pilot.census(9, 3)['maps']
    work = a.out / 'work'
    work.mkdir(exist_ok=True)
    records = a.out / 'results.jsonl'
    spent = sum(json.loads(line)['seconds'] for line in records.read_text().splitlines()) if records.exists() else 0.0
    done = done_keys(a.out)
    mine = [u for k, u in enumerate(units()) if k % a.shards == a.shard and u not in done]
    if a.limit:
        mine = mine[:a.limit]
    for index, S in mine:
        if (a.out / 'STOP').exists() or spent >= a.budget:
            print(f'shard {a.shard}: stop ({"STOP file" if spent < a.budget else "budget"}), spent {spent:.0f} s', flush=True)
            break
        T = pilot.from_links(maps[index]['links'])
        c = deleted_cnf(T, S)
        name = f'map{index}_del{S}'
        r = pilot.solve(c, work, name, min(a.cap, a.budget - spent))
        if r['status'] == 'SAT':
            os.replace(work / (name + '.model.json'), a.out / (name + '.model.json'))
        for p in work.glob(name + '.*'):
            p.unlink()
        r.update(map_index=index, deleted_face=S, solver=os.path.basename(pilot.CADICAL),
                 scope='S5 (9,3) map formula (ALL_OPTS) with the own conditions of face S dropped, plane S kept',
                 finished_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        spent += r['seconds']
        with records.open('a') as f:
            f.write(json.dumps(r) + '\n')
        print(f'{name}: {r["status"]} {r["seconds"]:.1f} s', flush=True)


if __name__ == '__main__':
    main()
