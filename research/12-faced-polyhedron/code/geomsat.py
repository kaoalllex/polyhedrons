"""Geometry-first SAT (Track 4, mathematical-model.md section 6(B)).

Given n planes in general position (exact, integer), search for a triangulation (dual of the polyhedron)
on the n face labels such that the face-plane realization is an embedded polyhedron:

  variables t_XYZ (triple {X,Y,Z} is a triangle / a vertex of the polyhedron)
  hard: each pair in exactly 2 triangles; every vertex link a single (n-1)-cycle (static short cycles +
        lazy cuts); for every triple  t_XYZ or not(IN[X;Y,Z] and IN[Y;Z,X] and IN[Z;X,Y])   (Lemma 5.1)
  IN / E predicates are Tseitin-encoded (full equivalences) from the *constants* (side bits, line orders).

Every SAT model is re-checked by the DIRECT exact checker of planes.py (see solve_sat(verify=True)).
"""
import itertools
import time
from itertools import combinations
from pysat.solvers import Solver

from planes import Arrangement, check_embedding, valid_triangulation, link_cycle


class Builder:
    """tiny Tseitin CNF builder with constant folding and common-subexpression caching"""

    def __init__(self, nfixed):
        self.nv = nfixed
        self.clauses = []
        self.cache = {}
        self.T = self.new()
        self.clauses.append([self.T])

    def new(self):
        self.nv += 1
        return self.nv

    def AND(self, lits):
        s = set()
        for l in lits:
            if l == self.T:
                continue
            if l == -self.T:
                return -self.T
            if -l in s:
                return -self.T
            s.add(l)
        if not s:
            return self.T
        if len(s) == 1:
            return next(iter(s))
        key = ("a", tuple(sorted(s)))
        v = self.cache.get(key)
        if v is None:
            v = self.new()
            self.cache[key] = v
            for l in s:
                self.clauses.append([-v, l])
            self.clauses.append([v] + [-l for l in s])
        return v

    def OR(self, lits):
        return -self.AND([-l for l in lits])

    def XOR(self, a, b):
        T = self.T
        if a == T:
            return -b
        if a == -T:
            return b
        if b == T:
            return -a
        if b == -T:
            return a
        if a == b:
            return -T
        if a == -b:
            return T
        flip = 1
        if a < 0:
            a, flip = -a, -flip
        if b < 0:
            b, flip = -b, -flip
        if a > b:
            a, b = b, a
        key = ("x", a, b)
        v = self.cache.get(key)
        if v is None:
            v = self.new()
            self.cache[key] = v
            self.clauses += [[-v, a, b], [-v, -a, -b], [v, -a, b], [v, a, -b]]
        return v * flip

    def XORS(self, lits):
        r = -self.T
        for l in lits:
            r = self.XOR(r, l)
        return r


_base_cache = {}


def base_clauses(n, static_cycle_len=4):
    """arrangement independent clauses: exactly-two partners per pair, short link cycles forbidden"""
    key = (n, static_cycle_len)
    if key in _base_cache:
        return _base_cache[key]
    tv = {t: i + 1 for i, t in enumerate(combinations(range(n), 3))}

    def T(a, b, c):
        return tv[tuple(sorted((a, b, c)))]

    cl = []
    for x, y in combinations(range(n), 2):
        lits = [T(x, y, w) for w in range(n) if w != x and w != y]
        for tri in combinations(lits, 3):           # at most 2
            cl.append([-l for l in tri])
        for i in range(len(lits)):                   # at least 2
            cl.append([lits[j] for j in range(len(lits)) if j != i])
    for X in range(n):
        others = [v for v in range(n) if v != X]
        for k in range(3, min(static_cycle_len, n - 2) + 1):
            for sub in combinations(others, k):
                first = sub[0]
                for perm in itertools.permutations(sub[1:]):
                    if perm[0] > perm[-1]:
                        continue
                    cyc = (first,) + perm
                    cl.append([-T(X, cyc[i], cyc[(i + 1) % k]) for i in range(k)])
    _base_cache[key] = (tv, cl)
    return tv, cl


class GeomEncoding:
    """CNF for a fixed arrangement.  ray='min' uses the line L_{X,min(Y,Z)} in IN[X;Y,Z]; 'max' uses L_{X,max(Y,Z)}."""

    def __init__(self, arr, static_cycle_len=4, hard_triples=True, ray="min", rev=False, soft=False):
        self.arr = arr
        n = self.n = arr.n
        self.tv, base = base_clauses(n, static_cycle_len)
        nt = len(self.tv)
        self.b = b = Builder(nt)
        b.clauses.extend(base)
        self.ray, self.rev = ray, rev
        self._E = {}
        self._pref = {}
        self._flip = {}
        self._suf = {}
        self.IN = {}
        self.viol = {}
        for T in combinations(range(n), 3):
            a, bb, c = T
            ins = [self.in_lit(a, bb, c), self.in_lit(bb, a, c), self.in_lit(c, a, bb)]
            tl = self.tv[T]
            v = b.AND([-tl] + ins)
            self.viol[T] = v
            if hard_triples:
                b.clauses.append([-v])
        self.clauses = b.clauses
        self.nvars = b.nv

    # ---- helpers
    def t(self, a, b, c):
        return self.tv[tuple(sorted((a, b, c)))]

    def order(self, x, y):
        o = self.arr.line_order(x, y)
        return o[::-1] if self.rev else o

    def prefix_xor(self, x, y):
        """PX[k] = XOR of t_{x,y,w} over the first k points of the (oriented) line order; PO = OR."""
        key = (min(x, y), max(x, y))
        r = self._pref.get(key)
        if r is None:
            o = self.order(*key)
            px, po = [-self.b.T], [-self.b.T]
            for w in o:
                tl = self.t(x, y, w)
                px.append(self.b.XOR(px[-1], tl))
                po.append(self.b.OR([po[-1], tl]))
            r = self._pref[key] = (px, po)
        return r

    def E(self, x, w, v):
        """P_{xwv} in the relative interior of edge e_xw  (edge on line L_xw)"""
        key = (min(x, w), max(x, w), v)
        r = self._E.get(key)
        if r is None:
            o = self.order(key[0], key[1])
            k = o.index(v)
            px, _ = self.prefix_xor(key[0], key[1])
            r = self._E[key] = self.b.AND([-self.t(x, w, v), px[k]])
        return r

    def flip(self, x, y):
        """boundary of polygon x crosses line L_xy at the run e_xy: far ends of e_xC, e_xD on opposite sides of H_y."""
        r = self._flip.get((x, y))
        if r is None:
            us = []
            for c in range(self.n):
                if c in (x, y):
                    continue
                pos = [cp for cp in range(self.n) if cp not in (x, c, y) and self.arr.side(x, c, cp, y) > 0]
                s = self.b.OR([self.t(x, c, cp) for cp in pos])
                us.append(self.b.AND([self.t(x, y, c), s]))
            r = self._flip[(x, y)] = self.b.XORS(us)
        return r

    def suffix_E(self, x, y):
        """SX[k] = XOR over points at positions >= k on L_xy of E(x,w;y)"""
        r = self._suf.get((x, y))
        if r is None:
            o = self.order(x, y)
            sx = [-self.b.T] * (len(o) + 1)
            for k in range(len(o) - 1, -1, -1):
                sx[k] = self.b.XOR(sx[k + 1], self.E(x, o[k], y))
            r = self._suf[(x, y)] = sx
        return r

    def in_lit(self, x, y, z):
        """IN[x; y,z] = P_xyz in closed region of polygon x (even-odd), ray along L_{x,y'} (y' = min or max of y,z)"""
        key = (x, min(y, z), max(y, z))
        r = self.IN.get(key)
        if r is None:
            yy, zz = (key[1], key[2]) if self.ray == "min" else (key[2], key[1])
            b = self.b
            o = self.order(x, yy)
            pz = o.index(zz)
            px, po = self.prefix_xor(x, yy)
            sx = self.suffix_E(x, yy)
            run = b.AND([-po[pz], self.flip(x, yy)])
            par = b.XOR(sx[pz + 1], run)
            r = b.OR([self.t(x, yy, zz), self.E(x, yy, zz), self.E(x, zz, yy), par])
            self.IN[key] = r
        return r

    def tri_from_model(self, model):
        s = set(l for l in model if l > 0)
        return [t for t, v in self.tv.items() if v in s]


def sub_cycles(tris, n):
    """components of each link (list of (X, [edges]) for links that are not one (n-1)-cycle)"""
    bad = []
    for X in range(n):
        adj = {}
        for t in tris:
            if X in t:
                y, z = [v for v in t if v != X]
                adj.setdefault(y, set()).add(z)
                adj.setdefault(z, set()).add(y)
        seen = set()
        comps = []
        for s0 in adj:
            if s0 in seen:
                continue
            comp, stack = [], [s0]
            seen.add(s0)
            while stack:
                u = stack.pop()
                comp.append(u)
                for w in adj[u]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            comps.append(comp)
        if len(comps) > 1:
            bad.append((X, comps))
    return bad


def cuts_for(enc, tris):
    cuts = []
    for X, comps in sub_cycles(tris, enc.n):
        tset = set(tris)
        for comp in comps:
            cs = set(comp)
            lits = [-enc.t(X, y, z) for y, z in combinations(sorted(comp), 2) if tuple(sorted((X, y, z))) in tset]
            cuts.append(lits)
    return cuts


def solve_sat(arr, solver="cadical195", verify=True, static_cycle_len=4, ray="min", rev=False, max_rounds=1000,
              enc=None):
    """returns (status, tris, info).  status 'SAT' | 'UNSAT'.  On SAT the direct checker is run."""
    t0 = time.time()
    enc = enc or GeomEncoding(arr, static_cycle_len=static_cycle_len, ray=ray, rev=rev)
    S = Solver(name=solver, bootstrap_with=enc.clauses)
    rounds = 0
    info = dict(cuts=0, nvars=enc.nvars, nclauses=len(enc.clauses), t_build=time.time() - t0)
    try:
        while True:
            rounds += 1
            if not S.solve():
                info.update(rounds=rounds, t_total=time.time() - t0)
                S.delete()
                return "UNSAT", None, info
            model = S.get_model()
            tris = enc.tri_from_model(model)
            cuts = cuts_for(enc, tris)
            if cuts:
                for c in cuts:
                    S.add_clause(c)
                info["cuts"] += len(cuts)
                continue
            break
    finally:
        pass
    S.delete()
    info.update(rounds=rounds, t_total=time.time() - t0)
    if verify:
        assert valid_triangulation(tris, arr.n), "SAT model is not a valid triangulation"
        res = check_embedding(arr, tris)
        info["direct_ok_triples"] = res["ok_triples"]
        info["direct_ok_pairs"] = res["ok_pairs"]
        if not (res["ok_triples"] and res["ok_pairs"]):
            info["DISAGREEMENT"] = dict(viol=res["viol_triples"], bad_pairs=res["bad_pairs"], simple=res["simple"])
    return "SAT", tris, info


def solve_maxsat(arr, timeout=None, static_cycle_len=4, ray="min", max_rounds=500, verbose=False):
    """minimise the number of violated non-triangle triple conditions (RC2).  Returns (cost, tris, info)."""
    from pysat.formula import WCNF
    from pysat.examples.rc2 import RC2
    t0 = time.time()
    enc = GeomEncoding(arr, static_cycle_len=static_cycle_len, hard_triples=False, ray=ray)
    w = WCNF()
    for c in enc.clauses:
        w.append(c)
    for T, v in enc.viol.items():
        if v == -enc.b.T:
            continue
        w.append([-v], weight=1)
    rc2 = RC2(w, solver="g4", adapt=True, exhaust=True, minz=True, trim=5)
    rounds = 0
    cuts_total = 0
    try:
        while True:
            rounds += 1
            model = rc2.compute()
            if model is None:
                return None, None, dict(rounds=rounds)
            tris = enc.tri_from_model(model)
            cuts = cuts_for(enc, tris)
            if not cuts:
                break
            for c in cuts:
                rc2.add_clause(c)
            cuts_total += len(cuts)
            if verbose:
                print("  maxsat round", rounds, "cost", rc2.cost, "cuts", len(cuts), "t=%.1f" % (time.time() - t0))
        cost = rc2.cost
    finally:
        rc2.delete()
    return cost, tris, dict(rounds=rounds, cuts=cuts_total, t_total=time.time() - t0, nvars=enc.nvars)


def solve_cpsat(arr, time_limit=60.0, workers=1, static_cycle_len=5, ray="min", hint=None, seed=0, bench=True):
    """anytime MaxSAT via OR-tools CP-SAT: minimise number of violated non-triangle triples.
    Returns (best_cost, lower_bound, tris, status, info).  static_cycle_len=5 makes the link constraint complete
    for n=12 (a 2-regular graph on 11 vertices that is not one cycle has a component of size <=5)."""
    from ortools.sat.python import cp_model
    t0 = time.time()
    enc = GeomEncoding(arr, static_cycle_len=static_cycle_len, hard_triples=False, ray=ray)
    m = cp_model.CpModel()
    if bench:
        extra_gates = []
        for (a, b2, c), v in enc.viol.items():
            extra_gates.append(enc.b.AND([v, enc.E(a, b2, c), enc.E(a, c, b2), enc.E(b2, c, a)]))
        enc.k3 = extra_gates
        enc.nvars = enc.b.nv
    nv = enc.nvars
    X = [None] + [m.NewBoolVar("v%d" % i) for i in range(1, nv + 1)]
    allcl = enc.b.clauses

    def lit(l):
        return X[l] if l > 0 else X[-l].Not()
    for c in allcl:
        m.AddBoolOr([lit(l) for l in c])
    vl = [enc.viol[T] for T in enc.viol if enc.viol[T] != -enc.b.T]
    obj = [lit(v) for v in vl]
    if bench:
        # weight 3 for a violated triple whose three edges are concurrent at P (= 3 polygon self-crossings)
        obj += [2 * lit(k) for k in enc.k3 if k != -enc.b.T]
    m.Minimize(sum(obj))
    if hint is not None:
        tset = set(hint)
        for T, v in enc.tv.items():
            m.AddHint(X[v], 1 if T in tset else 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = time_limit
    s.parameters.num_workers = workers
    s.parameters.random_seed = seed
    st = s.Solve(m)
    info = dict(t_total=time.time() - t0, nvars=nv)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        model = [(i if s.Value(X[i]) else -i) for i in range(1, nv + 1)]
        tris = enc.tri_from_model(model)
        return int(round(s.ObjectiveValue())), s.BestObjectiveBound(), tris, s.StatusName(st), info
    return None, None, None, s.StatusName(st), info
