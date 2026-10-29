"""Period defect of fixed gauge normals (fresh-eyes idea 2; Penrose / Sugihara-type LP).

Given gauge normals g_X (polygon of face X counter-clockwise about g_X in the coherent link order),
an edge e = XY of the polyhedron has direction g_X x g_Y; traversed in face X's ccw order its vector
is a_e (g_X x g_Y) with |a_e| >= 1 and sign(a_e) = s * kappa_e (kappa = edge convexity label,
s a global sign). Vertex rule: at a convex vertex (det > 0) the three kappas agree, at a saddle they
do not. Unknown vertex positions p_v; residual r_e = p_head - p_tail - a_e d_e. MILP:
    minimize sum |r_e|_1   s.t. vertex rules, sign constraints, |a_e| <= A.
Defect 0  <=>  a closed, locally consistently labelled polyhedral surface with these face normals
exists (necessary condition for an embedding; simplicity/embedding not imposed).
"""
import itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

from gauss_degree import coherent_triangles, links_from


def period_defect(G, tris, A=100.0, s=1, time_limit=60):
    G = np.asarray(G, float)
    G = G / np.linalg.norm(G, axis=1)[:, None]
    n = len(G)
    ot = coherent_triangles(tris)
    links = links_from(ot, n)
    vid = {frozenset(t): i for i, t in enumerate(ot)}
    # oriented edges: in face X traversal from v(X,B_{i-1},B_i) to v(X,B_i,B_{i+1}) along edge XB_i
    edges = {}
    for X in range(n):
        L = links[X]
        m = len(L)
        for i in range(m):
            Bp, B, Bn = L[i - 1], L[i], L[(i + 1) % m]
            key = frozenset((X, B))
            if key in edges:
                continue
            tail = vid[frozenset((X, Bp, B))]
            head = vid[frozenset((X, B, Bn))]
            d = np.cross(G[X], G[B])
            edges[key] = (tail, head, d / np.linalg.norm(d))
    E = list(edges)
    ne, nv = len(E), len(ot)
    # variable layout: p (3 nv) | a (ne) | k (ne, binary) | r+ (3 ne) | r- (3 ne)
    ip, ia, ik = 0, 3 * nv, 3 * nv + ne
    irp, irm = ik + ne, ik + ne + 3 * ne
    N = irm + 3 * ne
    c = np.zeros(N); c[irp:] = 1.0
    rows = []
    Aeq = lil_matrix((3 * ne, N)); beq = np.zeros(3 * ne)
    for j, key in enumerate(E):
        t, h, d = edges[key]
        for q in range(3):
            r = 3 * j + q
            Aeq[r, ip + 3 * h + q] += 1; Aeq[r, ip + 3 * t + q] -= 1
            Aeq[r, ia + j] = -d[q]
            Aeq[r, irp + 3 * j + q] = -1; Aeq[r, irm + 3 * j + q] = 1
    cons = [LinearConstraint(Aeq.tocsr(), beq, beq)]
    # sign constraints: k=1 -> s*a >= 1 ; k=0 -> s*a <= -1   (big-M = 2A)
    M = 2 * A
    Ain = lil_matrix((2 * ne, N)); lo = np.full(2 * ne, -np.inf); hi = np.zeros(2 * ne)
    for j in range(ne):
        # s*a - M*k >= 1 - M   ->  -(s a) + M k <= M - 1
        Ain[2 * j, ia + j] = -s; Ain[2 * j, ik + j] = M; hi[2 * j] = M - 1
        # s*a + M*(1-k) <= ... : s*a <= -1 + M k  ->  s a - M k <= -1
        Ain[2 * j + 1, ia + j] = s; Ain[2 * j + 1, ik + j] = -M; hi[2 * j + 1] = -1
    cons.append(LinearConstraint(Ain.tocsr(), lo, hi))
    # vertex rules
    eidx = {key: j for j, key in enumerate(E)}
    Av = lil_matrix((2 * nv, N)); vlo = np.zeros(2 * nv); vhi = np.zeros(2 * nv)
    nconv = 0
    for i, (a, b, cc) in enumerate(ot):
        ks = [ik + eidx[frozenset((a, b))], ik + eidx[frozenset((b, cc))], ik + eidx[frozenset((a, cc))]]
        if np.linalg.det(np.array([G[a], G[b], G[cc]])) > 0:
            nconv += 1
            Av[2 * i, ks[0]] = 1; Av[2 * i, ks[1]] = -1
            Av[2 * i + 1, ks[1]] = 1; Av[2 * i + 1, ks[2]] = -1
        else:
            for kk in ks:
                Av[2 * i, kk] = 1
            vlo[2 * i], vhi[2 * i] = 1, 2
            vlo[2 * i + 1], vhi[2 * i + 1] = -np.inf, np.inf
    cons.append(LinearConstraint(Av.tocsr(), vlo, vhi))
    lb = np.full(N, -np.inf); ub = np.full(N, np.inf)
    lb[ip:ip + 3] = 0; ub[ip:ip + 3] = 0                       # translation gauge
    lb[ia:ia + ne] = -A; ub[ia:ia + ne] = A
    lb[ik:ik + ne] = 0; ub[ik:ik + ne] = 1
    lb[irp:] = 0
    integ = np.zeros(N); integ[ik:ik + ne] = 1
    res = milp(c, constraints=cons, bounds=Bounds(lb, ub), integrality=integ,
               options={'time_limit': time_limit, 'disp': False})
    val = float(res.fun) if res.status in (0, 1) and res.fun is not None else None
    if return_L == 'full' and res.x is not None:
        L = res.x[ic:ic + 9].reshape(3, 3) if general else None
        return val, res.status, L, {'p': res.x[ip:ip + 3 * nv].reshape(nv, 3), 'a': res.x[ia:ia + ne],
                                    'edges': edges, 'E': E, 'faces': faces}
    if return_L:
        L = res.x[ic:ic + 9].reshape(3, 3) if (general and res.x is not None) else None
        return val, res.status, L
    return val, res.status, nconv


def surface_edges(G, tris):
    """Oriented edges (tail, head, unit direction) as used by period_defect, plus face cycles with
    orientation signs: faces[X] = list of (edge_key, +1/-1)."""
    G = np.asarray(G, float); G = G / np.linalg.norm(G, axis=1)[:, None]
    n = len(G); ot = coherent_triangles(tris); links = links_from(ot, n)
    vid = {frozenset(t): i for i, t in enumerate(ot)}
    edges, faces = {}, {X: [] for X in range(n)}
    for X in range(n):
        L = links[X]; m = len(L)
        for i in range(m):
            Bp, B, Bn = L[i - 1], L[i], L[(i + 1) % m]
            key = frozenset((X, B))
            tail = vid[frozenset((X, Bp, B))]; head = vid[frozenset((X, B, Bn))]
            if key not in edges:
                d = np.cross(G[X], G[B]); edges[key] = (tail, head, d / np.linalg.norm(d))
                faces[X].append((key, +1))
            else:
                faces[X].append((key, +1 if edges[key][0] == tail else -1))
    return edges, faces, len(ot)


def random_cocycle(edges, faces, nv, gen_values, seed=0):
    """Integer 1-cocycle phi: E -> Z^3 vanishing on face boundaries, zero on a spanning tree of the
    vertex graph, prescribed (gen_values[i]) on the 2g generator edges (tree-cotree)."""
    import random
    rnd = random.Random(seed)
    E = list(edges)
    # spanning tree of vertices (BFS)
    adj = {v: [] for v in range(nv)}
    for e in E:
        t, h, _ = edges[e]; adj[t].append((h, e)); adj[h].append((t, e))
    tree, seen, stack = set(), {0}, [0]
    while stack:
        v = stack.pop()
        for w, e in adj[v]:
            if w not in seen:
                seen.add(w); tree.add(e); stack.append(w)
    # spanning tree of faces through non-tree edges
    efaces = {}
    for X, lst in faces.items():
        for e, s in lst:
            efaces.setdefault(e, []).append(X)
    cot, fseen, fstack, parent = set(), {0}, [0], {}
    while fstack:
        X = fstack.pop()
        for e, s in faces[X]:
            if e in tree:
                continue
            Y = [f for f in efaces[e] if f != X][0]
            if Y not in fseen:
                fseen.add(Y); cot.add(e); parent[Y] = (X, e); fstack.append(Y)
    gens = [e for e in E if e not in tree and e not in cot]
    phi = {e: np.zeros(3, dtype=int) for e in E}
    for e, val in zip(gens, gen_values):
        phi[e] = np.array(val, dtype=int)
    # solve cotree edges from the leaves of the face tree upwards
    order = []
    st = [0]
    children = {}
    for Y, (X, e) in parent.items():
        children.setdefault(X, []).append(Y)
    def post(X):
        for Y in children.get(X, []):
            post(Y)
        order.append(X)
    post(0)
    for Y in order:
        if Y == 0:
            continue
        X, ec = parent[Y]
        tot = np.zeros(3, dtype=int); sc = None
        for e, s in faces[Y]:
            if e == ec:
                sc = s
            else:
                tot += s * phi[e]
        phi[ec] = -tot * sc
    for X, lst in faces.items():                      # check: closed on every face
        assert not np.any(sum(s * phi[e] for e, s in lst)), 'cocycle failed on face %d' % X
    return phi, gens


def torus_defect(G, tris, phi, A=100.0, time_limit=60, general=False, return_L=False):
    """Period defect in the flat 3-torus R^3 / (c Z^3): residual r_e = p_head - p_tail - a_e d_e
    - c*phi_e, with c >= 1 a variable lattice scale. phi = 0 gives the R^3 problem."""
    edges, faces, nv = surface_edges(G, tris)
    G = np.asarray(G, float); G = G / np.linalg.norm(G, axis=1)[:, None]
    ot = coherent_triangles(tris)
    E = list(edges); ne = len(E)
    ip, ia, ik = 0, 3 * nv, 3 * nv + ne
    irp, irm = ik + ne, ik + ne + 3 * ne
    ic = irm + 3 * ne
    N = ic + (9 if general else 1)
    c = np.zeros(N); c[irp:ic] = 1.0
    Aeq = lil_matrix((3 * ne, N)); beq = np.zeros(3 * ne)
    for j, key in enumerate(E):
        t, h, d = edges[key]
        for q in range(3):
            r = 3 * j + q
            Aeq[r, ip + 3 * h + q] += 1; Aeq[r, ip + 3 * t + q] -= 1
            Aeq[r, ia + j] = -d[q]
            Aeq[r, irp + 3 * j + q] = -1; Aeq[r, irm + 3 * j + q] = 1
            if general:                     # periods = L phi_e, L a free 3x3 matrix (row q)
                for kk in range(3):
                    if phi[key][kk]:
                        Aeq[r, ic + 3 * q + kk] = -float(phi[key][kk])
            else:
                Aeq[r, ic] = -float(phi[key][q])
    cons = [LinearConstraint(Aeq.tocsr(), beq, beq)]
    M = 2 * A
    Ain = lil_matrix((2 * ne, N)); hi = np.zeros(2 * ne)
    for j in range(ne):
        Ain[2 * j, ia + j] = -1; Ain[2 * j, ik + j] = M; hi[2 * j] = M - 1
        Ain[2 * j + 1, ia + j] = 1; Ain[2 * j + 1, ik + j] = -M; hi[2 * j + 1] = -1
    cons.append(LinearConstraint(Ain.tocsr(), np.full(2 * ne, -np.inf), hi))
    eidx = {key: j for j, key in enumerate(E)}
    nvx = len(ot)
    Av = lil_matrix((2 * nvx, N)); vlo = np.zeros(2 * nvx); vhi = np.zeros(2 * nvx)
    for i, (a, b, cc) in enumerate(ot):
        ks = [ik + eidx[frozenset((a, b))], ik + eidx[frozenset((b, cc))], ik + eidx[frozenset((a, cc))]]
        if np.linalg.det(np.array([G[a], G[b], G[cc]])) > 0:
            Av[2 * i, ks[0]] = 1; Av[2 * i, ks[1]] = -1
            Av[2 * i + 1, ks[1]] = 1; Av[2 * i + 1, ks[2]] = -1
        else:
            for kk in ks:
                Av[2 * i, kk] = 1
            vlo[2 * i], vhi[2 * i] = 1, 2
            vlo[2 * i + 1], vhi[2 * i + 1] = -np.inf, np.inf
    cons.append(LinearConstraint(Av.tocsr(), vlo, vhi))
    lb = np.full(N, -np.inf); ub = np.full(N, np.inf)
    lb[ip:ip + 3] = 0; ub[ip:ip + 3] = 0
    lb[ia:ia + ne] = -A; ub[ia:ia + ne] = A
    lb[ik:ik + ne] = 0; ub[ik:ik + ne] = 1
    lb[irp:ic] = 0
    if general:
        lb[ic:ic + 9] = -10 * A; ub[ic:ic + 9] = 10 * A
    else:
        lb[ic] = 1.0; ub[ic] = 10 * A
    integ = np.zeros(N); integ[ik:ik + ne] = 1
    res = milp(c, constraints=cons, bounds=Bounds(lb, ub), integrality=integ,
               options={'time_limit': time_limit, 'disp': False})
    val = float(res.fun) if res.status in (0, 1) and res.fun is not None else None
    if return_L == 'full' and res.x is not None:
        L = res.x[ic:ic + 9].reshape(3, 3) if general else None
        return val, res.status, L, {'p': res.x[ip:ip + 3 * nv].reshape(nv, 3), 'a': res.x[ia:ia + ne],
                                    'edges': edges, 'E': E, 'faces': faces}
    if return_L:
        L = res.x[ic:ic + 9].reshape(3, 3) if (general and res.x is not None) else None
        return val, res.status, L
    return val, res.status
