"""Power check of the V2 harness: mutated versions of the Sec. 5.2 predicate must disagree with
the direct exact point-in-polygon.  Usage: python3 test_mutants.py SEED"""
import sys, random, itertools, json
from exact_core import *
from test_v1_v2 import designed_simple_trial


def IN_mut(cf, X, Y, Z, mut):
    part = cf.part
    C, D = part[(X, Y)]
    s = cf.side_chi
    if s(X, Y, C, Z) == -s(X, Y, D, Z):
        return 1
    A, B = part[(X, Z)]
    if mut != "no_eXZ_boundary" and s(X, Z, A, Y) == -s(X, Z, B, Y):
        return 1
    plus = lambda W: cf.later_chi(X, Y, Z, W) > 0
    cnt = 0
    for W in range(cf.n):
        if W in (X, Y, Z) or (W in (C, D) and mut != "CD_in_loop"):
            continue
        if plus(W):
            A, B = part[(X, W)]
            if s(X, W, A, Y) == -s(X, W, B, Y):
                cnt += 1
    if plus(C) and plus(D) and mut != "no_run":
        Cp = other(part[(X, C)], Y)
        Dp = other(part[(X, D)], Y)
        diff = s(X, C, Cp, Y) != s(X, D, Dp, Y)
        if mut == "run_inverted":
            diff = not diff
        if mut == "run_always":
            diff = True
        if diff:
            cnt += 1
    return cnt & 1


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]))
    k12 = load_k12()

    def src12(r):
        tris = k12[r.randrange(59)]["triangles"]
        perm = list(range(12)); r.shuffle(perm)
        return relabel(tris, perm)
    muts = ["none", "no_run", "run_inverted", "run_always", "no_eXZ_boundary", "CD_in_loop"]
    res = {m: {"tests": 0, "mismatch": 0} for m in muts}
    nconf = 0
    while nconf < 150:
        cf = designed_simple_trial(rng, 12, src12(rng), "star" if nconf % 2 else "2opt")
        if not cf.gp:
            continue
        nconf += 1
        poly2 = [cf.to2d(0, v) for v in cf.polygon(0)]
        for Y, Z in itertools.permutations(range(1, 12), 2):
            if cf.is_tri(0, Y, Z):
                continue
            dm, _ = in_face_direct(cf, 0, cf.P(0, Y, Z), poly2)
            for m in muts:
                res[m]["tests"] += 1
                res[m]["mismatch"] += int(IN_mut(cf, 0, Y, Z, m) != dm)
    print(json.dumps(res))
    json.dump(res, open("/home/user/polyhedrons/research/12-faced-polyhedron/verification/test_mutants.json", "w"), indent=1)
