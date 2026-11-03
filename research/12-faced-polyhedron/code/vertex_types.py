"""Vertex types of realized polyhedra: convex corners, concave corners, saddles (float, NUMERICAL).

A vertex v = X n Y n Z with outward face normals n_X, n_Y, n_Z (coherent polygon orientation, flipped if the signed
volume is negative) and edge directions d (from v to the next vertex along each of its three edges): convex if
n_Z . d < 0 on all three edges, concave if > 0 on all three, saddle otherwise. Controls per record: every vertex of
the convex hull is a convex corner, and the saddle count equals gauss_gate.saddles in the own gauge.

Usage (from research/12-faced-polyhedron/): python3 code/vertex_types.py [FILE.json ...]
  without files: the realization archive of E-261030-10 by genus; FILE: a list of {planes, triangles} records."""
import json, sys, collections
import numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, 'code')
from gauss_gate import face_polygons, unit_planes, own_gauge, int_normals, saddles
from gauss_degree import coherent_triangles, links_from

def classify(planes, tris):
    n = len(planes); H = unit_planes(planes)
    otris = coherent_triangles([tuple(t) for t in tris])
    links = links_from(otris, n)
    polys = face_polygons(H, links)
    A = {X: 0.5 * np.cross(P, np.roll(P, -1, axis=0)).sum(axis=0) for X, P in polys.items()}
    vol = sum(A[X] @ polys[X][0] for X in A) / 3
    if vol < 0:
        A = {X: -a for X, a in A.items()}
    pt = {}
    for t in tris:
        X, Y, Z = t
        M = np.array([H[X][:3], H[Y][:3], H[Z][:3]])
        pt[frozenset(t)] = np.linalg.solve(M, -np.array([H[X][3], H[Y][3], H[Z][3]]))
    by_edge = collections.defaultdict(list)
    for t in tris:
        for a, b in ((t[0], t[1]), (t[0], t[2]), (t[1], t[2])):
            by_edge[frozenset((a, b))].append(frozenset(t))
    kinds = {}
    for t in tris:
        T = frozenset(t); sg = []
        for Z in t:
            e = T - {Z}
            other = [u for u in by_edge[e] if u != T]
            assert len(other) == 1
            sg.append(np.sign(A[Z] @ (pt[other[0]] - pt[T])))
        kinds[T] = 'convex' if all(s < 0 for s in sg) else 'concave' if all(s > 0 for s in sg) else 'saddle'
    c = collections.Counter(kinds.values())
    keys = list(pt); P = np.array([pt[k] for k in keys])
    hull = [keys[i] for i in ConvexHull(P).vertices]
    hull_ok = all(kinds[h] == 'convex' for h in hull)
    s_gauge = saddles(int_normals(H), otris, own_gauge(H, links))
    return c['convex'], c['concave'], c['saddle'], len(hull), hull_ok, s_gauge

def run(label, recs):
    rows = []
    for r in recs:
        tris = r.get('triangles') or [list(map(int, t.split(','))) for t in r['map'].split(';')]
        rows.append(classify(r['planes'], tris))
    bad = [x for x in rows if not x[4] or x[2] != x[5]]
    cv = collections.Counter(x[0] for x in rows); cc = collections.Counter(x[1] for x in rows); sd = collections.Counter(x[2] for x in rows)
    print('%s: n=%d V=%s | convex %s | concave %s | saddles %s | hull vertices %s | control failures %d'
          % (label, len(rows), sorted({x[0]+x[1]+x[2] for x in rows}), dict(sorted(cv.items())), dict(sorted(cc.items())),
             dict(sorted(sd.items())), dict(sorted(collections.Counter(x[3] for x in rows).items())), len(bad)))
    return rows

if __name__ == '__main__':
    for f in sys.argv[1:]:
        run(f, json.load(open(f)))
    if len(sys.argv) == 1:
        arch = json.load(open('experiments/E-261030-10-realization-archive-climb/results/arch/archive.json'))['real']
        for g in (2, 3):
            run('archive genus %d' % g, [r for r in arch if r['genus'] == g])
