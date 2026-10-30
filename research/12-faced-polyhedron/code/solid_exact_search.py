"""Solid-first with an EXACT inner step (advisor's direction 2): anneal the planes; for each plane set
the best solid is computed exactly by CP-SAT (solid_cpsat.best_solid: manifold, at most one edge run per
pair of planes, one disk face per plane) and the objective is the number of adjacent pairs of faces
(= 30 + 6 g for 12 faces). Plane moves change the oriented matroid; neutral moves drift on plateaus.
Target: n(n-1)/2 adjacent pairs (21 for n = 7 = Szilassi, 66 for n = 12).
Usage: python3 -I solid_exact_search.py N MINUTES SEED OUT_JSON [TIME_PER_SOLVE]"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from solid_cpsat import best_solid


def value(H, tl, hint=None):
    try:
        A = SF.Arrangement(H)
    except np.linalg.LinAlgError:
        return -1, None, None
    r = best_solid(A, time_limit=tl, max_cuts=5, hint=hint)
    if r is None:
        return -1, None, None
    inS, info = r
    v = info['adjacent'] if info['valid'] else info['adjacent'] - 3
    pen = 0
    if REACH and info['valid']:
        pen, rch = reach_penalty(A, (inS, info), A.n)
        info = dict(info); info['reach'] = rch; info['reach_penalty'] = pen
    if SECONDARY and info['valid'] and info['adjacent'] < A.n * (A.n - 1) // 2:
        # secondary score (advisor): slack of the best attempt at the next genus (+6 adjacent pairs)
        hint2 = {k for k, s_ in zip(sorted(A.bounded), inS) if s_}
        r2 = best_solid(A, time_limit=tl, hint=hint2, target_adj=info['adjacent'] + 6)
        sl = r2[1]['slack'] if r2 is not None else 60
        info = dict(info); info['next_slack'] = sl; info['hot'] = r2[1].get('hot', []) if r2 is not None else []
        return 10 * info['adjacent'] - min(sl, 59) - pen, A, (inS, info)
    return (10 * v if SECONDARY else v) - pen, A, (inS, info)


SECONDARY = '--secondary' in sys.argv
REACH = '--reach' in sys.argv


def reach_penalty(A, sol, n):
    """Dead-end penalty: how many adjacencies the current map can still gain by attaching tubes
    (code/handle_add.reach); maps that cannot grow to all n(n-1)/2 pairs are penalized."""
    from handle_add import reach
    inS, info = sol
    S = {k for k, s_ in zip(sorted(A.bounded), inS) if s_}
    tris = SF.extract_map(A, S)
    full = n * (n - 1) // 2
    if info.get('adjacent', 0) < 36:                   # low genus: too slow to decide, assume reachable
        return 0, None
    r, exhausted = reach(tris, n, node_limit=3000)
    if not exhausted:
        return 0, r
    return 40 * (full - r) // 6, r


if __name__ == '__main__':
    n, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    tl = float(sys.argv[5]) if len(sys.argv) > 5 else 5.0
    full = n * (n - 1) // 2
    full_val = 10 * full if SECONDARY else full
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    best = (-1, None, None); restarts = 0
    init = None
    if '--init' in sys.argv:                           # start from a known polyhedron: planes + its solid as hint
        from gauss_degree import coherent_triangles, links_from
        from local_viol import polygons
        lv = json.load(open(sys.argv[sys.argv.index('--init') + 1]))
        Hi = np.array(lv['planes'], float)
        if 'solid' in lv:                              # a solid-first result: use its cells directly
            init = (Hi, {tuple(x) for x in lv['solid']})
        else:
            L = links_from(coherent_triangles(lv['triangles']), n)
            Ai = SF.Arrangement(Hi); P = polygons(Hi, L)
            init = (Hi, SF.solid_from_winding(Ai, [P[X] for X in range(n)]))
    while time.monotonic() - t0 < 60 * minutes and best[0] < full_val:
        restarts += 1
        if init is not None and (restarts == 1 or rng.random() < 0.5):
            H = init[0].copy(); cur, A, sol = value(H, tl, init[1])
        else:
            H = rng.standard_normal((n, 4)) if (best[1] is None or rng.random() < 0.5) else best[1] + 0.05 * rng.standard_normal((n, 4))
            cur, A, sol = value(H, tl)
        T = 1.0; steps = 0
        while time.monotonic() - t0 < 60 * minutes and steps < (80 if SECONDARY else 300):
            steps += 1
            hot = sol[1].get('hot', []) if (sol is not None and '--guided' in sys.argv) else []
            j = int(rng.choice(hot)) if (hot and rng.random() < 0.7) else int(rng.integers(n))
            H2 = H.copy(); H2[j] += float(rng.choice([0.02, 0.08, 0.3])) * rng.standard_normal(4)
            hint = {k for k, v in zip(sorted(A.bounded), sol[0]) if v} if (sol is not None and A is not None) else None
            v2, A2, sol2 = value(H2, tl, hint)
            if v2 >= cur or rng.random() < np.exp((v2 - cur) / T):
                H, cur, sol, A = H2, v2, sol2, A2
                if cur > best[0]:
                    best = (cur, H.copy(), sol)
                    try:                                  # save every improvement (runs may be interrupted)
                        Ab = SF.Arrangement(best[1])
                        json.dump({'n': n, 'best_adjacent': int(cur), 'planes': best[1].tolist(), 'info': sol[1],
                                   'solid': [[int(v) for v in k] for k, s_ in zip(sorted(Ab.bounded), sol[0]) if s_]},
                                  open(out + '.best.json', 'w'))
                    except Exception:
                        pass
                    print('  new best value %d (adjacent %s, chi %s, next-genus slack %s, reach %s) at %.0fs' % (cur, sol[1].get('adjacent') if sol else '?', sol[1].get('chi') if sol else '?', sol[1].get('next_slack', '-') if sol else '?', sol[1].get('reach', '-') if sol else '?', time.monotonic() - t0), flush=True)
                    if cur == full_val:
                        break
            T = max(0.1, T * 0.99)
        print('restart %d: best %d / %d' % (restarts, best[0], full), flush=True)
    rec = {'n': n, 'best_adjacent': int(best[0]), 'full': full, 'planes': best[1].tolist() if best[1] is not None else None}
    if best[2] is not None:
        inS, info = best[2]; rec['info'] = info
        A = SF.Arrangement(best[1]); rec['solid'] = [[int(v) for v in k] for k, s in zip(sorted(A.bounded), inS) if s]
    json.dump(rec, open(out, 'w'))
    print('FINAL n=%d best %d / %d' % (n, best[0], full), flush=True)
    if best[0] == full_val:
        print('!!! FULL: embedded solid with all pairs of faces adjacent', flush=True)
