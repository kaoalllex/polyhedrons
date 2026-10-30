"""Genus-ladder step with the exact solid inner solver and a TARGET adjacency graph: take the highest
realized level M_g of a genus-ladder run (planes), target the adjacency graph of M_{g+1}, and anneal
the planes; for each plane set CP-SAT picks the embedded solid maximizing (target pairs adjacent) -
2 (non-target pairs adjacent). Success = all target pairs adjacent, no extra (then the map is checked).
Usage: python3 -I ladder_solid.py LADDER_JSON MINUTES SEED OUT_JSON [TIME_PER_SOLVE]"""
import json, sys, time, itertools
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from solid_cpsat import best_solid
from gauss_degree import coherent_triangles, links_from
from ladder import polygons

src, minutes, seed, out = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
tl = float(sys.argv[5]) if len(sys.argv) > 5 else 12.0
R = json.load(open(src))['levels']
g_ok = max(i for i, lv in enumerate(R) if lv.get('exact_embedded'))
cur_lv, nxt = R[g_ok], R[g_ok + 1]
target = {tuple(sorted(e)) for t in nxt['triangles'] for e in itertools.combinations(t, 2)}
H = np.array(cur_lv['planes'], float); n = len(H)
L = links_from(coherent_triangles(cur_lv['triangles']), n); A = SF.Arrangement(H); P = polygons(A.H, L)
hint = SF.solid_from_winding(A, [P[X] for X in range(n)])
print('from genus %d (realized) to genus %d: %d target pairs' % (cur_lv['genus'], nxt['genus'], len(target)), flush=True)
rng = np.random.default_rng(seed); t0 = time.monotonic()

def value(H, hint):
    try:
        A = SF.Arrangement(H)
    except np.linalg.LinAlgError:
        return -99, None, None
    r = best_solid(A, time_limit=tl, max_cuts=3, hint=hint, target_pairs=target)
    if r is None:
        return -99, None, None
    inS, info = r
    v = 10 * (info['matched'] - 2 * info['extra']) - (0 if info['valid'] else 50)
    if info['valid'] and info['matched'] < len(target):
        # secondary: slack of the best attempt that realizes exactly the target graph (soft extra runs,
        # soft one-face condition); 0 = the next level is realized
        h2 = {k for k, s_ in zip(sorted(A.bounded), inS) if s_}
        r2 = best_solid(A, time_limit=tl, hint=h2, target_adj=len(target), target_pairs=target)
        sl = r2[1]['slack'] if r2 is not None else 99
        info = dict(info); info['target_slack'] = sl
        if sl == 0 and r2 is not None:                 # the soft model realized the target graph exactly
            info['matched'] = len(target); info['extra'] = 0
            return 10 * len(target), A, (r2[0], info)
        v = 10 * len(target) - 10 - min(sl, 99)
    return v, A, (inS, info)

cur, A, sol = value(H, hint); best = (cur, H.copy(), sol); T = 1.0
print('start value %d %s' % (cur, sol[1] if sol else None), flush=True)
while time.monotonic() - t0 < 60 * minutes and best[0] < 10 * len(target):
    H2 = H.copy(); j = int(rng.integers(n)); H2[j] += float(rng.choice([0.01, 0.04, 0.15])) * rng.standard_normal(4)
    h = {k for k, s_ in zip(sorted(A.bounded), sol[0]) if s_} if sol else None
    v2, A2, sol2 = value(H2, h)
    if v2 >= cur or rng.random() < np.exp((v2 - cur) / T):
        H, cur, A, sol = H2, v2, A2, sol2
        if cur > best[0]:
            best = (cur, H.copy(), sol)
            print('  value %d (matched %d of %d, extra %d, valid %s, target slack %s) at %.0fs' % (cur, sol[1]['matched'], len(target),
                  sol[1]['extra'], sol[1]['valid'], sol[1].get('target_slack', '-'), time.monotonic() - t0), flush=True)
            Ab = SF.Arrangement(best[1])
            json.dump({'planes': best[1].tolist(), 'solid': [[int(x) for x in k] for k, s_ in zip(sorted(Ab.bounded), sol[0]) if s_],
                       'info': sol[1], 'target_genus': nxt['genus']}, open(out, 'w'))
    T = max(0.1, T * 0.995)
print('FINAL value %d of %d' % (best[0], 10 * len(target)), flush=True)
