"""EXACT verification (rational arithmetic) of a ladder configuration: n planes + 'links'
(cyclic neighbour lists, repetitions = doubled adjacencies). Independent of ladder.py's float code.

Checks:
  M. the map: every corner triple distinct; every pair of faces adjacent; Euler characteristic;
     each edge (dart X->Y at position i) has the same endpoints in face X and in face Y.
  G. geometry: all corner points distinct; every face polygon simple (no two non-adjacent edges
     meet, closed segments, collinear overlaps included);
  P. for every pair of faces X, Y: (closed face X) cap (closed face Y) = union of their shared edges,
     decided exactly on the line X cap Y (all critical points + every open interval between them).
Simple faces + P for every pair (all pairs are adjacent) => the faces form an embedded closed surface.
Usage: python3 -I ladder_exact.py RESULTS_JSON [INDEX ...]   (planes scaled by 10^9 and rounded)"""
import json, sys
from fractions import Fraction as F
from itertools import combinations


def solve3(P):
    (a1, b1, c1, d1), (a2, b2, c2, d2), (a3, b3, c3, d3) = P
    det = a1 * (b2 * c3 - b3 * c2) - b1 * (a2 * c3 - a3 * c2) + c1 * (a2 * b3 - a3 * b2)
    assert det != 0, 'three planes not in general position'
    r1, r2, r3 = -d1, -d2, -d3
    x = r1 * (b2 * c3 - b3 * c2) - b1 * (r2 * c3 - r3 * c2) + c1 * (r2 * b3 - r3 * b2)
    y = a1 * (r2 * c3 - r3 * c2) - r1 * (a2 * c3 - a3 * c2) + c1 * (a2 * r3 - a3 * r2)
    z = a1 * (b2 * r3 - b3 * r2) - b1 * (a2 * r3 - a3 * r2) + r1 * (a2 * b3 - a3 * b2)
    return (F(x, det), F(y, det), F(z, det))


def orient(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (v > 0) - (v < 0)


def on_seg(a, b, q):
    return orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])


def seg_meet(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 * o2 < 0 and o3 * o4 < 0:
        return True
    return on_seg(a, b, c) or on_seg(a, b, d) or on_seg(c, d, a) or on_seg(c, d, b)


def in_closed(Q, q):
    m = len(Q)
    for i in range(m):
        if on_seg(Q[i], Q[(i + 1) % m], q):
            return True
    c = False
    for i in range(m):
        a, b = Q[i], Q[(i + 1) % m]
        if (a[1] > q[1]) != (b[1] > q[1]):
            # x-coordinate of the crossing > q.x  <=>  sign test without division
            s = (b[0] - a[0]) * (q[1] - a[1]) - (q[0] - a[0]) * (b[1] - a[1])
            if (s > 0) == (b[1] > a[1]):
                c = not c
    return c


def verify(H, links, require_all_pairs=True):
    n = len(H)
    H = [tuple(int(round(v * 10 ** 9)) for v in h) for h in H]
    out = {}
    # ---- map
    corners = {}
    for X, L in links.items():
        m = len(L)
        for i in range(m):
            corners.setdefault(frozenset((X, L[i], L[(i + 1) % m])), []).append((X, i))
    out['corner_triples_distinct'] = all(len(t) == 3 for t in corners) and all(len(v) == 3 for v in corners.values())
    out['all_pairs_adjacent'] = all(Y in links[X] for X, Y in combinations(range(n), 2))
    V = len(corners); E = sum(len(L) for L in links.values()) // 2
    out['V_E_F_chi'] = (V, E, n, V - E + n)
    # ---- geometry
    P = {t: solve3([H[x] for x in sorted(t)]) for t in corners}
    out['points_distinct'] = len(set(P.values())) == len(P)
    drop = {}
    for X in range(n):
        a = [abs(v) for v in H[X][:3]]; drop[X] = a.index(max(a))
    def to2(X, p):
        k = drop[X]; return tuple(p[j] for j in range(3) if j != k)
    poly = {}
    for X, L in links.items():
        m = len(L)
        poly[X] = [P[frozenset((X, L[i], L[(i + 1) % m]))] for i in range(m)]   # vertex i
    Q2 = {X: [to2(X, p) for p in poly[X]] for X in poly}
    simple = {}
    for X, Q in Q2.items():
        m = len(Q); ok = True
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                if seg_meet(Q[i], Q[(i + 1) % m], Q[j], Q[(j + 1) % m]):
                    ok = False
        simple[X] = ok
    out['simple_faces'] = sum(simple.values()); out['nonsimple_faces'] = sorted(X for X, ok in simple.items() if not ok)
    # edge consistency: edge i of face X (on line X cap L[i]) joins vertex i-1 and vertex i
    def edges_on(X, Y):
        L = links[X]; m = len(L)
        return [frozenset((poly[X][i - 1], poly[X][i])) for i in range(m) if L[i] == Y]
    out['edges_consistent'] = all(sorted(map(sorted, edges_on(X, Y))) == sorted(map(sorted, edges_on(Y, X)))
                                  for X, Y in combinations(range(n), 2))
    # ---- pairs, exactly on the line X cap Y
    bad = []
    for X, Y in combinations(range(n), 2):
        hx, hy = H[X], H[Y]
        d = (hx[1] * hy[2] - hx[2] * hy[1], hx[2] * hy[0] - hx[0] * hy[2], hx[0] * hy[1] - hx[1] * hy[0])
        k = max(range(3), key=lambda j: abs(d[j]))
        aux = tuple(1 if j == k else 0 for j in range(3)) + (0,)        # plane x_k = 0 through the line
        p0 = solve3([hx, hy, aux])
        par = lambda p: (p[k] - p0[k]) / d[k]                            # exact parameter along the line
        pt = lambda t: tuple(p0[j] + t * d[j] for j in range(3))
        shared = [tuple(sorted(par(p) for p in e)) for e in edges_on(X, Y)]
        crit = set()
        for Z in (X, Y):
            L = links[Z]; m = len(L); Pz = poly[Z]
            for i in range(m):
                a, b = Pz[i - 1], Pz[i]
                if L[i] == (Y if Z == X else X):
                    crit.add(par(a)); crit.add(par(b)); continue
                # segment a-b in plane Z meets the line where the other plane's value changes sign
                W = Y if Z == X else X
                fa = sum(H[W][j] * a[j] for j in range(3)) + H[W][3]
                fb = sum(H[W][j] * b[j] for j in range(3)) + H[W][3]
                if fa == 0:
                    crit.add(par(a))
                if fb == 0:
                    crit.add(par(b))
                if fa * fb < 0:
                    t = fa / (fa - fb); crit.add(par(tuple(a[j] + t * (b[j] - a[j]) for j in range(3))))
        crit = sorted(crit)
        samples = list(crit) + [(u + v) / 2 for u, v in zip(crit[:-1], crit[1:])]
        for t in samples:
            q = pt(t)
            if in_closed(Q2[X], to2(X, q)) and in_closed(Q2[Y], to2(Y, q)):
                if not any(s0 <= t <= s1 for s0, s1 in shared):
                    bad.append((X, Y)); break
    out['bad_pairs'] = bad
    out['EMBEDDED'] = (out['corner_triples_distinct'] and (out['all_pairs_adjacent'] or not require_all_pairs) and out['points_distinct']
                       and out['simple_faces'] == n and out['edges_consistent'] and not bad)
    return out


if __name__ == '__main__':
    R = json.load(open(sys.argv[1]))
    idx = [int(i) for i in sys.argv[2:]] or range(len(R))
    for i in idx:
        r = R[i]
        links = {int(k): v for k, v in r['links'].items()}
        print(i, verify(r['planes'], links), flush=True)
