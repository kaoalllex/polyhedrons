"""EXACT verification (rational arithmetic) for ladder rung 8b (ladder4.py): 8 faces, 16 three-valent
and 2 four-valent vertices. Same checks as ladder_exact.verify, adapted:
  * free planes are rounded to integers (scale 10^9); each quadrilateral's dependent plane gets its
    offset EXACTLY from the point of the other three, so the 4-valent vertices are exact;
  * a corner triple occurs at 3 faces (3-valent vertex) or once inside a quadrilateral (4-valent);
  * for the two opposite faces of a quadrilateral, the common point is allowed besides their shared edge.
Usage: python3 -I ladder4_exact.py RESULTS_JSON [INDEX ...]"""
import json, sys
from fractions import Fraction as F
from itertools import combinations
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder_exact import solve3, seg_meet, in_closed


def verify4(planes, links, quads, dep):
    n = len(planes)
    H = [list(int(round(v * 10 ** 9)) for v in h) for h in planes]
    for q, d in zip(quads, dep):
        others = [x for x in q if x != d]
        P = solve3([H[x] for x in sorted(others)])
        H[d][3] = -(H[d][0] * P[0] + H[d][1] * P[1] + H[d][2] * P[2])
    H = [tuple(h) for h in H]
    out = {}
    qsets = [frozenset(q) for q in quads]
    corners = {}
    for X, L in links.items():
        m = len(L)
        for i in range(m):
            corners.setdefault(frozenset((X, L[i], L[(i + 1) % m])), []).append((X, i))
    def vkey(t):                                       # vertex identity: quad or triple
        for qi, qs in enumerate(qsets):
            if t <= qs:
                return ('quad', qi)
        return ('tri', t)
    ok_map = all(len(t) == 3 for t in corners) and all(
        (len(v) == 3) or (len(v) == 1 and vkey(t)[0] == 'quad') for t, v in corners.items())
    out['map_ok'] = ok_map
    out['all_pairs_adjacent'] = all(Y in links[X] for X, Y in combinations(range(n), 2))
    V = len({vkey(t) for t in corners}); E = sum(len(L) for L in links.values()) // 2
    out['V_E_F_chi'] = (V, E, n, V - E + n)
    P = {t: solve3([H[x] for x in sorted(t)]) for t in corners}
    pts = {}
    for t, p in P.items():
        pts.setdefault(vkey(t), set()).add(p)
    out['quad_points_exact'] = all(len(s) == 1 for k, s in pts.items() if k[0] == 'quad')
    allp = [next(iter(s)) for s in pts.values()]
    out['points_distinct'] = len(set(allp)) == len(allp)
    drop = {}
    for X in range(n):
        a = [abs(v) for v in H[X][:3]]; drop[X] = a.index(max(a))
    def to2(X, p):
        k = drop[X]; return tuple(p[j] for j in range(3) if j != k)
    poly = {X: [P[frozenset((X, L[i], L[(i + 1) % len(L)]))] for i in range(len(L))] for X, L in links.items()}
    Q2 = {X: [to2(X, p) for p in poly[X]] for X in poly}
    simple = 0
    for X, Q in Q2.items():
        m = len(Q); ok = True
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                if seg_meet(Q[i], Q[(i + 1) % m], Q[j], Q[(j + 1) % m]):
                    ok = False
        simple += ok
    out['simple_faces'] = simple
    def edges_on(X, Y):
        L = links[X]; m = len(L)
        return [frozenset((poly[X][i - 1], poly[X][i])) for i in range(m) if L[i] == Y]
    out['edges_consistent'] = all(sorted(map(sorted, edges_on(X, Y))) == sorted(map(sorted, edges_on(Y, X)))
                                  for X, Y in combinations(range(n), 2))
    qpts = {qi: next(iter(pts[('quad', qi)])) for qi in range(len(quads))}
    bad = []
    for X, Y in combinations(range(n), 2):
        hx, hy = H[X], H[Y]
        d = (hx[1] * hy[2] - hx[2] * hy[1], hx[2] * hy[0] - hx[0] * hy[2], hx[0] * hy[1] - hx[1] * hy[0])
        k = max(range(3), key=lambda j: abs(d[j]))
        p0 = solve3([hx, hy, tuple(1 if j == k else 0 for j in range(3)) + (0,)])
        par = lambda p: (p[k] - p0[k]) / d[k]
        pt = lambda t: tuple(p0[j] + t * d[j] for j in range(3))
        shared = [tuple(sorted(par(p) for p in e)) for e in edges_on(X, Y)]
        allowed_pts = [par(qpts[qi]) for qi, qs in enumerate(qsets) if X in qs and Y in qs]
        crit = set(allowed_pts)
        for Z in (X, Y):
            W = Y if Z == X else X
            L = links[Z]; m = len(L); Pz = poly[Z]
            for i in range(m):
                a, b = Pz[i - 1], Pz[i]
                if L[i] == W:
                    crit.add(par(a)); crit.add(par(b)); continue
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
                if not any(s0 <= t <= s1 for s0, s1 in shared) and t not in allowed_pts:
                    bad.append((X, Y)); break
    out['bad_pairs'] = bad
    out['EMBEDDED'] = (ok_map and out['all_pairs_adjacent'] and out['quad_points_exact'] and out['points_distinct']
                       and simple == n and out['edges_consistent'] and not bad)
    return out


if __name__ == '__main__':
    R = json.load(open(sys.argv[1]))
    for i in ([int(x) for x in sys.argv[2:]] or range(len(R))):
        r = R[i]
        if r.get('planes') is None:
            continue
        print(i, verify4(r['planes'], {int(k): v for k, v in r['links'].items()}, r['quads'], r['dep']), flush=True)
