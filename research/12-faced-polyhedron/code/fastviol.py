"""Fast floating-point violation counter for face-plane configurations (PI tool).

A configuration is n planes h_X = (a, b, c, e) meaning a x + b y + c z + e = 0, plus a
neighborly triangulation (the dual map). The violation count is the number of non-triangle
triples {X,Y,Z} whose triple point P_XYZ lies in all three closed faces (Lemma 5.1 of
mathematical-model.md). Each polygon self-crossing and each edge-face intersection is one such
triple, so the count is comparable to "crossings + intersections" of other searches.

The in-face test is the line-parity predicate of mathematical-model.md section 5.2. Floating
point only: candidates must be re-verified in exact arithmetic.
"""
import itertools
import numpy as np
from numba import njit


def triangulation_tables(n, triangles):
    """partner[X, W] = (A, B): the two third vertices of the triangles containing edge XW."""
    partner = -np.ones((n, n, 2), dtype=np.int64)
    istri = np.zeros((n, n, n), dtype=np.bool_)
    for t in triangles:
        for X, W, A in itertools.permutations(t):
            istri[X, W, A] = True
            if partner[X, W, 0] < 0:
                partner[X, W, 0] = A
            elif partner[X, W, 0] != A:
                partner[X, W, 1] = A
    assert (partner >= 0).sum() == n * (n - 1) * 2, "not neighborly"
    return partner, istri


def links(n, triangles):
    """Cyclic order of neighbours around each vertex of the triangulation."""
    partner, _ = triangulation_tables(n, triangles)
    out = []
    for X in range(n):
        W0 = (X + 1) % n
        cyc = [W0, int(partner[X, W0, 0])]
        while len(cyc) < n - 1:
            a, b = partner[X, cyc[-1]]
            cyc.append(int(a) if a != cyc[-2] else int(b))
        assert len(set(cyc)) == n - 1
        out.append(cyc)
    return out


@njit(cache=True)
def _triple_points(H):
    n = H.shape[0]
    P = np.zeros((n, n, n, 3))
    ok = True
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                M = np.empty((3, 3))
                r = np.empty(3)
                for i, X in enumerate((a, b, c)):
                    M[i, 0] = H[X, 0]; M[i, 1] = H[X, 1]; M[i, 2] = H[X, 2]
                    r[i] = -H[X, 3]
                det = np.linalg.det(M)
                if abs(det) < 1e-300:
                    ok = False
                    continue
                p = np.linalg.solve(M, r)
                for (x, y, z) in ((a, b, c), (a, c, b), (b, a, c), (b, c, a), (c, a, b), (c, b, a)):
                    P[x, y, z, 0] = p[0]; P[x, y, z, 1] = p[1]; P[x, y, z, 2] = p[2]
    return P, ok


@njit(cache=True)
def _side(H, P, a, b, c, d):
    v = H[d, 0] * P[a, b, c, 0] + H[d, 1] * P[a, b, c, 1] + H[d, 2] * P[a, b, c, 2] + H[d, 3]
    return v > 0


@njit(cache=True)
def _inface(H, P, partner, X, Y, Z):
    """Is P_XYZ in the closed face X? Parity along the line L_XY (section 5.2)."""
    n = H.shape[0]
    C = partner[X, Y, 0]
    D = partner[X, Y, 1]
    # boundary: R in relint e_XY
    if _side(H, P, X, Y, C, Z) != _side(H, P, X, Y, D, Z):
        return True
    # boundary: R in relint e_XZ
    A = partner[X, Z, 0]
    B = partner[X, Z, 1]
    if _side(H, P, X, Z, A, Y) != _side(H, P, X, Z, B, Y):
        return True
    ux = H[X, 1] * H[Y, 2] - H[X, 2] * H[Y, 1]
    uy = H[X, 2] * H[Y, 0] - H[X, 0] * H[Y, 2]
    uz = H[X, 0] * H[Y, 1] - H[X, 1] * H[Y, 0]
    tz = P[X, Y, Z, 0] * ux + P[X, Y, Z, 1] * uy + P[X, Y, Z, 2] * uz
    cnt = 0
    for W in range(n):
        if W == X or W == Y or W == Z or W == C or W == D:
            continue
        tw = P[X, Y, W, 0] * ux + P[X, Y, W, 1] * uy + P[X, Y, W, 2] * uz
        if tw > tz:
            A = partner[X, W, 0]
            B = partner[X, W, 1]
            if _side(H, P, X, W, A, Y) != _side(H, P, X, W, B, Y):
                cnt += 1
    tc = P[X, Y, C, 0] * ux + P[X, Y, C, 1] * uy + P[X, Y, C, 2] * uz
    if tc > tz:
        Cp = partner[X, C, 0] if partner[X, C, 0] != Y else partner[X, C, 1]
        Dp = partner[X, D, 0] if partner[X, D, 0] != Y else partner[X, D, 1]
        if _side(H, P, X, C, Cp, Y) != _side(H, P, X, D, Dp, Y):
            cnt += 1
    return (cnt & 1) == 1


@njit(cache=True)
def violations(H, partner, istri):
    """Number of non-triangle triples whose point lies in all three closed faces."""
    n = H.shape[0]
    P, ok = _triple_points(H)
    if not ok:
        return 10 ** 6
    v = 0
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if istri[a, b, c]:
                    continue
                if _inface(H, P, partner, a, b, c) and _inface(H, P, partner, b, c, a) \
                        and _inface(H, P, partner, c, a, b):
                    v += 1
    return v


@njit(cache=True)
def violation_list(H, partner, istri):
    n = H.shape[0]
    P, ok = _triple_points(H)
    out = []
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if istri[a, b, c]:
                    continue
                if _inface(H, P, partner, a, b, c) and _inface(H, P, partner, b, c, a) \
                        and _inface(H, P, partner, c, a, b):
                    out.append((a, b, c))
    return out
