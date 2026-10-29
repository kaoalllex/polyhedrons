"""Exact inner step for solid-first (advisor's direction 2): for FIXED planes, choose the set S of bounded
cells by CP-SAT so that the solid is a manifold (allowed octant patterns at every triple point, no
diagonal 1-cells), every pair of planes has AT MOST one edge run on its line, and the number of
adjacent pairs is maximal. An edge 1-cell = odd number of its 4 cells in S (XOR). With one disk face per
plane (checked afterwards with solid_fast; violated solutions are cut off by a no-good and the model is
re-solved, up to a limit) the result is an embedded polyhedron with n faces whose number of edges is
max_adjacent = 30 + 6 g for n = 12 (generally 3(n-2) + 6g... for n = 7, 21 = Szilassi).
Usage (histogram): python3 -I solid_cpsat.py N N_ARRANGEMENTS SEED [TIME_PER_SOLVE]"""
import sys, time, itertools
import numpy as np
from ortools.sat.python import cp_model
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from solid_fast import Tables, fast_eval


def allowed_octants():
    out = []
    for m in range(256):
        occ = [(m >> q) & 1 for q in range(8)]
        k = sum(occ)
        if k in (0, 8):
            out.append(occ); continue
        ok = True
        for val in (1, 0):
            nodes = [i for i in range(8) if occ[i] == val]
            seen = {nodes[0]}; st = [nodes[0]]
            while st:
                a = st.pop()
                for b in range(3):
                    y = a ^ (1 << b)
                    if occ[y] == val and y not in seen:
                        seen.add(y); st.append(y)
            if len(seen) != len(nodes):
                ok = False
        if ok:
            out.append(occ)
    return out


ALLOWED = allowed_octants()


def best_solid(A, T=None, time_limit=10.0, max_cuts=30, require_one_face=True, hint=None):
    T = T or Tables(A)
    nc = len(T.cells)
    model = cp_model.CpModel()
    x = [model.NewBoolVar('c%d' % i) for i in range(nc)]
    zero = model.NewConstant(0)
    lit = lambda c: x[c] if c >= 0 else zero
    # manifold vertices
    for v in range(T.OCT.shape[0]):
        cs = [int(c) for c in T.OCT[v]]
        if all(c < 0 for c in cs):
            continue
        vars_ = [lit(c) for c in cs]
        tup = [t for t in ALLOWED if all(t[q] == 0 for q in range(8) if cs[q] < 0)]
        model.AddAllowedAssignments(vars_, tup)
    # 1-cells: no diagonal pattern; edge indicator
    no = T.C4.shape[0]
    e = [None] * no
    for j in range(no):
        a, b, c, d = (int(t) for t in T.C4[j])          # (++), (+-), (-+), (--)
        la, lb, lc, ld = lit(a), lit(b), lit(c), lit(d)
        model.AddBoolOr([la.Not(), ld.Not(), lb, lc])     # not (++ and -- and not +- and not -+)
        model.AddBoolOr([lb.Not(), lc.Not(), la, ld])
        e[j] = model.NewBoolVar('e%d' % j)
        model.AddBoolXOr([la, lb, lc, ld, e[j].Not()])    # e = parity of the four cells
    # runs per pair of planes: run start at segment k = e_k and not e_{k-1}
    starts_by_pair = {}
    for j in range(no):
        p = int(T.PAIR[j]); k = int(T.KS[j])
        s = model.NewBoolVar('s%d' % j)
        if k == 0 or j == 0 or int(T.PAIR[j - 1]) != p:
            model.Add(s == e[j])
        else:
            model.AddBoolAnd([e[j], e[j - 1].Not()]).OnlyEnforceIf(s)
            model.AddBoolOr([e[j].Not(), e[j - 1], s])
            model.AddImplication(s, e[j])
        starts_by_pair.setdefault(p, []).append(s)
    adj = []
    for p, ss in starts_by_pair.items():
        model.Add(sum(ss) <= 1)
        a = model.NewBoolVar('a%d' % p); model.Add(sum(ss) == 1).OnlyEnforceIf(a); model.Add(sum(ss) == 0).OnlyEnforceIf(a.Not())
        adj.append(a)
    # one face per plane, via the Euler characteristic of the boundary region in each plane:
    # facets - (1-cells in its closure) + (vertices in its closure) = 1  (a single disk has chi = 1)
    nf = T.nf
    bf = []
    for f in range(nf):
        up, dn = int(T.fup[f]), int(T.fdn[f])
        b = model.NewBoolVar('b%d' % f)
        model.AddBoolXOr([lit(up), lit(dn), b.Not()])
        bf.append(b)
    chi_terms = {X: [] for X in range(T.n)}
    for f in range(nf):
        chi_terms[int(T.fplane[f])].append(bf[f])
    neg = {X: [] for X in range(T.n)}
    for j in range(no):
        for side, Fs in ((0, T.FX[j]), (1, T.FY[j])):
            f0, f1 = int(Fs[0]), int(Fs[1])
            o = model.NewBoolVar('o%d_%d' % (j, side))
            model.AddMaxEquality(o, [bf[f0], bf[f1]])
            neg[int(T.fplane[f0])].append(o)
    pos_v = {X: [] for X in range(T.n)}
    for v in range(T.OCT.shape[0]):
        for z in range(3):
            fs = [int(T.VF[v, 4 * z + q]) for q in range(4)]
            o = model.NewBoolVar('v%d_%d' % (v, z))
            model.AddMaxEquality(o, [bf[f] for f in fs])
            pos_v[int(T.fplane[fs[0]])].append(o)
            if require_one_face:
                # no pinch: the two diagonal quadrants of this plane at this vertex are not boundary alone
                q = [bf[f] for f in fs]                    # quadrant order (+,+), (+,-), (-,+), (-,-)
                model.AddBoolOr([q[0].Not(), q[3].Not(), q[1], q[2]])
                model.AddBoolOr([q[1].Not(), q[2].Not(), q[0], q[3]])
    if require_one_face:
        for X in range(T.n):
            model.Add(sum(chi_terms[X]) - sum(neg[X]) + sum(pos_v[X]) == 1)
    model.Add(sum(x) >= 1)
    model.Maximize(sum(adj))
    if hint is not None:                               # warm start from a previous solid (cell sign vectors)
        for i, k in enumerate(T.cells):
            model.AddHint(x[i], 1 if k in hint else 0)
    solver = cp_model.CpSolver(); solver.parameters.max_time_in_seconds = time_limit; solver.parameters.num_workers = 1
    cuts = 0; t0 = time.monotonic()
    while True:
        st = solver.Solve(model)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            return None
        inS = np.array([solver.Value(v) for v in x], np.int64)
        f, dsk, adjv, miss, diag, badv, chi, rt = fast_eval(inS, *T.args())
        val = int(round(solver.ObjectiveValue()))
        info = dict(adjacent=val, faces=int(f), disks=int(dsk), chi=int(chi), status=solver.StatusName(st), cuts=cuts,
                    seconds=round(time.monotonic() - t0, 2))
        if not require_one_face or (f == 0 and dsk == 0) or cuts >= max_cuts:
            info['valid'] = bool(f == 0 and dsk == 0 and diag == 0 and badv == 0)
            return inS, info
        model.AddBoolOr([x[i].Not() if inS[i] else x[i] for i in range(nc)])   # no-good cut
        cuts += 1


if __name__ == '__main__':
    n, N, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0
    rng = np.random.default_rng(seed); hist = {}; full = 3 * n * (n - 1) // 6 if False else n * (n - 1) // 2
    t0 = time.monotonic()
    for i in range(N):
        A = SF.Arrangement(rng.standard_normal((n, 4)))
        r = best_solid(A, time_limit=tl)
        if r is None:
            continue
        inS, info = r
        key = (info['adjacent'], info['valid'])
        hist[key] = hist.get(key, 0) + 1
        if info['valid'] and info['adjacent'] == full:
            print('!!! FULL NEIGHBOURLY SOLID on arrangement', i, info, flush=True)
        if (i + 1) % 20 == 0:
            print('after %d: %s (%.0fs)' % (i + 1, dict(sorted(hist.items())), time.monotonic() - t0), flush=True)
    print('n=%d, %d arrangements, %.0fs; histogram (adjacent pairs, one-disk-face-per-plane valid): %s'
          % (n, N, time.monotonic() - t0, dict(sorted(hist.items()))), flush=True)
