"""Lemma 5.1 (<=) on genuinely embedded configurations: perturbed Szilassi planes (n = 7).
Planes are fitted exactly (Fractions) through 3 vertices of each face of the model in
/home/user/polyhedrons/index.html (coordinates copied below), then perturbed by random
rationals of relative size eps, and checked for: GP, violation set (chi), direct simplicity and
direct pairwise face intersections (F_X cap F_Y == e_XY)."""
import itertools, random, json, sys
from fractions import Fraction
from exact_core import *

V = [[-1.2, 0, 1.2], [1.2, 0, 1.2], [0, -1.26, -1.2], [0, 1.26, -1.2],
     [0.2, -0.5, -0.8], [-0.2, 0.5, -0.8], [-0.375, -0.375, -0.3], [0.375, 0.375, -0.3],
     [0.45, -0.25, 0.2], [-0.45, 0.25, 0.2], [-0.7, 0, 0.2], [0.7, 0, 0.2], [-0.7, -0.25, 0.2], [0.7, 0.25, 0.2]]
F = [[9, 7, 5, 2, 1, 13], [10, 8, 6, 1, 2, 14], [7, 8, 10, 11, 3, 5],
     [8, 7, 9, 12, 4, 6], [6, 4, 3, 11, 13, 1], [9, 12, 14, 10, 11, 13], [3, 5, 2, 14, 12, 4]]
V = [[Fraction(str(x)) for x in v] for v in V]
F = [[i - 1 for i in f] for f in F]


def plane_through(p, q, r):
    u = [q[i] - p[i] for i in range(3)]
    w = [r[i] - p[i] for i in range(3)]
    nrm = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
    e = -sum(nrm[i] * p[i] for i in range(3))
    return nrm + [e]


def to_int(h):
    from math import lcm
    L = 1
    for x in h:
        L = lcm(L, Fraction(x).denominator)
    return [int(Fraction(x) * L) for x in h]


H0 = []
resid = []
for f in F:
    h = plane_through(V[f[0]], V[f[1]], V[f[2]])
    H0.append([Fraction(x) for x in h])
    resid.append([h[0] * V[i][0] + h[1] * V[i][1] + h[2] * V[i][2] + h[3] for i in f])
tris = sorted({tuple(sorted(i for i, f in enumerate(F) if v in f)) for v in range(14)})
assert len(tris) == 14 and all(len(t) == 3 for t in tris)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
    print("exact planarity residuals (should be 0):", [max(abs(x) for x in r) for r in resid])
    res = {}
    for eps in [Fraction(1, 10**6), Fraction(1, 10**4), Fraction(1, 10**3), Fraction(1, 300), Fraction(1, 100), Fraction(1, 30), Fraction(1, 10)]:
        rec = {"trials": 0, "zero_viol": 0, "zero_viol_embedded": 0, "zero_viol_NOT_embedded": 0,
               "pos_viol": 0, "pos_viol_but_embedded": 0}
        for trial in range(40):
            H = []
            for h in H0:
                scale = max(abs(x) for x in h)
                H.append(to_int([x + scale * eps * Fraction(rng.randint(-1000, 1000), 1000) for x in h]))
            cf = Config(H, tris)
            if not cf.gp:
                continue
            rec["trials"] += 1
            v = violations_chi(cf)
            polys2 = {X: [cf.to2d(X, p) for p in cf.polygon(X)] for X in range(7)}
            emb = all(simple_direct(polys2[X]) for X in range(7)) and all(
                pair_intersection_ok(cf, X, Y, polys2)[0] for X, Y in itertools.combinations(range(7), 2))
            if not v:
                rec["zero_viol"] += 1
                rec["zero_viol_embedded" if emb else "zero_viol_NOT_embedded"] += 1
            else:
                rec["pos_viol"] += 1
                if emb:
                    rec["pos_viol_but_embedded"] += 1
        res[str(eps)] = rec
        print(eps, rec, flush=True)
    json.dump(res, open("/home/user/polyhedrons/research/12-faced-polyhedron/verification/test_szilassi.json", "w"), indent=1)
