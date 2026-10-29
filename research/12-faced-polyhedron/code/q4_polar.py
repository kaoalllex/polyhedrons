"""Q4: polar duals of a vertex-version near-miss (12 points, 44 triangles) w.r.t. many centres.
Plane of point p w.r.t. the unit sphere about c: (p-c).(x-c) + 1 = 0. Same triangulation.
Usage: python3 -I q4_polar.py OBJ N_CENTRES SEED"""
import sys, numpy as np, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fastviol import triangulation_tables, violations
from gauss_degree import coherent_triangles, links_from, polygon_gauge, degree_at
from fixed_normals import integer_normals
V, F = [], []
for line in open(sys.argv[1]):
    p = line.split()
    if p and p[0] == 'v': V.append([float(x) for x in p[1:4]])
    if p and p[0] == 'f': F.append(sorted(int(x.split('/')[0]) - 1 for x in p[1:]))
V = np.array(V); pa, it = triangulation_tables(12, F); ot = coherent_triangles(F); L = links_from(ot, 12)
rng = np.random.default_rng(int(sys.argv[3])); sc = np.abs(V).max()
hist = collections.Counter(); best = (10 ** 9, None)
for i in range(int(sys.argv[2])):
    c = V.mean(0) + sc * float(rng.choice([0.05, 0.2, 0.5, 1.0])) * rng.standard_normal(3)
    n = V - c; H = np.hstack([n, (1 - n @ c)[:, None]])
    v = int(violations(H, pa, it))
    hist[v] += 1
    if v < best[0]:
        eps = [polygon_gauge(H, L, X) for X in range(12)]
        G = [[e * x for x in r] for e, r in zip(eps, integer_normals(H[:, :3]))]
        best = (v, degree_at(G, ot, [123457, -98765, 55555]))
print('violations histogram (lowest 10):', sorted(hist.items())[:10]); print('best', best[0], 'own Gauss degree', best[1])
