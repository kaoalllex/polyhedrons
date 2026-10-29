import sys, json, numpy as np, time
sys.path.insert(0,'/home/user/polyhedrons/research/12-faced-polyhedron/code')
from period_defect import surface_edges, random_cocycle, torus_defect
from gauss_search import find_admissible
from gauss_degree import coherent_triangles
tid=int(sys.argv[1]); ntr=int(sys.argv[2])
types=json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))
tri=types[tid]['triangles']; G,_=find_admissible(coherent_triangles(tri),np.random.default_rng(tid),minutes=1)
edges,faces,nv=surface_edges(G,tri); rng=np.random.default_rng(100+tid); best=(1e9,None)
for trial in range(ntr):
    vals=[tuple(int(x) for x in rng.integers(-2,3,size=3)) for _ in range(12)]
    phi,gens=random_cocycle(edges,faces,nv,vals,seed=trial)
    v,st,L=torus_defect(G,tri,phi,time_limit=30,general=True,return_L=True)
    d=np.linalg.det(L) if L is not None else 0
    if v is not None and v<best[0]:
        best=(v,vals,d); print('trial',trial,'new best defect %.4f det %.3g'%(v,d),flush=True)
    if v is not None and v<1e-7 and abs(d)>1e-6:
        print('ZERO DEFECT with nondegenerate lattice, trial',trial,'det',d,flush=True)
        json.dump({'type':tid,'normals':G.tolist(),'gen_values':vals,'det':d},open(sys.argv[3],'w')); break
print('best',best[0])
