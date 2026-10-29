"""Q12b: numerical search for a polyhedral IMMERSION (local violations = 0) of one type.
Energy = face self-crossings + vertices with >= 2 reflex corners (local_viol.py).
Usage: python3 -I immersion_anneal.py TYPES_JSON TYPE_ID MINUTES SEED OUT_JSON"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles, links_from
from local_viol import local_violations
types = json.load(open(sys.argv[1])); tid, minutes, seed, out = int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
rng = np.random.default_rng(seed)
tri = next(e for e in types if e['id'] == tid)['triangles']; L = links_from(coherent_triangles(tri), 12)
def en(H):
    try:
        c, m, _ = local_violations(H, L)
    except np.linalg.LinAlgError:
        return 10 ** 6
    return c + m
best_all = (10 ** 9, None); t0 = time.time()
while time.time() - t0 < 60 * minutes:
    H = rng.standard_normal((12, 4)); H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
    cur = en(H); best = (cur, H.copy()); Tmp = 2.0
    for step in range(30000):
        H2 = H.copy(); k = int(rng.integers(12)); sig = float(rng.choice([0.01, 0.05, 0.2]))
        H2[k] += sig * rng.standard_normal(4); H2[k] /= np.linalg.norm(H2[k, :3])
        c2 = en(H2)
        if c2 <= cur or rng.random() < np.exp((cur - c2) / Tmp):
            H, cur = H2, c2
            if cur < best[0]: best = (cur, H.copy())
        Tmp = max(0.03, Tmp * 0.9998)
        if best[0] == 0 or time.time() - t0 > 60 * minutes: break
    print('restart best', best[0], flush=True)
    if best[0] < best_all[0]: best_all = best
    if best_all[0] == 0: break
json.dump({'type_id': tid, 'best_local': int(best_all[0]), 'planes': best_all[1].tolist(), 'triangles': tri}, open(out, 'w'))
print('done', best_all[0], flush=True)
