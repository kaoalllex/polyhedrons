"""Genetic algorithm (island model) for the ladder / any fixed map.

Genome = the n face planes (gene k = plane of face k, 4 numbers; labels are tied to the map, so genes
are aligned between parents). Operators:
  * uniform crossover by gene (each plane from parent A or B) - a multi-plane move that the one-plane
    annealer and the exact one-plane relocation cannot make;
  * blend crossover per plane (after sign alignment), alpha in [-0.25, 1.25];
  * mutation: Gaussian kick of 1-3 planes (scales 0.003 .. 0.3);
  * short low-temperature quench of the child (memetic step, optional).
Fitness = honest pair energy (ladder.pair_energy) + 0.01 tanh(overlap). Islands evolve separately and
exchange their best individual every MIG generations (ring). Seeds: random and/or given configurations.
Usage: python3 -I ladder_ga.py MINUTES SEED OUT_JSON MAP_SOURCE_JSON MAP_INDEX [--seeded]"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import pack, pair_energy

ISL, POP, MIG, ELITE, TOUR = 6, 40, 25, 2, 3


def fit(H, LK, M):
    try:
        e, o = pair_energy(H, LK, M)
    except Exception:
        return 1e9
    return e + 0.01 * np.tanh(o)


def norm(H):
    H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
    return H


def rand_ind(n, rng):
    return norm(rng.standard_normal((n, 4)))


def crossover(A, B, rng):
    n = len(A)
    if rng.random() < 0.5:
        mask = rng.random(n) < 0.5
        C = np.where(mask[:, None], A, B)
    else:
        Bs = B * np.sign(np.sum(A * B, axis=1))[:, None]     # align plane orientation
        al = rng.uniform(-0.25, 1.25, size=(n, 1))
        C = al * A + (1 - al) * Bs
    return norm(C.copy())


def mutate(C, rng):
    n = len(C)
    for k in rng.choice(n, int(rng.integers(1, 4)), replace=False):
        C[k] += float(rng.choice([0.003, 0.01, 0.03, 0.1, 0.3])) * rng.standard_normal(4)
    return norm(C)


def quench(H, f, LK, M, rng, steps=150):
    n = len(H)
    for _ in range(steps):
        H2 = H.copy(); k = int(rng.integers(n))
        H2[k] += float(rng.choice([0.003, 0.01, 0.03])) * rng.standard_normal(4); H2[k, :3] /= np.linalg.norm(H2[k, :3])
        f2 = fit(H2, LK, M)
        if f2 <= f:
            H, f = H2, f2
    return H, f


def run(links, minutes, rng, seeds=()):
    LK, M, _ = pack(links); n = len(links)
    isl = []
    for i in range(ISL):
        pop = [rand_ind(n, rng) for _ in range(POP)]
        for j, s in enumerate(seeds):
            if j % ISL == i:
                pop[j // ISL % POP] = norm(np.array(s, float))
        fs = [fit(H, LK, M) for H in pop]
        isl.append([pop, fs])
    t0 = time.monotonic(); gen = 0; best = (1e9, None); hist = []
    while time.monotonic() - t0 < 60 * minutes:
        gen += 1
        for pop, fs in isl:
            order = np.argsort(fs)
            newp = [pop[i].copy() for i in order[:ELITE]]; newf = [fs[i] for i in order[:ELITE]]
            while len(newp) < POP:
                def pick():
                    c = rng.choice(POP, TOUR, replace=False)
                    return pop[min(c, key=lambda i: fs[i])]
                C = crossover(pick(), pick(), rng)
                if rng.random() < 0.7:
                    C = mutate(C, rng)
                f = fit(C, LK, M)
                if rng.random() < 0.3:
                    C, f = quench(C, f, LK, M, rng)
                newp.append(C); newf.append(f)
            pop[:] = newp; fs[:] = newf
            i = int(np.argmin(fs))
            if fs[i] < best[0]:
                best = (fs[i], pop[i].copy())
        if gen % MIG == 0:                                   # ring migration of the best individual
            bests = [(pp[int(np.argmin(ff))].copy(), min(ff)) for pp, ff in isl]
            for i, (pp, ff) in enumerate(isl):
                H, f = bests[(i - 1) % ISL]; w = int(np.argmax(ff)); pp[w] = H; ff[w] = f
        if gen % 50 == 0:
            hist.append((gen, round(best[0], 3)))
        if best[0] < 0.5:
            break
    return best, gen, hist


if __name__ == '__main__':
    minutes, seed, out, src, idx = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5])
    seeded = '--seeded' in sys.argv
    rng = np.random.default_rng(seed)
    r = json.load(open(src))[idx]
    links = {int(k): v for k, v in r['links'].items()}
    (b, H), gen, hist = run(links, minutes, rng, seeds=[r['planes']] if seeded else ())
    print('GA best %.3f after %d generations (seeded=%s); history %s' % (b, gen, seeded, hist[-6:]), flush=True)
    json.dump([{'links': r['links'], 'planes': H.tolist(), 'best_fast': float(b), 'generations': gen}], open(out, 'w'))
    if b < 0.5:
        print('!!! ZERO (float) by GA', flush=True)
