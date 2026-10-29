"""Verify a list of 12-vertex triangulations (lines 'no.NN abc def ...', hex vertex labels).
Usage: python3 -I verify_59.py LIST [OTHER_LIST_TO_CROSS_MAP]   (LIST: 'no.NN hex...' lines or Lutz manifold_lex format)
Checks: 44 triangles, 66 edges each in 2 triangles, vertex links 11-cycles, orientable,
computes automorphism group order (incl. reflections) and canonical form; reports isomorphism classes."""
import sys, re, itertools, collections
SAGE="014 018 023 027 036 049 056 05b 07a 08a 09b 125 126 137 139 147 15a 16b 18b 19a 23b 248 24a 258 269 279 2ab 345 34b 35a 367 389 38a 459 46a 46b 478 568 579 57b 67a 689 78b 9ab".split()
def parse(ws): return [tuple(int(c,16) for c in w) for w in ws]
def check(T):
    if len(T)!=44 or len(set(map(frozenset,T)))!=44: return "triangle count"
    E=collections.defaultdict(list)
    for t in T:
        for e in itertools.combinations(sorted(t),2): E[e].append(t)
    if len(E)!=66 or any(len(v)!=2 for v in E.values()): return "edge structure"
    for v in range(12):
        g=collections.defaultdict(list)
        for t in T:
            if v in t:
                a,b=[x for x in t if x!=v]; g[a].append(b); g[b].append(a)
        if len(g)!=11 or any(len(x)!=2 for x in g.values()): return "link"
        seen={0 if 0!=v else 1}; st=list(seen)
        while st:
            x=st.pop()
            for y in g[x]:
                if y not in seen: seen.add(y); st.append(y)
        if len(seen)!=11: return "link not a single cycle"
    # orientability
    ori={T[0]:1}; st=[T[0]]
    def dir_edges(t,s):
        a,b,c=t
        return {(a,b),(b,c),(c,a)} if s==1 else {(b,a),(c,b),(a,c)}
    while st:
        t=st.pop(); de=dir_edges(t,ori[t])
        for e in itertools.combinations(sorted(t),2):
            for u in E[e]:
                if u is t: continue
                d=e if e in de else (e[1],e[0])
                s=1 if (d[1],d[0]) in dir_edges(u,1) else -1
                if u in ori:
                    if ori[u]!=s: return "not orientable"
                else: ori[u]=s; st.append(u)
    return "ok"
def canon_all(T):
    E=collections.defaultdict(list)
    for t in T:
        for e in itertools.combinations(sorted(t),2): E[frozenset(e)].append(frozenset(t))
    def third(x,y,tri):
        for u in E[frozenset((x,y))]:
            if u!=tri: return next(iter(u-{x,y})), u
    forms=[]
    for t in T:
        for (a,b,c) in itertools.permutations(t):
            lab={a:0,b:1,c:2}; q=[(a,b,c)]; i=0; seen={frozenset(t)}
            while i<len(q):
                x,y,z=q[i]; i+=1
                for (p,r,o) in ((x,y,z),(y,z,x),(z,x,y)):
                    w,u=third(p,r,frozenset((x,y,z)))
                    if w not in lab: lab[w]=len(lab)
                    if u not in seen: seen.add(u); q.append((r,p,w))
            forms.append(tuple(sorted(tuple(sorted(lab[v] for v in tr)) for tr in seen)))
    return forms
def load(path):
    txt=open(path).read()
    if txt.lstrip().startswith("manifold_lex"):   # Lutz format, 1-indexed vertices
        out=[]
        for m in re.finditer(r"(manifold_lex_[^=]*#(\d+))=\[(.*?)\]\]", txt, re.S):
            tris=re.findall(r"\[(\d+),(\d+),(\d+)\]", m.group(3)+"]")
            out.append(["#"+m.group(2)]+["".join("0123456789ab"[int(x)-1] for x in t) for t in tris])
        return out
    return [l.split() for l in txt.splitlines() if l.strip()]
def main():
    lines=load(sys.argv[1])
    res=[]
    for l in lines:
        T=parse(l[1:]); st=check(T)
        f=canon_all(T) if st=="ok" else []
        c=min(f) if f else None
        res.append((l[0],st,c,f.count(c) if f else 0))
    print("entries:",len(res)," all ok:",all(r[1]=="ok" for r in res))
    print("distinct canonical forms:",len(set(r[2] for r in res)))
    print("automorphism orders (incl. reflections) by entry:")
    print(", ".join(f"{r[0]}:{r[3]}" for r in res))
    cnt=collections.Counter(r[3] for r in res); print("order histogram:",sorted(cnt.items()))
    if len(sys.argv)>2:   # cross-compare with a second list
        other=load(sys.argv[2]); oc={min(canon_all(parse(l[1:]))):l[0] for l in other}
        print("cross-map (first list -> second list):",", ".join(f"{r[0]}->{oc.get(r[2],'NONE')}" for r in res))
    sc=min(canon_all(parse(SAGE)))
    m=[r[0] for r in res if r[2]==sc]; print("Sage GenusSix() (ABS96 #58) matches entries:",m)
main()
