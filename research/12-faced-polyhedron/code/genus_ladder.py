"""Genus ladder at n = 12 (advisor's direction 3, 'Frankenstein'): every neighbourly 12-face map is a
simple 12-faced polyhedron (sphere, M0) plus 6 handles. Remove 'tubes' (6-triangle annuli between two
disjoint non-facial 3-cycles; code/tubes.py from the advisor) from the genus-6 triangulation down to a
sphere: M6 -> M5 -> ... -> M0 (all with the same 12 vertices = 12 faces of the dual). Then climb back:
search an embedded polyhedron for M0, then M1 seeded from the M0 solution, ... (CMA-ES + annealing on
the honest pair energy; every float zero re-checked in exact arithmetic, non-adjacent face pairs must
not meet at all). The highest realized genus and the handle where it fails are the result.
Usage: python3 -I genus_ladder.py TYPE_ID MINUTES_PER_LEVEL SEED OUT_JSON"""
import json, sys, time, random
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from tubes import tubes
from gauss_degree import coherent_triangles, links_from
from ladder import pack, pair_energy
from ladder_exact import verify
if not hasattr(np, 'Inf'):
    np.Inf = np.inf
import cma


def remove(tris, tube):
    A, B, S = tube
    T = [tuple(sorted(t)) for t in tris]
    for t in S:
        T.remove(tuple(sorted(t)))
    return T + [tuple(sorted(A)), tuple(sorted(B))]


def chain(tris, n, rng, tries=30):
    best = None
    for _ in range(tries):
        cur = [tuple(sorted(t)) for t in tris]; ch = [cur]
        while True:
            tb = tubes(cur, n)
            ok = []
            for x in tb:
                r = remove(cur, x)
                try:
                    links_from(coherent_triangles(r), n); ok.append(r)
                except AssertionError:
                    pass
            if not ok:
                break
            cur = ok[rng.randrange(len(ok))]; ch.append(cur)
        if best is None or len(ch) > len(best):
            best = ch
        if len(best) == 7:
            break
    return best[::-1]                                 # genus 0 first


def energy_fn(LK, M, n):
    def f(x):
        H = np.asarray(x, float).reshape(n, 4).copy(); nr = np.linalg.norm(H[:, :3], axis=1)
        if np.any(nr < 1e-6):
            return 1e6
        H[:, :3] /= nr[:, None]; H[:, 3] /= nr
        try:
            e, o = pair_energy(H, LK, M)
        except Exception:
            return 1e6
        return e + 0.01 * np.tanh(o)
    return f


def anneal_level(links, n, minutes, rng, seed_planes=None, steps=30000, free=None):
    """One-plane annealing on the honest pair energy; restarts alternate between the seed (perturbed)
    and random planes. free: only these planes move (large-neighbourhood steps)."""
    LK, M, _ = pack(links)
    def en(H):
        try:
            e, o = pair_energy(H, LK, M)
        except Exception:
            return 1e9
        return e + 0.01 * np.tanh(o)
    t0 = time.monotonic(); best = (1e9, None); r = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        r += 1
        if seed_planes is not None and r % 2 == 1:
            H = np.array(seed_planes) + 0.03 * rng.standard_normal((n, 4)); T = 0.3
        else:
            H = rng.standard_normal((n, 4)); T = 1.5
        H[:, :3] /= np.linalg.norm(H[:, :3], axis=1)[:, None]
        cur = en(H); bl = (cur, H.copy())
        for _ in range(steps):
            H2 = H.copy(); k = int(rng.integers(n)) if free is None else int(rng.choice(free)); H2[k] += float(rng.choice([0.005, 0.02, 0.08])) * rng.standard_normal(4)
            H2[k, :3] /= np.linalg.norm(H2[k, :3])
            c2 = en(H2)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, cur = H2, c2
                if cur < bl[0]:
                    bl = (cur, H.copy())
            T = max(0.02, T * 0.9997)
            if bl[0] < 0.5 or time.monotonic() - t0 > 60 * minutes:
                break
        if bl[0] < best[0]:
            best = bl
    return best, r


def search(links, n, minutes, rng, seed_planes=None):
    """Half the budget one-plane annealing, half CMA-ES."""
    (b1, H1), r1 = anneal_level(links, n, minutes / 2, rng, seed_planes)
    if b1 < 0.5:
        return (b1, H1), r1
    (b2, H2), r2 = search_cma(links, n, minutes / 2, rng, seed_planes if seed_planes is not None else H1.tolist())
    return ((b1, H1) if b1 <= b2 else (b2, H2)), r1 + r2


def search_cma(links, n, minutes, rng, seed_planes=None):
    LK, M, _ = pack(links); f = energy_fn(LK, M, n)
    t0 = time.monotonic(); best = (1e9, None); runs = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] >= 0.5:
        runs += 1
        if seed_planes is not None and runs % 2 == 1:
            x0 = np.array(seed_planes).ravel() + 0.02 * rng.standard_normal(4 * n); sig = 0.05
        else:
            x0 = rng.standard_normal(4 * n); sig = 0.5
        es = cma.CMAEvolutionStrategy(x0, sig, {'seed': int(rng.integers(1 << 30)), 'verbose': -9, 'tolflatfitness': 50,
                                                'popsize': int(4 + 3 * np.log(4 * n)) * (2 ** (runs % 3))})
        while not es.stop() and time.monotonic() - t0 < 60 * minutes:
            X = es.ask(); F = [f(x) for x in X]; es.tell(X, F)
            i = int(np.argmin(F))
            if F[i] < best[0]:
                H = np.array(X[i]).reshape(n, 4); nr = np.linalg.norm(H[:, :3], axis=1); H[:, :3] /= nr[:, None]; H[:, 3] /= nr
                best = (F[i], H)
            if best[0] < 0.5:
                break
    return best, runs


if __name__ == '__main__':
    tid, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = np.random.default_rng(seed); prng = random.Random(seed)
    types = json.load(open(__file__.rsplit('/', 2)[0] + '/data/k12_triangulations.json'))
    tri = next(t for t in types if t['id'] == tid)['triangles']
    ch = chain(tri, 12, prng)
    print('type %d: chain of %d levels (genus %d .. 6)' % (tid, len(ch), 7 - len(ch)), flush=True)
    res = []; seed_planes = None
    for lvl, T in enumerate(ch):
        g = 6 - (len(ch) - 1 - lvl)
        L = links_from(coherent_triangles(T), 12)
        (b, H), runs = search(L, 12, minutes, rng, seed_planes)
        rec = {'genus': g, 'triangles': [list(t) for t in T], 'best': float(b), 'planes': H.tolist(), 'cma_runs': runs}
        if b < 0.5:
            ex = verify(H.tolist(), L, require_all_pairs=False)
            rec['exact_embedded'] = bool(ex['EMBEDDED']); rec['exact'] = {k: (v if not isinstance(v, list) else len(v)) for k, v in ex.items()}
            if ex['EMBEDDED']:
                seed_planes = H.tolist()
        print('genus %d: best %.3f (%d CMA runs) %s' % (g, b, runs, ('EXACT EMBEDDED' if rec.get('exact_embedded') else '')), flush=True)
        res.append(rec)
        json.dump({'type_id': tid, 'levels': res}, open(out, 'w'))
        if not rec.get('exact_embedded') and lvl > 0:
            seed_planes = H.tolist()                  # keep climbing from the best attempt
