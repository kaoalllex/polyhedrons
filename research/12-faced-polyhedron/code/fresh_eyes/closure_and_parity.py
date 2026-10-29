"""(A) Umbrella-parity check on the 1005 HackerPoet seeds: for configurations whose 12 face polygons are
simple (0 crossings), predicted: sum_v C(r_v,2) even (=> #vertices with >=2 reflex corners even).
(B) For Gauss-admissible annealed normals (gauge fixed): is 'kappa-CSP (F4 + flip counts) + edge orientation
LP (every edge traversed in direction s*kappa_e*(g_X x g_B), polygon closure)' satisfiable over the offsets?"""
import sys, json, time, itertools
from fractions import Fraction
import numpy as np, z3
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code')
from gauss_degree import coherent_triangles, links_from
from local_viol import local_violations
from gauss_search import find_admissible
from fixed_normals import integer_normals

R = '/home/user/polyhedrons/research/12-faced-polyhedron/'
seeds = json.load(open(R + 'overnight/data/seeds.json'))
stats = {}
for sd in seeds:
    H = np.array(sd['planes'], float); ot = coherent_triangles(sd['triangles']); L = links_from(ot, 12)
    cr, multi, refl = local_violations(H, L)
    s2 = sum(v * (v - 1) // 2 for v in refl.values())
    key = ('simple' if cr == 0 else 'nonsimple', s2 % 2, multi % 2)
    stats[key] = stats.get(key, 0) + 1
print('(A) seeds by (faces simple?, sum C(r_v,2) mod 2, #multi-reflex mod 2):', stats, flush=True)

types = json.load(open(R + 'data/k12_triangulations.json'))

def winding(gX, Bs, G):
    gX = gX / np.linalg.norm(gX); P = [G[b] - (G[b] @ gX) * gX for b in Bs]
    t = sum(np.arctan2(np.linalg.det(np.array([gX, P[k], P[(k+1) % len(P)]])), P[k] @ P[(k+1) % len(P)]) for k in range(len(P)))
    return int(round(t / (2 * np.pi)))

def vert_lin(G, X, Y, Z):
    """v_XYZ as a 3x12 rational matrix acting on offsets e (planes G_X . x + e_X = 0)."""
    M = [[Fraction(c) for c in G[i]] for i in (X, Y, Z)]
    a, b, c = M
    det = a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
    cof = lambda r, s: (M[(r+1)%3][(s+1)%3]*M[(r+2)%3][(s+2)%3] - M[(r+1)%3][(s+2)%3]*M[(r+2)%3][(s+1)%3])
    inv = [[cof(s, r) / det for s in range(3)] for r in range(3)]       # inverse matrix
    out = [[Fraction(0)] * 12 for _ in range(3)]
    for r in range(3):
        for j, F in enumerate((X, Y, Z)):
            out[r][F] -= inv[r][j]                                     # v = M^{-1} (-e)
    return out

def closure_smt(Gi, ot, links, timeout=120):
    n = 12; G = np.array(Gi, float)
    sgn = {}
    for (a, b, c) in ot:
        d = int(np.sign(np.linalg.det(np.array([G[a], G[b], G[c]]))))
        for t in ((a,b,c),(b,c,a),(c,a,b)): sgn[t] = d
    k = {frozenset(e): z3.Bool('k%d_%d' % e) for e in itertools.combinations(range(n), 2)}
    s = z3.Solver(); s.set('timeout', timeout * 1000)
    for (a, b, c) in ot:
        x, y, zz = k[frozenset((a,b))], k[frozenset((b,c))], k[frozenset((a,c))]
        s.add(z3.And(x == y, y == zz) if sgn[(a,b,c)] > 0 else z3.Not(z3.And(x == y, y == zz)))
    E = [z3.Real('e%d' % i) for i in range(n)]; glob = z3.Bool('glob')
    for X in range(n):
        Bs = links[X]; m = len(Bs); w = winding(G[X], Bs, G)
        s.add(z3.Sum([z3.If(k[frozenset((X, Bs[i]))] != k[frozenset((X, Bs[(i+1) % m]))], 1, 0) for i in range(m)]) == 2 - 2*w)
        for i in range(m):
            c0 = vert_lin(Gi, X, Bs[i-1], Bs[i]); c1 = vert_lin(Gi, X, Bs[i], Bs[(i+1) % m])
            dvec = np.cross(np.array(Gi[X], dtype=object), np.array(Gi[Bs[i]], dtype=object))
            coef = [sum((c1[r][j] - c0[r][j]) * int(dvec[r]) for r in range(3)) for j in range(n)]
            lin = z3.Sum([z3.RealVal(str(cf)) * E[j] for j, cf in enumerate(coef) if cf != 0])
            pos = (k[frozenset((X, Bs[i]))] == glob)                   # orientation sign = s * kappa
            s.add(z3.If(pos, lin >= 1, lin <= -1))
    t0 = time.time(); r = s.check(); return str(r), time.time() - t0

for tid in (0, 58, 5):
    e = next(t for t in types if t['id'] == tid)
    ot = coherent_triangles(e['triangles']); links = links_from(ot, 12)
    for seed in (0, 1, 2, 4):
        Gf, _ = find_admissible(ot, np.random.default_rng(seed), minutes=1)
        if Gf is None: continue
        Gi = integer_normals(Gf)
        r, dt = closure_smt(Gi, ot, links)
        print('(B) type %2d seed %d  kappa-CSP + edge-orientation/closure LP: %s (%.1f s)' % (tid, seed, r, dt), flush=True)
