"""Grooved-box control object: a box with k pyramidal notches across the top/front edge (exact rationals).

Faces: 6 box planes, then 3 lateral planes per notch. Row convention of the repo: outward normal (a, b, c), the solid
is on the side a x + b y + c z + d <= 0 locally. A notch is the open cone {row_j > 0 for its 3 lateral rows}.
Usage: python3 grooved.py K [--out FILE]   writes planes, links, negative_links (one segment pairing swapped)."""
import itertools
import json
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'code'))
from ladder_exact import solve3, verify

W = 10


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def planes(k, seed):
    rng = random.Random(seed)
    rows = [[-1, 0, 0, 0], [1, 0, 0, -W], [0, -1, 0, 0], [0, 1, 0, -W], [0, 0, -1, 0], [0, 0, 1, -W]]
    for r in rows:  # tilt the box planes so that no two planes are parallel
        for j in range(3):
            if r[j] == 0:
                r[j] = Fr(rng.randint(-6, 6), 100)
    # x=0, x=W, y=0 (front), y=W, z=0, z=W (top)
    for i in range(k):
        c = Fr(W * (2 * i + 1), 2 * k)
        apex = (c, Fr(2), Fr(8))
        axis = (0, -1, 1)
        rays = []
        for th in ((0, 1), (Fr(-87, 100), Fr(-1, 2)), (Fr(87, 100), Fr(-1, 2))):
            r = [2 * axis[j] + th[0] * (1, 0, 0)[j] + th[1] * (0, 1, 1)[j] for j in range(3)]
            rays.append([r[j] + Fr(rng.randint(-8, 8), 100) for j in range(3)])
        for a, b in ((0, 1), (1, 2), (2, 0)):
            n = cross(rays[a], rays[b])
            if sum(n[j] * rays[3 - a - b][j] for j in range(3)) < 0:
                n = tuple(-x for x in n)  # cone side (third ray) has row > 0 ... row = n.x + d, d from apex
            row = [Fr(x) for x in n] + [-sum(n[j] * apex[j] for j in range(3))]
            rows.append(row)
    return rows


def integral(rows):
    out = []
    for r in rows:
        den = 1
        for x in r:
            den = den * Fr(x).denominator // __import__('math').gcd(den, Fr(x).denominator)
        out.append([int(Fr(x) * den) for x in r])
    return out


def val(r, p):
    return sum(r[j] * p[j] for j in range(3)) + r[3]


def geometry(rows):
    """Vertices, edges and links of the solid = closed box minus open cones, by exact predicates."""
    n = len(rows); k = (n - 6) // 3
    cones = [list(range(6 + 3 * i, 9 + 3 * i)) for i in range(k)]
    # the cone is {row > 0}; the solid's outward normal into the cone is the row itself

    def in_solid_face(x, p):
        v = [val(r, p) for r in rows]
        if any(v[i] > 0 for i in range(6)):
            return False
        for cone in cones:
            vals = [v[i] for i in cone]
            if x in cone:
                if any(v[i] < 0 for i in cone if i != x):
                    return False
            elif all(t > 0 for t in vals):
                return False
        return True

    pts = {}
    for t in itertools.combinations(range(n), 3):
        try:
            p = solve3([rows[i] for i in t])
        except AssertionError:
            continue
        if all(in_solid_face(x, p) for x in t):
            if sum(val(r, p) == 0 for r in rows) != 3:
                raise ValueError('not simple')
            pts[t] = p
    edges = []  # (x, y, vertex a, vertex b)
    for x, y in itertools.combinations(range(n), 2):
        vs = [t for t in pts if x in t and y in t]
        d = cross(rows[x][:3], rows[y][:3])
        vs.sort(key=lambda t: sum(pts[t][j] * d[j] for j in range(3)))
        for a, b in zip(vs, vs[1:]):
            m = tuple((pts[a][j] + pts[b][j]) / 2 for j in range(3))
            if in_solid_face(x, m) and in_solid_face(y, m):
                edges.append((x, y, a, b))
    links = {}
    for x in range(n):
        adj = {}
        for (p, q, a, b) in edges:
            if x in (p, q):
                y = q if x == p else p
                adj.setdefault(a, []).append((b, y)); adj.setdefault(b, []).append((a, y))
        if any(len(v) != 2 for v in adj.values()):
            raise ValueError(f'face {x} is not a single cycle')
        start = min(adj); cyc = [start]; ys = []
        prev = None; cur = start
        while True:
            nxt = [e for e in adj[cur] if e[0] != prev] if prev is not None else adj[cur][:1]
            b, y = nxt[0]
            ys.append(y); prev, cur = cur, b
            if cur == start:
                break
            cyc.append(cur)
        if len(cyc) != len(adj):
            raise ValueError(f'face {x} has several cycles')
        # ys[i] is the neighbour across the edge cyc[i] -> cyc[i+1]; orient counter-clockwise from outside
        area = [Fr(0)] * 3
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            c = cross(pts[a], pts[b]); area = [area[j] + c[j] for j in range(3)]
        if sum(area[j] * rows[x][j] for j in range(3)) < 0:
            cyc.reverse(); ys = ys[::-1][1:] + ys[::-1][:1]
            # reversed walk: edge i of the reversed cycle joins cyc[i] -> cyc[i+1] again; recompute below
            ys = [None] * len(cyc)
            for i, (a, b) in enumerate(zip(cyc, cyc[1:] + cyc[:1])):
                ys[i] = next(y for (p, q, e, f) in edges if x in (p, q) for y in [q if x == p else p]
                             if {e, f} == {a, b})
        # vertex i of the link convention is the corner between edge i and edge i+1; edge i joins vertex i-1, i
        links[x] = ys[-1:] + ys[:-1] if False else ys
    return pts, links


def links_in_ladder_order(links, pts):
    return links


def swapped_maps(rows, links):
    """Maps that pass the combinatorial checks of ladder_exact but fail the exact geometry: two entries of one face
    link exchanged, or the same exchange in the two links of a face pair (a different segment pairing)."""
    H = [[float(v) for v in r] for r in rows]
    found = []

    def ok(M):
        try:
            o = verify(H, M, require_all_pairs=False)
        except Exception:
            return False
        return o['corner_triples_distinct'] and o['edges_consistent'] and o['V_E_F_chi'][3] == 2 and not o['EMBEDDED']
    def corners_ok(M):
        c = {}
        for x, L in M.items():
            m = len(L)
            for i in range(m):
                c.setdefault(frozenset((x, L[i], L[(i + 1) % m])), []).append(x)
        return all(len(t) == 3 and len(set(v)) == 3 and len(v) == 3 for t, v in c.items())
    singles = [(x, i, j) for x, L in links.items() for i, j in itertools.combinations(range(len(L)), 2) if L[i] != L[j]]
    for (x, i, j), (y, p, q) in itertools.combinations(singles, 2):
        if x == y:
            continue
        M = {f: list(v) for f, v in links.items()}
        M[x][i], M[x][j] = M[x][j], M[x][i]
        M[y][p], M[y][q] = M[y][q], M[y][p]
        if corners_ok(M) and ok(M):
            found.append((f'swaps in faces {x}:{i},{j} and {y}:{p},{q}', M))
    return found


if __name__ == '__main__':
    k = int(sys.argv[1])
    rows = integral(planes(k, 2611090100 + k))
    pts, links = geometry(rows)
    o = verify([[float(v) for v in r] for r in rows], links, require_all_pairs=False)
    print({kk: o[kk] for kk in ('V_E_F_chi', 'corner_triples_distinct', 'edges_consistent', 'simple_faces', 'bad_pairs', 'EMBEDDED')})
    print('multiplicity top/front:', links[5].count(2), links[2].count(5))
    neg = swapped_maps(rows, links)
    print('swap candidates:', [d for d, _ in neg][:10], len(neg))
    if '--out' in sys.argv:
        Path(sys.argv[sys.argv.index('--out') + 1]).write_text(json.dumps(dict(
            planes=rows, links={str(a): b for a, b in links.items()},
            negative_links={str(a): b for a, b in neg[0][1].items()} if neg else None, negative_note=neg[0][0] if neg else None), indent=1) + '\n')
