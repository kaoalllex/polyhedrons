"""Step 4: arrangement-level local search.
Alternating optimisation:  (i) simulated annealing on the integer plane coefficients with the triangulation T
fixed, objective B(H,T) = edge-face + self-crossing count (violation_profile, exact direct predicates);
(ii) every `reopt` evaluations re-optimise T for the current planes with CP-SAT (warm start = current T; the
encoding minimises the same weighted count).  B(H, T_new) <= B(H, T_old) is guaranteed by the hint only when CP-SAT
finds it; we keep T_new only if its B is not larger.
Asymmetric random starts; no symmetry imposed.   Score 0 => CANDIDATE (saved + direct-checked)."""
import sys, time, json, math
from track4_common import *

def score(H, T, n=12):
    arr = Arrangement(H)
    if not arr.check_general_position():
        return None
    p = violation_profile(arr, T)
    return p["B"], p

def main(seed, dist, minutes, reopt=250, T0=2.0, cp_secs=25, init_secs=40):
    rng = random.Random(seed)
    t_start = time.time()
    arr = random_planes(12, dist, rng, scale=10 ** 5)
    H = [tuple(h) for h in arr.H]
    c, lb, T, st, info = geomsat.solve_cpsat(arr, time_limit=init_secs, workers=1, seed=seed)
    cur, prof = score(H, T)
    best = (cur, H, T, prof)
    log = [dict(t=round(time.time() - t_start, 1), evals=0, B=cur, V=prof["V"], note="init cpsat obj=%s" % c)]
    print(log[-1], flush=True)
    evals = 0
    sinceopt = 0
    tag = f"anneal_{dist}_{seed}"
    while time.time() - t_start < minutes * 60:
        i = rng.randrange(12)
        s = 10 ** rng.uniform(-3.2, -1.0)
        mag = max(abs(x) for x in H[i][:3])
        Hn = list(H)
        Hn[i] = tuple(int(h + round(rng.gauss(0, 1) * s * mag)) for h in H[i])
        if all(x == 0 for x in Hn[i][:3]):
            continue
        r = score(Hn, T)
        evals += 1; sinceopt += 1
        if r is None:
            continue
        sc, pr = r
        frac = (time.time() - t_start) / (minutes * 60)
        temp = T0 * (1 - frac) + 0.05
        if sc <= cur or rng.random() < math.exp(-(sc - cur) / temp):
            H, cur, prof = Hn, sc, pr
            if cur < best[0]:
                best = (cur, H, T, prof)
                print(dict(t=round(time.time() - t_start), evals=evals, B=cur, V=prof["V"], prof=prof), flush=True)
        if sinceopt >= reopt:
            sinceopt = 0
            arr = Arrangement(H)
            c, lb, T2, st, info = geomsat.solve_cpsat(arr, time_limit=cp_secs, workers=1, hint=T, seed=seed + evals)
            if T2 is not None:
                r2 = score(H, T2)
                if r2 and r2[0] <= cur:
                    T, cur, prof = T2, r2[0], r2[1]
                    if cur < best[0]:
                        best = (cur, H, T, prof)
            log.append(dict(t=round(time.time() - t_start), evals=evals, B=cur, V=prof["V"], best=best[0], cp=c))
            print(log[-1], flush=True)
            json.dump(dict(seed=seed, dist=dist, best=best[0], H=best[1], T=best[2], prof=best[3], log=log),
                      open(os.path.join(SCRATCH, tag + ".json"), "w"))
        if best[0] == 0:
            break
    out = dict(seed=seed, dist=dist, best_B=best[0], profile=best[3], H=[list(h) for h in best[1]],
               triangles=[list(t) for t in best[2]], evals=evals, minutes=minutes, log=log)
    if best[0] == 0:
        arr = Arrangement(best[1])
        res = check_embedding(arr, best[2])
        out["CANDIDATE_direct_check"] = dict(ok_triples=res["ok_triples"], ok_pairs=res["ok_pairs"])
        print("CANDIDATE!!", out["CANDIDATE_direct_check"], flush=True)
    fn = os.path.join(HERE, "..", "experiments", f"track4_{tag}.json")
    json.dump(out, open(fn, "w"))
    print("done", best[0], best[3], "evals", evals)

if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2], float(sys.argv[3]))
