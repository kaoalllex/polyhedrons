"""Anneal plane OFFSETS for fixed Gauss-admissible normals; minimize the float violation count.

Usage: python3 -I offset_anneal.py TYPES_JSON TYPE_ID MINUTES SEED OUT_JSON
Normals: found by gauss_search.find_admissible (degree -5, convex covering), then fixed.
Question: how close to an embedding can configurations with topologically admissible normals get?
"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles
from gauss_search import find_admissible
from fastviol import triangulation_tables, violations


def main():
    types = json.load(open(sys.argv[1]))
    tid, minutes, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = np.random.default_rng(seed)
    tri = next(e for e in types if e['id'] == tid)['triangles']
    ot = coherent_triangles(tri)
    G, _ = find_admissible(ot, rng, minutes=2)
    assert G is not None
    pa, it = triangulation_tables(12, tri)
    best_all = None
    t0 = time.time()
    while time.time() - t0 < 60 * minutes:
        e = rng.standard_normal(12)
        H = np.hstack([G, e[:, None]])
        cur = violations(H, pa, it); best = (cur, H.copy())
        Tmp, sig = 2.0, 0.3
        for step in range(200000):
            k = int(rng.integers(12)); H2 = H.copy()
            H2[k, 3] += sig * rng.standard_normal()
            c2 = violations(H2, pa, it)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / Tmp):
                H, cur = H2, c2
                if cur < best[0]:
                    best = (cur, H.copy())
            Tmp = max(0.02, Tmp * 0.99997); sig = max(0.003, sig * 0.99998)
            if time.time() - t0 > 60 * minutes:
                break
        print('restart best', best[0], flush=True)
        if best_all is None or best[0] < best_all[0]:
            best_all = best
    json.dump({'type_id': tid, 'best_count': int(best_all[0]), 'planes': best_all[1].tolist(), 'triangles': tri},
              open(out, 'w'))
    print('done', best_all[0], flush=True)


if __name__ == '__main__':
    main()
