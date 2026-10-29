"""Local (immersion) violations of a face-plane configuration (float, numpy).

immersion violations = (pairs of non-adjacent crossing edges inside a face)
                     + (vertices with two or more reflex corners)
plus the Gauss-map degree in the configuration's own gauge (must be -5 for an immersion).
A configuration with zero immersion violations is a polyhedral immersion (locally injective).
"""
import numpy as np


def polygons(H, links):
    n = len(H)
    polys = []
    for X in range(n):
        cyc = links[X]
        pts = []
        for i in range(len(cyc)):
            A, B = cyc[i], cyc[(i + 1) % len(cyc)]
            M = H[[X, A, B], :3]
            pts.append(np.linalg.solve(M, -H[[X, A, B], 3]))
        polys.append(np.array(pts))
    return polys


def _to2d(P, nrm):
    k = int(np.argmax(np.abs(nrm)))
    keep = [i for i in range(3) if i != k]
    Q = P[:, keep]
    if nrm[k] < 0:                      # keep orientation as seen from +nrm
        Q = Q[:, ::-1]
    return Q


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def local_violations(H, links):
    """Returns (crossings, multi_reflex_vertices, reflex_by_corner dict)."""
    n = len(H)
    polys = polygons(H, links)
    crossings = 0
    reflex = {}
    for X in range(n):
        Q = _to2d(polys[X], H[X, :3])
        m = len(Q)
        area = 0.5 * sum(Q[i][0] * Q[(i + 1) % m][1] - Q[(i + 1) % m][0] * Q[i][1] for i in range(m))
        o = 1.0 if area > 0 else -1.0
        for i in range(m):
            for j in range(i + 2, m):
                if i == 0 and j == m - 1:
                    continue
                a, b, c, d = Q[i], Q[(i + 1) % m], Q[j], Q[(j + 1) % m]
                if (_cross(a, b, c) * _cross(a, b, d) < 0) and (_cross(c, d, a) * _cross(c, d, b) < 0):
                    crossings += 1
        cyc = links[X]
        for i in range(m):           # corner at vertex i = P(X, cyc[i], cyc[i+1])
            prv, cur, nxt = Q[i - 1], Q[i], Q[(i + 1) % m]
            turn = _cross(prv, cur, nxt) * o
            key = frozenset((X, cyc[i], cyc[(i + 1) % m]))
            reflex.setdefault(key, 0)
            if turn < 0:
                reflex[key] += 1
    multi = sum(1 for v in reflex.values() if v >= 2)
    return crossings, multi, reflex
