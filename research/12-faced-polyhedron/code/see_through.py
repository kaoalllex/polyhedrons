"""See-through test (user's question 2026-10-30, ideas T2): can one look straight through the holes of
a polyhedron? A straight line that misses the surface threads a hole iff some cycle on the surface
winds around it (linking number != 0). Cycles: a basis of the edge graph (faces are disks, so the
1-skeleton carries all of H1). Winding of a closed polygon around the line = winding number of its
projection along the line around the line's point. Random lines (direction uniform, offset near a
random surface point); the rank of the observed linking vectors = number of independent see-through
holes (at most g: a line lies in the unbounded complementary region, whose H1 has rank g).
Usage: python3 -I see_through.py RESULT_JSON [N_LINES]   (planes + 'solid' or 'triangles')"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gauss_degree import coherent_triangles, links_from
from ladder import polygons


def surface(r):
    H = np.array(r['planes'], float); n = len(H)
    if 'triangles' in r:
        tris = [tuple(t) for t in r['triangles']]
    else:
        import solid_first as SF
        A = SF.Arrangement(H); tris = SF.extract_map(A, {tuple(x) for x in r['solid']}); H = A.H
    L = links_from(coherent_triangles(tris), n)
    return polygons(H, L)


def cycle_basis(P):
    key = {}; pts = []; edges = set()
    for X, Q in P.items():
        ids = []
        for q in Q:
            k = tuple(np.round(q, 7))
            if k not in key:
                key[k] = len(pts); pts.append(q)
            ids.append(key[k])
        for i in range(len(ids)):
            a, b = ids[i], ids[(i + 1) % len(ids)]
            edges.add((min(a, b), max(a, b)))
    pts = np.array(pts); V = len(pts); adj = {v: [] for v in range(V)}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    par = {0: None}; depth = {0: 0}; st = [0]; tree = set()
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in par:
                par[y] = x; depth[y] = depth[x] + 1; tree.add((min(x, y), max(x, y))); st.append(y)
    def path(a):
        out = [a]
        while par[out[-1]] is not None:
            out.append(par[out[-1]])
        return out
    cycles = []
    for a, b in edges - tree:                           # fundamental cycle of a non-tree edge
        pa, pb = path(a), path(b); sb = set(pb)
        lca = next(x for x in pa if x in sb)
        cyc = pa[:pa.index(lca) + 1] + pb[:pb.index(lca)][::-1]
        cycles.append(pts[cyc])
    return pts, cycles


def winding(C2, p):
    d = C2 - p; ang = np.arctan2(d[:, 1], d[:, 0])
    da = np.diff(np.concatenate([ang, ang[:1]]))
    da = (da + np.pi) % (2 * np.pi) - np.pi
    return int(round(da.sum() / (2 * np.pi)))


def hits(P, o, u):
    for Q in P.values():
        nrm = np.cross(Q[1] - Q[0], Q[2] - Q[0])
        k = int(np.argmax(np.abs(nrm))); nrm = nrm / np.linalg.norm(nrm)
        den = nrm @ u
        if abs(den) < 1e-12:
            continue
        t = nrm @ (Q[0] - o) / den; x = o + t * u
        a, b = [j for j in range(3) if j != k]
        q2 = Q[:, [a, b]]; x2 = x[[a, b]]; c = False
        for i in range(len(q2)):
            y1, y2 = q2[i], q2[(i + 1) % len(q2)]
            if (y1[1] > x2[1]) != (y2[1] > x2[1]):
                if y1[0] + (x2[1] - y1[1]) * (y2[0] - y1[0]) / (y2[1] - y1[1]) > x2[0]:
                    c = not c
        if c:
            return True
    return False


def see_through(r, N=20000, seed=0):
    P = surface(r); pts, cycles = cycle_basis(P); rng = np.random.default_rng(seed)
    allp = np.vstack(list(P.values())); scale = np.median(np.linalg.norm(allp - np.median(allp, 0), axis=1))
    vecs = []; free = 0
    for _ in range(N):
        u = rng.standard_normal(3); u /= np.linalg.norm(u)
        o = pts[rng.integers(len(pts))] + scale * 0.3 * rng.standard_normal(3)
        if hits(P, o, u):
            continue
        free += 1
        e1 = np.cross(u, [1, 0, 0] if abs(u[0]) < 0.9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(u, e1)
        p = np.array([o @ e1, o @ e2])
        w = [winding(np.c_[C @ e1, C @ e2], p) for C in cycles]
        if any(w):
            vecs.append(w)
    rank = int(np.linalg.matrix_rank(np.array(vecs, float))) if vecs else 0
    return dict(lines=N, missing_surface=free, threading=len(vecs), see_through_rank=rank, cycles=len(cycles))


if __name__ == '__main__':
    r = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    print(sys.argv[1], see_through(r, N), flush=True)
