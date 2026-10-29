"""Q13: 12 tangent planes of a smooth genus-6 surface (tube of radius r around the K5 graph:
tetrahedron + centre), then the best triangulation by the Track 4 CP-SAT (all types at once).
Usage: python3 -I q13_tube_planes.py N_SAMPLES SEED TIME_LIMIT"""
import sys, json, itertools, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from planes import Arrangement
import geomsat
P = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1], [0, 0, 0]], float)
E = list(itertools.combinations(range(5), 2))
rng = np.random.default_rng(int(sys.argv[2])); res = []
for s in range(int(sys.argv[1])):
    r = float(rng.uniform(0.15, 0.45))
    edges = rng.choice(len(E), size=12, replace=len(E) < 12)
    H = []
    for k in edges:
        a, b = P[E[k][0]], P[E[k][1]]
        t = rng.uniform(0.25, 0.75); c = a + t * (b - a); d = (b - a) / np.linalg.norm(b - a)
        w = rng.standard_normal(3); w -= (w @ d) * d; w /= np.linalg.norm(w)
        x = c + r * w                                 # point on the tube, outward normal w
        H.append([w[0], w[1], w[2], -w @ x])
    Hi = [[int(round(v * 10 ** 6)) for v in h] for h in H]
    try:
        c, lb, tris, st, info = geomsat.solve_cpsat(Arrangement(Hi), time_limit=float(sys.argv[3]))
    except Exception as e:
        print('sample', s, 'error', repr(e)[:100], flush=True); continue
    print('sample', s, 'r %.2f' % r, 'cost', c, 'status', st, flush=True)
    res.append(c)
print('best', min(res) if res else None)
