"""Track-3 validation: chirotope formulas (omsat.py, Eval and CNF backends) versus exact direct
geometry (omsat_geom.py) on Szilassi, perturbed Szilassi, and random integer plane sets.

usage: python3 omsat_validate.py [n_random_7] [n_random_12] [n_cnf_checks]
"""
import itertools
import json
import os
import random
import re
import sys
import time
from fractions import Fraction
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import omsat
from omsat import Triangulation, CNF, Eval, build, chirotope_from_planes
from omsat_geom import Geometry, cross, sub, dot

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ALL_OPTS = dict(gp=True, triples=True, inconsist=True, reflex=True, reflexconsist=True,
                poc=True)


def szilassi():
    """(planes, Triangulation) of the Szilassi polyhedron from index.html (MODELS.szilassi)."""
    s = open(os.path.join(ROOT, 'index.html')).read()
    i = s.index('szilassi: {')
    blk = s[i:i + 3000]
    vt = blk[blk.index('vertices:'):blk.index('faces:')]
    ft = blk[blk.index('faces:'):blk.index('colors:')]
    ft = ft[:ft.rindex(']') + 1]
    verts = [tuple(Fraction(x) for x in m.split(','))
             for m in re.findall(r'\[([-0-9., ]+)\]', vt)]
    faces = [[int(x) - 1 for x in m.split(',')] for m in re.findall(r'\[([0-9, ]+)\]', ft)]
    assert len(verts) == 14 and len(faces) == 7
    planes = []
    for f in faces:
        p0, p1, p2 = verts[f[0]], verts[f[1]], verts[f[2]]
        nrm = cross(sub(p1, p0), sub(p2, p0))
        e = -dot(nrm, p0)
        vec = list(nrm) + [e]
        L = 1
        for x in vec:
            L = L * x.denominator // gcd(L, x.denominator)
        vec = [int(x * L) for x in vec]
        g = 0
        for x in vec:
            g = gcd(g, abs(x))
        vec = [x // g for x in vec]
        for v in f:                      # planarity check
            assert dot(vec[:3], verts[v]) + vec[3] == 0
        planes.append(vec)
    # triangulation: vertex -> faces containing it
    tris = []
    for vi in range(14):
        fs = tuple(k for k, f in enumerate(faces) if vi in f)
        assert len(fs) == 3
        tris.append(fs)
    # links in the order of the face walk: edge (f[i], f[i+1]) shared with face Y_i
    links = {}
    for k, f in enumerate(faces):
        cyc = []
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]
            Y = [j for j, g in enumerate(faces) if j != k and a in g and b in g]
            assert len(Y) == 1
            cyc.append(Y[0])
        links[k] = cyc
    return planes, Triangulation(7, tris, links), verts, faces


def uniform(chi):
    return all(v != 0 for v in chi.values())


def eval_all(planes, T, opts=ALL_OPTS):
    chi = chirotope_from_planes(planes)
    B = Eval(T.n, chi)
    build(B, T, opts)
    return chi, B


def compare_direct(planes, T, B, stats):
    G = Geometry(planes, T)
    mism = []
    for key, val in B.named.items():
        kind = key[0]
        if kind == 'IN':
            d = G.IN(*key[1:])
        elif kind == 'RF':
            d = G.REFLEX(*key[1:])
        elif kind == 'RT':
            d = G.RTURN(*key[1:])
        else:
            continue
        stats[kind] = stats.get(kind, 0) + 1
        stats[kind + '_true'] = stats.get(kind + '_true', 0) + int(d)
        if bool(val) != bool(d):
            mism.append((key, val, d))
    # elementary predicates: E, lt, side on every applicable index
    P = omsat.Predicates(B, T)
    n = T.n
    for X, W in itertools.permutations(range(n), 2):
        for V in range(n):
            if V in (X, W):
                continue
            stats['E'] = stats.get('E', 0) + 1
            if bool(P.E(X, W, V)) != G.E(X, W, V):
                mism.append((('E', X, W, V),))
            for Z in range(n):
                if Z in (X, W, V):
                    continue
                stats['lt'] = stats.get('lt', 0) + 1
                if bool(P.lt(X, W, V, Z)) != G.lt(X, W, V, Z):
                    mism.append((('lt', X, W, V, Z),))
    for (a, b, c) in itertools.combinations(range(n), 3):
        for d in range(n):
            if d in (a, b, c):
                continue
            stats['side'] = stats.get('side', 0) + 1
            if bool(P.sd(a, b, c, d)) != (G.side(a, b, c, d) < 0):
                mism.append((('sd', a, b, c, d),))
    # soundness spot checks of derived families on SIMPLE polygons:
    simple = [G.simple(X) for X in range(n)]
    for X in range(n):
        if not simple[X]:
            continue
        ccw = G.ccw(X)
        for A, Bv in T.corners(X):
            stats['poc_tests'] = stats.get('poc_tests', 0) + 1
            # simple polygon: reflex iff turn opposite to orientation
            rt = G.RTURN(X, A, Bv)
            reflex_angle = (rt == ccw)        # ccw polygon + right turn => reflex
            if G.REFLEX(X, A, Bv) != reflex_angle or G.REFLEX(X, Bv, A) != reflex_angle:
                mism.append((('POC-geom', X, A, Bv),))
    emb = G.embedded()
    trip_ok = 'TRIPLE' not in B.violations
    if emb != trip_ok:
        mism.append((('LEMMA5.1', emb, trip_ok),))
    return mism, emb, simple


def cnf_check(planes, T, opts=ALL_OPTS, expect_sat=None):
    """(a) definitions-only CNF + chi units: every named literal equals the Eval value;
       (b) full CNF + chi units: SAT iff Eval reports no violated clause."""
    from pysat.solvers import Solver
    chi = chirotope_from_planes(planes)
    Bev = Eval(T.n, chi)
    build(Bev, T, opts)
    units = []
    C0 = CNF(T.n)
    for S, v in chi.items():
        units.append(C0.qvar[S] if v > 0 else -C0.qvar[S])
    # (a)
    C = CNF(T.n)
    C.defs_only = True
    build(C, T, opts)
    with Solver(name='cadical195', bootstrap_with=C.clauses) as s:
        assert s.solve(assumptions=units)
        m = set(l for l in s.get_model() if l > 0)
    bad = 0
    for k, lit in C.named.items():
        val = (lit in m) if lit > 0 else ((-lit) not in m)
        if lit in (1, -1):
            val = lit == 1
        if val != bool(Bev.named[k]):
            bad += 1
    # (b)
    C2 = CNF(T.n)
    build(C2, T, opts)
    with Solver(name='cadical195', bootstrap_with=C2.clauses) as s:
        sat = s.solve(assumptions=units)
        core = None if sat else s.get_core()
    ev_ok = len(Bev.violations) == 0
    return dict(named=len(C.named), named_mismatch=bad, sat=sat, eval_ok=ev_ok,
                agree=(sat == ev_ok), core_size=None if core is None else len(core),
                violations=sorted(set(Bev.violations)))


def normalise(planes, n):
    """Flip plane signs so that chi satisfies the reorientation normalisation, then return
    (planes, needs_mirror)."""
    INF = n
    fixed = [(0, 1, k, INF) for k in range(2, n)] + [(0, 2, 3, INF), (1, 2, 3, INF)]
    best = None
    for eps in itertools.product((1, -1), repeat=n):   # n small (7) only
        pl = [[e * x for x in p] for e, p in zip(eps, planes)]
        chi = chirotope_from_planes(pl)
        if all(chi[tuple(sorted(S))] * (-1) ** omsat.perm_parity(S) > 0 for S in fixed):
            best = pl
            break
    return best


def random_planes(n, R, rng):
    return [[rng.randint(-R, R) for _ in range(4)] for _ in range(n)]


def main():
    nr7 = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    nr12 = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    ncnf = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    rng = random.Random(20261029)
    out = {}
    t0 = time.time()
    planes0, T7, verts, faces = szilassi()
    print('Szilassi planes (index.html):', planes0)
    chi0 = chirotope_from_planes(planes0)
    zeros = [S for S, v in chi0.items() if v == 0]
    print('Szilassi chirotope: %d zero quadruples (not uniform):' % len(zeros), zeros)
    out['szilassi_raw'] = dict(planes=planes0, zero_quads=zeros)
    # uniform positive control: smallest perturbation (scale 1000, noise +-1) that is uniform
    rs = random.Random(7)
    while True:
        planes = [[1000 * x + rs.randint(-1, 1) for x in p] for p in planes0]
        if uniform(chirotope_from_planes(planes)):
            break
    print('Szilassi control planes:', planes)
    chi, B = eval_all(planes, T7)
    print('uniform:', uniform(chi), 'eval violations:', B.violations)
    stats = {}
    mism, emb, simple = compare_direct(planes, T7, B, stats)
    print('Szilassi direct embedded:', emb, 'mismatches:', len(mism), stats)
    out['szilassi'] = dict(planes=planes, uniform=uniform(chi), violations=B.violations,
                           embedded=emb, mismatches=len(mism))
    # reflex pattern on Szilassi (known: exactly one convex face)
    conv = []
    for X in range(7):
        r = [B.named[('RF', X, A, Bv)] for A, Bv in T7.corners(X)]
        conv.append(sum(r))
    print('reflex corners per face:', conv)
    out['szilassi']['reflex_per_face'] = conv
    # CNF check on Szilassi
    r = cnf_check(planes, T7)
    print('Szilassi CNF check:', r)
    out['szilassi']['cnf'] = r
    # perturbed Szilassi (scaled by 1000, integer noise of growing radius)
    pert = []
    agg = {}
    tot_m = 0
    for trial in range(nr7):
        rad = [1, 300, 3000, 10000, 20000, 40000][trial % 6]
        pl = [[1000 * x + rng.randint(-rad, rad) for x in p] for p in planes0]
        chi = chirotope_from_planes(pl)
        if not uniform(chi):
            continue
        B = Eval(7, chi)
        build(B, T7, ALL_OPTS)
        mism, emb, simple = compare_direct(pl, T7, B, agg)
        tot_m += len(mism)
        if mism:
            print('MISMATCH', trial, mism[:5])
        pert.append((rad, emb, sorted(set(B.violations))))
    out['perturbed_szilassi'] = dict(n=len(pert), embedded=sum(e for _, e, _ in pert),
                                     mismatches=tot_m, stats=agg)
    print('perturbed Szilassi:', len(pert), 'configs, embedded', sum(e for _, e, _ in pert),
          'mismatches', tot_m, agg)
    # embedded perturbed ones must satisfy every clause family
    viol_emb = [v for _, e, v in pert if e and v]
    print('embedded configs violating some family:', viol_emb)
    out['perturbed_szilassi']['embedded_with_violations'] = len(viol_emb)
    # random n=7 and n=12
    with open(os.path.join(RDIR, 'data', 'k12_first.json')) as f:
        e0 = json.load(f)[0]
    T12 = Triangulation(12, e0['triangles'], {int(k): v for k, v in e0['links'].items()})
    for n, T, cnt in ((7, T7, nr7), (12, T12, nr12)):
        agg = {}
        tot_m = 0
        nemb = 0
        k = 0
        tries = 0
        while k < cnt:
            tries += 1
            pl = random_planes(n, 40, rng)
            chi = chirotope_from_planes(pl)
            if not uniform(chi):
                continue
            k += 1
            B = Eval(n, chi)
            build(B, T, ALL_OPTS)
            if 'GP' in B.violations:
                print('GP violated on a realisable chirotope!')
            mism, emb, simple = compare_direct(pl, T, B, agg)
            nemb += emb
            tot_m += len(mism)
            if mism:
                print('MISMATCH n=%d' % n, mism[:5])
        print('random n=%d: %d configs, embedded %d, mismatches %d' % (n, k, nemb, tot_m), agg)
        out['random_n%d' % n] = dict(n=k, embedded=nemb, mismatches=tot_m, stats=agg)
    # CNF backend checks on random configs
    cres = []
    for n, T in ((7, T7), (12, T12)):
        for _ in range(ncnf):
            while True:
                pl = random_planes(n, 40, rng)
                if uniform(chirotope_from_planes(pl)):
                    break
            r = cnf_check(pl, T)
            cres.append((n, r))
            print('CNF check n=%d:' % n, r)
    out['cnf_checks'] = [dict(n=n, **r) for n, r in cres]
    out['seconds'] = time.time() - t0
    os.makedirs(os.path.join(RDIR, 'experiments', 'omsat'), exist_ok=True)
    with open(os.path.join(RDIR, 'experiments', 'omsat', 'validation.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print('done in %.1fs' % (time.time() - t0))


if __name__ == '__main__':
    main()
