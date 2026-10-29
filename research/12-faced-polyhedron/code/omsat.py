"""OM-SAT encoder (Track 3): fixed combinatorial type, unknown uniform rank-4 chirotope.

Elements: faces 0..n-1 and INF = n (the plane at infinity h_INF = (0,0,0,1)).
Faces live in planes H_X = {p : h_X . (p,1) = 0}, h_X = (n_X, -d_X) in Z^4.

SIGN CONVENTION.  chi(a,b,c,d) for an ordered tuple of distinct elements is
    chi(a,b,c,d) = sign det(h_a, h_b, h_c, h_d)        (rows in the given order).
Only sorted 4-subsets (natural order, INF = n last) are variables; an ordered tuple is
sgn(sorting permutation) * chi(sorted).  Boolean variable p_S is TRUE iff chi(S) = +1.
Internally predicates are built from "negative bits" nb(t) := [chi(t) = -1], so that
products of signs are XORs of bits.

Derived predicates (proofs in mathematical-model.md §4-5, re-derived in the Track-3 notes):
  side(abc;d)  = chi(abcd) chi(abc INF)  = sign(n_d . P_abc - d_d)
  on L_XY with direction u_XY := spatial part of *(h_X ^ h_Y ^ h_INF) = -(n_X x n_Y):
      sign(t_W - t_Z) = chi(XYZW) chi(XYZ INF) chi(XYW INF)
  E(X,W;V)  "P_XWV in relint e_XW" = [side(XWA;V) != side(XWB;V)], {A,B} partners of XW
  IN(X;Y,Z) "P_XYZ in closed F_X", ray from P_XYZ along +u_XY (mathematical-model §5.2)
  REFLEX(X;Y,Z) for a triangle XYZ: "points of L_XY just beyond the corner P_XYZ, on the
      side away from e_XY, lie in F_X" (= corner of X at P_XYZ is reflex, for simple F_X)
  RTURN(X;A,B) for consecutive A,B in the link of X: the boundary walk ... -> P_XA'A -> P_XAB
      -> P_XBB' turns right (clockwise seen from n_X) at P_XAB.

The module provides two interchangeable "backends" for the same predicate formulas:
  CNF  - Tseitin circuit building (literals are ints, 1 = TRUE constant)
  Eval - direct evaluation for a concrete chirotope (literals are Python bools)
"""
import itertools
import json
from fractions import Fraction


# ----------------------------------------------------------------------------- utilities

def perm_parity(seq):
    """Parity (0 even / 1 odd) of the permutation sorting seq (distinct items)."""
    s = list(seq)
    p = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] > s[j]:
                p ^= 1
    return p


def det4(m):
    """Exact integer/Fraction 4x4 determinant (Laplace on first row via 3x3 minors)."""
    def det3(a):
        return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
                - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
                + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    s = 0
    for j in range(4):
        minor = [[m[i][k] for k in range(4) if k != j] for i in range(1, 4)]
        s += (-1) ** j * m[0][j] * det3(minor)
    return s


def chirotope_from_planes(planes):
    """planes: list of n integer 4-vectors h_X = (n_X, -d_X). Returns dict sorted quad -> +-1
    (0 if degenerate)."""
    n = len(planes)
    H = [tuple(p) for p in planes] + [(0, 0, 0, 1)]
    chi = {}
    for S in itertools.combinations(range(n + 1), 4):
        d = det4([H[i] for i in S])
        chi[S] = (d > 0) - (d < 0)
    return chi


# ----------------------------------------------------------------------------- triangulation

class Triangulation:
    """Neighborly-type triangulation on faces 0..n-1 (the dual of the polyhedron)."""

    def __init__(self, n, triangles, links=None):
        self.n = n
        self.tris = [tuple(t) for t in triangles]
        self.triset = set(frozenset(t) for t in triangles)
        self.partners = {}
        for t in self.tris:
            for a, b in itertools.combinations(t, 2):
                c = [x for x in t if x not in (a, b)][0]
                self.partners.setdefault(frozenset((a, b)), []).append(c)
        for k, v in self.partners.items():
            assert len(v) == 2, (k, v)
        assert len(self.partners) == n * (n - 1) // 2, "not neighborly"
        # cyclic link of each face (orientation taken from `links` if given, else arbitrary)
        self.link = {}
        for X in range(n):
            if links is not None:
                cyc = list(links[X])
            else:
                nb = {}
                for Y in range(n):
                    if Y != X:
                        nb[Y] = self.partners[frozenset((X, Y))]
                start = min(nb)
                cyc = [start, nb[start][0]]
                while len(cyc) < n - 1:
                    a, b = nb[cyc[-1]]
                    cyc.append(a if a != cyc[-2] else b)
                assert cyc[0] in nb[cyc[-1]]
            assert sorted(cyc) == [Y for Y in range(n) if Y != X]
            for i in range(n - 1):
                assert frozenset((X, cyc[i], cyc[(i + 1) % (n - 1)])) in self.triset
            self.link[X] = cyc

    def is_tri(self, a, b, c):
        return frozenset((a, b, c)) in self.triset

    def part(self, a, b):
        return self.partners[frozenset((a, b))]

    def other_partner(self, a, b, not_c):
        p = self.partners[frozenset((a, b))]
        assert not_c in p
        return p[0] if p[1] == not_c else p[1]

    def nontriangles(self):
        return [t for t in itertools.combinations(range(self.n), 3) if not self.is_tri(*t)]

    def corners(self, X):
        """Consecutive pairs (A,B) of the link of X (corner P_XAB)."""
        c = self.link[X]
        m = len(c)
        return [(c[i], c[(i + 1) % m]) for i in range(m)]


# ----------------------------------------------------------------------------- backends

class CNF:
    """Tseitin circuit builder. Variable 1 is the constant TRUE."""
    TRUE, FALSE = 1, -1

    def __init__(self, n):
        self.n = n
        self.INF = n
        self.nv = 1
        self.clauses = [[1]]
        self.qvar = {}
        for S in itertools.combinations(range(n + 1), 4):
            self.nv += 1
            self.qvar[S] = self.nv
        self._xor = {}
        self._and = {}
        self.named = {}
        self.tags = {}          # clause-family counts

    def new(self):
        self.nv += 1
        return self.nv

    def NOT(self, x):
        return -x

    def chi_neg(self, t):
        """literal TRUE iff chi(t) = -1 (t ordered tuple of distinct elements)."""
        S = tuple(sorted(t))
        v = self.qvar[S]
        return v if perm_parity(t) else -v

    def chi_pos_lit(self, t):
        return -self.chi_neg(t)

    def xor(self, lits):
        par = 0
        cnt = {}
        for l in lits:
            if l == 1:
                par ^= 1
            elif l == -1:
                continue
            else:
                if l < 0:
                    par ^= 1
                cnt[abs(l)] = cnt.get(abs(l), 0) ^ 1
        vs = sorted(v for v, c in cnt.items() if c)
        if not vs:
            return 1 if par else -1
        if len(vs) == 1:
            return -vs[0] if par else vs[0]
        key = tuple(vs)
        if key not in self._xor:
            t = vs[0]
            for v in vs[1:]:
                k2 = (min(t, v), max(t, v))
                if k2 not in self._xor:
                    z = self.new()
                    a, b = k2
                    self.clauses += [[-z, a, b], [-z, -a, -b], [z, -a, b], [z, a, -b]]
                    self._xor[k2] = z
                t = self._xor[k2]
            self._xor[key] = t
        z = self._xor[key]
        return -z if par else z

    def and_(self, lits):
        s = set()
        for l in lits:
            if l == -1:
                return -1
            if l == 1:
                continue
            s.add(l)
        for l in s:
            if -l in s:
                return -1
        if not s:
            return 1
        if len(s) == 1:
            return next(iter(s))
        key = tuple(sorted(s))
        if key not in self._and:
            z = self.new()
            for l in key:
                self.clauses.append([-z, l])
            self.clauses.append([z] + [-l for l in key])
            self._and[key] = z
        return self._and[key]

    def or_(self, lits):
        return -self.and_([-l for l in lits])

    defs_only = False

    def clause(self, lits, tag):
        if self.defs_only:
            return
        out = []
        for l in lits:
            if l == 1:
                return
            if l == -1:
                continue
            out.append(l)
        if not out:
            out = [-1]            # empty clause (instance trivially UNSAT)
        self.clauses.append(out)
        self.tags[tag] = self.tags.get(tag, 0) + 1

    def equiv(self, a, b, tag):
        self.clause([-a, b], tag)
        self.clause([a, -b], tag)

    def name(self, key, lit):
        self.named[key] = lit
        return lit

    def gp(self):
        """3-term Grassmann-Pluecker relations for uniform chi (16 six-literal clauses each)."""
        INF = self.INF
        els = list(range(self.n + 1))
        cnt = 0
        for a, b in itertools.combinations(els, 2):
            rest = [e for e in els if e not in (a, b)]
            for c, d, e, f in itertools.combinations(rest, 4):
                # T1 = chi(abcd)chi(abef), T2 = -chi(abce)chi(abdf), T3 = chi(abcf)chi(abde)
                pairs = [((a, b, c, d), (a, b, e, f), 0),
                         ((a, b, c, e), (a, b, d, f), 1),
                         ((a, b, c, f), (a, b, d, e), 0)]
                L = [(self.chi_neg(p), self.chi_neg(q), k) for p, q, k in pairs]
                # forbid T1 = T2 = T3 (as neg bits: nb(p) ^ nb(q) ^ k all equal)
                for target in (0, 1):
                    for bits in itertools.product((0, 1), repeat=3):
                        # choose value of first literal of each pair; second is determined
                        cl = []
                        for (lp, lq, k), bp in zip(L, bits):
                            bq = bp ^ k ^ target
                            cl.append(-lp if bp else lp)
                            cl.append(-lq if bq else lq)
                        self.clauses.append(cl)
                        cnt += 1
        self.tags['GP'] = self.tags.get('GP', 0) + cnt

    def dimacs(self, path, comments=()):
        with open(path, 'w') as f:
            for c in comments:
                f.write('c %s\n' % c)
            f.write('p cnf %d %d\n' % (self.nv, len(self.clauses)))
            for cl in self.clauses:
                f.write(' '.join(map(str, cl)) + ' 0\n')


class Eval:
    """Evaluate the same predicate formulas on a concrete chirotope (dict sorted quad -> +-1)."""
    TRUE, FALSE = True, False

    def __init__(self, n, chi):
        self.n = n
        self.INF = n
        self.chi = chi
        self.named = {}
        self.violations = []
        self.tags = {}

    def NOT(self, x):
        return not x

    def chi_neg(self, t):
        S = tuple(sorted(t))
        s = self.chi[S]
        assert s != 0, ("degenerate quadruple", S)
        if perm_parity(t):
            s = -s
        return s < 0

    def xor(self, lits):
        r = False
        for l in lits:
            r ^= bool(l)
        return r

    def and_(self, lits):
        return all(lits)

    def or_(self, lits):
        return any(lits)

    def clause(self, lits, tag):
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if not any(lits):
            self.violations.append(tag)

    def equiv(self, a, b, tag):
        self.clause([not a, b], tag)
        self.clause([a, not b], tag)

    def name(self, key, lit):
        self.named[key] = lit
        return lit

    def gp(self):
        els = list(range(self.n + 1))
        bad = 0
        for a, b in itertools.combinations(els, 2):
            rest = [e for e in els if e not in (a, b)]
            for c, d, e, f in itertools.combinations(rest, 4):
                def s(t):
                    return -1 if self.chi_neg(t) else 1
                T = [s((a, b, c, d)) * s((a, b, e, f)), -s((a, b, c, e)) * s((a, b, d, f)),
                     s((a, b, c, f)) * s((a, b, d, e))]
                if len(set(T)) == 1:
                    bad += 1
        if bad:
            self.violations += ['GP'] * bad
        return bad


# ----------------------------------------------------------------------------- predicates

class Predicates:
    """All predicate formulas, written once against a backend B (CNF or Eval)."""

    def __init__(self, B, T):
        self.B, self.T = B, T
        self.INF = T.n
        self._c = {}

    def _memo(self, key, fn):
        if key not in self._c:
            self._c[key] = fn()
        return self._c[key]

    def nb(self, *t):
        return self.B.chi_neg(t)

    def sd(self, a, b, c, d):
        """TRUE iff side(abc;d) = -1  (vertex P_abc on the negative side of H_d)."""
        key = ('sd', frozenset((a, b, c)), d)
        return self._memo(key, lambda: self.B.xor([self.nb(a, b, c, d), self.nb(a, b, c, self.INF)]))

    def lt(self, X, Y, Z, W):
        """TRUE iff t_W < t_Z on L_XY (direction u_XY from the ordered pair (X,Y))."""
        key = ('lt', X, Y, Z, W)
        return self._memo(key, lambda: self.B.xor([self.nb(X, Y, Z, W), self.nb(X, Y, Z, self.INF),
                                                    self.nb(X, Y, W, self.INF)]))

    def E(self, X, W, V):
        """TRUE iff P_XWV lies in the relative interior of the edge e_XW."""
        key = ('E', frozenset((X, W)), V)

        def f():
            A, Bp = self.T.part(X, W)
            if V in (A, Bp):
                return self.B.FALSE
            return self.B.xor([self.sd(X, W, A, V), self.sd(X, W, Bp, V)])
        return self._memo(key, f)

    def IN(self, X, Y, Z):
        """TRUE iff P_XYZ lies in the closed region F_X (boundary or odd crossing parity),
        ray along L_XY in direction +u_XY.  Requires XYZ not a triangle."""
        key = ('IN', X, Y, Z)

        def f():
            B, T = self.B, self.T
            assert not T.is_tri(X, Y, Z)
            C, D = T.part(X, Y)
            Cp = T.other_partner(X, C, Y)
            Dp = T.other_partner(X, D, Y)
            b1 = self.E(X, Y, Z)
            b2 = self.E(X, Z, Y)
            terms = []
            for W in range(T.n):
                if W in (X, Y, Z, C, D):
                    continue
                terms.append(B.and_([B.NOT(self.lt(X, Y, Z, W)), self.E(X, W, Y)]))
            cross = B.xor([self.sd(X, C, Cp, Y), self.sd(X, D, Dp, Y)])
            terms.append(B.and_([B.NOT(self.lt(X, Y, Z, C)), cross]))
            par = B.xor(terms)
            return B.or_([b1, b2, par])
        return self._memo(key, f)

    def REFLEX(self, X, Y, Z):
        """For a triangle XYZ: TRUE iff the points of L_XY just beyond P_XYZ (away from the
        edge e_XY) lie in F_X.  Uses the ray along L_XY starting there."""
        key = ('RF', X, Y, Z)

        def f():
            B, T = self.B, self.T
            assert T.is_tri(X, Y, Z)
            D = T.other_partner(X, Y, Z)
            ltD = self.lt(X, Y, Z, D)
            terms = []
            for W in range(T.n):
                if W in (X, Y, Z, D):
                    continue
                far = B.xor([self.lt(X, Y, Z, W), ltD])
                terms.append(B.and_([far, self.E(X, W, Y)]))
            return B.xor(terms)
        return self._memo(key, f)

    def RTURN(self, X, A, Bv):
        """Corner P_XAB, A then B consecutive in link(X): walk P_XA'A -> P_XAB -> P_XBB'.
        TRUE iff right turn (clockwise seen from n_X).
        left turn  <=>  sign(t_B - t_A') on L_XA  *  side(X B B'; A)  = +1."""
        key = ('RT', X, A, Bv)

        def f():
            T = self.T
            Ap = T.other_partner(X, A, Bv)
            Bpp = T.other_partner(X, Bv, A)
            return self.B.xor([self.lt(X, A, Ap, Bv), self.sd(X, Bv, Bpp, A)])
        return self._memo(key, f)


# ----------------------------------------------------------------------------- instance

DEFAULT_OPTS = dict(gp=True, triples=True, inconsist=False, reflex=False, reflexconsist=False,
                    poc=False, symbreak=False, mirror=False)


def build(B, T, opts=None, sym=None):
    """Add all requested clause families to backend B.  Returns the Predicates object.

    opts keys:
      gp            3-term Grassmann-Pluecker relations                          (F1)
      triples       Lemma 5.1 forbidden triples, IN along L_XY, L_YZ, L_ZX        (F2)
      inconsist     IN(X;Y,Z) == IN(X;Z,Y) (two different rays)                  (F3)
      reflex        at most one reflex corner at each vertex                     (F4)
      reflexconsist reflex bit along L_XY == along L_XZ                          (F5)
      poc           polygon-orientation consistency: RTURN xor REFLEX constant
                    over the corners of each face                                (F6)
      symbreak      reorientation normalisation chi(0,1,k,INF)=chi(0,2,3,INF)=chi(1,2,3,INF)=+1
      mirror        chi(0,1,2,3) = +1  (only together with symbreak)
    sym: optional list of (perm, detsign) - chi(perm(S)) = detsign * chi(S) for all S
    """
    o = dict(DEFAULT_OPTS)
    if opts:
        o.update(opts)
    P = Predicates(B, T)
    n = T.n
    INF = n
    if o['gp']:
        B.gp()
    nt = T.nontriangles()
    if o['triples']:
        for X, Y, Z in nt:
            a = B.name(('IN', X, Y, Z), P.IN(X, Y, Z))
            b = B.name(('IN', Y, Z, X), P.IN(Y, Z, X))
            c = B.name(('IN', Z, X, Y), P.IN(Z, X, Y))
            B.clause([B.NOT(a), B.NOT(b), B.NOT(c)], 'TRIPLE')
    if o['inconsist']:
        for X, Y, Z in nt:
            for (p, q, r) in ((X, Y, Z), (Y, Z, X), (Z, X, Y)):
                l1 = B.name(('IN', p, q, r), P.IN(p, q, r))
                l2 = B.name(('IN', p, r, q), P.IN(p, r, q))
                B.equiv(l1, l2, 'INCONS')
    if o['reflex'] or o['reflexconsist'] or o['poc']:
        for X in range(n):
            for A, Bv in T.corners(X):
                B.name(('RF', X, A, Bv), P.REFLEX(X, A, Bv))
                B.name(('RF', X, Bv, A), P.REFLEX(X, Bv, A))
                B.name(('RT', X, A, Bv), P.RTURN(X, A, Bv))
    if o['reflexconsist']:
        for X in range(n):
            for A, Bv in T.corners(X):
                B.equiv(P.REFLEX(X, A, Bv), P.REFLEX(X, Bv, A), 'RFCONS')
    if o['reflex']:
        for t in T.tris:
            X, Y, Z = t
            r = [P.REFLEX(X, Y, Z), P.REFLEX(Y, Z, X), P.REFLEX(Z, X, Y)]
            for i, j in itertools.combinations(range(3), 2):
                B.clause([B.NOT(r[i]), B.NOT(r[j])], 'REFLEX1')
    if o['poc']:
        for X in range(n):
            cs = T.corners(X)
            w = [B.xor([P.RTURN(X, A, Bv), P.REFLEX(X, A, Bv)]) for A, Bv in cs]
            for i in range(1, len(w)):
                B.equiv(w[0], w[i], 'POC')
    if o['symbreak']:
        fixed = [(0, 1, k, INF) for k in range(2, n)] + [(0, 2, 3, INF), (1, 2, 3, INF)]
        for S in fixed:
            B.clause([B.NOT(B.chi_neg(S))], 'SB_REORIENT')
        if o['mirror']:
            B.clause([B.NOT(B.chi_neg((0, 1, 2, 3)))], 'SB_MIRROR')
    if sym:
        for perm, ds in sym:
            for S in itertools.combinations(range(n + 1), 4):
                img = tuple(perm[e] if e < n else INF for e in S)
                a = B.chi_neg(S)
                b = B.chi_neg(img)
                if ds > 0:
                    B.equiv(a, b, 'SYM')
                else:
                    B.equiv(a, B.NOT(b), 'SYM')
    return P


def load_types(path):
    with open(path) as f:
        d = json.load(f)
    out = []
    for e in d:
        links = {int(k): v for k, v in e['links'].items()} if 'links' in e else None
        out.append((e['id'], Triangulation(12, e['triangles'], links), e))
    return out
