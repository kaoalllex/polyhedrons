"""Symmetric OM-SAT instances (Track 3, independent re-derivation).

For a Lutz map (k12_g6_lutz.txt, numbering #1..#59) we compute ourselves:
  * an orientation of the triangulation and Aut(map) with the orientation character
    eps(g) = +1 iff g preserves the orientation;
  * the subgroups (by brute force closure of pairs of elements), their isomorphism types,
    and whether they act freely on the 12 faces;
  * an explicit faithful rational orthogonal representation rho : G -> O(3) with
    det rho(g) = eps(g) (searched among signed permutation matrices), and a check that a
    random rho-symmetric plane configuration (h_{g r} = diag(rho(g),1) h_r on orbit
    representatives r) has all 715 determinants non-zero (=> general position is WLOG);
  * the SAT instance: omsat.build(...) + chi(gS) = eps(g) chi(S) + orbit-flip normalisation
    + mirror normalisation (see omsat_sym_notes in the report).
"""
import itertools
import json
import os
import random
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import omsat
from omsat import Triangulation, CNF, Eval, build, chirotope_from_planes, perm_parity

RDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LUTZ = os.path.join(RDIR, 'literature', 'Hashirama1337s-szilassi-12', 'code', 'k12_g6_lutz.txt')


def parse_lutz(path=LUTZ):
    s = open(path).read()
    maps = {}
    for m in re.finditer(r'manifold_lex_d2_n12_o1_g6_#(\d+)=(\[\[.*?\]\])', s, re.S):
        k = int(m.group(1))
        tris = [tuple(int(x) - 1 for x in t.split(','))
                for t in re.findall(r'\[(\d+,\d+,\d+)\]', m.group(2))]
        maps[k] = tris
    assert len(maps) == 59
    return maps


def orient(tris):
    """Return oriented triangles (a,b,c) coherently oriented (orientable surface)."""
    tris = [tuple(t) for t in tris]
    edge_tris = {}
    for i, t in enumerate(tris):
        for a, b in itertools.combinations(t, 2):
            edge_tris.setdefault(frozenset((a, b)), []).append(i)
    ori = {0: tris[0]}
    stack = [0]
    while stack:
        i = stack.pop()
        a, b, c = ori[i]
        for x, y in ((a, b), (b, c), (c, a)):
            for j in edge_tris[frozenset((x, y))]:
                if j == i:
                    continue
                z = [v for v in tris[j] if v not in (x, y)][0]
                want = (y, x, z)        # opposite direction on the shared edge
                if j in ori:
                    o = ori[j]
                    cyc = [o, o[1:] + o[:1], o[2:] + o[:2]]
                    assert want in cyc, "non-orientable or inconsistent"
                else:
                    ori[j] = want
                    stack.append(j)
    assert len(ori) == len(tris)
    return [ori[i] for i in range(len(tris))]


def links_from_oriented(otris, n=12):
    succ = {v: {} for v in range(n)}
    for a, b, c in otris:
        succ[a][b] = c
        succ[b][c] = a
        succ[c][a] = b
    links = {}
    for v in range(n):
        start = min(succ[v])
        cyc = [start]
        while len(cyc) < n - 1:
            cyc.append(succ[v][cyc[-1]])
        assert succ[v][cyc[-1]] == start
        links[v] = cyc
    return links, succ


def automorphisms(otris, n=12):
    """All permutations g of 0..n-1 mapping the triangle set to itself; with eps(g)."""
    triset = set(frozenset(t) for t in otris)
    oriset = set()
    for a, b, c in otris:
        oriset |= {(a, b, c), (b, c, a), (c, a, b)}
    edge_tris = {}
    for t in otris:
        for a, b in itertools.combinations(t, 2):
            edge_tris.setdefault(frozenset((a, b)), []).append(frozenset(t))
    t0 = otris[0]
    out = []
    for tgt in otris:
        for perm3 in itertools.permutations(tgt):
            g = {t0[i]: perm3[i] for i in range(3)}
            # propagate across edges
            queue = [frozenset(t0)]
            seen = {frozenset(t0)}
            ok = True
            while queue and ok:
                t = queue.pop()
                for a, b in itertools.combinations(sorted(t), 2):
                    for t2 in edge_tris[frozenset((a, b))]:
                        if t2 == t:
                            continue
                        z = [v for v in t2 if v not in (a, b)][0]
                        ga, gb = g[a], g[b]
                        img_t = [s for s in edge_tris[frozenset((ga, gb))]
                                 if s != frozenset(g[v] for v in t)]
                        gz = [v for v in img_t[0] if v not in (ga, gb)][0]
                        if z in g:
                            if g[z] != gz:
                                ok = False
                                break
                        else:
                            if gz in g.values():
                                ok = False
                                break
                            g[z] = gz
                        if t2 not in seen:
                            seen.add(t2)
                            queue.append(t2)
                    if not ok:
                        break
            if not ok or len(g) != n:
                continue
            perm = tuple(g[i] for i in range(n))
            if set(frozenset(perm[v] for v in t) for t in otris) != triset:
                continue
            a, b, c = otris[0]
            eps = 1 if (perm[a], perm[b], perm[c]) in oriset else -1
            out.append((perm, eps))
    out = sorted(set(out))
    return out


def compose(p, q):            # (p o q)(i) = p[q[i]]
    return tuple(p[q[i]] for i in range(len(q)))


def closure(gens, n=12):
    e = tuple(range(n))
    G = {e}
    frontier = [e]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = compose(g, x)
                if y not in G:
                    G.add(y)
                    new.append(y)
        frontier = new
    return frozenset(G)


def order(p):
    e = tuple(range(len(p)))
    k, q = 1, p
    while q != e:
        q = compose(p, q)
        k += 1
    return k


def classify(G):
    """crude isomorphism type of a small permutation group"""
    m = len(G)
    ords = sorted(order(g) for g in G)
    abelian = all(compose(a, b) == compose(b, a) for a in G for b in G)
    inv = ords.count(2)
    if m == 1:
        return 'C1'
    if m == 2:
        return 'C2'
    if m == 3:
        return 'C3'
    if m == 4:
        return 'C4' if 4 in ords else 'D2'
    if m == 6:
        return 'C6' if abelian else 'D3'
    if m == 12 and inv == 3 and ords.count(3) == 8:
        return 'T'
    return 'order%d%s' % (m, 'ab' if abelian else '')


def subgroups(auts):
    """all subgroups generated by <= 2 elements, as frozensets of perms"""
    els = [p for p, _ in auts]
    subs = set()
    for a in els:
        subs.add(closure([a]))
    for a, b in itertools.combinations(els, 2):
        subs.add(closure([a, b]))
    return subs


def free(G, n=12):
    e = tuple(range(n))
    return all(all(g[i] != i for i in range(n)) for g in G if g != e)


# --- explicit representation

def signed_perm_matrices():
    out = []
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            M = tuple(tuple(s[i] if j == p[i] else 0 for j in range(3)) for i in range(3))
            out.append(M)
    return out


def matmul(A, B):
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)) for i in range(3))


def mdet(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def find_reps(G, eps, max_reps=50):
    """Isomorphisms rho: G -> signed permutation matrices (O(3) cap GL(3,Z)) with
    det rho = eps.  G given as list of perms; uses 2 generators."""
    Gl = sorted(G)
    e = tuple(range(12))
    # pick generators
    gens = None
    for a in Gl:
        if closure([a]) == G:
            gens = [a]
            break
    if gens is None:
        for a, b in itertools.combinations(Gl, 2):
            if closure([a, b]) == G:
                gens = [a, b]
                break
    mats = signed_perm_matrices()
    I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    reps = []
    for imgs in itertools.product(mats, repeat=len(gens)):
        # build map by BFS
        rho = {e: I3}
        frontier = [e]
        ok = True
        while frontier and ok:
            new = []
            for x in frontier:
                for g, M in zip(gens, imgs):
                    y = compose(g, x)
                    My = matmul(M, rho[x])
                    if y in rho:
                        if rho[y] != My:
                            ok = False
                            break
                    else:
                        rho[y] = My
                        new.append(y)
                if not ok:
                    break
            frontier = new
        if not ok or len(rho) != len(G):
            continue
        if len(set(rho.values())) != len(G):
            continue          # not faithful
        if any(mdet(rho[g]) != eps[g] for g in G):
            continue
        reps.append(rho)
        if len(reps) >= max_reps:
            break
    return reps


def symmetric_config(G, rho, rng, R=50):
    """random rho-symmetric integer planes, h_{g r} = diag(rho(g),1) h_r."""
    planes = [None] * 12
    for r in range(12):
        if planes[r] is not None:
            continue
        h = [rng.randint(-R, R) for _ in range(4)]
        for g in G:
            M = rho[g]
            img = [sum(M[i][k] * h[k] for k in range(3)) for i in range(3)] + [h[3]]
            assert planes[g[r]] is None or planes[g[r]] == img
            planes[g[r]] = img
    return planes


def orbits(G, n=12):
    seen = set()
    out = []
    for i in range(n):
        if i in seen:
            continue
        o = sorted(set(g[i] for g in G))
        seen |= set(o)
        out.append(o)
    return out


def orbfix_quads(G, n=12):
    """INF-quadruples whose orbit-parity vectors (|S cap orbit_i| mod 2) form a GF(2) basis.
    Flipping h on whole orbits (vector f in GF(2)^k) multiplies chi(S) by (-1)^{<v(S),f>};
    a basis of k such vectors makes f -> (signs of the k chosen quads) bijective."""
    orbs = orbits(G, n)
    oid = {v: k for k, o in enumerate(orbs) for v in o}
    k = len(orbs)
    INF = n
    piv = {}
    basis = []
    for S in itertools.combinations(range(n), 3):
        v = 0
        for x in S:
            v ^= 1 << oid[x]
        w = v
        while w:
            h = w.bit_length() - 1
            if h in piv:
                w ^= piv[h]
            else:
                piv[h] = w
                basis.append(S + (INF,))
                break
        if len(basis) == k:
            break
    assert len(basis) == k
    return basis, orbs


def build_sym(T, G, eps, opts, mirror=True, orbfix=True):
    C = CNF(12)
    sym = [(g, eps[g]) for g in G if g != tuple(range(12))]
    o = dict(opts)
    o['symbreak'] = False
    o['mirror'] = False
    build(C, T, o, sym=sym)
    basis, orbs = orbfix_quads(G)
    for S in (basis if orbfix else []):
        C.clause([C.chi_pos_lit(S)], 'SB_ORBFLIP')
    if mirror:
        C.clause([C.chi_pos_lit((0, 1, 2, 3))], 'SB_MIRROR')
    return C, basis, orbs


def sym_consistency(G, eps, n=12):
    """immediate contradictions chi(S) = -chi(S) forced by the symmetry relation."""
    bad = []
    INF = n
    for S in itertools.combinations(range(n + 1), 4):
        for g in G:
            img = tuple(g[e] if e < n else INF for e in S)
            if tuple(sorted(img)) == S:
                sgnp = -1 if perm_parity(img) else 1
                if sgnp * eps[g] != 1:
                    bad.append((S, g))
    return bad


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('map', type=int)
    ap.add_argument('group')
    ap.add_argument('--opts', default='')
    ap.add_argument('--which', type=int, default=0, help='index of conjugacy-class representative')
    ap.add_argument('--solver', default='cadical195')
    ap.add_argument('--timeout', type=float, default=600)
    ap.add_argument('--proof', default='')
    ap.add_argument('--dimacs', default='')
    ap.add_argument('--nonorm', action='store_true', help='no orbit-flip / mirror normalisation')
    args = ap.parse_args()
    maps = parse_lutz()
    otris = orient(maps[args.map])
    links, succ = links_from_oriented(otris)
    T = Triangulation(12, otris, links)
    auts = automorphisms(otris)
    eps = dict(auts)
    print('map #%d: |Aut| = %d, orientation-preserving %d' % (
        args.map, len(auts), sum(1 for _, e in auts if e > 0)))
    subs = [H for H in subgroups(auts) if classify(H) == args.group]
    # conjugacy classes in Aut
    classes = []
    for H in sorted(subs, key=lambda H: sorted(H)):
        conj = False
        for K in classes:
            for a, _ in auts:
                ainv = tuple(sorted(range(12), key=lambda i: a[i]))
                if frozenset(compose(compose(a, h), ainv) for h in H) == K:
                    conj = True
                    break
            if conj:
                break
        if not conj:
            classes.append(H)
    print('subgroups of type %s: %d, conjugacy classes: %d' % (args.group, len(subs), len(classes)))
    H = classes[args.which]
    print('chosen subgroup: free action on faces: %s; orbits %s' % (free(H), orbits(H)))
    print('eps on subgroup:', sorted(eps[g] for g in H))
    gens = sorted(H)
    bad = sym_consistency(H, eps)
    print('forced-zero quadruples:', len(bad))
    reps = find_reps(H, eps)
    print('faithful signed-permutation reps with det = eps:', len(reps))
    rng = random.Random(1)
    unif = []
    for rho in reps:
        u = False
        for _ in range(5):        # one uniform sample proves generic uniformity
            pl = symmetric_config(H, rho, rng, R=1000)
            chi = chirotope_from_planes(pl)
            if all(v != 0 for v in chi.values()):
                u = True
                break
        unif.append(u)
    print('random symmetric configs uniform:', sum(unif), '/', len(unif))
    # sanity: chi of an explicit symmetric configuration obeys chi(gS) = eps(g) chi(S)
    if reps:
        pl = symmetric_config(H, reps[0], rng)
        chi = chirotope_from_planes(pl)
        ev = Eval(12, chi)
        okc = all(ev.chi_neg(tuple(g[e] if e < 12 else 12 for e in S)) == (ev.chi_neg(S) ^ (eps[g] < 0))
                  for g in H for S in itertools.combinations(range(13), 4))
        print('explicit symmetric configuration satisfies the SYM relation:', okc)
    opts = dict(gp=True, triples=True)
    for k in args.opts.split(','):
        if k:
            opts[k] = True
    C, basis, orbs = build_sym(T, H, eps, opts, mirror=not args.nonorm, orbfix=not args.nonorm)
    print('orbit-flip normalisation quads:', basis)
    # controls: (i) without forbidden triples the symmetric instance is SAT;
    # (ii) an explicit symmetric configuration, normalised by orbit flips (+ mirror), satisfies it
    from pysat.solvers import Solver as _S
    C0, _, _ = build_sym(T, H, eps, dict(gp=True, triples=False))
    with _S(name='cadical195', bootstrap_with=C0.clauses) as s0:
        print('control (no triples) SAT:', s0.solve())
        if reps:
            for _ in range(20):
                pl = symmetric_config(H, reps[0], rng, R=1000)
                chi = chirotope_from_planes(pl)
                if all(v != 0 for v in chi.values()):
                    break
            oid = {v: k for k, o in enumerate(orbs) for v in o}
            for f in itertools.product((1, -1), repeat=len(orbs)):
                pf = [[f[oid[X]] * x for x in pl[X]] for X in range(12)]
                cf = chirotope_from_planes(pf)
                ev = Eval(12, cf)
                if all(not ev.chi_neg(S) for S in basis):
                    break
            if ev.chi_neg((0, 1, 2, 3)):
                cf = {S: (-v if 12 not in S else v) for S, v in cf.items()}
            units = [C0.qvar[S] if v > 0 else -C0.qvar[S] for S, v in cf.items()]
            print('control (explicit symmetric chi, normalised) SAT:', s0.solve(assumptions=units))
    print('instance: vars %d clauses %d families %s' % (C.nv, len(C.clauses), C.tags))
    # sanity: the rho-symmetric random config chirotope satisfies the SYM clauses
    if args.dimacs:
        C.dimacs(args.dimacs, comments=['OM-SAT Track 3 map #%d group %s opts %s' % (args.map, args.group, opts)])
    from pysat.solvers import Solver
    import threading
    t0 = time.time()
    kw = {}
    if args.proof:
        kw['with_proof'] = True
    s = Solver(name=args.solver, bootstrap_with=C.clauses, **kw)
    timer = threading.Timer(args.timeout, lambda: s.interrupt())
    timer.start()
    r = s.solve_limited(expect_interrupt=True)
    timer.cancel()
    dt = time.time() - t0
    res = {True: 'SAT', False: 'UNSAT', None: 'TIMEOUT'}[r]
    print('RESULT map #%d %s opts=%s solver=%s: %s in %.1fs' % (args.map, args.group, args.opts, args.solver, res, dt))
    print('stats', s.accum_stats())
    if r is False and args.proof:
        pr = s.get_proof()
        with open(args.proof, 'w') as f:
            for line in pr:
                f.write(line + '\n')
        print('proof lines', len(pr), 'written to', args.proof)
    if r is True:
        m = s.get_model()
        chi = {''.join(map(str, S)): (1 if m[v - 1] > 0 else -1) for S, v in C.qvar.items()}
        out = os.path.join(RDIR, 'experiments', 'omsat', 'sym_%d_%s_chi.json' % (args.map, args.group))
        json.dump(chi, open(out, 'w'))
        print('chirotope saved', out)
    s.delete()


if __name__ == '__main__':
    main()
