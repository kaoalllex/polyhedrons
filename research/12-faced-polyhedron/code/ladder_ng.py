"""Nevergrad optimizers (Differential Evolution, NGOpt, PSO, ...) on a fixed map with the honest pair
energy (same fitness and guards as ladder_cma.py). Works for the ladder maps and for the 12-face types
(MAP_SOURCE_JSON entries with 'links' and optionally 'planes').
Usage: python3 -I ladder_ng.py OPTIMIZER MINUTES SEED OUT_JSON MAP_SOURCE_JSON MAP_INDEX
OPTIMIZER: any nevergrad registry name, e.g. NGOpt, TwoPointsDE, DE, PSO, RandomSearch."""
import json, sys, time
import numpy as np
import nevergrad as ng
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import pack
from ladder_cma import make_f

if __name__ == '__main__':
    name, minutes, seed, out, src, idx = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6])
    r = json.load(open(src))[idx]
    links = {int(k): v for k, v in r['links'].items()}; LK, M, _ = pack(links); n = len(links)
    f = make_f(LK, M, n)
    np.random.seed(seed)
    param = ng.p.Array(init=np.random.default_rng(seed).standard_normal(4 * n)).set_mutation(sigma=0.5)
    param.random_state = np.random.RandomState(seed)
    opt = ng.optimizers.registry[name](parametrization=param, budget=10 ** 9, num_workers=1)
    t0 = time.monotonic(); best = (1e9, None); evals = 0; crashes = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        try:
            x = opt.ask(); v = f(x.value); opt.tell(x, v); evals += 1
        except (TypeError, ValueError) as ex:     # nevergrad metamodel bug under NumPy 2: restart from the best point
            crashes += 1
            p2 = ng.p.Array(init=best[1] if best[1] is not None else np.random.default_rng(seed + crashes).standard_normal(4 * n)).set_mutation(sigma=0.2)
            p2.random_state = np.random.RandomState(seed + crashes)
            opt = ng.optimizers.registry[name](parametrization=p2, budget=10 ** 9, num_workers=1)
            continue
        if v < best[0]:
            best = (v, np.array(x.value))
    H = best[1].reshape(n, 4).copy(); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
    print('%s best %.3f after %d evaluations (%d optimizer restarts after internal errors)' % (name, best[0], evals, crashes), flush=True)
    json.dump([{'links': r['links'], 'planes': H.tolist(), 'best_fast': float(best[0])}], open(out, 'w'))
    if best[0] < 0.5:
        print('!!! ZERO (float) by', name, flush=True)
