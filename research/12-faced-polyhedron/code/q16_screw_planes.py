"""Idea from Ringel-Youngs current graphs (Kirchhoff): 12 planes as an orbit of a SCREW motion
(rotation by alpha about the z-axis + translation tau along it, plane_k = S^k plane_0), slightly
perturbed; not a symmetry of the finite polyhedron, so not excluded by the symmetric theorem.
Best triangulation over all 59 types by the Track 4 CP-SAT. Usage: N SEED TIME_LIMIT"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from planes import Arrangement
import geomsat
rng = np.random.default_rng(int(sys.argv[2])); best = None
for s in range(int(sys.argv[1])):
    alpha = rng.uniform(0.3, 2 * np.pi - 0.3); tau = rng.uniform(0.02, 0.4)
    n0 = rng.standard_normal(3); n0 /= np.linalg.norm(n0); d0 = rng.uniform(0.5, 1.5)
    H = []
    for k in range(12):
        c, si = np.cos(k * alpha), np.sin(k * alpha)
        R = np.array([[c, -si, 0], [si, c, 0], [0, 0, 1]])
        n = R @ n0; t = np.array([0, 0, k * tau])
        H.append([*n, -(d0 + n @ t)])                 # plane n.x = d0 + n.t  (image of n0.x = d0)
    H = np.array(H) + 0.01 * rng.standard_normal((12, 4))
    Hi = [[int(round(v * 10 ** 6)) for v in h] for h in H]
    try:
        c, lb, tris, st, info = geomsat.solve_cpsat(Arrangement(Hi), time_limit=float(sys.argv[3]))
    except Exception as e:
        print('sample', s, 'degenerate', repr(e)[:60], flush=True); continue
    print('sample', s, 'alpha %.2f tau %.2f' % (alpha, tau), 'cost', c, st, flush=True)
    if c is not None and (best is None or c < best): best = c
print('best', best)
