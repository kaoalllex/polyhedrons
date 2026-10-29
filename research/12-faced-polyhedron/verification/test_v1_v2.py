"""V1(b), V1(c), V2 tests (exact).  Usage: python3 test_v1_v2.py N12 N7 NSIMPLE SEED
Prints a JSON summary on the last line."""
import sys, json, time, random, itertools
from fractions import Fraction
from exact_core import *


def check_config(cf, stats, do_pairs=True):
    n = cf.n
    polys3 = {X: cf.polygon(X) for X in range(n)}
    polys2 = {X: [cf.to2d(X, v) for v in polys3[X]] for X in range(n)}
    simple = {X: simple_direct(polys2[X]) for X in range(n)}
    # V1(c): side formula on all (triple, plane) pairs; order formula on all lines
    for a, b, c in itertools.combinations(range(n), 3):
        for d in range(n):
            if d in (a, b, c):
                continue
            stats["side_tests"] += 1
            for perm in ((a, b, c), (b, c, a), (c, b, a)):
                if cf.side_chi(*perm, d) != cf.side_geo(a, b, c, d):
                    stats["side_fail"] += 1
    for X, Y in itertools.permutations(range(n), 2):
        others = [W for W in range(n) if W not in (X, Y)]
        for Z, W in itertools.permutations(others, 2):
            stats["order_tests"] += 1
            tZ = cf.t(X, Y, cf.P(X, Y, Z))
            tW = cf.t(X, Y, cf.P(X, Y, W))
            # direction u* = n_Y x n_X = -(n_X x n_Y): formula claims sign(t*_W - t*_Z) = later_chi
            if sgn(-(tW - tZ)) != cf.later_chi(X, Y, Z, W):
                stats["order_fail_ustar"] += 1
            if sgn(tW - tZ) != cf.later_chi(X, Y, Z, W):
                stats["order_fail_nxny"] += 1
    # V2: IN predicate vs direct point-in-polygon, all non-triangle triples, all 3 faces
    direct_member = {}
    for a, b, c in itertools.combinations(range(n), 3):
        if cf.is_tri(a, b, c):
            continue
        for X, Y, Z in ((a, b, c), (b, c, a), (c, a, b)):
            p = cf.P(a, b, c)
            dm, (on, par, wn) = in_face_direct(cf, X, p, polys2[X])
            direct_member[(X, Y, Z)] = dm
            i1 = IN_chi(cf, X, Y, Z)
            i2 = IN_chi(cf, X, Y, Z, reverse=True)
            i3 = IN_chi(cf, X, Z, Y)        # ray along L_XZ instead of L_XY
            key = "simple" if simple[X] else "nonsimple"
            stats["in_tests_" + key] += 1
            if not (i1 == i2 == i3 == dm):
                stats["in_fail_" + key] += 1
                if len(stats["in_fail_examples"]) < 5:
                    stats["in_fail_examples"].append(
                        {"H": cf.H, "tris": cf.tris, "XYZ": (X, Y, Z), "chi": (i1, i2, i3), "direct": dm})
            if not on:
                if wn % 2 == 0 and wn != 0:
                    stats["even_nonzero_winding"] += 1   # nonzero rule != parity rule
                if (wn != 0) != bool(par):
                    stats["nonzero_vs_parity_differ"] += 1
    # violation sets, both ways
    vdir = set()
    for a, b, c in itertools.combinations(range(n), 3):
        if not cf.is_tri(a, b, c):
            if direct_member[(a, b, c)] and direct_member[(b, c, a)] and direct_member[(c, a, b)]:
                vdir.add((a, b, c))
    vchi = set(violations_chi(cf))
    if vdir != vchi:
        stats["violset_fail"] += 1
    stats["viol_hist"][len(vdir)] = stats["viol_hist"].get(len(vdir), 0) + 1
    # V1(b): Lemma 5.1 mechanics
    # (i) every non-simple polygon X has a violated triple {X,W1,W2} at each crossing
    for X in range(n):
        if not simple[X]:
            stats["nonsimple_faces"] += 1
            if not any(X in T for T in vdir):
                stats["lemma_nonsimple_without_violation"] += 1
    if do_pairs:
        for X, Y in itertools.combinations(range(n), 2):
            ok, bad = pair_intersection_ok(cf, X, Y, polys2)
            stats["pairs_tested"] += 1
            covered = any(X in T and Y in T for T in vdir)
            if not ok:
                stats["bad_pairs"] += 1
                if not covered:
                    stats["lemma_badpair_without_violation"] += 1
                    if len(stats["lemma_examples"]) < 5:
                        stats["lemma_examples"].append({"H": cf.H, "tris": cf.tris, "pair": (X, Y), "bad": str(bad)[:300]})
            if covered and ok:
                # a violated triple containing X and Y forces F_X cap F_Y != e_XY unless the
                # point is on e_XY; record for information
                stats["covered_but_pair_ok"] += 1
        if not vdir:
            stats["zero_violation_configs"] += 1
            allok = all(simple.values()) and all(
                pair_intersection_ok(cf, X, Y, polys2)[0] for X, Y in itertools.combinations(range(n), 2))
            if not allok:
                stats["zero_viol_but_not_embedded"] += 1


def new_stats():
    return {k: 0 for k in ["side_tests", "side_fail", "order_tests", "order_fail_ustar", "order_fail_nxny",
                           "in_tests_simple", "in_fail_simple", "in_tests_nonsimple", "in_fail_nonsimple",
                           "even_nonzero_winding", "nonzero_vs_parity_differ", "violset_fail",
                           "nonsimple_faces", "lemma_nonsimple_without_violation", "pairs_tested", "bad_pairs",
                           "lemma_badpair_without_violation", "covered_but_pair_ok", "zero_violation_configs",
                           "zero_viol_but_not_embedded", "configs", "nongp_skipped"]} | {
        "in_fail_examples": [], "lemma_examples": [], "viol_hist": {}}


def run_random(n, ntrials, rng, tri_source, dists, do_pairs=True, budget=None):
    st = new_stats()
    t0 = time.time()
    for k in range(ntrials):
        if budget and time.time() - t0 > budget:
            break
        dist = dists[k % len(dists)]
        while True:
            H = random_planes(n, rng, dist=dist)
            tris = tri_source(rng)
            cf = Config(H, tris)
            if cf.gp:
                break
            st["nongp_skipped"] += 1
        st["configs"] += 1
        check_config(cf, st, do_pairs=do_pairs)
    st["time"] = round(time.time() - t0, 1)
    return st


# ---------------------------------------------------------------- designed simple faces (2D lift)

def random_simple_polygon(m, rng, R=60, kind="star"):
    while True:
        if kind == "star":
            import math
            angs = sorted(rng.random() * 2 * math.pi for _ in range(m))
            pts = [(int(round(math.cos(a) * rng.uniform(0.2, 1) * R)), int(round(math.sin(a) * rng.uniform(0.2, 1) * R)))
                   for a in angs]
        else:  # 2-opt untangling of a random cyclic order
            pts = [(rng.randint(-R, R), rng.randint(-R, R)) for _ in range(m)]
            changed = True
            it = 0
            while changed and it < 2000:
                changed = False
                it += 1
                for i in range(m):
                    for j in range(i + 2, m):
                        if i == 0 and j == m - 1:
                            continue
                        a, b, c, d = pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]
                        if segments_intersect(a, b, c, d):
                            pts[i + 1:j + 1] = reversed(pts[i + 1:j + 1])
                            changed = True
        if len(set(pts)) < m:
            continue
        if any(cross(*tr) == 0 for tr in itertools.combinations(pts, 3)):
            continue
        if simple_direct(pts):
            return pts


def designed_simple_trial(rng, n, tris, kind):
    """Face X = 0 lies in z = 0 and is the given random simple polygon (in link order)."""
    cf0 = Config([[1, 2, 3, 4]] * 0 + random_planes(n, rng), tris)  # only for the link
    L = cf0.link[0]
    m = n - 1
    pts = random_simple_polygon(m, rng, kind=kind)
    # vertex i = P(0, L[i], L[i+1]) = pts[i]; line of face L[i] passes through pts[i-1], pts[i]
    H = [None] * n
    H[0] = (0, 0, 1, 0)
    for i in range(m):
        (x1, y1), (x2, y2) = pts[i - 1], pts[i]
        a, b = y2 - y1, x1 - x2
        e = -(a * x1 + b * y1)
        cz = rng.choice([v for v in range(-40, 41) if v != 0])
        H[L[i]] = (a, b, cz, e)
    return Config(H, tris)


def run_designed(ntrials, rng, n, tri_source, budget=None):
    st = {"tests": 0, "fail": 0, "configs": 0, "nongp": 0, "examples": [], "inside": 0}
    t0 = time.time()
    for k in range(ntrials):
        if budget and time.time() - t0 > budget:
            break
        kind = "star" if k % 2 == 0 else "2opt"
        tris = tri_source(rng)
        cf = designed_simple_trial(rng, n, tris, kind)
        if not cf.gp:
            st["nongp"] += 1
            continue
        st["configs"] += 1
        X = 0
        poly2 = [cf.to2d(X, v) for v in cf.polygon(X)]
        assert simple_direct(poly2)
        for Y, Z in itertools.combinations(range(1, n), 2):
            if cf.is_tri(X, Y, Z):
                continue
            p = cf.P(X, Y, Z)
            dm, _ = in_face_direct(cf, X, p, poly2)
            vals = (IN_chi(cf, X, Y, Z), IN_chi(cf, X, Y, Z, True), IN_chi(cf, X, Z, Y), IN_chi(cf, X, Z, Y, True))
            st["tests"] += 1
            st["inside"] += dm
            if any(v != dm for v in vals):
                st["fail"] += 1
                if len(st["examples"]) < 5:
                    st["examples"].append({"H": cf.H, "tris": cf.tris, "XYZ": (X, Y, Z), "chi": vals, "direct": dm})
    st["time"] = round(time.time() - t0, 1)
    return st


if __name__ == "__main__":
    N12, N7, NS, seed = (int(x) for x in sys.argv[1:5])
    rng = random.Random(seed)
    k12 = load_k12()

    def src12(r):
        tris = k12[r.randrange(len(k12))]["triangles"]
        perm = list(range(12)); r.shuffle(perm)
        return relabel(tris, perm)

    def src7(r):
        perm = list(range(7)); r.shuffle(perm)
        return relabel(TORUS7, perm)

    out = {}
    phases = sys.argv[5].split(",") if len(sys.argv) > 5 else ["n7", "n12", "des"]
    if "n7" in phases:
        out["n7_random"] = run_random(7, N7, rng, src7, ["cube", "tangent", "small"], budget=150)
        print("n7", json.dumps({k: v for k, v in out["n7_random"].items() if "example" not in k}), flush=True)
    # NOTE: the "small" distribution (coefficients in [-3,3]) is not used for n = 12: 12 such planes
    # are essentially never in general position (the resampling loop did not terminate).
    out["n12_random"] = run_random(12, N12, rng, src12, ["cube", "tangent"], budget=120)
    print("n12", json.dumps({k: v for k, v in out["n12_random"].items() if "example" not in k}), flush=True)
    out["designed_simple_n12"] = run_designed(NS, rng, 12, src12, budget=90)
    print("des12", json.dumps({k: v for k, v in out["designed_simple_n12"].items() if k != "examples"}), flush=True)
    out["designed_simple_n7"] = run_designed(NS, rng, 7, src7, budget=30)
    print("des7", json.dumps({k: v for k, v in out["designed_simple_n7"].items() if k != "examples"}), flush=True)
    json.dump(out, open(f"/home/user/polyhedrons/research/12-faced-polyhedron/verification/test_v1_v2_seed{seed}_{"-".join(phases)}.json", "w"), indent=1, default=str)
    print("DONE")
