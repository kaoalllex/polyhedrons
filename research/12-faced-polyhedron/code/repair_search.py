"""Targeted repair of a near-realization: find the violated faces exactly (non-simple faces and faces in
bad pairs, code/ladder_exact.py), then anneal only those planes plus K random others per restart,
restarting from the seed. Every float zero is re-checked exactly.
Usage: python3 -I repair_search.py SEED_JSON MINUTES SEED OUT_JSON [K]   (SEED_JSON: planes + triangles)"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from
from genus_ladder import anneal_level
from ladder_exact import verify

r = json.load(open(sys.argv[1])); minutes = float(sys.argv[2]); rng = np.random.default_rng(int(sys.argv[3]))
out = sys.argv[4]; K = int(sys.argv[5]) if len(sys.argv) > 5 else 2
H0 = np.array(r['planes'], float); n = len(H0)
nr = np.linalg.norm(H0[:, :3], axis=1); H0[:, :3] /= nr[:, None]; H0[:, 3] /= nr
L = links_from(coherent_triangles([tuple(t) for t in r['triangles']]), n)
ex = verify(H0.tolist(), L, require_all_pairs=False)
bad = sorted(set(ex['nonsimple_faces']) | {x for p in ex['bad_pairs'] for x in p})
print('violated faces %s (non-simple %s, bad pairs %s)' % (bad, ex['nonsimple_faces'], ex['bad_pairs']), flush=True)
t0 = time.monotonic(); best = (1e9, None); k = 0
while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
    k += 1
    free = bad + [int(x) for x in rng.choice([x for x in range(n) if x not in bad], K, replace=False)]
    left = 60 * minutes - (time.monotonic() - t0)
    (b, H), _ = anneal_level(L, n, min(left / 60, 1.0), rng, H0.tolist(), steps=20000, free=free)
    if b < best[0]:
        best = (b, H); print('  restart %d: best %.3f (free %s) at %.0fs' % (k, b, free, time.monotonic() - t0), flush=True)
rec = {'best': float(best[0]), 'planes': best[1].tolist(), 'triangles': r['triangles']}
if best[0] < 0.5:
    rec['exact'] = bool(verify(best[1].tolist(), L, require_all_pairs=False)['EMBEDDED'])
json.dump(rec, open(out, 'w'))
print('FINAL best %.3f %s' % (best[0], 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
