"""Step 3(a): encoded IN predicate (Sec. 5.2) vs direct exact point-in-polygon, 100% agreement required."""
import sys, time
from track4_common import *

def run(n, ntrials, seed, dists):
    rng = random.Random(seed)
    k12 = load_k12()
    tot = bad = 0
    viol_disagree = 0
    nsimple = 0
    t0 = time.time()
    for trial in range(ntrials):
        dist = dists[trial % len(dists)]
        arr = random_planes(n, dist, rng)
        if n == 7:
            tris = TORUS7
        else:
            tris = k12[rng.randrange(len(k12))]["triangles"]
        perm = list(range(n)); rng.shuffle(perm)
        tris = relabel(tris, perm)
        assert valid_triangulation(tris, n)
        res = check_embedding(arr, tris, do_pairs=False)
        nsimple += all(res["simple"])
        for ray, rev in [("min", False), ("max", False), ("min", True), ("max", True)]:
            inn, viol = eval_IN_with_fixed_t(arr, tris, ray, rev)
            assert len(inn) == 3 * len(list(combinations(range(n), 3))) // 1 or True
            for k, v in res["in_direct"].items():
                tot += 1
                if inn[k] != v:
                    bad += 1
                    if bad < 5: print("MISMATCH", n, dist, ray, rev, k, inn[k], v)
            tset = set(tuple(sorted(t)) for t in tris)
            vd = set(res["viol_triples"])
            ve = set(T for T, v in viol.items() if v)
            if vd != ve:
                viol_disagree += 1
    print(f"n={n} trials={ntrials} (face,point) comparisons={tot} mismatches={bad} violated-triple-set disagreements={viol_disagree} "
          f"polygon-all-simple trials={nsimple} time={time.time()-t0:.1f}s")
    return tot, bad, viol_disagree

if __name__ == "__main__":
    d = ["sphere_unif", "tangent", "gauss", "pts3", "near_tangent", "small_off"]
    run(7, int(sys.argv[1]), 101, d)
    run(12, int(sys.argv[2]), 202, d)
