"""Exact single-plane relocation (PI tool).

With the other n-1 planes fixed, every sign that the violation count depends on is the sign of
a linear function of the moving plane h_k in R^4: h_k . P_abc for the fixed triple points P_abc
(a, b, c != k), and h_k . (n_a x n_b, 0) for the fixed line directions (this is the sign of
chi(a, b, k, inf)). So the violation count is constant on the cells of an arrangement of
C(n-1,3) + C(n-1,2) hyperplanes through the origin of R^4 (220 for n = 12). Every cell has a
vertex (intersection of three of the hyperplanes); probing the 8 cells around every vertex
visits every cell of the (simple) arrangement, so the minimum over all positions of plane k is
found exactly, up to floating-point robustness of the probes.

The winning cell is then re-centred by an LP (maximize the minimum normalized margin).
"""
import itertools
import numpy as np
from numba import njit, prange
from scipy.optimize import linprog

from fastviol import _inface, triangulation_tables


@njit(cache=True)
def _solve3(H, a, b, c, out):
    m00, m01, m02 = H[a, 0], H[a, 1], H[a, 2]
    m10, m11, m12 = H[b, 0], H[b, 1], H[b, 2]
    m20, m21, m22 = H[c, 0], H[c, 1], H[c, 2]
    det = m00 * (m11 * m22 - m12 * m21) - m01 * (m10 * m22 - m12 * m20) + m02 * (m10 * m21 - m11 * m20)
    if abs(det) < 1e-14:
        return False
    r0, r1, r2 = -H[a, 3], -H[b, 3], -H[c, 3]
    out[0] = (r0 * (m11 * m22 - m12 * m21) - m01 * (r1 * m22 - m12 * r2) + m02 * (r1 * m21 - m11 * r2)) / det
    out[1] = (m00 * (r1 * m22 - m12 * r2) - r0 * (m10 * m22 - m12 * m20) + m02 * (m10 * r2 - r1 * m20)) / det
    out[2] = (m00 * (m11 * r2 - r1 * m21) - m01 * (m10 * r2 - r1 * m20) + r0 * (m10 * m21 - m11 * m20)) / det
    return True


@njit(cache=True)
def _fill_k(H, P, k):
    """Recompute the triple points that involve plane k. Returns False if degenerate."""
    n = H.shape[0]
    p = np.empty(3)
    for a in range(n):
        if a == k:
            continue
        for b in range(a + 1, n):
            if b == k:
                continue
            if not _solve3(H, a, b, k, p):
                return False
            for (x, y, z) in ((a, b, k), (a, k, b), (b, a, k), (b, k, a), (k, a, b), (k, b, a)):
                P[x, y, z, 0] = p[0]; P[x, y, z, 1] = p[1]; P[x, y, z, 2] = p[2]
    return True


@njit(cache=True)
def _count(H, P, partner, istri, cap):
    n = H.shape[0]
    v = 0
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                if istri[a, b, c]:
                    continue
                if _inface(H, P, partner, a, b, c) and _inface(H, P, partner, b, c, a) \
                        and _inface(H, P, partner, c, a, b):
                    v += 1
                    if v >= cap:
                        return v
    return v


@njit(cache=True)
def _cross4(a, b, c):
    """A vector orthogonal to a, b, c in R^4 (generalized cross product)."""
    out = np.empty(4)
    M = np.empty((3, 4))
    M[0] = a; M[1] = b; M[2] = c
    for i in range(4):
        cols = [j for j in range(4) if j != i]
        m = np.empty((3, 3))
        for r in range(3):
            for s in range(3):
                m[r, s] = M[r, cols[s]]
        out[i] = (-1) ** i * np.linalg.det(m)
    return out


@njit(parallel=True, cache=True)
def _scan(H0, P0, k, N, partner, istri, eps, stride, offset, cap0):
    """Probe 8 cells around every stride-th vertex of the arrangement N (rows = hyperplane normals)."""
    m = N.shape[0]
    tri = []
    for i in range(m):
        for j in range(i + 1, m):
            for l in range(j + 1, m):
                tri.append((i, j, l))
    T = len(tri)
    idx = np.arange(offset, T, stride)
    best = np.full(idx.shape[0], cap0, dtype=np.int64)
    besth = np.zeros((idx.shape[0], 4))
    for t in prange(idx.shape[0]):
        i, j, l = tri[idx[t]]
        v = _cross4(N[i], N[j], N[l])
        nv = np.sqrt((v * v).sum())
        if nv < 1e-12:
            continue
        v = v / nv
        A = np.empty((3, 4))
        A[0] = N[i]; A[1] = N[j]; A[2] = N[l]
        G = A @ A.T
        if abs(np.linalg.det(G)) < 1e-18:
            continue
        W = A.T @ np.linalg.inv(G)          # columns: dual basis, A @ W = I
        H = H0.copy()
        P = P0.copy()
        bt = cap0
        for s in range(8):
            h = v.copy()
            for q in range(3):
                sg = 1.0 if (s >> q) & 1 else -1.0
                h += eps * sg * W[:, q]
            nh = np.sqrt(h[0] ** 2 + h[1] ** 2 + h[2] ** 2)
            if nh < 1e-9:
                continue
            for q in range(4):
                H[k, q] = h[q] / nh
            if not _fill_k(H, P, k):
                continue
            c = _count(H, P, partner, istri, bt)
            if c < bt:
                bt = c
                for q in range(4):
                    besth[t, q] = H[k, q]
        best[t] = bt
    return best, besth


def hyperplanes_for(H, k):
    """Normals (in h-space) of the arrangement governing plane k."""
    n = len(H)
    others = [x for x in range(n) if x != k]
    rows = []
    for a, b, c in itertools.combinations(others, 3):
        M = H[[a, b, c], :3]
        p = np.linalg.solve(M, -H[[a, b, c], 3])
        rows.append([p[0], p[1], p[2], 1.0])
    for a, b in itertools.combinations(others, 2):
        d = np.cross(H[a, :3], H[b, :3])
        rows.append([d[0], d[1], d[2], 0.0])
    N = np.array(rows)
    return N / np.linalg.norm(N, axis=1)[:, None]


def center_in_cell(N, h):
    """Chebyshev-type centring: maximize t s.t. s_i N_i . x >= t, |x|_inf <= 1, with s_i = sign(N_i . h)."""
    s = np.sign(N @ h)
    A = -(s[:, None] * N)
    A = np.hstack([A, np.ones((len(N), 1))])
    res = linprog(c=[0, 0, 0, 0, -1], A_ub=A, b_ub=np.zeros(len(N)),
                  bounds=[(-1, 1)] * 4 + [(0, None)], method='highs')
    if res.status != 0 or res.x[4] <= 0:
        return h, 0.0
    x = res.x[:4]
    return x / np.linalg.norm(x[:3]), float(res.x[4])


def all_triple_points(H):
    n = len(H)
    P = np.zeros((n, n, n, 3))
    for a, b, c in itertools.combinations(range(n), 3):
        p = np.linalg.solve(H[[a, b, c], :3], -H[[a, b, c], 3])
        for x, y, z in itertools.permutations((a, b, c)):
            P[x, y, z] = p
    return P


def relocate(H, partner, istri, k, eps=1e-6, stride=1, offset=0, cap=10 ** 6):
    """Best position of plane k (others fixed). Returns (count, new_plane, margin)."""
    N = hyperplanes_for(H, k)
    P = all_triple_points(H)
    best, besth = _scan(H.copy(), P, k, N, partner, istri, eps, stride, offset, cap)
    i = int(np.argmin(best))
    h = besth[i]
    hc, margin = center_in_cell(N, h)
    return int(best[i]), h, hc, margin
