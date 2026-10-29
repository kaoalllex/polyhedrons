"""'Solid first' (cross-field-ideas P7, work backwards from the answer): the state is the n face planes
plus a set S of bounded cells of their arrangement. The solid S is ALWAYS embedded; what may be wrong
is its face structure. For a generic arrangement:
  * a 1-cell (segment of a line X cap Y between consecutive triple points) has 4 surrounding 3-cells;
    1 or 3 of them in S -> a polyhedron edge between the X-face and the Y-face; 2 adjacent -> the face
    continues flat across the line; 2 diagonal -> non-manifold edge (violation);
  * faces of S in plane X = connected components of the boundary facets of plane X, glued across
    1-cells where the face continues flat; each must be a disk (Euler characteristic 1);
  * a triple point is a manifold point iff the S-octants and the other octants are each face-connected.
Target (Szilassi-type, n faces pairwise adjacent): exactly one face per plane, a disk, every pair of
planes with exactly one edge run on their common line, no non-manifold edges / vertices. Then every
vertex is 3-valent, V = n(n-1)/3, and for n = 12 the genus is 6 automatically. Every zero is an
embedded polyhedron by construction, of whatever combinatorial type it happens to have.
"""
import itertools, sys
import numpy as np
from scipy.optimize import linprog


class Arrangement:
    def __init__(self, H):
        H = np.asarray(H, float)
        self.H = H / np.linalg.norm(H[:, :3], axis=1)[:, None]
        self.n = n = len(H)
        self.P = {t: np.linalg.solve(self.H[list(t), :3], -self.H[list(t), 3]) for t in itertools.combinations(range(n), 3)}
        self.cells = {}                                  # sign vector -> list of vertex points
        for t, p in self.P.items():
            base = np.sign(self.H[:, :3] @ p + self.H[:, 3]).astype(int)
            for s in itertools.product((-1, 1), repeat=3):
                sv = base.copy(); sv[list(t)] = s; key = tuple(sv)
                self.cells.setdefault(key, []).append(p)
        # unbounded cells = sign vectors seen at infinity = sectors of the great-circle arrangement
        # n_w . u = 0 (around each vertex u = +-(n_a x n_b), four sectors); no LP needed
        unb = set()
        for a, b in itertools.combinations(range(n), 2):
            u = np.cross(self.H[a, :3], self.H[b, :3])
            for sg in (1, -1):
                base = np.sign(self.H[:, :3] @ (sg * u)).astype(int)
                for s in itertools.product((-1, 1), repeat=2):
                    sv = base.copy(); sv[[a, b]] = s; unb.add(tuple(sv))
        self.bounded = {k for k in self.cells if k not in unb}
        # 1-cells: per pair (X, Y), segments between consecutive triple points on the line
        self.ones = {}                                   # (X, Y) -> list of (sign vector over all planes with X, Y = 0, t0, t1, ends)
        for X, Y in itertools.combinations(range(n), 2):
            d = np.cross(self.H[X, :3], self.H[Y, :3])
            pts = sorted(((self.P[tuple(sorted((X, Y, c)))] @ d, c) for c in range(n) if c not in (X, Y)))
            segs = []
            for i in range(len(pts) - 1):
                (ta, ca), (tb, cb) = pts[i], pts[i + 1]
                mid = 0.5 * (self.P[tuple(sorted((X, Y, ca)))] + self.P[tuple(sorted((X, Y, cb)))])
                sv = np.sign(self.H[:, :3] @ mid + self.H[:, 3]).astype(int); sv[X] = 0; sv[Y] = 0
                segs.append((tuple(sv), ca, cb))
            self.ones[(X, Y)] = segs

    def _bounded(self, key):
        s = np.array(key, float)
        A = -(s[:, None] * self.H[:, :3])               # s_w n_w . u >= z  ->  -s_w n_w . u + z <= 0
        res = linprog(c=[0, 0, 0, -1], A_ub=np.c_[A, np.ones(self.n)], b_ub=np.zeros(self.n),
                      bounds=[(-1, 1)] * 3 + [(None, 1)], method='highs')
        return res.status == 0 and -res.fun < 1e-9      # no recession direction -> bounded


def _cell(sv, X, sx, Y, sy):
    c = list(sv); c[X] = sx; c[Y] = sy
    return tuple(c)


def evaluate(A, S, detail=False):
    """Violation count of the face structure of the solid S (set of bounded cell sign vectors)."""
    n = A.n
    parent = {}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    def facet(X, sv_wo_X):
        return (X, sv_wo_X)
    diag = 0
    edges = []                                           # (X, Y, segment index, facet_X, facet_Y)
    bfacets = set()
    for (X, Y), segs in A.ones.items():
        for k, (sv, ca, cb) in enumerate(segs):
            inn = {(a, b): _cell(sv, X, a, Y, b) in S for a in (1, -1) for b in (1, -1)}
            cnt = sum(inn.values())
            if cnt in (0, 4):
                continue
            if cnt == 2 and inn[(1, 1)] == inn[(-1, -1)]:
                diag += 1
                continue
            # boundary facets of plane X on the two sides of the line (sY = +-) and of plane Y
            fx = {b: (inn[(1, b)] != inn[(-1, b)]) for b in (1, -1)}
            fy = {a: (inn[(a, 1)] != inn[(a, -1)]) for a in (1, -1)}
            fid_x = {b: facet(X, _cell(sv, X, 0, Y, b)) for b in (1, -1)}
            fid_y = {a: facet(Y, _cell(sv, X, a, Y, 0)) for a in (1, -1)}
            for b in (1, -1):
                if fx[b]:
                    bfacets.add(fid_x[b]); parent.setdefault(fid_x[b], fid_x[b])
            for a in (1, -1):
                if fy[a]:
                    bfacets.add(fid_y[a]); parent.setdefault(fid_y[a], fid_y[a])
            if cnt == 2:                                 # flat continuation of one plane's face
                if fx[1] and fx[-1]:
                    union(fid_x[1], fid_x[-1])
                if fy[1] and fy[-1]:
                    union(fid_y[1], fid_y[-1])
            else:                                        # an edge between an X-facet and a Y-facet
                bx = 1 if fx[1] else -1; ay = 1 if fy[1] else -1
                edges.append((X, Y, k, fid_x[bx], fid_y[ay]))
    # vertices: manifold check from the 8 octants
    badv = 0
    cube_adj = [(a, b) for a in range(8) for b in range(8) if a < b and bin(a ^ b).count('1') == 1]
    for t, p in A.P.items():
        base = list(np.sign(A.H[:, :3] @ p + A.H[:, 3]).astype(int))
        occ = []
        for code in range(8):
            sv = list(base)
            for q in range(3):
                sv[t[q]] = 1 if (code >> q) & 1 else -1
            occ.append(tuple(sv) in S)
        k = sum(occ)
        if k in (0, 8):
            continue
        for val in (True, False):
            nodes = [i for i in range(8) if occ[i] == val]
            seen = {nodes[0]}; stack = [nodes[0]]
            while stack:
                a = stack.pop()
                for u, v in cube_adj:
                    for x, y in ((u, v), (v, u)):
                        if x == a and occ[y] == val and y not in seen:
                            seen.add(y); stack.append(y)
            if len(seen) != len(nodes):
                badv += 1
                break
    # faces = components of boundary facets per plane
    comps = {}
    for f in bfacets:
        comps.setdefault(f[0], set()).add(find(f))
    face_bad = sum(abs(len(comps.get(X, ())) - 1) if comps.get(X) else 1 for X in range(n))
    # disk check: Euler characteristic of each component in its plane (facets - 1-cells + vertices)
    comp_facets = {}
    for f in bfacets:
        comp_facets.setdefault(find(f), []).append(f)
    disk_bad = 0
    ones_in_plane = {}
    for (X, Y), segs in A.ones.items():
        for k, (sv, ca, cb) in enumerate(segs):
            for Z, W in ((X, Y), (Y, X)):
                for s in (1, -1):
                    c = list(sv); c[W] = s; c[Z] = 0
                    ones_in_plane.setdefault((Z, tuple(c)), []).append(('e', X, Y, k))
    vert_in_plane = {}
    for t, p in A.P.items():
        base = list(np.sign(A.H[:, :3] @ p + A.H[:, 3]).astype(int))
        for Z in t:
            others = [w for w in t if w != Z]
            for s1 in (1, -1):
                for s2 in (1, -1):
                    c = list(base); c[others[0]] = s1; c[others[1]] = s2; c[Z] = 0
                    vert_in_plane.setdefault((Z, tuple(c)), []).append(t)
    for root, fs in comp_facets.items():
        E = set(); V = set()
        for f in fs:
            E.update(ones_in_plane.get(f, [])); V.update(vert_in_plane.get(f, []))
        if len(fs) - len(E) + len(V) != 1:
            disk_bad += 1
    # adjacency: edge runs per pair of planes (consecutive segments with an edge between the same faces)
    runs = {}
    by_line = {}
    for X, Y, k, fx, fy in edges:
        by_line.setdefault((X, Y), []).append((k, find(fx), find(fy)))
    for (X, Y), lst in by_line.items():
        lst.sort(); r = 0; prev = None
        for k, cx, cy in lst:
            if prev is None or k != prev[0] + 1 or (cx, cy) != prev[1:]:
                r += 1
            prev = (k, cx, cy)
        runs[(X, Y)] = r
    adj_bad = sum(abs(runs.get((X, Y), 0) - 1) for X, Y in itertools.combinations(range(n), 2))
    missing = sum(1 for X, Y in itertools.combinations(range(n), 2) if runs.get((X, Y), 0) == 0)
    total = face_bad + disk_bad + adj_bad + diag + badv
    if detail:
        return total, dict(faces=face_bad, disks=disk_bad, adjacency=adj_bad, missing=missing, diagonal_edges=diag, bad_vertices=badv,
                           n_edges=len(edges), n_runs=sum(runs.values()))
    return total


def solid_from_winding(A, polys):
    """S = bounded cells with winding number 1 of the given oriented face polygons."""
    from q17_winding import winding
    keys = [k for k in A.bounded]
    cen = np.array([np.mean(A.cells[k], axis=0) for k in keys])
    w = np.rint(winding(polys, cen)).astype(int)
    if w.sum() < 0:
        w = -w
    return {k for k, x in zip(keys, w) if x == 1}
