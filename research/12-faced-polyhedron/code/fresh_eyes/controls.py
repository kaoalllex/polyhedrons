"""Controls for closure_and_parity.py (B): (1) Szilassi (n=7) gauge normals must give SAT for
kappa-CSP + edge-orientation LP; (2) n=12 random planes: the LP with the configuration's OWN edge
orientation pattern (kappa-CSP dropped) must be SAT (checks vert_lin / sign conventions).
(3) parity of (face self-crossings + multi-reflex vertices) on the 1005 seeds."""
import sys, json, itertools, time
import numpy as np, z3
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code')
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code/fresh_eyes')
from gauss_degree import coherent_triangles, links_from
from fixed_normals import integer_normals
from local_viol import local_violations
import importlib.util
spec = importlib.util.spec_from_file_location('cp', '/home/user/polyhedrons/research/12-faced-polyhedron/code/fresh_eyes/closure_and_parity.py')
src = open(spec.origin).read()
# reuse helper functions only (skip the experiment loops)
helpers = src[src.index('def winding'):src.index('for tid in (0, 58, 5)')]
ns = {}; exec('import numpy as np, z3, itertools, time\nfrom fractions import Fraction\n' + helpers, ns)
winding, vert_lin = ns['winding'], ns['vert_lin']

def closure_smt_n(Gi, ot, links, n, use_kappa=True, fixed_sigma=None):
    G = np.array(Gi, float); sgn = {}
    for (a, b, c) in ot:
        d = int(np.sign(np.linalg.det(np.array([G[a], G[b], G[c]]))))
        for t in ((a,b,c),(b,c,a),(c,a,b)): sgn[t] = d
    k = {frozenset(e): z3.Bool('k%d_%d' % e) for e in itertools.combinations(range(n), 2)}
    s = z3.Solver(); E = [z3.Real('e%d' % i) for i in range(n)]; glob = z3.Bool('glob')
    if use_kappa:
        for (a, b, c) in ot:
            x, y, zz = k[frozenset((a,b))], k[frozenset((b,c))], k[frozenset((a,c))]
            s.add(z3.And(x == y, y == zz) if sgn[(a,b,c)] > 0 else z3.Not(z3.And(x == y, y == zz)))
    for X in range(n):
        Bs = links[X]; m = len(Bs)
        if use_kappa:
            w = winding(G[X], Bs, G)
            s.add(z3.Sum([z3.If(k[frozenset((X, Bs[i]))] != k[frozenset((X, Bs[(i+1) % m]))], 1, 0) for i in range(m)]) == 2 - 2*w)
        for i in range(m):
            c0 = vert_lin(Gi, X, Bs[i-1], Bs[i]); c1 = vert_lin(Gi, X, Bs[i], Bs[(i+1) % m])
            dv = np.cross(np.array(Gi[X], dtype=object), np.array(Gi[Bs[i]], dtype=object))
            coef = [sum((c1[r][j] - c0[r][j]) * int(dv[r]) for r in range(3)) for j in range(n)]
            lin = z3.Sum([z3.RealVal(str(cf)) * E[j] for j, cf in enumerate(coef) if cf != 0])
            if fixed_sigma is not None:
                s.add(lin >= 1 if fixed_sigma[(X, Bs[i])] > 0 else lin <= -1)
            else:
                s.add(z3.If(k[frozenset((X, Bs[i]))] == glob, lin >= 1, lin <= -1))
    return str(s.check())

# (1) Szilassi
V = np.array([[-1.2,0,1.2],[1.2,0,1.2],[0,-1.26,-1.2],[0,1.26,-1.2],[0.2,-0.5,-0.8],[-0.2,0.5,-0.8],
 [-0.375,-0.375,-0.3],[0.375,0.375,-0.3],[0.45,-0.25,0.2],[-0.45,0.25,0.2],[-0.7,0,0.2],[0.7,0,0.2],[-0.7,-0.25,0.2],[0.7,0.25,0.2]])
F = [[9,7,5,2,1,13],[10,8,6,1,2,14],[7,8,10,11,3,5],[8,7,9,12,4,6],[6,4,3,11,13,1],[9,12,14,10,11,13],[3,5,2,14,12,4]]
F = [[i-1 for i in f] for f in F]; nF = 7
P = []
for f in F:
    X = V[f]; c = X.mean(0); u, s_, vt = np.linalg.svd(X - c); P.append(vt[2])
def edges(f): return {(f[k], f[(k+1) % len(f)]) for k in range(len(f))}
done = {0}; todo = [0]
while todo:
    i = todo.pop()
    for j in range(nF):
        if j in done: continue
        if {frozenset(e) for e in edges(F[i])} & {frozenset(e) for e in edges(F[j])}:
            if edges(F[i]) & edges(F[j]): F[j] = F[j][::-1]
            done.add(j); todo.append(j)
E = {}
for i, f in enumerate(F):
    for k_ in range(len(f)): E[(f[k_], f[(k_+1) % len(f)])] = i
def area(n, f):
    a = np.cross(n, [1,0,0]) if abs(n[0]) < .9 else np.cross(n, [0,1,0]); a /= np.linalg.norm(a); b = np.cross(n, a)
    Q = np.c_[V[f] @ a, V[f] @ b]
    return 0.5 * sum(Q[k,0]*Q[(k+1)%len(f),1] - Q[(k+1)%len(f),0]*Q[k,1] for k in range(len(f)))
G = np.array([np.sign(area(P[i], f)) * P[i] for i, f in enumerate(F)])
tris = {}
for i, f in enumerate(F):
    m = len(f); Bs = [E[(f[(k+1) % m], f[k])] for k in range(m)]
    for k_ in range(m):
        t = (i, Bs[k_], Bs[(k_+1) % m]); r = min(range(3), key=lambda j: t[j]); tris[t[r:] + t[:r]] = 1
ot = list(tris); links = links_from(ot, 7)
Gi = integer_normals(G)
print('(1) Szilassi: %d oriented triangles; kappa-CSP + closure LP:' % len(ot), closure_smt_n(Gi, ot, links, 7), flush=True)

# (2) random n=12 planes, type 0, own orientation pattern
types = json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))
e0 = next(t for t in types if t['id'] == 0); ot0 = coherent_triangles(e0['triangles']); L0 = links_from(ot0, 12)
rng = np.random.default_rng(7)
for trial in range(2):
    Gi = [list(map(int, rng.integers(-1000, 1000, 3))) for _ in range(12)]
    e_true = rng.integers(-10**6, 10**6, 12)
    sig = {}
    for X in range(12):
        Bs = L0[X]; m = len(Bs)
        for i in range(m):
            c0 = np.array(ns['vert_lin'](Gi, X, Bs[i-1], Bs[i]), dtype=object); c1 = np.array(ns['vert_lin'](Gi, X, Bs[i], Bs[(i+1) % m]), dtype=object)
            dv = np.cross(np.array(Gi[X], dtype=object), np.array(Gi[Bs[i]], dtype=object))
            val = sum(sum((c1[r][j] - c0[r][j]) * int(e_true[j]) for j in range(12)) * int(dv[r]) for r in range(3))
            sig[(X, Bs[i])] = 1 if val > 0 else -1
    print('(2) random planes, own orientation pattern, LP:', closure_smt_n(Gi, ot0, L0, 12, use_kappa=False, fixed_sigma=sig), flush=True)

# (3) parity of crossings + multi on seeds
seeds = json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/overnight/data/seeds.json'))
par = {}
for sd in seeds:
    H = np.array(sd['planes'], float); ot = coherent_triangles(sd['triangles']); L = links_from(ot, 12)
    cr, multi, refl = local_violations(H, L)
    par[(cr + multi) % 2] = par.get((cr + multi) % 2, 0) + 1
print('(3) seeds: (crossings + multi) mod 2 ->', par)
