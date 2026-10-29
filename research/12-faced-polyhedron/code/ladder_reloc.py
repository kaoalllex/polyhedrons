"""Plateau breaker for the ladder: EXACT single-plane relocation with the honest pair energy.

With the other n-1 planes fixed, every combinatorial predicate used by ladder.pair_energy is the sign
of a linear function of the moving plane h_k in R^4: h_k . (P_abc, 1) for the fixed triple points
(a, b, c != k) and h_k . (n_a x n_b, 0) for the fixed line directions. The energy is therefore
constant on the cells of this central arrangement of C(n-1,3) + C(n-1,2) hyperplanes (56 for n = 8);
every cell has a vertex ray (intersection of three hyperplanes), so probing the 8 cones around every
vertex ray visits every cell (h and -h are the same plane). Iterated: relocate each plane in turn
to its best cell (ties broken at random = plateau moves).
Usage: python3 -I ladder_reloc.py RESULTS_JSON INDEX SWEEPS SEED OUT_JSON"""
import json, sys, time
from itertools import combinations
import numpy as np
import numba
from numba import prange
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ladder import pack, pair_energy


def hyperplanes(H, k):
    n = len(H); G = []
    others = [i for i in range(n) if i != k]
    for a, b, c in combinations(others, 3):
        p = np.linalg.solve(H[[a, b, c], :3], -H[[a, b, c], 3]); G.append([*p, 1.0])
    for a, b in combinations(others, 2):
        d = np.cross(H[a, :3], H[b, :3]); G.append([*d, 0.0])
    G = np.array(G); G /= np.linalg.norm(G, axis=1)[:, None]
    return G


@numba.njit(cache=True)
def nondegenerate(H, k):
    n = H.shape[0]
    for a in range(n):
        if a == k:
            continue
        c = np.cross(H[k, :3], H[a, :3])
        if (c ** 2).sum() < 1e-16:
            return False
        for b in range(a + 1, n):
            if b == k:
                continue
            if abs(c @ H[b, :3]) < 1e-10:
                return False
    return True


@numba.njit(parallel=True, cache=True)
def scan(H, LK, M, k, G, T, eps):
    nt = T.shape[0]
    best_e = np.full(nt, 1e18); best_p = np.zeros((nt, 4))
    for t in prange(nt):
        A = np.empty((3, 4))
        for q in range(3):
            A[q] = G[T[t, q]]
        u, s, vt = np.linalg.svd(A)
        if s[2] < 1e-9:
            continue
        r = vt[3]
        AAt = A @ A.T
        dt = np.linalg.det(AAt)
        if abs(dt) < 1e-14:
            continue
        inv = np.linalg.inv(AAt)
        for code in range(8):
            sv = np.empty(3)
            for q in range(3):
                sv[q] = 1.0 if (code >> q) & 1 else -1.0
            w = A.T @ (inv @ sv)
            p = r + eps * w / np.sqrt((w ** 2).sum())
            nrm = np.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
            if nrm < 1e-6:
                continue
            # reject probes too close to any other hyperplane (thin-cell robustness)
            ok = True
            for g in range(G.shape[0]):
                if abs(G[g] @ p) < 1e-3 * eps:
                    ok = False
                    break
            if not ok:
                continue
            H2 = H.copy()
            for q in range(4):
                H2[k, q] = p[q] / nrm
            if not nondegenerate(H2, k):
                continue
            e, o = pair_energy(H2, LK, M)
            val = e + 0.01 * np.tanh(o)
            if val < best_e[t]:
                best_e[t] = val; best_p[t] = H2[k]
    return best_e, best_p


def relocate(H, LK, M, k, rng, eps=1e-4):
    G = hyperplanes(H, k)
    T = np.array(list(combinations(range(len(G)), 3)), np.int64)
    be, bp = scan(H, LK, M, k, G, T, eps)
    m = be.min()
    ties = np.flatnonzero(be <= m + 1e-12)
    j = int(rng.choice(ties))
    return float(m), bp[j], len(ties)


if __name__ == '__main__':
    R = json.load(open(sys.argv[1])); r = R[int(sys.argv[2])]
    sweeps, seed, out = int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = np.random.default_rng(seed)
    links = {int(k): v for k, v in r['links'].items()}
    LK, M, _ = pack(links); H = np.array(r['planes'], float); n = len(H)
    e, o = pair_energy(H, LK, M); cur = e + 0.01 * np.tanh(o)
    print('start', round(cur, 4), flush=True)
    for sw in range(sweeps):
        for k in rng.permutation(n):
            t0 = time.time()
            m, p, nt = relocate(H, LK, M, int(k), rng)
            if m <= cur + 1e-12:
                H[k] = p; cur = m
            print('sweep %d plane %d: best cell %.4f (%d ties) -> current %.4f  [%.0fs]' % (sw, k, m, nt, cur, time.time() - t0), flush=True)
            if cur < 0.5:
                break
        json.dump({'links': {str(a): b for a, b in links.items()}, 'planes': H.tolist(), 'energy': cur}, open(out, 'w'))
        if cur < 0.5:
            print('!!! ZERO (float) after relocation', flush=True)
            break
