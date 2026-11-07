"""Standalone rational check of the auxiliary eight-face candidate; no project imports.

Run from research/12-faced-polyhedron:
  python3 experiments/E-261103-05-s5-symmetric-solid-first/verify_independent.py FILE
"""
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def det(rows):
    if len(rows) == 1:
        return rows[0][0]
    return sum((-1) ** j * rows[0][j] * det([r[:j] + r[j + 1:] for r in rows[1:]])
               for j in range(len(rows)))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def on_segment(p, a, b):
    return orient(a, b, p) == 0 and all(min(x, y) <= z <= max(x, y)
                                      for z, x, y in zip(p, a, b))


def segments_meet(a, b, c, d):
    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    if any((o == 0 and on_segment(p, u, v)) for o, p, u, v in
           ((o1, c, a, b), (o2, d, a, b), (o3, a, c, d), (o4, b, c, d))):
        return True
    return o1 * o2 < 0 and o3 * o4 < 0


def inside(p, polygon):
    """Membership in a closed simple polygon, using the exact winding number."""
    winding = 0
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if on_segment(p, a, b):
            return True
        if a[1] <= p[1] < b[1] and orient(a, b, p) > 0:
            winding += 1
        elif b[1] <= p[1] < a[1] and orient(a, b, p) < 0:
            winding -= 1
    return winding != 0


def project(p, drop):
    return tuple(x for i, x in enumerate(p) if i != drop)


def merge(intervals):
    out = []
    for a, b in sorted(intervals):
        require(a <= b, "reversed interval")
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(b, out[-1][1]))
        else:
            out.append((a, b))
    return out


def section(polygon, plane, direction, drop):
    """Closed polygon intersected with another plane, in t = direction dot x."""
    cuts = {}
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        va, vb = dot(plane[:3], a) + plane[3], dot(plane[:3], b) + plane[3]
        for p, value in ((a, va), (b, vb)):
            if value == 0:
                cuts[dot(direction, p)] = p
        if va * vb < 0:
            p = tuple(x + va / (va - vb) * (y - x) for x, y in zip(a, b))
            cuts[dot(direction, p)] = p
    keys = sorted(cuts)
    intervals = [(t, t) for t in keys]
    flat = [project(p, drop) for p in polygon]
    for a, b in zip(keys, keys[1:]):
        midpoint = tuple((x + y) / 2 for x, y in zip(cuts[a], cuts[b]))
        if inside(project(midpoint, drop), flat):
            intervals.append((a, b))
    return merge(intervals)


def intersect_intervals(a, b):
    return merge([(max(x, u), min(y, v)) for x, y in a for u, v in b
                  if max(x, u) <= min(y, v)])


def check(record):
    require(set(record) == {'planes', 'links'}, "expected only planes and paired cyclic links")
    require(all(type(x) is int for row in record['planes'] for x in row), "expected integer planes")
    h = [tuple(map(Q, row)) for row in record['planes']]
    n = len(h)
    require(n == 8 and all(len(row) == 4 and any(row[:3]) for row in h), "expected eight valid planes")
    links = {int(k): v for k, v in record['links'].items()}
    require(set(links) == set(range(n)), "missing or extra face labels")
    for f, link in links.items():
        require(len(link) >= 3 and all(type(x) is int and 0 <= x < n and x != f for x in link),
                f"invalid link {f}")

    points, normal_dets = {}, []
    for triple in itertools.combinations(range(n), 3):
        rows = [list(h[i][:3]) for i in triple]
        denominator = det(rows)
        require(denominator != 0, f"triple at infinity {triple}")
        normal_dets.append(abs(denominator))
        p = []
        for j in range(3):
            replaced = [r[:] for r in rows]
            for k, i in enumerate(triple):
                replaced[k][j] = -h[i][3]
            p.append(det(replaced) / denominator)
        points[triple] = tuple(p)
    four_dets = [abs(det([list(h[i]) for i in quad]))
                 for quad in itertools.combinations(range(n), 4)]
    require(all(four_dets), "four concurrent planes or rank-degenerate quadruple")
    require(len(set(points.values())) == len(points), "coincident arrangement triple points")

    faces, polygons, drops = {}, {}, {}
    corners, edges = defaultdict(list), defaultdict(list)
    for f, link in links.items():
        cycle = [tuple(sorted((f, link[k - 1], link[k]))) for k in range(len(link))]
        require(all(len(set(t)) == 3 for t in cycle), f"collapsed corner in face {f}")
        require(len(set(cycle)) == len(cycle), f"repeated vertex in face {f}")
        polygon = [points[t] for t in cycle]
        require(all(dot(h[f][:3], p) + h[f][3] == 0 for p in polygon), f"nonplanar face {f}")
        drop = next(j for j in range(3) if h[f][j] != 0)
        flat = [project(p, drop) for p in polygon]
        m = len(cycle)
        require(all(orient(flat[k - 1], flat[k], flat[(k + 1) % m]) != 0 for k in range(m)),
                f"collinear consecutive edges in face {f}")
        require(sum(a[0] * b[1] - a[1] * b[0] for a, b in zip(flat, flat[1:] + flat[:1])) != 0,
                f"zero-area face {f}")
        for i, j in itertools.combinations(range(m), 2):
            if j == i + 1 or (i == 0 and j == m - 1):
                continue
            require(not segments_meet(flat[i], flat[(i + 1) % m], flat[j], flat[(j + 1) % m]),
                    f"self-intersection in face {f}, edges {i},{j}")
        faces[f], polygons[f], drops[f] = cycle, polygon, drop
        for k, vertex in enumerate(cycle):
            corners[vertex].append(f)
            a, b = vertex, cycle[(k + 1) % m]
            require(points[a] != points[b], f"zero-length edge in face {f}")
            edges[tuple(sorted((a, b)))].append((f, link[k], a, b))

    vertex_neighbors, vertex_edges = defaultdict(set), defaultdict(list)
    face_constraints, pair_edges = defaultdict(list), defaultdict(list)
    for vertex, incident in corners.items():
        require(sorted(incident) == list(vertex), f"vertex incident-face mismatch {vertex}")
    for edge, incident in edges.items():
        require(len(incident) == 2, f"edge has {len(incident)} incident faces: {edge}")
        f, stated_g, a, b = incident[0]
        g, stated_f, c, d = incident[1]
        require(f != g and (stated_g, stated_f) == (g, f), f"paired edge mismatch {edge}")
        require(set(a) & set(b) == {f, g}, f"wrong supporting plane pair {edge}")
        u, v = edge
        vertex_neighbors[u].add(v)
        vertex_neighbors[v].add(u)
        vertex_edges[u].append((f, g))
        vertex_edges[v].append((f, g))
        factor = -1 if (a, b) == (c, d) else 1
        face_constraints[f].append((g, factor))
        face_constraints[g].append((f, factor))
        pair_edges[tuple(sorted((f, g)))].append(edge)
    require(set(vertex_neighbors) == set(corners), "isolated vertex")
    for vertex in corners:
        require(len(vertex_neighbors[vertex]) == 3, f"noncubic vertex {vertex}")
        require(Counter(tuple(sorted(pair)) for pair in vertex_edges[vertex]) ==
                Counter(itertools.combinations(vertex, 2)), f"vertex link is not a triangle {vertex}")
    reached, todo = set(), [next(iter(corners))]
    while todo:
        vertex = todo.pop()
        if vertex not in reached:
            reached.add(vertex)
            todo.extend(vertex_neighbors[vertex] - reached)
    require(reached == set(corners), "disconnected surface")
    signs, todo = {0: 1}, [0]
    while todo:
        f = todo.pop()
        for g, factor in face_constraints[f]:
            if g in signs:
                require(signs[g] == signs[f] * factor, "nonorientable surface")
            else:
                signs[g] = signs[f] * factor
                todo.append(g)
    require(len(signs) == n, "disconnected face graph")
    require(set(pair_edges) == set(itertools.combinations(range(n), 2)), "missing face adjacency")

    sections_checked = 0
    for f, g in itertools.combinations(range(n), 2):
        direction = cross(h[f][:3], h[g][:3])
        require(any(direction), f"parallel or coincident planes {f},{g}")
        actual = intersect_intervals(section(polygons[f], h[g], direction, drops[f]),
                                     section(polygons[g], h[f], direction, drops[g]))
        expected = merge([tuple(sorted((dot(direction, points[a]), dot(direction, points[b]))))
                          for a, b in pair_edges[f, g]])
        require(actual == expected, f"unintended intersection for faces {f},{g}: {actual} != {expected}")
        sections_checked += 1

    v, e, chi = len(corners), len(edges), len(corners) - len(edges) + n
    require((v, e, n, chi) == (24, 36, 8, -4), "wrong auxiliary topology")
    slacks = [abs(dot(h[f][:3], p) + h[f][3]) for t, p in points.items() for f in range(n) if f not in t]
    edge_sq = [dot(sub(points[a], points[b]), sub(points[a], points[b])) for a, b in edges]
    selected = [points[t] for t in corners]
    vertex_sq = [dot(sub(a, b), sub(a, b)) for a, b in itertools.combinations(selected, 2)]
    return dict(verdict="ACCEPT", evidence="PROVED-1; exact rational computation, pending verify_all reproduction",
                target="auxiliary S1 (8,3); not S5", V_E_F_chi=[v, e, n, chi], genus=(2 - chi) // 2,
                adjacent_pairs=len(pair_edges), excess_edges=e - len(pair_edges),
                multiplicity_histogram=dict(sorted(Counter(map(len, pair_edges.values())).items())),
                repeated_pairs={f"{f},{g}": len(es) for (f, g), es in pair_edges.items() if len(es) > 1},
                face_sizes=[len(faces[f]) for f in range(n)], pair_sections_checked=sections_checked,
                finite_arrangement_vertices=len(points), normal_triples_checked=len(normal_dets),
                plane_quadruples_checked=len(four_dets), min_abs_normal_determinant=min(normal_dets),
                min_abs_plane_determinant=min(four_dets), min_abs_nonincident_plane_value=min(slacks),
                min_squared_edge_length=min(edge_sq), min_squared_vertex_distance=min(vertex_sq),
                rounded_at_1e_9_changes_input=False)


if __name__ == '__main__':
    path = Path(sys.argv[1])
    raw = path.read_bytes()
    try:
        result = check(json.loads(raw))
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        print(json.dumps(dict(verdict="REJECT", error=str(exc))))
        sys.exit(1)
    result['candidate_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, default=str, indent=2))
