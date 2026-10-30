"""Search one genus-ladder level again (e.g. with an improved energy): take level g+1 of a ladder
result file, seed from the realized level g (or the best attempt), run annealing + CMA-ES.
Usage: python3 -I level_search.py LADDER_JSON TARGET_GENUS MINUTES SEED OUT_JSON"""
import json, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from genus_ladder import search
from gauss_degree import coherent_triangles, links_from
from ladder_exact import verify

R = json.load(open(sys.argv[1]))['levels']; g = int(sys.argv[2]); minutes = float(sys.argv[3])
rng = np.random.default_rng(int(sys.argv[4])); out = sys.argv[5]
lv = next(l for l in R if l['genus'] == g); below = next(l for l in R if l['genus'] == g - 1)
L = links_from(coherent_triangles(lv['triangles']), 12)
(b, H), runs = search(L, 12, minutes, rng, below['planes'])
rec = {'genus': g, 'best': float(b), 'planes': H.tolist(), 'triangles': lv['triangles']}
if b < 0.5:
    ex = verify(H.tolist(), L, require_all_pairs=False); rec['exact'] = bool(ex['EMBEDDED'])
json.dump(rec, open(out, 'w'))
print('genus %d: best %.3f (previous run %.3f) %s' % (g, b, lv['best'], 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
