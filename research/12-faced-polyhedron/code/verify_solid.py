"""Independent exact check of a solid-first result: read planes + solid (cells), extract the polyhedron
map (vertices = triple points where three planes carry boundary facets), then verify the polyhedron in
rational arithmetic with ladder_exact.verify (simple faces, every pair of faces meets exactly in its
shared edges or not at all), and report V, E, F, genus and the number of adjacent pairs.
Usage: python3 -I verify_solid.py RESULT_JSON"""
import json, sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import solid_first as SF
from gauss_degree import coherent_triangles, links_from
from ladder_exact import verify

r = json.load(open(sys.argv[1]))
H = np.array(r['planes'], float); n = len(H); S = {tuple(x) for x in r['solid']}
A = SF.Arrangement(H)
tris = SF.extract_map(A, S)
L = links_from(coherent_triangles(tris), n)
adj = sum(1 for X in range(n) for Y in range(X + 1, n) if Y in L[X])
out = verify(A.H.tolist(), L, require_all_pairs=False)
V, E, F, chi = out['V_E_F_chi']
print({'faces': n, 'V': V, 'E': E, 'chi': chi, 'genus': (2 - chi) // 2, 'adjacent_pairs': adj, 'of': n * (n - 1) // 2,
       'simple_faces': out['simple_faces'], 'bad_pairs': out['bad_pairs'], 'EXACT_EMBEDDED': out['EMBEDDED']})
