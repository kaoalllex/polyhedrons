"""CMA-ES (BIPOP restarts) for a fixed ladder map: the genome is the flattened n x 4 plane matrix,
fitness = honest pair energy + 0.01 tanh(overlap). Covariance adaptation learns correlated
multi-plane moves (what the one-plane annealer and relocation lack).
Usage: python3 -I ladder_cma.py MINUTES SEED OUT_JSON MAP_SOURCE_JSON MAP_INDEX [--seeded]"""
import json, sys, time
import numpy as np
if not hasattr(np, 'Inf'):
    np.Inf = np.inf          # cma 3.3 still uses the alias removed in NumPy 2
import cma
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import pack, pair_energy


def make_f(LK, M, n):
    def f(x):
        H = np.asarray(x, float).reshape(n, 4).copy()
        nr = np.linalg.norm(H[:, :3], axis=1)
        if np.any(nr < 1e-6):
            return 1e6
        H[:, :3] /= nr[:, None]; H[:, 3] /= nr
        try:
            e, o = pair_energy(H, LK, M)
        except Exception:
            return 1e6
        return e + 0.01 * np.tanh(o)
    return f


if __name__ == '__main__':
    minutes, seed, out, src, idx = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
    r = json.load(open(src))[idx]
    links = {int(k): v for k, v in r['links'].items()}; LK, M, _ = pack(links); n = len(links)
    f = make_f(LK, M, n); rng = np.random.default_rng(seed)
    t0 = time.monotonic(); best = (1e9, None); runs = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        runs += 1
        x0 = np.array(r['planes']).ravel() if ('--seeded' in sys.argv and runs == 1) else rng.standard_normal(4 * n)
        sig = 0.05 if ('--seeded' in sys.argv and runs == 1) else 0.5
        popsize = int(4 + 3 * np.log(4 * n)) * (2 ** (runs % 4))       # BIPOP-like alternation of population sizes
        es = cma.CMAEvolutionStrategy(x0, sig, {'seed': int(rng.integers(1 << 30)), 'popsize': popsize, 'verbose': -9,
                                                'tolfun': 1e-12, 'tolflatfitness': 50})
        while not es.stop() and time.monotonic() - t0 < 60 * minutes:
            X = es.ask(); F = [f(x) for x in X]; es.tell(X, F)
            i = int(np.argmin(F))
            if F[i] < best[0]:
                best = (F[i], np.array(X[i]))
            if best[0] < 0.5:
                break
    H = best[1].reshape(n, 4).copy(); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
    print('CMA-ES best %.3f after %d runs' % (best[0], runs), flush=True)
    json.dump([{'links': r['links'], 'planes': H.tolist(), 'best_fast': float(best[0])}], open(out, 'w'))
    if best[0] < 0.5:
        print('!!! ZERO (float) by CMA-ES', flush=True)
