"""Exact direct-geometry evaluator for the Track-3 predicates (independent of the chirotope
formulas in omsat.py).  Everything is computed from the planes with Fractions:
vertices, segment membership, point-in-polygon in a 2D chart of the face plane, turns from
3D cross products, embeddedness from pairwise face intersections on the lines L_XY.

Planes: h_X = (a,b,c,e) integers, plane {p : a x + b y + c z + e = 0}.
"""
import itertools
from fractions import Fraction


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def sub(u, v):
    return (u[0] - v[0], u[1] - v[1], u[2] - v[2])


def sgn(x):
    return (x > 0) - (x < 0)


class Geometry:
    def __init__(self, planes, T):
        self.h = [tuple(int(x) for x in p) for p in planes]
        self.T = T
        self.n = len(planes)
        self._P = {}

    def normal(self, X):
        return self.h[X][:3]

    def P(self, a, b, c):
        key = frozenset((a, b, c))
        if key not in self._P:
            M = [self.h[i][:3] for i in (a, b, c)]
            r = [-self.h[i][3] for i in (a, b, c)]
            D = dot(M[0], cross(M[1], M[2]))
            assert D != 0, "parallel planes"
            # Cramer
            cols = list(zip(*M))
            def detc(k):
                cc = [list(col) for col in cols]
                cc[k] = r
                m = list(zip(*cc))
                return dot(m[0], cross(m[1], m[2]))
            self._P[key] = tuple(Fraction(detc(k), D) for k in range(3))
        return self._P[key]

    def value(self, d, p):
        """n_d . p + e_d"""
        return dot(self.h[d][:3], p) + self.h[d][3]

    def side(self, a, b, c, d):
        return sgn(self.value(d, self.P(a, b, c)))

    def u(self, X, Y):
        nx, ny = self.normal(X), self.normal(Y)
        c = cross(nx, ny)
        return (-c[0], -c[1], -c[2])

    def t(self, X, Y, p):
        return dot(self.u(X, Y), p)

    def E(self, X, W, V):
        A, B = self.T.part(X, W)
        if V in (A, B):
            return False
        ta = self.t(X, W, self.P(X, W, A))
        tb = self.t(X, W, self.P(X, W, B))
        tv = self.t(X, W, self.P(X, W, V))
        return min(ta, tb) < tv < max(ta, tb)

    def lt(self, X, Y, Z, W):
        return self.t(X, Y, self.P(X, Y, W)) < self.t(X, Y, self.P(X, Y, Z))

    # --- polygons in 2D charts
    def chart_k(self, X):
        nx = self.normal(X)
        return max(range(3), key=lambda k: abs(nx[k]))

    def to2d(self, X, p):
        k = self.chart_k(X)
        return tuple(p[i] for i in range(3) if i != k)

    def polygon3d(self, X):
        cs = self.T.corners(X)
        return [self.P(X, A, B) for A, B in cs]

    def polygon2d(self, X):
        return [self.to2d(X, p) for p in self.polygon3d(X)]

    @staticmethod
    def on_segment2(p, a, b):
        cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        if cr != 0:
            return False
        return (min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
                min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))

    @staticmethod
    def crossing_parity(p, poly):
        """even-odd rule, horizontal ray to +x; p not on boundary."""
        x, y = p
        c = False
        m = len(poly)
        for i in range(m):
            a, b = poly[i], poly[(i + 1) % m]
            if (a[1] > y) != (b[1] > y):
                xi = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                if xi > x:
                    c = not c
        return c

    def in_closed(self, X, p3):
        """p3 in closed F_X := boundary of polygon X or odd crossing parity."""
        poly = self.polygon2d(X)
        p = self.to2d(X, p3)
        m = len(poly)
        for i in range(m):
            if self.on_segment2(p, poly[i], poly[(i + 1) % m]):
                return True
        return self.crossing_parity(p, poly)

    def IN(self, X, Y, Z):
        return self.in_closed(X, self.P(X, Y, Z))

    def REFLEX(self, X, Y, Z):
        """points of L_XY just beyond P_XYZ, away from e_XY, in F_X (direct)."""
        D = self.T.other_partner(X, Y, Z)
        v = self.P(X, Y, Z)
        w = self.P(X, Y, D)
        tv, tw = self.t(X, Y, v), self.t(X, Y, w)
        sgn_away = -1 if tw > tv else 1
        cands = []
        for W in range(self.n):
            if W in (X, Y, Z):
                continue
            q = self.P(X, Y, W)
            tq = self.t(X, Y, q)
            if (tq - tv) * sgn_away > 0:
                cands.append((abs(tq - tv), q))
        if cands:
            q = min(cands, key=lambda c: c[0])[1]
            mid = tuple((v[i] + q[i]) / 2 for i in range(3))
        else:
            mid = tuple(2 * v[i] - w[i] for i in range(3))
        # mid must not be on the boundary
        poly = self.polygon2d(X)
        p = self.to2d(X, mid)
        m = len(poly)
        assert not any(self.on_segment2(p, poly[i], poly[(i + 1) % m]) for i in range(m))
        return self.crossing_parity(p, poly)

    def RTURN(self, X, A, B):
        Ap = self.T.other_partner(X, A, B)
        Bp = self.T.other_partner(X, B, A)
        pin, v, pout = self.P(X, Ap, A), self.P(X, A, B), self.P(X, B, Bp)
        c = cross(sub(v, pin), sub(pout, v))
        s = dot(self.normal(X), c)
        assert s != 0
        return s < 0

    # --- simplicity, orientation, embeddedness
    @staticmethod
    def seg_intersect2(a, b, c, d):
        def orient(p, q, r):
            return sgn((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))
        o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
        if o1 != o2 and o3 != o4 and 0 not in (o1, o2, o3, o4):
            return True
        on = Geometry.on_segment2
        return ((o1 == 0 and on(c, a, b)) or (o2 == 0 and on(d, a, b)) or
                (o3 == 0 and on(a, c, d)) or (o4 == 0 and on(b, c, d)))

    def simple(self, X):
        poly = self.polygon2d(X)
        m = len(poly)
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                if self.seg_intersect2(poly[i], poly[(i + 1) % m], poly[j], poly[(j + 1) % m]):
                    return False
        return True

    def ccw(self, X):
        """signed area of polygon X w.r.t. n_X positive?"""
        pts = self.polygon3d(X)
        s = (0, 0, 0)
        m = len(pts)
        for i in range(m):
            c = cross(pts[i], pts[(i + 1) % m])
            s = (s[0] + c[0], s[1] + c[1], s[2] + c[2])
        a = dot(self.normal(X), s)
        assert a != 0
        return a > 0

    def line_breaks(self, X, Y):
        """t-values on L_XY of all points where the boundary of F_X or F_Y meets L_XY."""
        ts = set()
        for F, G in ((X, Y), (Y, X)):
            poly = self.polygon3d(F)
            m = len(poly)
            for i in range(m):
                a, b = poly[i], poly[(i + 1) % m]
                va, vb = self.value(G, a), self.value(G, b)
                if va == 0:
                    ts.add(self.t(X, Y, a))
                if vb == 0:
                    ts.add(self.t(X, Y, b))
                if va * vb < 0:
                    lam = va / (va - vb)
                    q = tuple(a[k] + lam * (b[k] - a[k]) for k in range(3))
                    ts.add(self.t(X, Y, q))
        return sorted(ts)

    def point_on_line(self, X, Y, tval):
        """point of L_XY with parameter t (u . p = tval)."""
        # point p0 on the line: solve n_X.p=-eX, n_Y.p=-eY, u.p=tval
        nx, ny, u = self.normal(X), self.normal(Y), self.u(X, Y)
        M = [nx, ny, u]
        r = [-self.h[X][3], -self.h[Y][3], tval]
        D = dot(M[0], cross(M[1], M[2]))
        cols = list(zip(*M))
        out = []
        for k in range(3):
            cc = [list(col) for col in cols]
            cc[k] = r
            m = list(zip(*cc))
            out.append(Fraction(dot(m[0], cross(m[1], m[2])), D))
        return tuple(out)

    def pair_ok(self, X, Y):
        """F_X cap F_Y == e_XY (closed regions; valid as a test when polygons are simple)."""
        C, D = self.T.part(X, Y)
        tc, td = self.t(X, Y, self.P(X, Y, C)), self.t(X, Y, self.P(X, Y, D))
        lo, hi = min(tc, td), max(tc, td)
        br = self.line_breaks(X, Y)
        tests = list(br) + [(br[i] + br[i + 1]) / 2 for i in range(len(br) - 1)]
        for tv in tests:
            p = self.point_on_line(X, Y, tv)
            both = self.in_closed(X, p) and self.in_closed(Y, p)
            if both != (lo <= tv <= hi):
                return False
        return True

    def embedded(self):
        if not all(self.simple(X) for X in range(self.n)):
            return False
        return all(self.pair_ok(X, Y) for X, Y in itertools.combinations(range(self.n), 2))
