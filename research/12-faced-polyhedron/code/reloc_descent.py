"""Coordinate descent by exact single-plane relocation (PI experiment E-PI-1).

Usage: python3 -I reloc_descent.py SEEDS_JSON SOURCE OUT_JSON MINUTES [STRIDE] [THREADS] [SEED]
SEEDS_JSON: output of import_hackerpoet.py (planes, triangles). SOURCE: e.g. topology_33/shape_c5_i0_1154.obj
Each step relocates one plane to the best cell (count <= current; plateau moves accepted),
then re-centres it in its cell. Logs every step; keeps the best configuration.
"""
import json, sys, time
import numpy as np
import numba

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fastviol import triangulation_tables, violations, violation_list
from relocate import relocate


def main():
    seeds, src, out, minutes = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
    stride = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    threads = int(sys.argv[6]) if len(sys.argv) > 6 else 2
    rng = np.random.default_rng(int(sys.argv[7]) if len(sys.argv) > 7 else 0)
    numba.set_num_threads(threads)
    rec = next(r for r in json.load(open(seeds)) if r['source'] == src)
    H = np.array(rec['planes'])
    pa, it = triangulation_tables(12, rec['triangles'])
    cur = int(violations(H, pa, it))
    best = (cur, H.copy())
    log = [{"step": 0, "count": cur}]
    print(src, 'start', cur, flush=True)
    t0 = time.time(); step = 0
    while time.time() - t0 < 60 * minutes:
        for k in rng.permutation(12):
            if time.time() - t0 > 60 * minutes:
                break
            step += 1
            c, h, hc, m = relocate(H, pa, it, int(k), stride=stride, offset=int(rng.integers(stride)), cap=cur + 1)
            H2 = H.copy(); H2[k] = hc
            vc = int(violations(H2, pa, it))
            if vc > c:                      # centring left the cell (numerical); fall back to probe point
                H2[k] = h; vc = int(violations(H2, pa, it))
            moved = float(np.abs(H2[k] - H[k]).max())
            if vc <= cur:
                H, cur = H2, vc
            log.append({"step": step, "plane": int(k), "found": c, "count": cur, "margin": m, "moved": moved,
                        "t": round(time.time() - t0, 1)})
            print(step, k, 'found', c, 'now', cur, 'margin %.1e moved %.2e' % (m, moved), flush=True)
            if cur < best[0]:
                best = (cur, H.copy())
                json.dump({"source": src, "best_count": cur, "planes": best[1].tolist(),
                           "triangles": rec['triangles'], "violated": [list(map(int, x)) for x in violation_list(best[1], pa, it)],
                           "log": log}, open(out, 'w'))
    json.dump({"source": src, "best_count": best[0], "planes": best[1].tolist(), "triangles": rec['triangles'],
               "violated": [list(map(int, x)) for x in violation_list(best[1], pa, it)], "log": log}, open(out, 'w'))
    print('done best', best[0], flush=True)


if __name__ == '__main__':
    main()
