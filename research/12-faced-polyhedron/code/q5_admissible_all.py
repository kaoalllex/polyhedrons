"""Q5: can annealing find Gauss-admissible normals for every one of the 59 types?"""
import json, sys, time
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gauss_degree import coherent_triangles
from gauss_search import find_admissible
types = json.load(open(sys.argv[1])); part = int(sys.argv[2]); nparts = int(sys.argv[3])
for e in types:
    if e['id'] % nparts != part:
        continue
    ot = coherent_triangles(e['triangles']); t = time.time()
    res = [find_admissible(ot, np.random.default_rng(s), minutes=0.5)[0] is not None for s in range(3)]
    print(e['id'], 'found', sum(res), '/3', '%.0fs' % (time.time() - t), flush=True)
