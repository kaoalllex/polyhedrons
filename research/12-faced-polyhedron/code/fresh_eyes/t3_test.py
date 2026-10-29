import sys, json, numpy as np, time
sys.path.insert(0,'/home/user/polyhedrons/research/12-faced-polyhedron/code')
from period_defect import surface_edges, random_cocycle, torus_defect, period_defect
from gauss_search import find_admissible
from gauss_degree import coherent_triangles
types=json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))
for tid in (0,58):
    tri=types[tid]['triangles']; G,_=find_admissible(coherent_triangles(tri),np.random.default_rng(tid),minutes=1)
    edges,faces,nv=surface_edges(G,tri)
    zero=[(0,0,0)]*12
    phi0,_=random_cocycle(edges,faces,nv,zero)
    t=time.time(); print('type',tid,'R^3 (phi=0):',torus_defect(G,tri,phi0,time_limit=40),'%.0fs'%(time.time()-t),flush=True)
    rng=np.random.default_rng(1)
    for trial in range(4):
        vals=[tuple(int(x) for x in rng.integers(-1,2,size=3)) for _ in range(12)]
        phi,gens=random_cocycle(edges,faces,nv,vals,seed=trial)
        t=time.time(); print('type',tid,'T^3 wrap',trial,torus_defect(G,tri,phi,time_limit=40),'%.0fs'%(time.time()-t),flush=True)
