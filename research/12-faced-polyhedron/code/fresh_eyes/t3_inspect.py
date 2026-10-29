import sys, json, numpy as np
sys.path.insert(0,'/home/user/polyhedrons/research/12-faced-polyhedron/code')
from period_defect import surface_edges, random_cocycle, torus_defect
types=json.load(open('/home/user/polyhedrons/research/12-faced-polyhedron/data/k12_triangulations.json'))
def seg_x(a,b,c,d):
    o=lambda p,q,r:(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return o(a,b,c)*o(a,b,d)<0 and o(c,d,a)*o(c,d,b)<0
for f in sys.argv[1:]:
    D=json.load(open(f)); tid=D['type']; tri=types[tid]['triangles']; G=np.array(D['normals'])
    G=G/np.linalg.norm(G,axis=1)[:,None]
    edges,faces,nv=surface_edges(G,tri)
    trials=[i for i in range(100)]
    # reproduce the cocycle (seed = trial index used in the sweep is unknown here; search by gen_values)
    for seed in range(100):
        phi,gens=random_cocycle(edges,faces,nv,[tuple(v) for v in D['gen_values']],seed=seed)
        v,st,L,sol=torus_defect(G,tri,phi,time_limit=30,general=True,return_L='full')
        if v is not None and v<1e-7 and abs(np.linalg.det(L))>1e-6: break
    a=sol['a']; E=sol['E']; ed=sol['edges']
    nsimple=0; info=[]
    for X,lst in faces.items():
        # walk the face boundary accumulating edge vectors in face order
        pts=[np.zeros(3)]
        for e,s in lst:
            j=E.index(e); pts.append(pts[-1]+s*a[j]*ed[e][2])
        closure=np.linalg.norm(pts[-1]); P=np.array(pts[:-1])
        g=G[X]; u=np.cross(g,[1,0,0] if abs(g[0])<0.9 else [0,1,0]); u/=np.linalg.norm(u); w=np.cross(g,u)
        Q=[(p@u,p@w) for p in P]; m=len(Q)
        cr=sum(1 for i in range(m) for j in range(i+2,m) if not(i==0 and j==m-1) and seg_x(Q[i],Q[(i+1)%m],Q[j],Q[(j+1)%m]))
        nsimple+= cr==0; info.append(cr)
    print(f,'type',tid,'det L %.1f'%np.linalg.det(L),'faces simple',nsimple,'/12; crossings per face',info,'| edge lengths min %.2f max %.1f'%(np.abs(a).min(),np.abs(a).max()))
