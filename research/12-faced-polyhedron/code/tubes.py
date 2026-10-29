"""Count 'tubes' in neighborly triangulations: 6-triangle annuli between two vertex-disjoint
NON-facial 3-cycles A, B (no interior vertices). Removing a tube and capping A, B with triangles
gives a triangulation with the same vertex set and genus one less (6 fewer edges)."""
import json, itertools, sys
from collections import Counter

def tubes(tris, n):
    F = set(frozenset(t) for t in tris)
    found = []
    verts = range(n)
    for A in itertools.combinations(verts, 3):
        if frozenset(A) in F: continue
        rest = [v for v in verts if v not in A]
        for B in itertools.combinations(rest, 3):
            if B < A: continue
            if frozenset(B) in F: continue
            U = set(A) | set(B)
            mixed = [t for t in F if t <= U and (t & set(A)) and (t & set(B))]
            if len(mixed) < 6: continue
            for S in itertools.combinations(mixed, 6):
                c = Counter()
                for t in S:
                    for e in itertools.combinations(sorted(t), 2):
                        c[frozenset(e)] += 1
                ok = True
                for e, k in c.items():
                    inA = e <= set(A); inB = e <= set(B)
                    if (inA or inB) and k != 1: ok = False; break
                    if not (inA or inB) and k != 2: ok = False; break
                if ok and sum(1 for e in c if e <= set(A)) == 3 and sum(1 for e in c if e <= set(B)) == 3:
                    found.append((A, B, [tuple(sorted(t)) for t in S]))
    return found

if __name__ == '__main__':
    # K7 torus control
    k7 = [((i)%7,(i+1)%7,(i+3)%7) for i in range(7)] + [((i)%7,(i+2)%7,(i+3)%7) for i in range(7)]
    t7 = tubes(k7, 7)
    print('K7 torus: tubes =', len(t7), t7[:2])
    d = json.load(open(sys.argv[1]))
    tot = []
    for e in d:
        t = tubes(e['triangles'], 12)
        tot.append(len(t))
    print('59 maps: tubes per map:', tot)
    print('maps with >=1 tube:', sum(1 for x in tot if x), 'of', len(tot), '; total', sum(tot))
