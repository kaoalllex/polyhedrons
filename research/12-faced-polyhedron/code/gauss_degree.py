"""Gauss-map degree prefilter on face normals (Track 6, families F7/F8).

For an embedded (or immersed) closed oriented polyhedral surface, smoothing gives a Gauss map of
degree chi/2. In the polyhedral picture it is the PL map from the dual triangulation to S^2
sending face X to its outward unit normal and each vertex (triangle XYZ, oriented) to the
spherical triangle of the three normals (edges map to short arcs: exterior dihedral angles lie
in (-pi, pi)). So for every generic direction u

    sum over triangles T=(X,Y,Z) with u in cone(g_X,g_Y,g_Z) of sign det(g_X,g_Y,g_Z) = chi/2 = -5

where g_X = eps_X n_X is the "gauge" normal (face X's polygon, traversed in the coherent link
order, is counter-clockwise about g_X; this is the outward normal or, for the reversed surface
orientation, the inward one, and the formula holds in both conventions). Moreover every direction u
is covered by at least one POSITIVE triangle (a convex corner: the vertex maximizing <u, x>).

Given only the face planes' normals as lines (signs unknown), a realization needs some eps in
{+-1}^12 with degree -5 and covering. NOTE: the global flip eps -> -eps NEGATES every triangle
sign and maps u -> -u, so it negates the degree; all 2^12 sign vectors must be searched.
All arithmetic is exact (integer normals, integer test directions).
"""
import itertools
import random

import numpy as np


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def coherent_triangles(tris):
    """Orient the triangles of a closed orientable surface coherently (BFS over edges)."""
    tris = [tuple(t) for t in tris]
    edge_tris = {}
    for i, t in enumerate(tris):
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            edge_tris.setdefault(frozenset((a, b)), []).append(i)
    out = [None] * len(tris)
    out[0] = tris[0]
    stack = [0]
    while stack:
        i = stack.pop()
        a, b, c = out[i]
        for x, y in ((a, b), (b, c), (c, a)):
            for j in edge_tris[frozenset((x, y))]:
                if out[j] is None:
                    t = tris[j]
                    z = [v for v in t if v not in (x, y)][0]
                    out[j] = (y, x, z)            # neighbour must traverse the shared edge as y -> x
                    stack.append(j)
    assert all(o is not None for o in out)
    # check coherence
    seen = set()
    for a, b, c in out:
        for e in ((a, b), (b, c), (c, a)):
            assert e not in seen, 'not orientable'
            seen.add(e)
    return out


def links_from(otris, n):
    """Cyclic link of each vertex consistent with the oriented triangles: (X, B_i, B_{i+1})."""
    succ = {X: {} for X in range(n)}
    for a, b, c in otris:
        succ[a][b] = c
        succ[b][c] = a
        succ[c][a] = b
    links = {}
    for X in range(n):
        s = succ[X]
        start = min(s)
        cyc = [start]
        while s[cyc[-1]] != start:
            cyc.append(s[cyc[-1]])
            assert len(cyc) <= len(s), 'link is not a single cycle'
        assert len(cyc) == len(s), 'link is not a single cycle'
        links[X] = cyc
    return links


def tri_signs(G, otris):
    return [det3(G[a], G[b], G[c]) for a, b, c in otris]


def degree_at(G, otris, u, dets=None):
    if dets is None:
        dets = tri_signs(G, otris)
    D = 0
    for (a, b, c), d in zip(otris, dets):
        s = 1 if d > 0 else -1
        if (det3(u, G[b], G[c]) * s > 0 and det3(G[a], u, G[c]) * s > 0 and det3(G[a], G[b], u) * s > 0):
            D += s
    return D


def covered_positive(G, otris, u, dets):
    for (a, b, c), d in zip(otris, dets):
        if d > 0 and det3(u, G[b], G[c]) > 0 and det3(G[a], u, G[c]) > 0 and det3(G[a], G[b], u) > 0:
            return True
    return False


def admissible_gauges(N, otris, target=-5, n_cover=64, seed=0):
    """All eps in {+-1}^n with degree == target at a generic direction and positive covering
    at n_cover random directions plus the 6 axis-ish directions. N: integer normals."""
    n = len(N)
    rng = random.Random(seed)
    U = [[rng.randint(-10 ** 6, 10 ** 6) for _ in range(3)] for _ in range(n_cover)]
    u0 = [rng.randint(-10 ** 6, 10 ** 6) for _ in range(3)]
    out = []
    for eps in itertools.product((1, -1), repeat=n):
        G = [[e * x for x in v] for e, v in zip(eps, N)]
        dets = tri_signs(G, otris)
        if any(d == 0 for d in dets):
            continue
        if degree_at(G, otris, u0, dets) != target:
            continue
        if all(covered_positive(G, otris, u, dets) for u in U):
            out.append(eps)
    return out


def polygon_gauge(H, links, X):
    """eps_X of a concrete configuration: +1 if face X's polygon (link order) has positive signed
    area about the plane normal n_X (float; for non-simple polygons this is the area sign)."""
    n = len(H)
    cyc = links[X]
    pts = []
    for i in range(len(cyc)):
        A, B = cyc[i], cyc[(i + 1) % len(cyc)]
        M = np.array([H[X][:3], H[A][:3], H[B][:3]], float)
        r = -np.array([H[X][3], H[A][3], H[B][3]], float)
        pts.append(np.linalg.solve(M, r))
    nX = np.array(H[X][:3], float)
    area = np.zeros(3)
    for i in range(len(pts)):
        area += np.cross(pts[i], pts[(i + 1) % len(pts)])
    return 1 if area @ nX > 0 else -1
