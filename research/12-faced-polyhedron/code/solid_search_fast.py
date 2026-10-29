"""Solid-first search with topology macro-moves on the fast numba evaluator (solid_fast.py).
Same moves as solid_search.run3: plane moves (+carry +greedy polish), tunnel / handle macro-moves,
cell flips; objective = face-structure defects + |chi - chi_target| / 2; restarts half from the best.
--once: every pair of planes exactly one edge run (12 faces, 7 faces); otherwise >= 1 (ladder rungs).
Usage: python3 -I solid_search_fast.py N MINUTES SEED OUT_JSON [--once] [--init SOLIDS_JSON]"""
import json, sys, time
from collections import deque
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from solid_fast import Tables, fast_eval


class State:
    def __init__(self, H, inS_keys=None, rng=None, p=0.5):
        self.H = H; self.A = SF.Arrangement(H); self.T = Tables(self.A)
        self.idx = {k: i for i, k in enumerate(self.T.cells)}
        if inS_keys is None:
            self.inS = (rng.random(len(self.T.cells)) < p).astype(np.int64)
        else:
            self.inS = np.array([1 if k in inS_keys else 0 for k in self.T.cells], np.int64)
        self.nb = [[self.idx[x] for x in (tuple(k[:i] + (-k[i],) + k[i + 1:]) for i in range(len(k))) if x in self.idx]
                   for k in self.T.cells]

    def keys(self):
        return {k for k, v in zip(self.T.cells, self.inS) if v}


def obj(st, once, chi_t, detail=False):
    f, dsk, adj, miss, diag, badv, chi, rt = fast_eval(st.inS, *st.T.args())
    v = f + dsk + (adj if once else miss) + diag + badv + abs(chi - chi_t) / 2.0
    if detail:
        return v, dict(faces=int(f), disks=int(dsk), adjacency=int(adj), missing=int(miss), diagonal=int(diag),
                       bad_vertices=int(badv), chi=int(chi), runs=int(rt))
    return v


def polish(st, once, chi_t, rng, cur=None):
    if cur is None:
        cur = obj(st, once, chi_t)
    improved = True
    while improved:
        improved = False
        for i in rng.permutation(len(st.inS)):
            st.inS[i] ^= 1
            c = obj(st, once, chi_t)
            if c < cur:
                cur = c; improved = True
            else:
                st.inS[i] ^= 1
    return cur


def carry(old, H2, rng):
    S = old.keys()
    new = State(H2, inS_keys=S)
    for i, k in enumerate(new.T.cells):
        if k in old.idx:
            continue
        nbk = new.nb[i]
        if nbk and sum(new.inS[j] for j in nbk) * 2 > len(nbk):
            new.inS[i] = 1
    return new


def macro(st, rng, kind):
    inS = st.inS; ncell = len(inS)
    if kind == 'drill':
        pool = [i for i in range(ncell) if inS[i] and (len(st.nb[i]) < st.A.n or any(not inS[j] for j in st.nb[i]))]
        allowed = lambda j: inS[j] == 1
    else:
        pool = [i for i in range(ncell) if not inS[i] and any(inS[j] for j in st.nb[i])]
        allowed = lambda j: inS[j] == 0
    if len(pool) < 2:
        return False
    a, b = (pool[i] for i in rng.choice(len(pool), 2, replace=False))
    prev = {a: -1}; dq = deque([a])
    while dq:
        x = dq.popleft()
        if x == b:
            break
        for y in st.nb[x]:
            if y not in prev and allowed(y):
                prev[y] = x; dq.append(y)
    if b not in prev:
        return False
    path = []; x = b
    while x != -1:
        path.append(x); x = prev[x]
    if len(path) < 3:
        return False
    for x in path:
        inS[x] = 0 if kind == 'drill' else 1
    return True


def run(n, minutes, seed, once, init=None):
    g_t = -(-(n - 3) * (n - 4) // 12); chi_t = 2 - 2 * g_t
    rng = np.random.default_rng(seed); t0 = time.monotonic()
    best = (1e9, None, None, None); restarts = 0
    while time.monotonic() - t0 < 60 * minutes and best[0] > 0:
        restarts += 1
        try:
            if init is not None and restarts == 1:
                st = State(np.array(init['planes'], float), inS_keys={tuple(x) for x in init['solid']})
            elif best[1] is not None and rng.random() < 0.5:
                st = carry(State(best[1], inS_keys=best[2]), best[1] + 0.03 * rng.standard_normal(best[1].shape), rng)
            else:
                st = State(rng.standard_normal((n, 4)), rng=rng)
        except np.linalg.LinAlgError:
            continue
        cur = polish(st, once, chi_t, rng); T = 1.0
        for _ in range(800):
            if time.monotonic() - t0 > 60 * minutes:
                break
            r = rng.random()
            if r < 0.4:
                H2 = st.H.copy(); j = int(rng.integers(n)); H2[j] += float(rng.choice([0.02, 0.08, 0.3])) * rng.standard_normal(4)
                try:
                    st2 = carry(st, H2, rng)
                except np.linalg.LinAlgError:
                    continue
            else:
                st2 = State.__new__(State); st2.__dict__ = dict(st.__dict__); st2.inS = st.inS.copy()
                if r < 0.7:
                    if not macro(st2, rng, 'drill' if rng.random() < 0.5 else 'handle'):
                        continue
                else:
                    st2.inS[int(rng.integers(len(st2.inS)))] ^= 1
            c2 = polish(st2, once, chi_t, rng)
            if c2 <= cur or rng.random() < np.exp((cur - c2) / T):
                st, cur = st2, c2
                if cur < best[0]:
                    best = (cur, st.H.copy(), st.keys(), obj(st, once, chi_t, True)[1])
                    if cur == 0:
                        break
            T = max(0.05, T * 0.993)
        print('restart %d: best %s %s' % (restarts, best[0], best[3]), flush=True)
    return best, restarts


if __name__ == '__main__':
    n, minutes, seed, out = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    once = '--once' in sys.argv
    init = json.load(open(sys.argv[sys.argv.index('--init') + 1])) if '--init' in sys.argv else None
    (b, H, S, d), rs = run(n, minutes, seed, once, init)
    json.dump({'n': n, 'once': once, 'best': float(b), 'detail': d, 'planes': H.tolist() if H is not None else None,
               'solid': [[int(x) for x in k] for k in S] if S is not None else None}, open(out, 'w'))
    print('FINAL n=%d best %s after %d restarts %s' % (n, b, rs, d), flush=True)
    if b == 0:
        print('!!! ZERO: embedded solid with the target face structure', flush=True)
