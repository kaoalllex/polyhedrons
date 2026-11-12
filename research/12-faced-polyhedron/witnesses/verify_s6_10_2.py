"""Independent rational S6(10,2) filter; no project geometry imports."""
from fractions import Fraction as Q
from itertools import combinations
from collections import defaultdict, deque
from pathlib import Path
import hashlib
import json
import sys
import time


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j * a[0][j] * det([r[:j]+r[j+1:] for r in a[1:]]) for j in range(len(a)))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def mix(a, b, t):
    return tuple(x+(y-x)*t for x, y in zip(a, b))


def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def on(a, b, p):
    return orient(a,b,p)==0 and all(min(x,y)<=z<=max(x,y) for x,y,z in zip(a,b,p))


def segments_meet(a,b,c,d):
    x,y,z,w=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    return (x*y<0 and z*w<0) or any((v==0 and on(p,q,r)) for v,p,q,r in ((x,a,b,c),(y,a,b,d),(z,c,d,a),(w,c,d,b)))


def inside(poly, p):
    winding=0
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if on(a,b,p): return True
        t=orient(a,b,p)
        if a[1]<=p[1]<b[1] and t>0: winding+=1
        if b[1]<=p[1]<a[1] and t<0: winding-=1
    return winding!=0


def check(path):
    started=time.monotonic()
    data=json.loads(path.read_text())
    h=data['planes']; n=len(h)
    assert n==10 and all(all(isinstance(x,int) for x in row) for row in h)
    links={int(f):ns for f,ns in data['links'].items()}
    assert set(links)==set(range(n))
    assert all(len(ns)>=3 and len(ns)==len(set(ns)) and f not in ns for f,ns in links.items())
    assert all(f in links[g] for f,ns in links.items() for g in ns)
    min_d3=min(Q(abs(det([h[i][:3] for i in t])),__import__('math').prod(max(map(abs,h[i][:3])) for i in t)) for t in combinations(range(n),3))
    min_d4=min(Q(abs(det([h[i] for i in t])),__import__('math').prod(max(map(abs,h[i])) for i in t)) for t in combinations(range(n),4))
    assert min_d3>0 and min_d4>0
    corner={f:[tuple(sorted((f,ns[k-1],ns[k]))) for k in range(len(ns))] for f,ns in links.items()}
    vertices=set(t for cs in corner.values() for t in cs)
    xyz={}
    for t in vertices:
        a=[h[i][:3] for i in t]; d=det(a); rhs=[-h[i][3] for i in t]
        xyz[t]=tuple(Q(det([row[:j]+[rhs[k]]+row[j+1:] for k,row in enumerate(a)]),d) for j in range(3))
        assert all(dot(h[f][:3],xyz[t])+h[f][3]==0 for f in t)
        assert all(dot(h[f][:3],xyz[t])+h[f][3]!=0 for f in range(n) if f not in t)
    assert len(set(xyz.values()))==len(vertices)
    edge_faces=defaultdict(list); incidence=defaultdict(list)
    polygons={}; projections={}
    for f,cs in corner.items():
        assert len(cs)==len(set(cs))
        for t in cs: incidence[t].append(f)
        axis=max(range(3),key=lambda k:abs(h[f][k]))
        projections[f]=tuple(k for k in range(3) if k!=axis)
        poly=[tuple(xyz[t][k] for k in projections[f]) for t in cs]; polygons[f]=poly
        for i,(u,v) in enumerate(zip(cs,cs[1:]+cs[:1])):
            assert u!=v
            edge_faces[tuple(sorted((u,v)))].append((f,u,v))
            assert orient(poly[i-1],poly[i],poly[(i+1)%len(poly)])!=0
        for i,j in combinations(range(len(poly)),2):
            if (i-j)%len(poly) in (1,len(poly)-1): continue
            assert not segments_meet(poly[i],poly[(i+1)%len(poly)],poly[j],poly[(j+1)%len(poly)]),('self crossing',f,i,j)
    assert all(sorted(fs)==list(t) for t,fs in incidence.items())
    assert all(len(fs)==2 for fs in edge_faces.values())
    v_edges=defaultdict(list); pair_edges=defaultdict(list)
    orient_edges=defaultdict(list)
    for e,fs in edge_faces.items():
        (f,u,v),(g,s,t)=fs
        assert {f,g}==set(e[0]) & set(e[1])
        assert {u,v}=={s,t}
        pair_edges[tuple(sorted((f,g)))].append(e)
        relation=-1 if (u,v)==(s,t) else 1
        orient_edges[f].append((g,relation)); orient_edges[g].append((f,relation))
        for q in e: v_edges[q].append(e)
    assert all(len(es)==1 for es in pair_edges.values())
    assert set(pair_edges)=={tuple(sorted((f,g))) for f,ns in links.items() for g in ns}
    assert all(len(es)==3 for es in v_edges.values())
    for v,es in v_edges.items():
        pairs={tuple(sorted(fs[0][0:1]+fs[1][0:1])) for e in es for fs in [edge_faces[e]]}
        assert pairs==set(combinations(v,2))
    orientation={0:1}; todo=[0]
    while todo:
        f=todo.pop()
        for g,rel in orient_edges[f]:
            want=orientation[f]*rel
            if g in orientation: assert orientation[g]==want
            else: orientation[g]=want; todo.append(g)
    assert len(orientation)==n
    V,E,F=len(vertices),len(edge_faces),n
    assert (V,E,F,V-E+F)==(24,36,10,-2)
    pair_checks=0; sample_checks=0
    for f,g in combinations(range(n),2):
        direction=cross(h[f][:3],h[g][:3]); axis=next(k for k in range(3) if direction[k])
        breaks={}
        for a,b in ((f,g),(g,f)):
            ps=[xyz[t] for t in corner[a]]
            for u,v in zip(ps,ps[1:]+ps[:1]):
                du=dot(h[b][:3],u)+h[b][3]; dv=dot(h[b][:3],v)+h[b][3]
                if du==0: breaks[u[axis]]=u
                if dv==0: breaks[v[axis]]=v
                if du*dv<0:
                    p=mix(u,v,du/(du-dv)); breaks[p[axis]]=p
        shared=pair_edges.get((f,g),[])
        bounds=None
        if shared:
            a,b=shared[0]; bounds=sorted((xyz[a][axis],xyz[b][axis]))
            assert bounds[0]<bounds[1]
        keys=sorted(breaks)
        samples=[breaks[k] for k in keys]+[mix(breaks[a],breaks[b],Q(1,2)) for a,b in zip(keys,keys[1:])]
        for p in samples:
            inside_both=all(inside(polygons[a],tuple(p[k] for k in projections[a])) for a in (f,g))
            expected=bounds is not None and bounds[0]<=p[axis]<=bounds[1]
            assert inside_both==expected,('unintended face intersection',f,g,p,inside_both,expected)
            sample_checks+=1
        pair_checks+=1
    edge_squared=[dot(sub(xyz[a],xyz[b]),sub(xyz[a],xyz[b])) for a,b in edge_faces]
    vertex_squared=[dot(sub(a,b),sub(a,b)) for a,b in combinations(xyz.values(),2)]
    return dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),verdict='ACCEPT',target='S6(10,2)',counts=dict(V=V,E=E,F=F,chi=-2,genus=2,adjacent_pairs=len(pair_edges)),face_sizes=sorted(map(len,corner.values())),face_pair_checks=pair_checks,line_sample_checks=sample_checks,all_vertices_distinct=True,all_edges_positive=True,all_faces_simple=True,cubic=True,closed=True,connected=True,orientable=True,no_four_planes_concurrent=True,no_triple_normals_dependent=True,unintended_intersections=0,min_edge_squared=str(min(edge_squared)),min_vertex_distance_squared=str(min(vertex_squared)),normalized_min_abs_det3=str(min_d3),normalized_min_abs_det4=str(min_d4),seconds=round(time.monotonic()-started,3),scope='Independent exact-arithmetic filter. No novelty or minimality proof; not human review.')


def controls():
    square=[(Q(0),Q(0)),(Q(2),Q(0)),(Q(2),Q(2)),(Q(0),Q(2))]
    assert inside(square,(Q(1),Q(1)))
    assert inside(square,(Q(0),Q(1)))
    assert not inside(square,(Q(3),Q(1)))
    assert segments_meet((0,0),(2,2),(0,2),(2,0))
    assert segments_meet((0,0),(2,0),(1,0),(3,0))
    assert not segments_meet((0,0),(1,0),(2,0),(3,0))
    assert det([[1,2,3],[0,1,4],[5,6,0]])==1


if __name__=='__main__':
    controls()
    for name in sys.argv[1:]: print(json.dumps(check(Path(name))),flush=True)
