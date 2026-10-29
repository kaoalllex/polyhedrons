import sys, json, numpy as np, time
sys.path.insert(0,'/home/user/polyhedrons/research/12-faced-polyhedron/code')
from period_defect import surface_edges, random_cocycle, torus_defect
from gauss_search import find_admissible
from gauss_degree import coherent_triangles
types=json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))
for tid in (0,58):
    tri=types[tid]['triangles']; G,_=find_admissible(coherent_triangles(tri),np.random.default_rng(tid),minutes=1)
    edges,faces,nv=surface_edges(G,tri); rng=np.random.default_rng(1)
    for trial in range(4):
        if trial==0: vals=[(1,0,0),(0,1,0),(0,0,1)]+[(0,0,0)]*9
        else: vals=[tuple(int(x) for x in rng.integers(-1,2,size=3)) for _ in range(12)]
        phi,gens=random_cocycle(edges,faces,nv,vals,seed=trial)
        t=time.time(); v,st,L=torus_defect(G,tri,phi,time_limit=60,general=True,return_L=True)
        print('type',tid,'general lattice wrap',trial,'defect',v,'det(L) %.3g'%(np.linalg.det(L) if L is not None else float('nan')),'%.0fs'%(time.time()-t),flush=True)
