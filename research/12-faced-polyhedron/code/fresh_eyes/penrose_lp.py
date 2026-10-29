"""'Penrose relaxation' of the fixed-normal closure LP. Unknown per edge e=XY a scalar alpha_e with
edge vector (in face X's CCW traversal) = alpha_e * (g_X x g_Y); sign(alpha_e) = s*kappa_e; every face closes:
sum_i alpha_{X B_i} (g_X x g_{B_i}) = 0.  NO period conditions (cycles of the edge graph around handles need not
close). LP_loc feasible but full LP infeasible => the fixed-normal obstruction is cohomological (Penrose-type:
locally consistent, globally impossible figure). Same normals/seeds as closure_and_parity.py; Szilassi control."""
import sys, json, itertools, time
import numpy as np, z3
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code')
from gauss_degree import coherent_triangles, links_from
from gauss_search import find_admissible
from fixed_normals import integer_normals

def winding(gX, Bs, G):
    gX = gX / np.linalg.norm(gX); P = [G[b] - (G[b] @ gX) * gX for b in Bs]
    t = sum(np.arctan2(np.linalg.det(np.array([gX, P[k], P[(k+1) % len(P)]])), P[k] @ P[(k+1) % len(P)]) for k in range(len(P)))
    return int(round(t / (2 * np.pi)))

def penrose(Gi, ot, links, n, with_kappa=True):
    G = np.array(Gi, float); sgn = {}
    for (a, b, c) in ot:
        d = int(np.sign(np.linalg.det(np.array([G[a], G[b], G[c]]))))
        for t in ((a,b,c),(b,c,a),(c,a,b)): sgn[t] = d
    k = {frozenset(e): z3.Bool('k%d_%d' % e) for e in itertools.combinations(range(n), 2)}
    al = {frozenset(e): z3.Real('a%d_%d' % e) for e in itertools.combinations(range(n), 2)}
    s = z3.Solver(); glob = z3.Bool('glob'); s.set('timeout', 120000)
    for (a, b, c) in ot:
        x, y, zz = k[frozenset((a,b))], k[frozenset((b,c))], k[frozenset((a,c))]
        s.add(z3.And(x == y, y == zz) if sgn[(a,b,c)] > 0 else z3.Not(z3.And(x == y, y == zz)))
    for e in k:
        s.add(z3.If(k[e] == glob, al[e] >= 1, al[e] <= -1))
    for X in range(n):
        Bs = links[X]; m = len(Bs); w = winding(G[X], Bs, G)
        s.add(z3.Sum([z3.If(k[frozenset((X, Bs[i]))] != k[frozenset((X, Bs[(i+1) % m]))], 1, 0) for i in range(m)]) == 2 - 2*w)
        T = [np.cross(np.array(Gi[X], dtype=object), np.array(Gi[B], dtype=object)) for B in Bs]
        for r in range(3):
            s.add(z3.Sum([int(T[i][r]) * al[frozenset((X, Bs[i]))] for i in range(m)]) == 0)
    t0 = time.time(); res = s.check(); return str(res), time.time() - t0

R = '/home/user/polyhedrons/research/12-faced-polyhedron/'
types = json.load(open(R + 'data/k12_triangulations.json'))
for tid in (0, 58, 5):
    e = next(t for t in types if t['id'] == tid)
    ot = coherent_triangles(e['triangles']); links = links_from(ot, 12)
    for seed in (0, 1, 2, 4):
        Gf, _ = find_admissible(ot, np.random.default_rng(seed), minutes=1)
        if Gf is None: continue
        Gi = integer_normals(Gf)
        r, dt = penrose(Gi, ot, links, 12)
        print('type %2d seed %d  LP_loc (face closures + kappa-CSP, no periods): %s (%.1f s)' % (tid, seed, r, dt), flush=True)
