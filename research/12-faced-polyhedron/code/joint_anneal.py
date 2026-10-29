"""Q1: anneal normals AND offsets, keeping the normals Gauss-admissible (degree -5, convex
covering on sample directions) at every step; minimize the float violation count.
Usage: python3 -I joint_anneal.py TYPES_JSON TYPE_ID MINUTES SEED OUT_JSON [START_JSON]
"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles
from gauss_search import find_admissible, cover_counts, tri_index
from fastviol import triangulation_tables, violations


def admissible(G, T, U):
    pos, neg = cover_counts(G, T, U)
    return bool(np.all(pos - neg == -5) and np.all(pos > 0))


def main():
    types = json.load(open(sys.argv[1]))
    tid, minutes, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = np.random.default_rng(seed)
    tri = next(e for e in types if e['id'] == tid)['triangles']
    ot = coherent_triangles(tri); T = tri_index(ot)
    U = rng.standard_normal((1500, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
    pa, it = triangulation_tables(12, tri)
    if len(sys.argv) > 6:                       # Q2: start from a seed configuration
        from gauss_degree import links_from, polygon_gauge
        sd = json.load(open(sys.argv[6]))
        tri = sd['triangles']; ot = coherent_triangles(tri); T = tri_index(ot)
        pa, it = triangulation_tables(12, tri)
        Hs = np.array(sd['planes'], float); Hs /= np.linalg.norm(Hs[:, :3], axis=1)[:, None]
        L = links_from(ot, 12)
        eps = np.array([polygon_gauge(Hs, L, X) for X in range(12)], float)
        G, _ = find_admissible(ot, rng, minutes=3, G0=Hs[:, :3] * eps[:, None], small=True)
        assert G is not None, 'no admissible normals near the seed'
        e = Hs[:, 3] * eps
        print('seed', sd.get('source'), 'max normal change %.3f' % float(np.max(np.linalg.norm(G - Hs[:, :3] * eps[:, None], axis=1))), flush=True)
    else:
        G, _ = find_admissible(ot, rng, minutes=2)
        e = rng.standard_normal(12)
    H = np.hstack([G, e[:, None]]); cur = violations(H, pa, it); best = (cur, H.copy())
    Tmp = 2.0; t0 = time.time(); step = 0; nacc = 0
    while time.time() - t0 < 60 * minutes:
        step += 1
        H2 = H.copy(); k = int(rng.integers(12))
        if rng.random() < 0.7:
            H2[k, 3] += float(rng.choice([0.01, 0.05, 0.2])) * rng.standard_normal()
        else:
            v = H2[k, :3] + float(rng.choice([0.01, 0.05, 0.2])) * rng.standard_normal(3)
            H2[k, :3] = v / np.linalg.norm(v)
            if not admissible(H2[:, :3], T, U):
                continue
        c2 = violations(H2, pa, it)
        if c2 <= cur or rng.random() < np.exp((cur - c2) / Tmp):
            H, cur = H2, c2; nacc += 1
            if cur < best[0]:
                best = (cur, H.copy())
        Tmp = max(0.03, Tmp * 0.99995)
        if step % 20000 == 0:
            print(step, 'cur', cur, 'best', best[0], 'T %.2f' % Tmp, flush=True)
    json.dump({'type_id': tid, 'best_count': int(best[0]), 'planes': best[1].tolist(), 'triangles': tri, 'steps': step},
              open(out, 'w'))
    print('done best', best[0], 'steps', step, flush=True)


if __name__ == '__main__':
    main()
