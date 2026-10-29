"""Convert HackerPoet/NeighborlyPolyhedra near-miss .obj files into face planes + triangulation.

Usage: python3 -I import_hackerpoet.py REPO_DIR OUT_JSON [MAX_VIOLATIONS]

Each .obj has 44 vertices and 12 faces (11-gons). For each face we fit a plane by SVD
(the source stores float vertices, so planes are only approximately consistent), and for each
vertex we record the triple of faces containing it: the 44 triples form the dual neighborly
triangulation. The file name encodes the source's own counts: shape_c<crossings>_i<intersections>_*.obj
(c = polygon self-crossings, i = edge-face intersections).
"""
import json, os, re, sys
import numpy as np


def parse_obj(path):
    verts, faces = [], []
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if not p:
                continue
            if p[0] == 'v':
                verts.append([float(x) for x in p[1:4]])
            elif p[0] == 'f':
                faces.append([int(x.split('/')[0]) - 1 for x in p[1:]])
    return np.array(verts), faces


def convert(path):
    V, faces = parse_obj(path)
    if len(V) != 44 or len(faces) != 12 or any(len(f) != 11 for f in faces):
        return None
    planes, resid = [], []
    for f in faces:
        P = V[f]
        c = P.mean(axis=0)
        _, s, vt = np.linalg.svd(P - c)
        n = vt[2]
        planes.append([*n.tolist(), float(-n @ c)])      # n.x + d = 0
        resid.append(float(np.abs((P - c) @ n).max()))
    inc = [[] for _ in range(44)]
    for fi, f in enumerate(faces):
        for v in f:
            inc[v].append(fi)
    if any(len(x) != 3 for x in inc):
        return None
    tris = sorted(sorted(x) for x in inc)
    scale = float(np.abs(V).max())
    return {"planes": planes, "triangles": tris, "faces": faces,
            "vertices": V.tolist(), "max_planarity_residual": max(resid) / scale}


def main():
    root, out = sys.argv[1], sys.argv[2]
    maxv = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 9
    recs = []
    for d in sorted(os.listdir(root)):
        if not d.startswith('topology_'):
            continue
        k = int(d.split('_')[1])
        for f in sorted(os.listdir(os.path.join(root, d))):
            m = re.match(r'(shape|study)_c(\d+)_i(\d+)_(.*)\.obj$', f)
            if not m:
                continue
            c, i = int(m.group(2)), int(m.group(3))
            if c + i > maxv:
                continue
            r = convert(os.path.join(root, d, f))
            if r is None:
                print('skip', d, f, file=sys.stderr)
                continue
            r.update({"source": f"{d}/{f}", "hp_topology": k, "hp_crossings": c, "hp_intersections": i})
            recs.append(r)
    with open(out, 'w') as fh:
        json.dump(recs, fh)
    print(len(recs), 'records; max planarity residual (relative):',
          max(r['max_planarity_residual'] for r in recs))


if __name__ == '__main__':
    main()
