"""Iterated local search for the ladder plateau: kick 2-3 planes at once (a move the one-plane
annealer and the exact one-plane relocation cannot make), quench with low-temperature annealing on
the honest pair energy, accept if not worse (drift on plateaus). Starts from every configuration in
the given result files (best ones first).
Usage: python3 -I ladder_ils.py MINUTES SEED OUT_JSON RESULTS_JSON [RESULTS_JSON ...]"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import pack, pair_energy


def en(H, LK, M):
    try:
        e, o = pair_energy(H, LK, M)
    except Exception:
        return 1e9
    return e + 0.01 * np.tanh(o)


def quench(H, LK, M, rng, steps=4000, T0=0.3):
    cur = en(H, LK, M); best = (cur, H.copy()); T = T0; n = len(H)
    for _ in range(steps):
        H2 = H.copy(); k = int(rng.integers(n)); sig = float(rng.choice([0.003, 0.01, 0.03]))
        H2[k] += sig * rng.standard_normal(4); H2[k, :3] /= np.linalg.norm(H2[k, :3])
        c2 = en(H2, LK, M)
        if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
            H, cur = H2, c2
            if cur < best[0]:
                best = (cur, H.copy())
        T = max(0.01, T * 0.999)
        if best[0] < 0.5:
            break
    return best


if __name__ == '__main__':
    minutes, seed, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = np.random.default_rng(seed)
    starts = []
    for f in sys.argv[4:]:
        for r in json.load(open(f)):
            starts.append(r)
    starts.sort(key=lambda r: r.get('best_fast', r.get('energy', 99)))
    per = 60 * minutes / max(1, len(starts)); results = []
    for si, r in enumerate(starts):
        links = {int(k): v for k, v in r['links'].items()}; LK, M, _ = pack(links)
        H = np.array(r['planes'], float); n = len(H)
        cur = en(H, LK, M); best = (cur, H.copy()); t0 = time.time(); it = 0; acc = 0
        while time.time() - t0 < per and best[0] >= 0.5:
            it += 1
            Hk = H.copy()
            for k in rng.choice(n, int(rng.integers(2, 4)), replace=False):
                Hk[k] += float(rng.choice([0.05, 0.15, 0.4])) * rng.standard_normal(4)
                Hk[k, :3] /= np.linalg.norm(Hk[k, :3])
            c, Hq = quench(Hk, LK, M, rng)
            if c <= cur + 1e-9:
                H, cur = Hq, c; acc += 1
                if cur < best[0]:
                    best = (cur, H.copy())
        print('start %d (from %.3f): best %.3f after %d kicks (%d accepted)' % (si, en(np.array(r['planes']), LK, M), best[0], it, acc), flush=True)
        results.append({'links': r['links'], 'planes': best[1].tolist(), 'energy': float(best[0])})
        json.dump(results, open(out, 'w'))
        if best[0] < 0.5:
            print('!!! ZERO (float) by ILS from start', si, flush=True)
