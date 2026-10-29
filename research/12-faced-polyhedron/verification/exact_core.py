"""Independent exact (integer / Fraction) core for the adversarial verification of
mathematical-model.md Sec. 5 (Lemma 5.1, Sec. 5.1 sign formulas, Sec. 5.2 in-face predicate).

Written from the specification only; imports nothing from ../code.
Planes are integer 4-vectors h = (a, b, c, e) meaning a x + b y + c z + e = 0
(h . (p, 1) = n . p - d with n = (a, b, c), d = -e).  Index n is the plane at infinity (0,0,0,1).
"""
import itertools
import random
from fractions import Fraction

# ---------------------------------------------------------------- linear algebra (exact)

def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def det4(r0, r1, r2, r3):
    rows = (r0, r1, r2, r3)
    tot = 0
    for j in range(4):
        if r3[j] == 0:
            continue
        minor = [[r[k] for k in range(4) if k != j] for r in rows[:3]]
        tot += (-1) ** (3 + j) * r3[j] * det3(*minor)
    return tot


def sgn(x):
    return (x > 0) - (x < 0)


def perm_sign(seq):
    s = list(seq)
    sign = 1
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] > s[j]:
                sign = -sign
    return sign


def solve3(rows, rhs):
    """Exact Gaussian elimination, Fractions. rows: 3x3, rhs: 3."""
    M = [[Fraction(x) for x in r] + [Fraction(b)] for r, b in zip(rows, rhs)]
    for col in range(3):
        piv = next(i for i in range(col, 3) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        for i in range(3):
            if i != col and M[i][col] != 0:
                f = M[i][col] / M[col][col]
                M[i] = [x - f * y for x, y in zip(M[i], M[col])]
    return tuple(M[i][3] / M[i][i] for i in range(3))


# ---------------------------------------------------------------- triangulations

def partners_table(n, triangles):
    part = {}
    for t in triangles:
        for X, W, A in itertools.permutations(t):
            part.setdefault((X, W), []).append(A)
    for X in range(n):
        for W in range(n):
            if X != W:
                assert len(part[(X, W)]) == 2, (X, W, part.get((X, W)))
    return part


def links_from(n, part):
    out = []
    for X in range(n):
        W0 = (X + 1) % n
        cyc = [W0, part[(X, W0)][0]]
        while len(cyc) < n - 1:
            a, b = part[(X, cyc[-1])]
            cyc.append(a if a != cyc[-2] else b)
        assert len(set(cyc)) == n - 1 and X not in cyc
        a, b = part[(X, cyc[-1])]
        assert cyc[0] in (a, b)
        out.append(cyc)
    return out


TORUS7 = sorted({tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}
                | {tuple(sorted(((i) % 7, (i + 2) % 7, (i + 3) % 7))) for i in range(7)})


def relabel(tris, perm):
    return [tuple(sorted(perm[v] for v in t)) for t in tris]


# ---------------------------------------------------------------- configuration

class Config:
    def __init__(self, H, triangles):
        self.H = [tuple(int(x) for x in h) for h in H]
        self.n = n = len(H)
        self.INF = n
        self.vec = self.H + [(0, 0, 0, 1)]
        self.tris = [tuple(sorted(t)) for t in triangles]
        self.triset = set(self.tris)
        self.part = partners_table(n, self.tris)
        self.link = links_from(n, self.part)
        self._det = {}
        for q in itertools.combinations(range(n + 1), 4):
            self._det[q] = det4(*(self.vec[i] for i in q))
        self.gp = all(v != 0 for v in self._det.values())
        self._P = {}

    # chirotope ---------------------------------------------------------
    def chi(self, *idx):
        if len(set(idx)) < 4:
            return 0
        s = tuple(sorted(idx))
        return perm_sign(idx) * sgn(self._det[s])

    def side_chi(self, a, b, c, d):          # Sec. 5.1 formula
        return self.chi(a, b, c, d) * self.chi(a, b, c, self.INF)

    def later_chi(self, X, Y, Z, W):         # Sec. 5.1: sign(t_W - t_Z)
        I = self.INF
        return self.chi(X, Y, Z, W) * self.chi(X, Y, Z, I) * self.chi(X, Y, W, I)

    def is_tri(self, a, b, c):
        return tuple(sorted((a, b, c))) in self.triset

    # direct geometry ---------------------------------------------------
    def P(self, a, b, c):
        key = tuple(sorted((a, b, c)))
        if key not in self._P:
            rows = [self.H[i][:3] for i in key]
            rhs = [-self.H[i][3] for i in key]
            self._P[key] = solve3(rows, rhs)
        return self._P[key]

    def f(self, d, p):                       # plane functional at a Fraction point
        h = self.H[d]
        return h[0] * p[0] + h[1] * p[1] + h[2] * p[2] + h[3]

    def side_geo(self, a, b, c, d):
        return sgn(self.f(d, self.P(a, b, c)))

    def u(self, X, Y):                       # n_X x n_Y  (fastviol's direction)
        a, b = self.H[X], self.H[Y]
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def t(self, X, Y, p):
        u = self.u(X, Y)
        return u[0] * p[0] + u[1] * p[1] + u[2] * p[2]

    def polygon(self, X):
        L = self.link[X]
        m = len(L)
        # vertex i = P(X, L[i], L[i+1]); edge e_{X L[i]} = [vertex i-1, vertex i]
        return [self.P(X, L[i], L[(i + 1) % m]) for i in range(m)]

    def proj_axis(self, X):
        n = self.H[X][:3]
        return max(range(3), key=lambda k: abs(n[k]))

    def to2d(self, X, p):
        k = self.proj_axis(X)
        return tuple(p[i] for i in range(3) if i != k)


# ---------------------------------------------------------------- Sec. 5.2 predicate (chirotope only)

def other(pair, x):
    a, b = pair
    assert x in (a, b)
    return b if a == x else a


def IN_chi(cf, X, Y, Z, reverse=False):
    """Sec. 5.2 IN[X;Y,Z], computed only from chi via the Sec. 5.1 formulas.
    reverse=True uses the opposite ray direction (Plus replaced by Minus)."""
    part = cf.part
    C, D = part[(X, Y)]
    s = cf.side_chi
    if s(X, Y, C, Z) == -s(X, Y, D, Z):
        return 1
    A, B = part[(X, Z)]
    if s(X, Z, A, Y) == -s(X, Z, B, Y):
        return 1

    def plus(W):
        v = cf.later_chi(X, Y, Z, W)
        return (v < 0) if reverse else (v > 0)
    cnt = 0
    for W in range(cf.n):
        if W in (X, Y, Z, C, D):
            continue
        if plus(W):
            A, B = part[(X, W)]
            if s(X, W, A, Y) == -s(X, W, B, Y):
                cnt += 1
    if plus(C) and plus(D):
        Cp = other(part[(X, C)], Y)
        Dp = other(part[(X, D)], Y)
        if s(X, C, Cp, Y) != s(X, D, Dp, Y):
            cnt += 1
    return cnt & 1


def violations_chi(cf):
    out = []
    for a, b, c in itertools.combinations(range(cf.n), 3):
        if cf.is_tri(a, b, c):
            continue
        if IN_chi(cf, a, b, c) and IN_chi(cf, b, c, a) and IN_chi(cf, c, a, b):
            out.append((a, b, c))
    return out


# ---------------------------------------------------------------- direct point-in-polygon (2D, exact)

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def on_segment(p, q, r):
    return (cross(p, q, r) == 0 and min(p[0], q[0]) <= r[0] <= max(p[0], q[0])
            and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]))


def pip(poly, r):
    """Returns (on_boundary, evenodd_parity, winding_number) for 2D polygon and point r."""
    m = len(poly)
    for i in range(m):
        if on_segment(poly[i], poly[(i + 1) % m], r):
            return True, None, None
    par = 0
    wn = 0
    for i in range(m):
        p, q = poly[i], poly[(i + 1) % m]
        if (p[1] > r[1]) != (q[1] > r[1]):
            x = p[0] + (r[1] - p[1]) * (q[0] - p[0]) / (q[1] - p[1])
            if x > r[0]:
                par ^= 1
        if p[1] <= r[1]:
            if q[1] > r[1] and cross(p, q, r) > 0:
                wn += 1
        else:
            if q[1] <= r[1] and cross(p, q, r) < 0:
                wn -= 1
    return False, par, wn


def in_face_direct(cf, X, p, poly2d=None):
    """Membership of the 3D point p (in H_X) in F_X = curve U {odd parity}. Returns (in, info)."""
    if poly2d is None:
        poly2d = [cf.to2d(X, v) for v in cf.polygon(X)]
    on, par, wn = pip(poly2d, cf.to2d(X, p))
    return (1 if on or par else 0), (on, par, wn)


def segments_intersect(p1, p2, q1, q2):
    d1, d2 = cross(q1, q2, p1), cross(q1, q2, p2)
    d3, d4 = cross(p1, p2, q1), cross(p1, p2, q2)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return (on_segment(q1, q2, p1) or on_segment(q1, q2, p2) or on_segment(p1, p2, q1)
            or on_segment(p1, p2, q2))


def simple_direct(poly):
    m = len(poly)
    for i in range(m):
        for j in range(i + 1, m):
            if j == i + 1 or (i == 0 and j == m - 1):
                continue
            if segments_intersect(poly[i], poly[(i + 1) % m], poly[j], poly[(j + 1) % m]):
                return False
    return True


# ---------------------------------------------------------------- direct pairwise face intersection

def pair_intersection_ok(cf, X, Y, polys2d):
    """Directly decide whether F_X cap F_Y == e_XY (parity regions), by sampling L_XY at all
    breakpoints (exact crossings of either polygon's boundary with the other plane) and at
    midpoints between them.  Independent of Sec. 5.2 and of Lemma 5.1."""
    pts = []
    for (A, B) in ((X, Y), (Y, X)):
        poly = cf.polygon(A)
        m = len(poly)
        for i in range(m):
            p, q = poly[i - 1], poly[i]
            fp, fq = cf.f(B, p), cf.f(B, q)
            if fp == 0:
                pts.append(p)
            if fp != 0 and fq != 0 and (fp > 0) != (fq > 0):
                lam = fp / (fp - fq)
                pts.append(tuple(p[k] + lam * (q[k] - p[k]) for k in range(3)))
    # parametrize by t = u . p (u along L_XY); all pts lie on L_XY
    tv = sorted({(cf.t(X, Y, p), p) for p in pts}, key=lambda z: z[0])
    # dedupe equal t
    uniq = []
    for t_, p in tv:
        if not uniq or uniq[-1][0] != t_:
            uniq.append((t_, p))
    C, D = cf.part[(X, Y)]
    tC, tD = cf.t(X, Y, cf.P(X, Y, C)), cf.t(X, Y, cf.P(X, Y, D))
    lo, hi = min(tC, tD), max(tC, tD)
    samples = list(uniq)
    for (t1, p1), (t2, p2) in zip(uniq, uniq[1:]):
        samples.append(((t1 + t2) / 2, tuple((a + b) / 2 for a, b in zip(p1, p2))))
    bad = []
    for t_, p in samples:
        inX, _ = in_face_direct(cf, X, p, polys2d[X])
        inY, _ = in_face_direct(cf, Y, p, polys2d[Y])
        in_e = lo <= t_ <= hi
        if (inX and inY) != in_e:
            bad.append((t_, inX, inY, in_e))
    return not bad, bad


# ---------------------------------------------------------------- random instances

def random_planes(n, rng, R=50, dist="cube"):
    H = []
    for _ in range(n):
        if dist == "cube":
            h = [rng.randint(-R, R) for _ in range(4)]
        elif dist == "tangent":   # planes tangent-ish to a sphere of radius ~R/2: e ~ -|n| R/2
            nrm = [rng.randint(-R, R) for _ in range(3)]
            l1 = sum(abs(x) for x in nrm)
            h = nrm + [-(l1 * rng.randint(R // 3, R // 2)) // max(1, R // 10) + rng.randint(-R, R)]
        elif dist == "small":
            h = [rng.randint(-3, 3) for _ in range(4)]
        else:
            raise ValueError(dist)
        H.append(h)
    return H


def load_k12(path="/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json"):
    import json
    return json.load(open(path))
