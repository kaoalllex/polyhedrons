import numpy as np, itertools
rng=np.random.default_rng(1)
V=np.array([[-1.2,0,1.2],[1.2,0,1.2],[0,-1.26,-1.2],[0,1.26,-1.2],[0.2,-0.5,-0.8],[-0.2,0.5,-0.8],
 [-0.375,-0.375,-0.3],[0.375,0.375,-0.3],[0.45,-0.25,0.2],[-0.45,0.25,0.2],[-0.7,0,0.2],[0.7,0,0.2],[-0.7,-0.25,0.2],[0.7,0.25,0.2]])
F=[[9,7,5,2,1,13],[10,8,6,1,2,14],[7,8,10,11,3,5],[8,7,9,12,4,6],[6,4,3,11,13,1],[9,12,14,10,11,13],[3,5,2,14,12,4]]
F=[[i-1 for i in f] for f in F]; nF=len(F)
# planes
P=[]
for f in F:
    X=V[f]; c=X.mean(0); u,s,vt=np.linalg.svd(X-c); n=vt[2]; P.append((n,n@c)); assert s[2]<1e-2,(s)
# orient faces consistently (BFS)
def edges(f): return {(f[k],f[(k+1)%len(f)]) for k in range(len(f))}
done={0}; todo=[0]
while todo:
    i=todo.pop()
    for j in range(nF):
        if j in done: continue
        und={frozenset(e) for e in edges(F[i])}&{frozenset(e) for e in edges(F[j])}
        if und:
            if edges(F[i])&edges(F[j]): F[j]=F[j][::-1]
            done.add(j); todo.append(j)
E={}
for i,f in enumerate(F):
    for k in range(len(f)):
        a,b=f[k],f[(k+1)%len(f)]; E[(a,b)]=i
assert all((b,a) in E for (a,b) in E), "not consistently oriented"
def proj2(n,X):
    a=np.cross(n,[1,0,0]) if abs(n[0])<.9 else np.cross(n,[0,1,0]); a/=np.linalg.norm(a); b=np.cross(n,a); return np.c_[X@a,X@b]
def area(n,f):
    Q=proj2(n,V[f]); return 0.5*sum(Q[k,0]*Q[(k+1)%len(f),1]-Q[(k+1)%len(f),0]*Q[k,1] for k in range(len(f)))
N=[]
for i,f in enumerate(F):
    n,d=P[i]; W=np.sign(area(n,f)); N.append(W*n)   # gauge normal: walk is CCW around N
N=np.array(N)
def turn(i,k):
    f=F[i]; a,b,c=V[f[k-1]],V[f[k]],V[f[(k+1)%len(f)]]; return np.sign(np.dot(N[i],np.cross(b-a,c-b)))
# faces at each vertex, ordered: in face X the edge before v is shared with Y, after v with Z
refl={}
for i,f in enumerate(F):
    for k,v in enumerate(f): refl[(i,v)]=(turn(i,k)<0)
def face_of_edge(a,b): return E[(a,b)]
tri={}
for i,f in enumerate(F):
    for k,v in enumerate(f):
        prev,nxt=f[k-1],f[(k+1)%len(f)]
        Y=face_of_edge(v,prev)   # other face on edge (prev,v): it traverses (v,prev)
        Z=face_of_edge(nxt,v)
        tri.setdefault(v,[]).append((i,Y,Z))
nsad=0; ok=True
for v,ts in tri.items():
    X,Y,Z=ts[0]; dt=np.sign(np.linalg.det(np.array([N[X],N[Y],N[Z]])))
    r=[refl[(t[0],v)] for t in ts]; 
    if sum(r)>1: ok=False
    if (sum(r)%2==1)!=(dt<0): ok=False
    nsad+= (dt<0)
print("at-most-one-reflex & (saddle <=> det(N)<0):",ok,"  saddles:",nsad,"of",len(tri))
print("reflex corners per face:",[sum(refl[(i,v)] for v in F[i]) for i in range(nF)])
# Gauss degree with oriented triangles (X,Y,Z)
T=sorted({tuple(ts[0]) for ts in tri.values()})
def deg(m):
    s=0
    for (X,Y,Z) in T:
        M=np.array([N[X],N[Y],N[Z]]).T; c=np.linalg.solve(M,m)
        if (c>0).all(): s+=np.sign(np.linalg.det(M))
    return s
print("Gauss degree at random directions:",[deg(rng.normal(size=3)) for _ in range(6)])
print("degree at -N_W:",[deg(-N[w]) for w in range(nF)])
# point-in-solid by ray casting
def in_poly3(i,p):
    n,d=P[i]; f=F[i]; Q=proj2(n,V[f]); q=proj2(n,p[None])[0]; c=False
    for k in range(len(f)):
        (x1,y1),(x2,y2)=Q[k],Q[(k+1)%len(f)]
        if (y1>q[1])!=(y2>q[1]) and q[0]< x1+(q[1]-y1)*(x2-x1)/(y2-y1): c=not c
    return c
def inside(p):
    r=rng.normal(size=3); cnt=0
    for i in range(nF):
        n,d=P[i]; t=(d-n@p)/(n@r)
        if t>0 and in_poly3(i,p+t*r): cnt+=1
    return cnt%2==1
lam=[]
for i,f in enumerate(F):
    # interior point: try centroids of corner triangles
    for k in range(len(f)):
        c=(V[f[k-1]]+V[f[k]]+V[f[(k+1)%len(f)]])/3
        if in_poly3(i,c): break
    lam.append(inside(c+1e-4*N[i]))
print("gauge normal points inward? per face:",lam)
# edge convexity
kap={}
for (a,b),X in E.items():
    if a>b: continue
    Y=E[(b,a)]; m=(V[a]+V[b])/2; e=V[b]-V[a]
    uX=np.cross(N[X],e); uX*= 1 if in_poly3(X,m+1e-4*uX/np.linalg.norm(uX)) else -1
    uY=np.cross(N[Y],e); uY*= 1 if in_poly3(Y,m+1e-4*uY/np.linalg.norm(uY)) else -1
    kap[frozenset((X,Y))]=inside(m+1e-4*(uX/np.linalg.norm(uX)+uY/np.linalg.norm(uY)))
print("convex edges:",sum(kap.values()),"of",len(kap))
rule=True
for v,ts in tri.items():
    X,Y,Z=ts[0]; dt=np.linalg.det(np.array([N[X],N[Y],N[Z]]))
    ks={kap[frozenset((X,Y))],kap[frozenset((Y,Z))],kap[frozenset((X,Z))]}
    if (len(ks)==1)!=(dt>0): rule=False
print("edge-type rule (all 3 edges same type <=> corner vertex):",rule)
# symmetry: half-turn about z
R=np.diag([-1,-1,1]); perm=[int(np.argmin(np.linalg.norm(V-R@v,axis=1))) for v in V]
fperm=[ [j for j,g in enumerate(F) if set(g)=={perm[x] for x in f}][0] for f in F]
print("C2 face permutation:",fperm, " fixed faces:",[i for i in range(nF) if fperm[i]==i])
print("fixed face normal:",[np.round(P[i][0],3) for i in range(nF) if fperm[i]==i])
# supporting planes
print("face planes supporting the polyhedron:",[i for i in range(nF) if len({np.sign(np.round(P[i][0]@x-P[i][1],6)) for x in V}-{0})==1])
# chambers in the solid
pts=rng.uniform(-1.4,1.4,size=(20000,3)); ch={}
for p in pts:
    key=tuple(int(np.sign(P[i][0]@p-P[i][1])) for i in range(nF)); ch.setdefault(key,set()).add(inside(p))
mixed=[k for k,s in ch.items() if len(s)>1]
print("chambers sampled:",len(ch)," inside chambers:",sum(1 for s in ch.values() if s=={True})," mixed(should be 0):",len(mixed))
print("degree at -N_W + tiny perturbation:",[deg(-N[w]+1e-7*rng.normal(size=3)) for w in range(nF)])
print("degenerate normal triples det(N)=0:",[t for t in itertools.combinations(range(nF),3) if abs(np.linalg.det(N[list(t)]))<1e-9])
