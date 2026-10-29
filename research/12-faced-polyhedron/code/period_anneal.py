"""Anneal Gauss-admissible normals to minimize the period defect (period_defect.py).
Usage: python3 -I period_anneal.py TYPES_JSON TYPE_ID MINUTES SEED OUT_JSON"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles
from gauss_search import find_admissible, cover_counts, tri_index
from period_defect import period_defect
types = json.load(open(sys.argv[1])); tid, minutes, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
rng = np.random.default_rng(seed); tri = types[tid]['triangles']; ot = coherent_triangles(tri); T = tri_index(ot)
U = rng.standard_normal((1500, 3)); U /= np.linalg.norm(U, axis=1)[:, None]
def admissible(G):
    pos, neg = cover_counts(G, T, U); return bool(np.all(pos - neg == -5) and np.all(pos > 0))
G, _ = find_admissible(ot, rng, minutes=2)
cur = period_defect(G, tri, time_limit=15)[0]; best = (cur, G.copy()); t0 = time.time(); Tmp = 2.0; it = 0
print('start defect', cur, flush=True)
while time.time() - t0 < 60 * minutes and best[0] > 1e-6:
    it += 1
    G2 = G.copy(); k = int(rng.integers(12))
    v = G2[k] + float(rng.choice([0.02, 0.05, 0.15])) * rng.standard_normal(3); G2[k] = v / np.linalg.norm(v)
    if not admissible(G2):
        continue
    d2 = period_defect(G2, tri, time_limit=15)[0]
    if d2 is None:
        continue
    if d2 <= cur or rng.random() < np.exp((cur - d2) / Tmp):
        G, cur = G2, d2
        if cur < best[0]:
            best = (cur, G.copy())
    Tmp = max(0.05, Tmp * 0.97)
    print(it, 'cur %.3f best %.3f' % (cur, best[0]), flush=True)
json.dump({'type_id': tid, 'best_defect': best[0], 'normals': best[1].tolist()}, open(out, 'w'))
print('done best', best[0], flush=True)
