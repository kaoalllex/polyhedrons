"""Large-neighbourhood step for one handle: from a realized polyhedron (planes + triangles) attach the
tube of extendable candidate INDEX (beam_ladder order) and search only the planes of the six faces of
the tube (plus K random others per restart), keeping the rest fixed; restarts from the seed with small
noise on the free planes only. Every float zero is re-checked exactly.
Usage: python3 -I lns_handle.py LEVEL_JSON INDEX MINUTES SEED OUT_JSON [K]"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beam_ladder import extendable
from ladder import pack, pair_energy
from genus_ladder import anneal_level
from ladder_exact import verify

lv = json.load(open(sys.argv[1])); idx = int(sys.argv[2]); minutes = float(sys.argv[3])
rng = np.random.default_rng(int(sys.argv[4])); out = sys.argv[5]; K = int(sys.argv[6]) if len(sys.argv) > 6 else 2
H0 = np.array(lv['planes'], float); n = len(H0)
C = extendable([tuple(t) for t in lv['triangles']], n)
H0n = H0.copy(); H0n[:, :3] /= np.linalg.norm(H0[:, :3], axis=1)[:, None]; H0n[:, 3] /= np.linalg.norm(H0[:, :3], axis=1)
order = sorted(range(len(C)), key=lambda i: pair_energy(H0n, *pack(C[i][3])[:2])[0])
t1, t2, R, L = C[order[idx]]
tube = sorted(set(t1) | set(t2))
print('tube %s-%s, free planes %s (+%d random per restart)' % (t1, t2, tube, K), flush=True)
t0 = time.monotonic(); best = (1e9, None); r = 0
while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
    r += 1
    free = tube + [int(x) for x in rng.choice([x for x in range(n) if x not in tube], K, replace=False)]
    left = 60 * minutes - (time.monotonic() - t0)
    (b, H), _ = anneal_level(L, n, min(left / 60, 1.0), rng, H0n.tolist(), steps=20000, free=free)
    if b < best[0]:
        best = (b, H); print('  restart %d: best %.3f (free %s) at %.0fs' % (r, b, free, time.monotonic() - t0), flush=True)
rec = {'tube': [list(t1), list(t2)], 'best': float(best[0]), 'planes': best[1].tolist(), 'triangles': [list(t) for t in R]}
if best[0] < 0.5:
    rec['exact'] = bool(verify(best[1].tolist(), L, require_all_pairs=False)['EMBEDDED'])
json.dump(rec, open(out, 'w'))
print('FINAL best %.3f %s' % (best[0], 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
