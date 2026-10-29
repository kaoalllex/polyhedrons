"""Search for face normals that pass the Gauss-map prefilter (experiment E3).

Find 12 unit vectors g_X (gauge normals, signs included) such that the PL map
(dual triangulation) -> S^2 has degree -5 and its POSITIVE triangles cover the sphere.
These are necessary conditions for an embedded realization with these normals (gauss_degree.py).
Energy = 10 |deg + 5| + (number of sample directions not covered by a positive triangle).
Simulated annealing on the normals; the degree changes only when two normals pass through
antipodal position (every pair of faces is adjacent).

Usage: python3 -I gauss_search.py TRIANGULATIONS_JSON TYPE_ID MINUTES SEED OUT_JSON
"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles


def tri_index(otris):
    return np.array(otris, dtype=np.int64)


def cover_counts(G, T, U):
    """For sample directions U (m,3): returns (pos(u), neg(u)) counts of triangles containing u."""
    A, B, C = G[T[:, 0]], G[T[:, 1]], G[T[:, 2]]
    d = np.einsum('ij,ij->i', A, np.cross(B, C))                 # det(A,B,C)
    s = np.sign(d)
    # u in cone(A,B,C) iff det(u,B,C), det(A,u,C), det(A,B,u) all have sign s
    d1 = U @ np.cross(B, C).T                                      # det(u,B,C)
    d2 = U @ np.cross(C, A).T                                      # det(A,u,C) = u.(C x A)
    d3 = U @ np.cross(A, B).T                                      # det(A,B,u) = u.(A x B)
    inside = (d1 * s > 0) & (d2 * s > 0) & (d3 * s > 0)
    pos = (inside & (s > 0)).sum(axis=1)
    neg = (inside & (s < 0)).sum(axis=1)
    return pos, neg


def energy(G, T, U):
    pos, neg = cover_counts(G, T, U)
    deg = pos - neg
    dmed = int(np.median(deg))
    return 10 * abs(dmed + 5) + int((pos == 0).sum()) + int((deg != dmed).sum()), dmed, int((pos == 0).sum())


def main():
    types = json.load(open(sys.argv[1]))
    tid, minutes, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = np.random.default_rng(seed)
    ent = next(e for e in types if e['id'] == tid)
    ot = coherent_triangles(ent['triangles'])
    T = tri_index(ot)
    U = rng.standard_normal((3000, 3))
    U /= np.linalg.norm(U, axis=1)[:, None]
    G = rng.standard_normal((12, 3))
    G /= np.linalg.norm(G, axis=1)[:, None]
    E, deg, unc = energy(G, T, U)
    best = (E, G.copy(), deg, unc)
    t0 = time.time(); it = 0
    Tmp = 3.0
    while time.time() - t0 < 60 * minutes and best[0] > 0:
        it += 1
        k = int(rng.integers(12))
        G2 = G.copy()
        if rng.random() < 0.1:
            G2[k] = -G2[k]                                           # sign flip (gauge change)
        else:
            G2[k] += float(rng.choice([0.03, 0.1, 0.3, 1.0])) * rng.standard_normal(3)
            G2[k] /= np.linalg.norm(G2[k])
        E2, d2, u2 = energy(G2, T, U)
        if E2 <= E or rng.random() < np.exp((E - E2) / Tmp):
            G, E, deg, unc = G2, E2, d2, u2
            if E < best[0]:
                best = (E, G.copy(), deg, unc)
        Tmp = max(0.05, Tmp * 0.9997)
        if it % 2000 == 0:
            print(it, 'E', E, 'deg', deg, 'uncovered', unc, 'best', best[0], 'T %.2f' % Tmp, flush=True)
    json.dump({'type_id': tid, 'seed': seed, 'best_energy': best[0], 'degree': best[2], 'uncovered_samples': best[3],
               'normals': best[1].tolist(), 'iterations': it}, open(out, 'w'))
    print('done best', best[0], 'deg', best[2], 'uncovered', best[3], flush=True)


if __name__ == '__main__':
    main()
