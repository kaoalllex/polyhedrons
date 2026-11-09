"""Second S5 encoder (E-261109-03), written from theory/mathematical-model.md section 5 and the S5 definition.
Shares no code with omsat.py / omsat_validate.py / pilot.py. Elements 0..F-1 are face planes, F is the plane at infinity.
Variables 1..C(F+1,4) are the chirotope signs; every other variable is a Tseitin gate of those (so a pinned chirotope
determines the whole formula, which `holds` evaluates without a solver).
Conditions: 3-term Grassmann-Pluecker; (a) no non-vertex triple point in all three faces (Lemma 5.1); (b) on every line
L_XY the faces X, Y overlap only in the prescribed shared segments (crossing parity along the ordered triple points);
(c) the segments of one pair are pairwise disjoint."""
from itertools import combinations


def det4(m):
    def det3(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    return sum((-1) ** j * m[0][j] * det3([[r[k] for k in range(4) if k != j] for r in m[1:]]) for j in range(4))


def chirotope(planes):
    """Signs of det(h_a, h_b, h_c, h_d), a<b<c<d, over planes (a, b, c, d: ax+by+cz+d = 0) and infinity (0,0,0,1)."""
    rows = [tuple(int(round(v * 10 ** 9)) if isinstance(v, float) else int(v) for v in p) for p in planes] + [(0, 0, 0, 1)]
    out = {}
    for q in combinations(range(len(rows)), 4):
        d = det4([rows[i] for i in q])
        if d == 0:
            raise ValueError(f'non-uniform: zero minor {q}')
        out[q] = d > 0
    return out


class Enc:
    def __init__(self, links, gauge=False):
        self.links = {int(k): list(v) for k, v in (links.items() if isinstance(links, dict) else enumerate(links))}
        self.F = F = len(self.links)
        self.INF = F
        self.nv = 0
        self.clauses = []
        self.gates = []
        self.cache = {}
        self.chi = {}
        for q in combinations(range(F + 1), 4):
            self.chi[q] = self.new()
        self.nchi = self.nv
        self.check_map()
        self.gp()
        if gauge:
            self.gauge()
        self.embedding()

    # ---- gates -------------------------------------------------------------------------------------------
    def new(self):
        self.nv += 1
        return self.nv

    def clause(self, *lits):
        out = []
        for l in lits:
            if l is True:
                return
            if l is not False:
                out.append(l)
        self.clauses.append(out)

    def xor(self, a, b):
        if a is False: return b
        if b is False: return a
        if a is True: return self.neg(b)
        if b is True: return self.neg(a)
        if a == b: return False
        if a == -b: return True
        key = ('x',) + tuple(sorted((a, b)))
        if key in self.cache: return self.cache[key]
        v = self.new(); self.cache[key] = v; self.gates.append(('xor', v, a, b))
        self.clauses += [[-v, a, b], [-v, -a, -b], [v, -a, b], [v, a, -b]]
        return v

    def xorn(self, lits):
        r = False
        for l in lits:
            r = self.xor(r, l)
        return r

    def neg(self, a):
        return (not a) if isinstance(a, bool) else -a

    def and_(self, a, b):
        if a is False or b is False: return False
        if a is True: return b
        if b is True: return a
        if a == b: return a
        if a == -b: return False
        key = ('a',) + tuple(sorted((a, b)))
        if key in self.cache: return self.cache[key]
        v = self.new(); self.cache[key] = v; self.gates.append(('and', v, a, b))
        self.clauses += [[-v, a], [-v, b], [v, -a, -b]]
        return v

    def or_(self, a, b):
        return self.neg(self.and_(self.neg(a), self.neg(b)))

    def orn(self, lits):
        r = False
        for l in lits:
            r = self.or_(r, l)
        return r

    def lit(self, *t):
        """Literal 'chi(t) > 0' for distinct elements t in any order."""
        s = sorted(t)
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if t[i] > t[j])
        v = self.chi[tuple(s)]
        return -v if inv % 2 else v

    # ---- map ---------------------------------------------------------------------------------------------
    def check_map(self):
        F, L = self.F, self.links
        corners = {}
        for X, l in L.items():
            for i in range(len(l)):
                t = frozenset((X, l[i], l[(i + 1) % len(l)]))
                assert len(t) == 3, 'degenerate corner'
                corners.setdefault(t, []).append(X)
        assert all(sorted(v) == sorted(t) for t, v in corners.items()), 'repeated or inconsistent corner triple'
        self.vertices = set(corners)
        self.segs = {}
        for X, Y in combinations(range(F), 2):
            sx = sorted(tuple(sorted((L[X][k - 1], L[X][(k + 1) % len(L[X])]))) for k, W in enumerate(L[X]) if W == Y)
            sy = sorted(tuple(sorted((L[Y][k - 1], L[Y][(k + 1) % len(L[Y])]))) for k, W in enumerate(L[Y]) if W == X)
            assert sx == sy, f'inconsistent segments of pair {X},{Y}'
            self.segs[(X, Y)] = sx

    # ---- chirotope axioms --------------------------------------------------------------------------------
    def gp(self):
        for tau in combinations(range(self.F + 1), 2):
            rest = [x for x in range(self.F + 1) if x not in tau]
            for a, b, c, d in combinations(rest, 4):
                u1 = self.xor(self.lit(*tau, a, b), self.lit(*tau, c, d))
                u2 = self.xor(self.lit(*tau, a, c), self.lit(*tau, b, d))
                u3 = self.xor(self.lit(*tau, a, d), self.lit(*tau, b, c))
                # T1 = not u1, T2 = u2 (negated term), T3 = not u3; forbid all-equal
                self.clause(u1, -u2, u3)
                self.clause(-u1, u2, -u3)

    def gauge(self):
        F = self.F
        for k in range(2, F):
            self.clause(self.lit(0, 1, k, F))
        self.clause(self.lit(0, 2, 3, 4))

    # ---- geometry of a line L_XY (X < Y) -----------------------------------------------------------------
    def gt(self, X, Y, W, Z):
        """t_W > t_Z along L_XY, in the direction fixed by the order X < Y."""
        if W > Z:
            return self.neg(self.gt(X, Y, Z, W))
        return self.xorn([self.lit(X, Y, Z, W), self.lit(X, Y, Z, self.INF), self.lit(X, Y, W, self.INF)])

    def sdiff(self, P, Q, Y):
        """Sides of the points P_P and P_Q (triples of planes) with respect to plane Y differ."""
        return self.xorn([self.lit(*P, Y), self.lit(*P, self.INF), self.lit(*Q, Y), self.lit(*Q, self.INF)])

    def face_on_line(self, X, Y, F):
        """Per point Z of the line L_XY: (parity incl. Z, parity before Z, in-run incl. Z, in-run before Z) for face F."""
        key = ('line', X, Y, F)
        if key in self.cache:
            return self.cache[key]
        G = Y if F == X else X
        L = self.links[F]; m = len(L)
        others = [W for W in range(self.F) if W not in (X, Y)]
        flips = {W: [] for W in others}
        for j, W in enumerate(L):
            if W == G:
                continue
            a, c = L[j - 1], L[(j + 1) % m]
            if G in (a, c):
                continue
            flips[W].append(self.sdiff((F, W, a), (F, W, c), G))
        for k, W in enumerate(L):
            if W != G:
                continue
            C, D, Cf, Df = L[k - 1], L[(k + 1) % m], L[k - 2], L[(k + 2) % m]
            rf = self.sdiff((F, C, Cf), (F, D, Df), G)
            later_is_C = self.gt(X, Y, C, D)
            flips[C].append(self.and_(rf, later_is_C))
            flips[D].append(self.and_(rf, self.neg(later_is_C)))
        fl = {W: self.xorn(v) for W, v in flips.items()}
        res = {}
        for Z in others:
            le = self.xorn([self.and_(fl[W], True if W == Z else self.neg(self.gt(X, Y, W, Z))) for W in others])
            lt = self.xorn([self.and_(fl[W], False if W == Z else self.gt(X, Y, Z, W)) for W in others if W != Z])
            res[Z] = (le, lt)
        self.cache[key] = res
        return res

    def run_on_line(self, X, Y):
        """Per point Z: (some prescribed segment contains the gap right of Z, ... left of Z)."""
        key = ('run', X, Y)
        if key in self.cache:
            return self.cache[key]
        others = [W for W in range(self.F) if W not in (X, Y)]
        res = {}
        for Z in others:
            def LE(W): return True if W == Z else self.neg(self.gt(X, Y, W, Z))
            def LT(W): return False if W == Z else self.gt(X, Y, Z, W)
            res[Z] = (self.orn([self.xor(LE(C), LE(D)) for C, D in self.segs[(X, Y)]]),
                      self.orn([self.xor(LT(C), LT(D)) for C, D in self.segs[(X, Y)]]))
        self.cache[key] = res
        return res

    def member(self, X, Y, F, Z):
        """P_XYZ (X < Y) lies in the closed region F_F, F in {X, Y}, read along L_XY."""
        le, lt = self.face_on_line(X, Y, F)[Z]
        rle, rlt = self.run_on_line(X, Y)[Z]
        return self.or_(self.or_(le, rle), self.or_(lt, rlt))

    def embedding(self):
        F = self.F
        for X, Y in combinations(range(F), 2):
            px, py, run = self.face_on_line(X, Y, X), self.face_on_line(X, Y, Y), self.run_on_line(X, Y)
            for Z in range(F):
                if Z in (X, Y):
                    continue
                self.clause(self.neg(px[Z][0]), self.neg(py[Z][0]), run[Z][0])      # (b)
            segs = self.segs[(X, Y)]
            for s, t in combinations(range(len(segs)), 2):                          # (c)
                for (C, D), pts in ((segs[s], segs[t]), (segs[t], segs[s])):
                    for e in pts:
                        a, b = self.gt(X, Y, C, e), self.gt(X, Y, D, e)
                        self.clause(self.neg(a), b); self.clause(a, self.neg(b))
        for X, Y, Z in combinations(range(F), 3):                                   # (a)
            if frozenset((X, Y, Z)) in self.vertices:
                continue
            self.clause(self.neg(self.member(X, Y, X, Z)), self.neg(self.member(Y, Z, Y, X)),
                        self.neg(self.member(X, Z, Z, Y)))

    # ---- evaluation and output ---------------------------------------------------------------------------
    def assignment(self, chi):
        val = {self.chi[q]: s for q, s in chi.items()}
        for kind, v, a, b in self.gates:
            x = val[abs(a)] == (a > 0); y = val[abs(b)] == (b > 0)
            val[v] = (x != y) if kind == 'xor' else (x and y)
        return val

    def holds(self, chi):
        val = self.assignment(chi)
        return all(any(val[abs(l)] == (l > 0) for l in c) for c in self.clauses)

    def pin(self, chi):
        return [[self.chi[q] if s else -self.chi[q]] for q, s in chi.items()]

    def dimacs(self, path, extra=(), comment=''):
        cl = self.clauses + list(extra)
        with open(path, 'w') as f:
            f.write(f'c {comment}\np cnf {self.nv} {len(cl)}\n')
            for c in cl:
                f.write(' '.join(map(str, c)) + ' 0\n')
