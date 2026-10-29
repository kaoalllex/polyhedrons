"""Idea from external review (z.ai #5): SYMMETRIC plane arrangements with an arbitrary (possibly
asymmetric) triangulation. The symmetric-case theorem excludes symmetric polyhedra, not symmetric
plane sets with symmetry-breaking combinatorics. 12 planes = one generic orbit of the tetrahedral
rotation group T (order 12): plane n.x = 1 rotated; best triangulation by Track 4 CP-SAT.
Usage: python3 -I q15_symmetric_planes.py N_SAMPLES SEED TIME_LIMIT"""
import sys, itertools, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from planes import Arrangement
import geomsat
def T_group():
    I = np.eye(3); G = [I]
    for k in range(3):                                  # half-turns about axes
        D = -np.eye(3); D[k, k] = 1; G.append(D)
    for s in itertools.product((1, -1), repeat=3):      # 3-fold about body diagonals
        if s[0] * s[1] * s[2] != 1:
            continue
        P = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
        S = np.diag(s)
        G.append(S @ P @ S); G.append(S @ P.T @ S)
    return G
G = T_group(); assert len(G) == 12
rng = np.random.default_rng(int(sys.argv[2])); best = None
for s in range(int(sys.argv[1])):
    n = rng.standard_normal(3); n /= np.linalg.norm(n)
    H = [[*(R @ n), -1.0] for R in G]
    Hi = [[int(round(v * 10 ** 6)) for v in h] for h in H]
    try:
        c, lb, tris, st, info = geomsat.solve_cpsat(Arrangement(Hi), time_limit=float(sys.argv[3]))
    except Exception as e:
        print('sample', s, 'degenerate/error', repr(e)[:80], flush=True); continue
    print('sample', s, 'n', np.round(n, 3), 'cost', c, st, flush=True)
    if c is not None and (best is None or c < best):
        best = c
print('best', best)
