"""Search one target map seeded from given planes (level skipping: e.g. genus 5 from a genus-3
polyhedron or from a failed genus-4 attempt). Annealing + CMA-ES on the honest pair energy; the best
planes are always saved (failed attempts seed later runs); a float zero is re-checked exactly.
Usage: python3 -I seed_search.py SEED_JSON TARGET_JSON MINUTES SEED OUT_JSON
  SEED_JSON: any JSON with 'planes'; TARGET_JSON: JSON with 'triangles' (the target map)"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from genus_ladder import search
from gauss_degree import coherent_triangles, links_from
from ladder_exact import verify

src, tgt, minutes, seed, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
planes = json.load(open(src))['planes']; tris = [tuple(t) for t in json.load(open(tgt))['triangles']]
n = len(planes); L = links_from(coherent_triangles(tris), n)
E = len({frozenset(e) for t in tris for e in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))}); g = (2 - (n - E + len(tris))) // 2
(b, H), runs = search(L, n, minutes, np.random.default_rng(seed), planes)
rec = {'genus': g, 'best': float(b), 'planes': H.tolist(), 'triangles': [list(t) for t in tris], 'seeded_from': src}
if b < 0.5:
    rec['exact'] = bool(verify(H.tolist(), L, require_all_pairs=(E == n * (n - 1) // 2))['EMBEDDED'])
json.dump(rec, open(out, 'w'))
print('genus %d: best %.3f %s' % (g, b, 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
