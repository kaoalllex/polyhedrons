"""V3: compare code/fastviol.py (float) with the exact chirotope count on the near-miss seeds
and on random configurations.  Usage: python3 test_v3_fastviol.py SEEDS_JSON NRANDOM SEED"""
import sys, json, time, random, itertools
from fractions import Fraction
import numpy as np
from exact_core import *

sys.path.insert(0, "/home/user/polyhedrons/research/12-faced-polyhedron/code")
import fastviol  # the code under test


def exact_int_planes(planes):
    """Floats -> exact Fractions -> per-plane positive power-of-two scaling to integers."""
    out = []
    for h in planes:
        fr = [Fraction(x) for x in h]  # exact value of the double
        L = 1
        for x in fr:
            L = max(L, x.denominator)  # denominators are powers of two
        out.append([int(x * L) for x in fr])
    return out


def fast_count(Hf, tris):
    part, istri = fastviol.triangulation_tables(len(Hf), tris)
    return int(fastviol.violations(np.array(Hf, dtype=np.float64), part, istri))


def fast_list(Hf, tris):
    part, istri = fastviol.triangulation_tables(len(Hf), tris)
    return set(tuple(t) for t in fastviol.violation_list(np.array(Hf, dtype=np.float64), part, istri))


if __name__ == "__main__":
    seeds = json.load(open(sys.argv[1]))
    NR, seed = int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    res = {"nearmiss": {"n": 0, "ours_field_vs_exact_disagree": 0, "fast_rerun_vs_exact_disagree": 0,
                        "nongp": 0, "disagreements": []},
           "random": {"n": 0, "disagree": 0, "examples": []}}
    t0 = time.time()
    for idx, e in enumerate(seeds):
        H = exact_int_planes(e["planes"])
        cf = Config(H, e["triangles"])
        r = res["nearmiss"]
        r["n"] += 1
        if not cf.gp:
            r["nongp"] += 1
        vx = set(violations_chi(cf))
        fl = fast_list(e["planes"], e["triangles"])
        fc = len(fl)
        if fc != e["ours"]:
            pass
        if e["ours"] != len(vx) or fl != vx:
            r["ours_field_vs_exact_disagree"] += int(e["ours"] != len(vx))
            r["fast_rerun_vs_exact_disagree"] += int(fl != vx)
            r["disagreements"].append({"index": idx, "source": e["source"], "ours": e["ours"], "fast_rerun": fc,
                                       "exact": len(vx), "only_exact": sorted(vx - fl), "only_fast": sorted(fl - vx)})
        if idx % 200 == 0:
            print(idx, round(time.time() - t0, 1), r["ours_field_vs_exact_disagree"], r["fast_rerun_vs_exact_disagree"], flush=True)
    k12 = load_k12()
    for k in range(NR):
        tris = k12[rng.randrange(59)]["triangles"]
        perm = list(range(12)); rng.shuffle(perm)
        tris = relabel(tris, perm)
        H = random_planes(12, rng, R=10**6)
        cf = Config(H, tris)
        if not cf.gp:
            continue
        res["random"]["n"] += 1
        vx = set(violations_chi(cf))
        fl = fast_list([list(map(float, h)) for h in H], tris)
        if vx != fl:
            res["random"]["disagree"] += 1
            if len(res["random"]["examples"]) < 5:
                res["random"]["examples"].append({"H": H, "tris": tris, "only_exact": sorted(vx - fl), "only_fast": sorted(fl - vx)})
    res["time"] = round(time.time() - t0, 1)
    json.dump(res, open("/home/user/polyhedrons/research/12-faced-polyhedron/verification/test_v3_fastviol.json", "w"), indent=1)
    print(json.dumps({k: (v if k != "nearmiss" else {kk: vv for kk, vv in v.items() if kk != "disagreements"}) for k, v in res.items() if k != "random"}))
    print("random", {k: v for k, v in res["random"].items() if k != "examples"})
    print("first disagreements:", json.dumps(res["nearmiss"]["disagreements"][:8]))
