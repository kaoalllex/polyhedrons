"""Polish a solid-first polyhedron (planes + solid) or a map-based one (planes + triangles): random plane moves that keep the SAME face structure (same set of
adjacent pairs, one disk face per plane, embedded) while increasing 'beauty' (code/beauty.py).
Usage: python3 -I polish_solid.py RESULT_JSON OUT_JSON SECONDS"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from gauss_degree import coherent_triangles, links_from
from ladder import pack, pair_energy
from beauty import beauty

r = json.load(open(sys.argv[1])); secs = float(sys.argv[3])
H = np.array(r['planes'], float); n = len(H); A = SF.Arrangement(H)
tris = SF.extract_map(A, {tuple(x) for x in r['solid']}) if 'solid' in r else [tuple(t) for t in r['triangles']]
L = links_from(coherent_triangles(tris), n); LK, M, _ = pack(L)
H = A.H.copy()
assert pair_energy(H, LK, M)[0] == 0
b = beauty(H, L)['beauty']; b0 = b; rng = np.random.default_rng(0); t0 = time.time()
while time.time() - t0 < secs:
    H2 = H.copy(); k = int(rng.integers(n)); H2[k] += float(rng.choice([0.002, 0.01, 0.03])) * rng.standard_normal(4)
    H2[k, :3] /= np.linalg.norm(H2[k, :3])
    try:
        if pair_energy(H2, LK, M)[0] != 0:
            continue
        b2 = beauty(H2, L)['beauty']
    except np.linalg.LinAlgError:
        continue
    if b2 >= b:
        H, b = H2, b2
A2 = SF.Arrangement(H)
# rebuild the solid for the polished planes from the polygons (winding number 1 cells)
from ladder import polygons
P = polygons(H, L); S2 = SF.solid_from_winding(A2, [P[X] for X in range(n)])
json.dump({'planes': H.tolist(), 'solid': [[int(v) for v in k] for k in S2], 'triangles': [list(map(int, t)) for t in tris],
           'beauty_before': b0, 'beauty_after': b},
          open(sys.argv[2], 'w'))
print('beauty %.2e -> %.2e' % (b0, b))
