"""Positive control for the normals-first step (normals_first.run_arm): the SAME map as the realization
(no handle added), its own orientation fixed, normals annealed within a radius of the realization's and the
offsets decided exactly. A realization's neighbourhood is open, so small radii must give SAT; the SAT rate
versus radius calibrates what an UNSAT streak of the next map at the same radii means.
Usage: python3 -I nf_control.py LEVEL_JSON MINUTES SEED OUT_JSONL [RADII]"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from
import gauss_gate as GG
from normals_first import run_arm

lv = json.load(open(sys.argv[1])); minutes, seed, out = float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
radii = tuple(float(x) for x in (sys.argv[5] if len(sys.argv) > 5 else '0.02,0.05,0.1,0.2,0.4').split(','))
H = lv['planes']; M = [tuple(t) for t in lv['triangles']]; n = len(H)
eps = GG.own_gauge(H, links_from(coherent_triangles(M), n))
rng = np.random.default_rng(seed)
t0 = time.monotonic(); stats = {}
while time.monotonic() - t0 < 60 * minutes:
    for r in radii:
        rec, st = run_arm(H, M, M, None, 0.01, rng, out, radii=(r,), mode='fixed', fixed_gauge=eps, timeout=300,
                          anneal_minutes=0.5, tag='control r=%g' % r, try_seed=False,
                          log=lambda *a: print(time.strftime('%H:%M:%S'), *a, flush=True))
        for k, v in st.items():
            stats.setdefault(r, {}).setdefault(k, 0); stats[r][k] += v
print('CONTROL', stats, flush=True)
