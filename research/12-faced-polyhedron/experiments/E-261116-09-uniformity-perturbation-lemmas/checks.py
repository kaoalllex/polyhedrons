"""E-261116-09 part A exact checks (PLAN.md): integer witnesses for L2 and the universal local check of L6 at k = 4.

witnesses: equivariant covector configurations (plane a x + b y + c z + d = 0 as (a, b, c, d); positive transport
  h_{g(i)} = g . h_i) for C3 3+3+3 and C2 4 x 2 + 1 at nine faces and free C2 at eight; every 4 x 4 minor of the
  configuration (chart covector included) must be nonzero. The first two reproduce the Codex review §4 minima (8, 44).
local_k4: the generic central arrangement of four planes through p = 0 (x, y, z, x + y + z). For every union U of its
  14 cones whose boundary is a manifold vertex of valence 4 using each plane once, and both perturbation signs
  (x + y + z = +-1; every generic perturbation is one of them up to a near-identity affine map, PLAN L6), the
  perturbed solid keeps the membership of the 14 unbounded cells and puts the bounded cell in or out. A patch is
  valid if its boundary is a connected surface with every edge in exactly two boundary 2-faces, every vertex link one
  cycle with 0, 2 or 3 maximal arcs on distinct planes, every labelled face a closed disk (connected, chi = 1), and the
  whole patch a disk (connected, chi = 1). Controls: the six convex 4-faced cones are valid vertices and keep the
  bounded cell out (their solid is the perturbed intersection of four half-spaces); two opposite cones, the eight
  3-faced cones and a patch with one far cell flipped are rejected. The far trace and the outgoing edges are kept by construction (unbounded
  faces inherit), so they are not tested. Faces are sign vectors found by exact Fourier-Motzkin feasibility.
Usage: python3 checks.py OUT_JSON"""
from fractions import Fraction
import itertools
import json
import sys


def det(m):
    m = [list(map(Fraction, r)) for r in m]; n = len(m); s = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c]), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]; s = -s
        s *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [a - f * b for a, b in zip(m[r], m[c])]
    return s


def minima(cov):
    vals = [abs(det(q)) for q in itertools.combinations(cov, 4)]
    return dict(elements=len(cov), quads=len(vals), min_abs_minor=int(min(vals)), zeros=sum(v == 0 for v in vals))


def witnesses():
    inf = (0, 0, 0, 1)
    c3 = [r for a, b, c, d in [(2, 3, 5, 7), (1, -4, 2, 11), (5, -1, 6, 13)] for r in ((a, b, c, d), (b, c, a, d), (c, a, b, d))]
    reps = [(2, 3, 5, 7), (1, -4, 3, 11), (5, -1, 6, 13), (3, 7, -2, 17)]
    c2 = [r for a, b, c, d in reps for r in ((a, b, c, d), (-a, -b, c, d))]
    return dict(C3_333_standard=minima(c3 + [inf]),
                C2_4x2p1_moved=minima(c2 + [(0, 0, 1, 19), (2, 5, 7, 100000)]),
                C2_free_8_standard=minima(c2 + [inf]))


# ---- L6: faces of a plane arrangement in R^3 as sign vectors -------------------------------------------------

def feasible(planes, sigma):
    """Exists x in R^3 with n_i x + d_i = 0 where sigma_i = 0 and sigma_i (n_i x + d_i) > 0 elsewhere."""
    rows = [[Fraction(v) for v in (*n, d)] for (n, d) in planes]  # coefficients x, y, z, constant
    eqs = [r for r, s in zip(rows, sigma) if s == 0]
    gts = [[s * v for v in r] for r, s in zip(rows, sigma) if s != 0]
    nv = 3
    while eqs:  # substitute equalities, one at a time
        e = eqs.pop()
        j = next((j for j in range(nv) if e[j]), None)
        if j is None:
            if e[nv]:
                return False
            continue
        def sub(r):
            f = r[j] / e[j]
            return [a - f * b for a, b in zip(r, e)]
        eqs = [sub(r) for r in eqs]; gts = [sub(r) for r in gts]
    for j in range(nv):  # Fourier-Motzkin on strict inequalities
        pos = [r for r in gts if r[j] > 0]; neg = [r for r in gts if r[j] < 0]; zer = [r for r in gts if r[j] == 0]
        gts = zer + [[-q[j] * a + p[j] * b for a, b in zip(p, q)] for p in pos for q in neg]
    return all(r[nv] > 0 for r in gts)


def faces(planes):
    return [s for s in itertools.product((-1, 0, 1), repeat=len(planes)) if feasible(planes, s)]


def rank(vectors):
    vs = [list(map(Fraction, v)) for v in vectors]; r = 0
    for c in range(3):
        p = next((i for i in range(r, len(vs)) if vs[i][c]), None)
        if p is None:
            continue
        vs[r], vs[p] = vs[p], vs[r]
        for i in range(len(vs)):
            if i != r and vs[i][c]:
                f = vs[i][c] / vs[r][c]; vs[i] = [a - f * b for a, b in zip(vs[i], vs[r])]
        r += 1
    return r


def below(g, f):
    return all(a == 0 or a == b for a, b in zip(g, f))


def zero_at(f):
    return [i for i, v in enumerate(f) if v == 0]


class Arr:
    """Face poset of an arrangement (sign vectors), with incidences precomputed."""
    def __init__(self, planes):
        self.k = len(planes); self.F = faces(planes)
        self.dim = {f: 3 - rank([planes[i][0] for i in zero_at(f)]) for f in self.F}
        central = faces([(n, 0) for n, _ in planes])
        self.bounded = {f: not any(any(t) and below(t, f) for t in central) for f in self.F}
        self.cells = [f for f in self.F if 0 not in f]
        self.down = {f: frozenset(g for g in self.F if below(g, f)) for f in self.F}
        self.up = {g: frozenset(f for f in self.F if below(g, f)) for g in self.F}
        self.walls = []  # (2-face, its plane, the two cells it separates)
        for f in self.F:
            if self.dim[f] == 2:
                i = zero_at(f)[0]; a, b = list(f), list(f); a[i] = 1; b[i] = -1
                self.walls.append((f, i, tuple(a), tuple(b)))
        self.plane = {f: i for f, i, _, _ in self.walls}


def boundary(arr, solid):
    """Boundary 2-faces (separating a solid cell from a non-solid one) and the closed set X they span."""
    two = [f for f, _, a, b in arr.walls if (a in solid) != (b in solid)]
    X = set().union(*(arr.down[f] for f in two)) if two else set()
    return two, X


def arcs(labels):
    """Maximal arcs of a cyclic label sequence: their number (1 for a constant cycle) and labels."""
    runs = [a for a, b in zip(labels, labels[1:] + labels[:1]) if a != b]
    return (len(runs) or 1), runs


def connected(arr, S):
    S = set(S)
    if not S:
        return False
    start = next(iter(S)); seen = {start}; stack = [start]
    while stack:
        f = stack.pop()
        for g in (arr.up[f] | arr.down[f]) & S:
            if g not in seen:
                seen.add(g); stack.append(g)
    return seen == S


def chi(arr, S):
    """Euler characteristic of the closed union S intersected with a large ball (unbounded faces are pointed)."""
    return sum((-1) ** arr.dim[f] for f in S if arr.bounded[f])


def walk_labels(arr, v, two, X):
    """Link of v in the boundary: one cycle through the faces just above v; its sequence of planes, or None."""
    nodes = [e for e in arr.up[v] & X if arr.dim[e] == arr.dim[v] + 1]
    two_v = set(two) & arr.up[v]
    if not nodes:
        return []
    adj = {e: [f for f in two_v if e in arr.down[f]] for e in nodes}
    if any(len(a) != 2 for a in adj.values()):
        return None
    start = nodes[0]; f = adj[start][0]; cur = start; labels = []; count = 0
    while True:
        labels.append(arr.plane[f]); count += 1
        cur = next(e for e in nodes if e != cur and f in adj[e])
        if cur == start:
            break
        f = next(g for g in adj[cur] if g != f)
    return labels if count == len(nodes) else None


def original_ok(arr, U):
    two, X = boundary(arr, U)
    lab = walk_labels(arr, tuple([0] * arr.k), two, X)
    if not lab:
        return False
    n, runs = arcs(lab)
    return n == arr.k and sorted(runs) == list(range(arr.k))


def patch_ok(arr, solid):
    two, X = boundary(arr, solid)
    if not connected(arr, X) or chi(arr, X) != 1:
        return False, 'patch not a disk'
    for e in X:
        if arr.dim[e] == 1 and len(arr.up[e] & set(two)) != 2:
            return False, 'edge not manifold'
    for v in X:
        if arr.dim[v] == 0:
            lab = walk_labels(arr, v, two, X)
            if lab is None:
                return False, 'vertex link not one cycle'
            n, runs = arcs(lab)
            if n not in (1, 2, 3) or len(set(runs)) != len(runs):
                return False, f'vertex with {n} arcs'
    new_edges = set()
    for e in X:
        if arr.dim[e] == 1 and arr.bounded[e]:
            labs = {arr.plane[f] for f in arr.up[e] & set(two)}
            if len(labs) == 2:
                new_edges.add(tuple(sorted(labs)))
    for i in range(arr.k):
        Xi = set().union(*(arr.down[f] for f in two if arr.plane[f] == i))
        if not connected(arr, Xi) or chi(arr, Xi) != 1:
            return False, f'face {i} not a disk'
    return True, sorted(new_edges)


def local_k4():
    normals = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]
    central = Arr([(n, 0) for n in normals])
    cones = central.cells
    assert len(cones) == 14
    valid_U = [U for r in range(1, 14) for U in map(set, itertools.combinations(cones, r)) if original_ok(central, U)]
    out = dict(cones=len(cones), valid_vertices=len(valid_U), cases=[], universal=True, controls={})
    for sign in (1, -1):
        arr = Arr([(n, 0) for n in normals[:3]] + [(normals[3], -sign)])
        bounded_cells = [c for c in arr.cells if arr.bounded[c]]
        assert len(arr.cells) == 15 and len(bounded_cells) == 1, (len(arr.cells), bounded_cells)
        T = bounded_cells[0]
        assert all(c in cones for c in arr.cells if c != T)
        for U in valid_U:
            res = {}
            for inside in (False, True):
                solid = set(U) | ({T} if inside else set())
                res['in' if inside else 'out'] = patch_ok(arr, solid)
            ok = [k for k, (good, _) in res.items() if good]
            two, X = boundary(central, U)
            runs = arcs(walk_labels(central, tuple([0] * 4), two, X))[1]
            cyclic = {tuple(sorted(e)) for e in zip(runs, runs[1:] + runs[:1])}
            out['cases'].append(dict(sign=sign, U=sorted(U), cones_in=len(U), valid_choices=ok,
                                     new_adjacencies={k: [e for e in v[1] if tuple(e) not in cyclic]
                                                      for k, v in res.items() if v[0]},
                                     rejected={k: v[1] for k, v in res.items() if not v[0]}))
            out['universal'] &= bool(ok)
    # controls: the convex 4-faced cone must be valid and must pass; a non-manifold vertex (two opposite cones) and a
    # vertex using only three planes must be rejected by original_ok; a patch with a flipped far cell must fail.
    quads = [c for c in cones if original_ok(central, {c})]
    out['controls']['convex_cones_valid'] = len(quads)
    out['controls']['convex_keeps_bounded_cell_out'] = all(c['valid_choices'] == ['out'] for c in out['cases']
                                                         if c['cones_in'] == 1)
    opp = {cones[0], tuple(-v for v in cones[0])}
    out['controls']['opposite_cones_rejected'] = not original_ok(central, opp)
    tri = [c for c in cones if not original_ok(central, {c})]
    out['controls']['three_plane_cones_rejected'] = len(tri)
    arr = Arr([(n, 0) for n in normals[:3]] + [(normals[3], -1)])
    U = next(set(u) for u in valid_U if len(u) > 1)
    flip = U ^ {next(c for c in cones if c not in U and any(sum(a != b for a, b in zip(c, u)) == 1 for u in U))}
    out['controls']['flipped_far_cell_rejected'] = not any(patch_ok(arr, flip | s)[0] for s in (set(),
                                                                                                    {c for c in arr.cells if arr.bounded[c]}))
    return out


def main(path):
    w = witnesses(); l = local_k4()
    counts = {}
    for c in l['cases']:
        key = f"sign {c['sign']:+d}, valid {'+'.join(c['valid_choices']) or 'none'}, new adjacencies " + \
              '/'.join(str(len(v)) for v in c['new_adjacencies'].values())
        counts[key] = counts.get(key, 0) + 1
    report = dict(witnesses=w, local_k4={k: v for k, v in l.items() if k != 'cases'}, local_k4_case_counts=counts)
    report['PASS'] = (w['C3_333_standard']['min_abs_minor'] == 8 and w['C2_4x2p1_moved']['min_abs_minor'] == 44
                      and w['C2_free_8_standard']['zeros'] == 0 and l['universal']
                      and l['controls']['convex_cones_valid'] == 6 and l['controls']['opposite_cones_rejected']
                      and l['controls']['convex_keeps_bounded_cell_out']
                      and l['controls']['flipped_far_cell_rejected'])
    with open(path, 'w') as f:
        json.dump(report, f, indent=1); f.write('\n')
    print(json.dumps(dict(witnesses=w, local_k4=report['local_k4'], PASS=report['PASS'])))


if __name__ == '__main__':
    main(sys.argv[1])
