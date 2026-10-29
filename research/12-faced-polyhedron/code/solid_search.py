"""Solid-first search (see solid_first.py): annealing over (planes, solid S). Moves: flip one bounded
cell in / out of S, or perturb one plane and carry S over (cells keep their sign vectors; new bounded
cells join S if most of their existing neighbours are in S). The combinatorial type is NOT fixed: any
zero is an embedded polyhedron with n faces, each pair adjacent (exactly once if --once, else >= 1).
Usage: python3 -I solid_search.py N MINUTES SEED OUT_JSON [--once]"""
import json, sys, time, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF


def carry(A_old, S, A_new):
    S2 = {k for k in S if k in A_new.bounded}
    for k in A_new.bounded:
        if k in A_old.cells:
            continue
        nb = [tuple(k[:i] + (-k[i],) + k[i + 1:]) for i in range(len(k))]
        nb = [x for x in nb if x in A_new.cells]
        if nb and sum(x in S for x in nb) * 2 > len(nb):
            S2.add(k)
    return S2


def objective(A, S, once):
    t, d = SF.evaluate(A, S, detail=True)
    if not once:                                      # ladder rungs with doubled adjacencies: only missing pairs count
        t = t - d['adjacency'] + d['missing']
    return t, d


def polish_S(A, S, once, rng, cur=None):
    """Greedy cell flips (random order) until no single flip improves: the best solid for these planes
    reachable from S."""
    if cur is None:
        cur = objective(A, S, once)[0]
    cells = list(A.bounded); improved = True
    while improved:
        improved = False
        for i in rng.permutation(len(cells)):
            S2 = set(S); S2.symmetric_difference_update({cells[i]})
            c2 = objective(A, S2, once)[0]
            if c2 < cur:
                S, cur, improved = S2, c2, True
    return S, cur


def run2(n, minutes, seed, once=True):
    """Two-level variant: anneal the planes; after every plane move the solid is re-polished greedily."""
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    best = (1e9, None, None, None); restarts = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] > 0:
        restarts += 1
        H = rng.standard_normal((n, 4)); A = SF.Arrangement(H)
        S, cur = polish_S(A, {k for k in A.bounded if rng.random() < 0.5}, once, rng); T = 1.0
        for _ in range(400):
            if time.monotonic() - t0 > 60 * minutes:
                break
            H2 = H.copy(); j = int(rng.integers(n)); H2[j] += float(rng.choice([0.02, 0.08, 0.3])) * rng.standard_normal(4)
            try:
                A2 = SF.Arrangement(H2)
            except np.linalg.LinAlgError:
                continue
            S2, c2 = polish_S(A2, carry(A, S, A2), once, rng)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, A, S, cur = H2, A2, S2, c2
                if cur < best[0]:
                    best = (cur, H.copy(), sorted(S), objective(A, S, once)[1])
                    if cur == 0:
                        break
            T = max(0.05, T * 0.99)
        print('restart %d: best so far %s %s' % (restarts, best[0], best[3]), flush=True)
    return best, restarts


def run(n, minutes, seed, once=True):
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    best = (1e9, None, None, None); restarts = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] > 0:
        restarts += 1
        H = rng.standard_normal((n, 4)); A = SF.Arrangement(H)
        S = {k for k in A.bounded if rng.random() < 0.5}
        cur, d = objective(A, S, once); T = 2.0; steps = 0
        while time.monotonic() - t0 < 60 * minutes and steps < 6000 * n:
            steps += 1
            if rng.random() < 0.6:
                k = list(A.bounded)[int(rng.integers(len(A.bounded)))]
                S2 = set(S); S2.symmetric_difference_update({k}); A2 = A; H2 = H
            else:
                H2 = H.copy(); j = int(rng.integers(n)); H2[j] += float(rng.choice([0.01, 0.05, 0.2])) * rng.standard_normal(4)
                try:
                    A2 = SF.Arrangement(H2)
                except np.linalg.LinAlgError:
                    continue
                S2 = carry(A, S, A2)
            c2, d2 = objective(A2, S2, once)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, A, S, cur, d = H2, A2, S2, c2, d2
                if cur < best[0]:
                    best = (cur, H.copy(), sorted(S), d)
                    if cur == 0:
                        break
            T = max(0.05, T * 0.9995)
        print('restart %d: best so far %s %s' % (restarts, best[0], best[3]), flush=True)
    return best, restarts


def _path(nb, a, b, allowed):
    """BFS shortest path from a to b through cells in 'allowed' (a, b included)."""
    from collections import deque
    prev = {a: None}; dq = deque([a])
    while dq:
        x = dq.popleft()
        if x == b:
            out = []
            while x is not None:
                out.append(x); x = prev[x]
            return out
        for y in nb[x]:
            if y not in prev and (y in allowed or y == b):
                prev[y] = x; dq.append(y)
    return None


def macro(A, S, rng, kind):
    """Topology-changing macro-move: 'drill' removes a path of cells of S between two boundary cells
    (a tunnel); 'handle' adds a path of outside bounded cells between two cells touching S."""
    nb = SF.cell_graph(A)
    inside = [k for k in S if any(x not in S for x in nb[k]) or len(nb[k]) < len(k)]
    outside = [k for k in A.bounded if k not in S and any(x in S for x in nb[k])]
    pool = inside if kind == 'drill' else outside
    if len(pool) < 2:
        return None
    a, b = (pool[i] for i in rng.choice(len(pool), 2, replace=False))
    allowed = S if kind == 'drill' else set(A.bounded) - S
    path = _path(nb, a, b, allowed)
    if path is None or len(path) < 3:
        return None
    return (set(S) - set(path)) if kind == 'drill' else (set(S) | set(path))


def objective_g(A, S, once, chi_target):
    t, d = objective(A, S, once)
    chi = SF.boundary_euler(A, S)
    d = dict(d); d['chi'] = chi
    return t + abs(chi - chi_target) / 2.0, d


def run3(n, minutes, seed, once=True):
    """Annealing with plane moves (+ carry + greedy polish), cell flips, and tunnel / handle macro-moves;
    objective += |chi(boundary) - chi_target| / 2 (target genus of the n-face neighbourly map)."""
    g_target = -(-(n - 3) * (n - 4) // 12); chi_t = 2 - 2 * g_target
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    best = (1e9, None, None, None); restarts = 0
    def f(A, S):
        return objective_g(A, S, once, chi_t)[0]
    while time.monotonic() - t0 < 60 * minutes and best[0] > 0:
        restarts += 1
        if best[1] is not None and rng.random() < 0.5:     # intensify: restart near the best state
            H = best[1] + 0.03 * rng.standard_normal(best[1].shape)
            try:
                A = SF.Arrangement(H)
            except np.linalg.LinAlgError:
                continue
            Ab = SF.Arrangement(best[1]); S = carry(Ab, set(best[2]), A)
        else:
            H = rng.standard_normal((n, 4)); A = SF.Arrangement(H)
            S = {k for k in A.bounded if rng.random() < 0.5}
        S, _ = polish_S(A, S, once, rng); cur = f(A, S); T = 1.0
        for _ in range(600):
            if time.monotonic() - t0 > 60 * minutes:
                break
            r = rng.random()
            if r < 0.4:
                H2 = H.copy(); j = int(rng.integers(n)); H2[j] += float(rng.choice([0.02, 0.08, 0.3])) * rng.standard_normal(4)
                try:
                    A2 = SF.Arrangement(H2)
                except np.linalg.LinAlgError:
                    continue
                S2, _ = polish_S(A2, carry(A, S, A2), once, rng)
            elif r < 0.7:
                A2, H2 = A, H
                S2 = macro(A, S, rng, 'drill' if rng.random() < 0.5 else 'handle')
                if S2 is None:
                    continue
                S2, _ = polish_S(A, S2, once, rng)
            else:
                A2, H2 = A, H
                k = list(A.bounded)[int(rng.integers(len(A.bounded)))]
                S2 = set(S); S2.symmetric_difference_update({k})
            c2 = f(A2, S2)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                H, A, S, cur = H2, A2, S2, c2
                if cur < best[0]:
                    best = (cur, H.copy(), sorted(S), objective_g(A, S, once, chi_t)[1])
                    if cur == 0:
                        break
            T = max(0.05, T * 0.993)
        print('restart %d: best so far %s %s' % (restarts, best[0], best[3]), flush=True)
    return best, restarts


if __name__ == '__main__':
    n, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    once = '--once' in sys.argv
    eng = run3 if '--macro' in sys.argv else (run2 if '--two-level' in sys.argv else run)
    (b, H, S, d), rs = eng(n, minutes, seed, once)
    json.dump({'n': n, 'best': float(b), 'detail': {k: int(v) for k, v in (d or {}).items()},
               'planes': H.tolist() if H is not None else None,
               'solid': [[int(x) for x in k] for k in S] if S is not None else None}, open(out, 'w'))
    print('FINAL n=%d best %s after %d restarts %s' % (n, b, rs, d), flush=True)
    if b == 0:
        print('!!! ZERO: embedded solid with the target face structure', flush=True)
