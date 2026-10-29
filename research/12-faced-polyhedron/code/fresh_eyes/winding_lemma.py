"""Check the face-winding lemma  r_X = sigma_X + 2 w_X - 2  (gauge normals g):
 w_X     = winding number about 0 of the polygon (p_B1..p_B11), p_B = projection of g_B to g_X^perp,
           B_i in link (= CCW boundary) order of face X, plane oriented by g_X;
 sigma_X = #corners of X at saddle vertices (det(g_X,g_Bi,g_Bi+1) < 0);
 r_X     = #reflex corners of F_X.
Part 1: Szilassi (actual polygons). Part 2: Gauss-admissible normals from the annealer (types 0,5,58):
 does the kappa-CSP (F4 vertex rule + per-face flip count a_X = 2 - 2 w_X) have a solution?"""
import sys, json, math, itertools
import numpy as np
sys.path.insert(0, '/home/user/polyhedrons/research/12-faced-polyhedron/code')

def winding(gX, Bs, G):
    gX = gX / np.linalg.norm(gX)
    P = [G[b] - (G[b] @ gX) * gX for b in Bs]
    tot = 0.0
    for k in range(len(P)):
        a, b = P[k], P[(k + 1) % len(P)]
        tot += math.atan2(np.linalg.det(np.array([gX, a, b])), a @ b)
    w = tot / (2 * math.pi)
    assert abs(w - round(w)) < 1e-6, w
    return int(round(w))

# ---------------- Part 1: Szilassi ----------------
V = np.array([[-1.2,0,1.2],[1.2,0,1.2],[0,-1.26,-1.2],[0,1.26,-1.2],[0.2,-0.5,-0.8],[-0.2,0.5,-0.8],
 [-0.375,-0.375,-0.3],[0.375,0.375,-0.3],[0.45,-0.25,0.2],[-0.45,0.25,0.2],[-0.7,0,0.2],[0.7,0,0.2],[-0.7,-0.25,0.2],[0.7,0.25,0.2]])
F = [[9,7,5,2,1,13],[10,8,6,1,2,14],[7,8,10,11,3,5],[8,7,9,12,4,6],[6,4,3,11,13,1],[9,12,14,10,11,13],[3,5,2,14,12,4]]
F = [[i-1 for i in f] for f in F]; nF = len(F)
P = []
for f in F:
    X = V[f]; c = X.mean(0); u, s, vt = np.linalg.svd(X - c); P.append(vt[2])
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
    for k in range(len(f)): E[(f[k], f[(k+1) % len(f)])] = i
def area(n, f):
    a = np.cross(n, [1,0,0]) if abs(n[0]) < .9 else np.cross(n, [0,1,0]); a /= np.linalg.norm(a); b = np.cross(n, a)
    Q = np.c_[V[f] @ a, V[f] @ b]
    return 0.5 * sum(Q[k,0]*Q[(k+1)%len(f),1] - Q[(k+1)%len(f),0]*Q[k,1] for k in range(len(f)))
G = np.array([np.sign(area(P[i], f)) * P[i] for i, f in enumerate(F)])
print("Szilassi: face  sigma  w  r_actual  sigma+2w-2")
okall = True
for i, f in enumerate(F):
    m = len(f)
    Bs = [E[(f[(k+1) % m], f[k])] for k in range(m)]          # neighbour across edge (f[k], f[k+1])
    sig = 0; r = 0
    for k in range(m):                                         # corner at f[k+1] between B_k and B_{k+1}
        B1, B2 = Bs[k], Bs[(k+1) % m]
        if np.linalg.det(np.array([G[i], G[B1], G[B2]])) < 0: sig += 1
        a, b, c = V[f[k]], V[f[(k+1) % m]], V[f[(k+2) % m]]
        if G[i] @ np.cross(b - a, c - b) < 0: r += 1
    w = winding(G[i], Bs, G)
    print("  ", i+1, sig, w, r, sig + 2*w - 2)
    okall &= (r == sig + 2*w - 2)
print("Szilassi identity holds on all faces:", okall)

# ---------------- Part 2: annealed admissible normals ----------------
import z3
from gauss_degree import coherent_triangles, links_from, degree_at, covered_positive, tri_signs
from gauss_search import find_admissible
from fixed_normals import integer_normals
types = json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))

def kappa_csp(Gi, ot, links):
    n = 12
    sgn = {}
    for (a, b, c) in ot:
        d = int(np.sign(np.linalg.det(np.array([Gi[a], Gi[b], Gi[c]], float))))
        for t in ((a,b,c),(b,c,a),(c,a,b)): sgn[t] = d
    k = {frozenset(e): z3.Bool('k%d_%d' % tuple(sorted(e))) for e in itertools.combinations(range(n), 2)}
    s = z3.Solver(); info = []
    for (a, b, c) in ot:
        x, y, zz = k[frozenset((a,b))], k[frozenset((b,c))], k[frozenset((a,c))]
        if sgn[(a,b,c)] > 0: s.add(x == y, y == zz)
        else: s.add(z3.Not(z3.And(x == y, y == zz)))
    feasible_counts = True
    for X in range(n):
        Bs = links[X]; m = len(Bs)
        w = winding(np.array(Gi[X], float), Bs, np.array(Gi, float))
        sig = sum(1 for i in range(m) if sgn[(X, Bs[i], Bs[(i+1) % m])] < 0)
        aX = 2 - 2*w; rX = sig - aX
        info.append((w, sig, rX))
        if aX < 0 or rX < 0 or rX > 8: feasible_counts = False
        flips = [z3.If(k[frozenset((X, Bs[i]))] != k[frozenset((X, Bs[(i+1) % m]))], 1, 0) for i in range(m)]
        s.add(z3.Sum(flips) == aX)
    res = s.check() if feasible_counts else z3.unsat
    return feasible_counts, str(res), info

tot = {}
for tid in (0, 5, 58):
    e = next(t for t in types if t['id'] == tid)
    ot = coherent_triangles(e['triangles']); links = links_from(ot, 12)
    for seed in range(8):
        Gf, it = find_admissible(ot, np.random.default_rng(seed), minutes=1)
        if Gf is None:
            print('type', tid, 'seed', seed, 'no admissible normals found'); continue
        Gi = integer_normals(Gf)
        dets = tri_signs(Gi, ot)
        rng = np.random.default_rng(1000 + seed)
        U = [list(map(int, rng.integers(-10**6, 10**6, 3))) for _ in range(64)]
        exact_ok = degree_at(Gi, ot, U[0], dets) == -5 and all(covered_positive(Gi, ot, u, dets) for u in U)
        cnt, res, info = kappa_csp(Gi, ot, links)
        ws = [x[0] for x in info]; rs = [x[2] for x in info]
        s_cnt = sum(1 for d in dets if d < 0)
        print('type %2d seed %d exact-admissible %s saddles %d  w_X %s  r_X %s  counts-ok %s  kappaCSP %s'
              % (tid, seed, exact_ok, s_cnt, ws, rs, cnt, res), flush=True)
        tot.setdefault(tid, []).append((exact_ok, cnt, res))
print(json.dumps({str(k): v for k, v in tot.items()}))
