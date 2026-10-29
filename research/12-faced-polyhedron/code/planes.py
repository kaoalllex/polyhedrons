"""Exact geometry for the face-plane formulation (Track 4, geometry-first SAT).

Planes are integer 4-vectors h = (a, b, c, -d) meaning a x + b y + c z = d, i.e. h . (x,y,z,1) = 0.
All predicates below are exact (Python ints / fractions.Fraction).

Contents
  Arrangement      : n planes; exact triple points, side bits, order of points along lines, general position
  check_embedding  : DIRECT exact embedding checker for a triangulation (independent of Lemma 5.1 encodings):
                     face polygons from link cycles, exact simplicity test, exact even-odd point-in-polygon
                     tests for all triples, and a direct test F_X cap F_Y == e_XY for every pair of faces.
  generators for random arrangements.
"""
from fractions import Fraction
from itertools import combinations
import math
import random


# ---------------------------------------------------------------- small exact linear algebra
def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def sgn(x):
    return (x > 0) - (x < 0)


def det4(r0, r1, r2, r3):
    tot = 0
    rows = (r0, r1, r2, r3)
    for m in range(4):
        cols = [c for c in range(4) if c != m]
        minor = det3([r1[c] for c in cols], [r2[c] for c in cols], [r3[c] for c in cols])
        tot += (-1) ** m * r0[m] * minor
    return tot


class DegenerateArrangement(Exception):
    pass


class Arrangement:
    """n planes with exact derived data (cached)."""

    def __init__(self, H):
        self.H = [tuple(int(x) for x in h) for h in H]
        self.n = len(self.H)
        self._tp = {}
        self._ord = {}
        self._side = {}

    # triple point as homogeneous integer vector (p0,p1,p2,p3), p3 > 0, so the point is (p0,p1,p2)/p3
    def tp(self, i, j, k):
        key = tuple(sorted((i, j, k)))
        r = self._tp.get(key)
        if r is None:
            a, b, c = (self.H[x] for x in key)
            p = []
            for m in range(4):
                cols = [q for q in range(4) if q != m]
                mm = det3([a[q] for q in cols], [b[q] for q in cols], [c[q] for q in cols])
                p.append(mm if m % 2 == 0 else -mm)
            if p[3] < 0:
                p = [-x for x in p]
            if p[3] == 0:
                raise DegenerateArrangement("triple point at infinity %s" % (key,))
            g = math.gcd(math.gcd(p[0], p[1]), math.gcd(p[2], p[3]))
            p = tuple(x // g for x in p)
            r = self._tp[key] = p
        return r

    def pt(self, i, j, k):
        p = self.tp(i, j, k)
        return (Fraction(p[0], p[3]), Fraction(p[1], p[3]), Fraction(p[2], p[3]))

    def side(self, i, j, k, d):
        """sign of n_d . P_ijk - d_d  (P_ijk on which side of plane d); +1 / -1; raises if 0 (non general)."""
        key = (tuple(sorted((i, j, k))), d)
        r = self._side.get(key)
        if r is None:
            s = sgn(dot(self.H[d], self.tp(i, j, k)))
            if s == 0:
                raise DegenerateArrangement("4 planes concurrent %s %s" % key)
            r = self._side[key] = s
        return r

    def line_dir(self, x, y):
        """direction of L_xy for x<y: n_x cross n_y"""
        assert x < y
        return cross(self.H[x][:3], self.H[y][:3])

    def line_param(self, x, y, w):
        """exact parameter s of P_xyw along L_xy (x<y): s = (n_x cross n_y) . P  (Fraction)"""
        if x > y:
            x, y = y, x
        u = self.line_dir(x, y)
        p = self.tp(x, y, w)
        return Fraction(dot(u, p[:3]), p[3])

    def line_order(self, x, y):
        """list of w (w != x,y) sorted by increasing parameter along L_xy (canonical direction, x<y)."""
        if x > y:
            x, y = y, x
        r = self._ord.get((x, y))
        if r is None:
            ws = [w for w in range(self.n) if w != x and w != y]
            keyed = [(self.line_param(x, y, w), w) for w in ws]
            keyed.sort()
            for a, b in zip(keyed, keyed[1:]):
                if a[0] == b[0]:
                    raise DegenerateArrangement("coincident triple points on line %d %d" % (x, y))
            r = self._ord[(x, y)] = [w for _, w in keyed]
        return r

    def check_general_position(self):
        """True iff all 4x4 determinants among the n planes and the plane at infinity are nonzero."""
        try:
            for t in combinations(range(self.n), 3):
                self.tp(*t)
                for d in range(self.n):
                    if d not in t:
                        self.side(*t, d)
            for x, y in combinations(range(self.n), 2):
                self.line_order(x, y)
        except DegenerateArrangement:
            return False
        return True

    def check_general_position_dets(self):
        """independent check: all 4x4 determinants among h_1..h_n, h_inf=(0,0,0,1) nonzero."""
        vecs = list(self.H) + [(0, 0, 0, 1)]
        for t in combinations(range(len(vecs)), 4):
            if det4(*(vecs[i] for i in t)) == 0:
                return False
        return True

    # ---- 2D charts
    def chart_axes(self, x):
        nx = self.H[x][:3]
        k = max(range(3), key=lambda m: abs(nx[m]))
        assert nx[k] != 0
        return tuple(m for m in range(3) if m != k)

    def to2d(self, x, q):
        ax = self.chart_axes(x)
        return (q[ax[0]], q[ax[1]])


# ---------------------------------------------------------------- triangulation helpers
def link_cycle(tris, X, n):
    """cyclic order of the neighbours of X in the link, or None if not a single (n-1)-cycle."""
    adj = {}
    for t in tris:
        if X in t:
            y, z = [v for v in t if v != X]
            adj.setdefault(y, []).append(z)
            adj.setdefault(z, []).append(y)
    if len(adj) != n - 1 or any(len(v) != 2 for v in adj.values()):
        return None
    start = min(adj)
    cyc = [start]
    prev, cur = start, adj[start][0]
    while cur != start:
        cyc.append(cur)
        if len(cyc) > n:
            return None
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        prev, cur = cur, nxt
    if len(cyc) != n - 1:
        return None
    return cyc


def valid_triangulation(tris, n):
    """combinatorial sanity: every pair in exactly 2 triangles, all links single (n-1)-cycles"""
    cnt = {}
    for t in tris:
        for a, b in combinations(sorted(t), 2):
            cnt[(a, b)] = cnt.get((a, b), 0) + 1
    if len(cnt) != n * (n - 1) // 2 or any(v != 2 for v in cnt.values()):
        return False
    return all(link_cycle(tris, X, n) is not None for X in range(n))


# ---------------------------------------------------------------- exact 2D predicates
def orient(a, b, c):
    return sgn((b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]))


def on_segment(a, b, p):
    if orient(a, b, p) != 0:
        return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def segments_intersect(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(a, b, c):
        return True
    if o2 == 0 and on_segment(a, b, d):
        return True
    if o3 == 0 and on_segment(c, d, a):
        return True
    if o4 == 0 and on_segment(c, d, b):
        return True
    return False


def polygon_simple(poly):
    m = len(poly)
    if len(set(poly)) != m:
        return False
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        for j in range(i + 1, m):
            c, d = poly[j], poly[(j + 1) % m]
            if j == i + 1 or (i == 0 and j == m - 1):
                # adjacent edges: must share only the common vertex (no collinear fold-back)
                if j == i + 1:
                    s, o1, o2 = b, a, d
                else:
                    s, o1, o2 = a, b, c
                if orient(o1, s, o2) == 0:
                    # collinear: overlap iff both go in the same direction from s
                    if (o1[0] - s[0]) * (o2[0] - s[0]) + (o1[1] - s[1]) * (o2[1] - s[1]) > 0:
                        return False
                continue
            if segments_intersect(a, b, c, d):
                return False
    return True


def point_in_polygon(poly, q):
    """even-odd rule, boundary counted as inside. exact."""
    m = len(poly)
    for i in range(m):
        if on_segment(poly[i], poly[(i + 1) % m], q):
            return True
    inside = False
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        if (a[1] > q[1]) != (b[1] > q[1]):
            # x coordinate of crossing at y = q[1]
            xc = a[0] + (q[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if xc > q[0]:
                inside = not inside
    return inside


# ---------------------------------------------------------------- DIRECT embedding checker
def face_polygons(arr, tris):
    """for each face X the 2D (chart) polygon of corners P_{X,B_i,B_{i+1}} (Fractions) plus the link order"""
    n = arr.n
    polys, links = [], []
    for X in range(n):
        B = link_cycle(tris, X, n)
        if B is None:
            raise ValueError("not a valid triangulation at %d" % X)
        links.append(B)
        poly = []
        for i in range(n - 1):
            p3 = arr.pt(X, B[i], B[(i + 1) % (n - 1)])
            poly.append(arr.to2d(X, p3))
        polys.append(poly)
    return polys, links


def check_embedding(arr, tris, do_pairs=True):
    """DIRECT exact embedding check.  Returns dict:
        simple[X]      polygon of face X simple
        in_direct      dict (X,(Y,Z)) -> bool  exact even-odd PIP of P_XYZ in polygon X (all 3*C(n,3))
        viol_triples   non-triangle triples with P in all three faces (direct PIP)
        bad_pairs      pairs {X,Y} with F_X cap F_Y != e_XY (direct line test)
        ok_triples     all polygons simple and no violated triple   (Lemma 5.1 criterion, direct predicates)
        ok_pairs       all polygons simple and no bad pair          (independent criterion)
    """
    n = arr.n
    tset = set(tuple(sorted(t)) for t in tris)
    polys, links = face_polygons(arr, tris)
    simple = [polygon_simple(p) for p in polys]
    in_direct = {}
    for X in range(n):
        for Y, Z in combinations([v for v in range(n) if v != X], 2):
            q = arr.to2d(X, arr.pt(X, Y, Z))
            in_direct[(X, (Y, Z))] = point_in_polygon(polys[X], q)
    viol = []
    for T in combinations(range(n), 3):
        if T in tset:
            continue
        a, b, c = T
        if in_direct[(a, (b, c))] and in_direct[(b, (a, c))] and in_direct[(c, (a, b))]:
            viol.append(T)
    bad_pairs = []
    if do_pairs:
        for X, Y in combinations(range(n), 2):
            if not pair_ok(arr, tris, polys, links, X, Y):
                bad_pairs.append((X, Y))
    return dict(simple=simple, in_direct=in_direct, viol_triples=viol, bad_pairs=bad_pairs,
                ok_triples=all(simple) and not viol,
                ok_pairs=all(simple) and not bad_pairs)


def pair_ok(arr, tris, polys, links, X, Y):
    """direct test F_X cap F_Y == e_XY along L_XY (exact, via critical parameters + midpoints)."""
    n = arr.n
    partners = [w for w in range(n) if w not in (X, Y) and tuple(sorted((X, Y, w))) in
                set(tuple(sorted(t)) for t in tris)]
    assert len(partners) == 2
    x, y = min(X, Y), max(X, Y)
    u = arr.line_dir(x, y)
    uu = Fraction(dot(u, u))
    ws = arr.line_order(x, y)
    svals = [arr.line_param(x, y, w) for w in ws]
    b = arr.pt(x, y, ws[0])
    s0 = svals[0]

    def point(s):
        f = (s - s0) / uu
        return (b[0] + f * u[0], b[1] + f * u[1], b[2] + f * u[2])

    sC = sorted(arr.line_param(x, y, w) for w in partners)
    tests = [svals[0] - 1, svals[-1] + 1]
    tests += svals
    tests += [(a + c) / 2 for a, c in zip(svals, svals[1:])]
    for s in tests:
        q = point(s)
        inX = point_in_polygon(polys[X], arr.to2d(X, q))
        inY = point_in_polygon(polys[Y], arr.to2d(Y, q))
        expected = sC[0] <= s <= sC[1]
        if (inX and inY) != expected:
            return False
    return True


# ---------------------------------------------------------------- Szilassi / generic polyhedron -> planes
def planes_from_polyhedron(verts, faces):
    """verts: list of Fraction triples; faces: lists of 0-based vertex indices.
    Returns integer plane vectors (a,b,c,-d), normalised so that the polyhedron centroid has a x+b y+c z-d < 0 (not
    required; sign irrelevant for the SAT)."""
    H = []
    for f in faces:
        p0 = verts[f[0]]
        normal = None
        for i in range(1, len(f)):
            for j in range(i + 1, len(f)):
                nrm = cross([verts[f[i]][m] - p0[m] for m in range(3)], [verts[f[j]][m] - p0[m] for m in range(3)])
                if any(c != 0 for c in nrm):
                    normal = nrm
                    break
            if normal:
                break
        den = 1
        for c in normal:
            den = den * Fraction(c).denominator // math.gcd(den, Fraction(c).denominator)
        ni = [int(Fraction(c) * den) for c in normal]
        g = math.gcd(math.gcd(ni[0], ni[1]), ni[2])
        ni = [c // g for c in ni]
        d = sum(Fraction(ni[m]) * p0[m] for m in range(3))
        dd = Fraction(d)
        den2 = dd.denominator
        ni = [c * den2 for c in ni]
        d = int(dd * den2)
        g = math.gcd(math.gcd(math.gcd(ni[0], ni[1]), ni[2]), abs(d))
        ni = [c // g for c in ni]
        d //= g
        for v in f:
            assert sum(Fraction(ni[m]) * verts[v][m] for m in range(3)) == d, "face not planar"
        H.append((ni[0], ni[1], ni[2], -d))
    return H


# ---------------------------------------------------------------- random arrangements
def _unit(rng):
    while True:
        v = [rng.gauss(0, 1) for _ in range(3)]
        r = math.sqrt(sum(x * x for x in v))
        if r > 1e-6:
            return [x / r for x in v]


def random_planes(n, dist, rng, scale=10 ** 4, max_tries=50):
    """integer plane vectors for a random arrangement, general position guaranteed (retry)."""
    for _ in range(max_tries):
        H = []
        for _i in range(n):
            if dist == "sphere_unif":      # isotropic normal, offset uniform in [-1,1]
                nv = _unit(rng); d = rng.uniform(-1, 1)
            elif dist == "tangent":        # tangent to the unit sphere
                nv = _unit(rng); d = 1.0
            elif dist == "near_tangent":   # distance from origin in [0.5,1]
                nv = _unit(rng); d = rng.uniform(0.5, 1.0)
            elif dist == "gauss":          # Gaussian normal and offset
                nv = [rng.gauss(0, 1) for _ in range(3)]; d = rng.gauss(0, 1)
            elif dist == "pts3":           # plane through 3 Gaussian points
                P = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)]
                u = [P[1][m] - P[0][m] for m in range(3)]
                w = [P[2][m] - P[0][m] for m in range(3)]
                nv = list(cross(u, w))
                r = math.sqrt(sum(x * x for x in nv))
                nv = [x / r for x in nv]
                d = sum(nv[m] * P[0][m] for m in range(3))
            elif dist == "small_off":      # offsets small: planes nearly through a common point
                nv = _unit(rng); d = rng.uniform(-0.3, 0.3)
            else:
                raise ValueError(dist)
            H.append((round(nv[0] * scale), round(nv[1] * scale), round(nv[2] * scale), -round(d * scale)))
        arr = Arrangement(H)
        if arr.check_general_position():
            return arr
    raise RuntimeError("no general position arrangement found")


def perturb(H, rel, rng, scale_to=10 ** 6):
    """scale planes to ~scale_to magnitude and add random integer noise of relative size rel (uniform ints)."""
    out = []
    for h in H:
        m = max(abs(x) for x in h[:3])
        f = scale_to / m
        hh = [round(x * f) for x in h]
        amp = max(1, round(rel * scale_to))
        out.append(tuple(x + rng.randint(-amp, amp) for x in hh))
    return out


# ---------------------------------------------------------------- violation profile (comparable to edge-face / self-crossing counts)
def violation_profile(arr, tris):
    """Classify each violated non-triangle triple {X,Y,Z} (P_XYZ in F_X, F_Y, F_Z, direct exact predicates) by the
    number k of the three edges e_XY, e_XZ, e_YZ that pass through P in their relative interior:
        k=0 : V0  face-face-face interior point (no edge involved)
        k=1 : V1  one edge pierces the interior of the third face            -> 1 edge-face intersection
        k=2 : V2  two edges of one polygon cross in its plane               -> 1 polygon self-crossing
        k=3 : V3  three edges concurrent at P                               -> 3 self-crossings (one per face)
    Returns dict(V, V0..V3, SC=V2+3*V3, EF=V1, B=SC+EF+V0)."""
    n = arr.n
    tset = set(tuple(sorted(t)) for t in tris)
    res = check_embedding(arr, tris, do_pairs=False)
    ind = res["in_direct"]
    partners = {}
    for t in tset:
        for a, b in combinations(t, 2):
            c = [v for v in t if v != a and v != b][0]
            partners.setdefault((a, b), []).append(c)

    def on_edge(x, y, z):   # P_xyz in relint of edge e_xy
        s = sorted(partners[(min(x, y), max(x, y))], key=lambda w: arr.line_param(x, y, w))
        sz = arr.line_param(x, y, z)
        return arr.line_param(x, y, s[0]) < sz < arr.line_param(x, y, s[1])

    V = [0, 0, 0, 0]
    for T in res["viol_triples"]:
        x, y, z = T
        k = int(on_edge(x, y, z)) + int(on_edge(x, z, y)) + int(on_edge(y, z, x))
        V[k] += 1
    nv = sum(V)
    return dict(V=nv, V0=V[0], V1=V[1], V2=V[2], V3=V[3], SC=V[2] + 3 * V[3], EF=V[1], B=V[0] + V[1] + V[2] + 3 * V[3],
                nonsimple_faces=sum(1 for s in res["simple"] if not s))
