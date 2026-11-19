"""Reconcile check: C3 extra-edge demand classes at (9, 4) and admissible fixed-triangle counts."""
import itertools, time
t0 = time.time()
rho = [3*(v//3) + (v+1) % 3 for v in range(9)]
rinv = [rho.index(v) for v in range(9)]
def conj(s, p):  # s p s^-1
    out = [0]*9
    for v in range(9): out[s[v]] = s[p[v]]
    return out
N = [s for s in itertools.permutations(range(9)) if conj(s, rho) in (rho, rinv)]
def porb(p):
    o, q = set(), p
    for _ in range(3):
        o.add(tuple(sorted(q))); q = (rho[q[0]], rho[q[1]])
    return frozenset(o)
orbs = sorted({porb(p) for p in itertools.combinations(range(9), 2)}, key=sorted)
idx = {o: i for i, o in enumerate(orbs)}
def img(s, o):
    return idx[frozenset(tuple(sorted((s[a], s[b]))) for a, b in o)]
perm = [[img(s, o) for o in orbs] for s in N]
dem = [d for d in itertools.combinations_with_replacement(range(len(orbs)), 3) if len(set(d)) > 1]
reps = {min(tuple(sorted(p[i] for i in d)) for p in perm) for d in dem}
# fixed triangles: oriented C3-invariant triangles and their supports
fixed = [t for t in itertools.permutations(range(9), 3) if (rho[t[0]], rho[t[1]], rho[t[2]]) in (t, t[1:]+t[:1], t[2:]+t[:2])]
fixed_or = {min(t, t[1:]+t[:1], t[2:]+t[:2]) for t in fixed}
print(dict(normaliser=len(N), pair_orbits=len(orbs), multisets=len(list(itertools.combinations_with_replacement(range(12), 3))),
           mult_le3=len(dem), classes=len(reps), fixed_oriented=len(fixed_or), fixed_supports=len({frozenset(t) for t in fixed_or}),
           b_allowed=[b for b in range(len({frozenset(t) for t in fixed_or})+1) if (30-b) % 3 == 0], seconds=round(time.time()-t0, 2)))
