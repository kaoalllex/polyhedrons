"""Drift inside the realization space of a realized level: random plane moves that keep the CURRENT map
realized (pair energy 0: an embedded polyhedron at every step) while lowering the pair energy of the
NEXT map (one more handle), with Metropolis acceptance. The realization space is open, so the walk can
cover a lot of it; a zero of the next map's energy is re-checked exactly.
Usage: python3 -I drift_search.py LEVEL_JSON TARGET_JSON MINUTES SEED OUT_JSON
  LEVEL_JSON: planes + triangles of a realized polyhedron; TARGET_JSON: triangles of the next map"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from
from ladder import pack, pair_energy
from ladder_exact import verify

lv = json.load(open(sys.argv[1])); tg = json.load(open(sys.argv[2]))
minutes, rng, out = float(sys.argv[3]), np.random.default_rng(int(sys.argv[4])), sys.argv[5]
H = np.array(lv['planes'], float); n = len(H)
nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
L0 = links_from(coherent_triangles([tuple(t) for t in lv['triangles']]), n); K0, M0, _ = pack(L0)
L1 = links_from(coherent_triangles([tuple(t) for t in tg['triangles']]), n); K1, M1, _ = pack(L1)
assert pair_energy(H, K0, M0)[0] == 0, 'the start is not a realization of the current map'


def f1(H):
    e, o = pair_energy(H, K1, M1)
    return e + 0.01 * np.tanh(o)


cur = f1(H); best = (cur, H.copy()); T = 0.5; t0 = time.monotonic(); steps = acc = 0
print('start: next-map energy %.3f' % cur, flush=True)
while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
    steps += 1
    H2 = H.copy(); k = int(rng.integers(n)); H2[k] += float(rng.choice([0.002, 0.01, 0.04, 0.15])) * rng.standard_normal(4)
    H2[k, :3] /= np.linalg.norm(H2[k, :3])
    try:
        if pair_energy(H2, K0, M0)[0] != 0:           # must stay an embedded polyhedron of the current map
            continue
        c2 = f1(H2)
    except Exception:
        continue
    if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
        H, cur = H2, c2; acc += 1
        if cur < best[0]:
            if int(cur) < int(best[0]):
                print('  next-map energy %.3f at %.0fs (step %d)' % (cur, time.monotonic() - t0, steps), flush=True)
            best = (cur, H.copy())
    T = max(0.05, T * 0.9999)
rec = {'best': float(best[0]), 'planes': best[1].tolist(), 'triangles': tg['triangles'], 'steps': steps, 'accepted': acc}
if best[0] < 0.5:
    rec['exact'] = bool(verify(best[1].tolist(), L1, require_all_pairs=False)['EMBEDDED'])
json.dump(rec, open(out, 'w'))
print('FINAL next-map energy %.3f after %d steps (%d accepted) %s' % (best[0], steps, acc, 'EXACT EMBEDDED' if rec.get('exact') else ''), flush=True)
