"""Step 3(b): n=7 calibration. (i) cross validation SAT vs brute force over the 120 labelled tori with the direct
checker; (ii) fraction of random 7-plane arrangements admitting a Szilassi-type torus; (iii) robustness of Szilassi."""
import sys, time, json
from track4_common import *
from szilassi import szilassi_arr

def crossval(ndist, dists, seed):
    rng = random.Random(seed)
    labs = labelings_torus7()
    assert len(labs) == 120
    out = {}
    for dist in dists:
        n_arr = n_sat = n_disagree = lemma_dis = enc_dis = nok_labels = 0
        t0 = time.time()
        for _ in range(ndist):
            arr = random_planes(7, dist, rng)
            n_arr += 1
            ok_direct = []
            enc = geomsat.GeomEncoding(arr, hard_triples=False)
            S = Solver(name="glucose4", bootstrap_with=enc.clauses)
            for tris in labs:
                r = check_embedding(arr, tris)
                tset = set(tris)
                assum = [v if T in tset else -v for T, v in enc.tv.items()]
                assert S.solve(assumptions=assum)
                m = {abs(l): l > 0 for l in S.get_model()}
                ok_enc = not any((m[abs(v)] if v > 0 else not m[abs(v)]) for v in enc.viol.values())
                if r["ok_triples"] != r["ok_pairs"]:
                    lemma_dis += 1
                if ok_enc != r["ok_triples"]:
                    enc_dis += 1
                if r["ok_pairs"]:
                    ok_direct.append(tris)
            S.delete()
            st, tr, info = geomsat.solve_sat(arr)
            if (st == "SAT") != bool(ok_direct):
                n_disagree += 1
            n_sat += st == "SAT"
            nok_labels += len(ok_direct)
        out[dist] = dict(arrangements=n_arr, sat=n_sat, sat_vs_bruteforce_disagreements=n_disagree,
                         lemma5_1_vs_pairs_disagreements=lemma_dis, encoding_vs_direct_disagreements=enc_dis,
                         valid_labelled_tori_total=nok_labels, secs=round(time.time() - t0, 1))
        print(dist, out[dist], flush=True)
    return out

def crossval_pert(N, seed):
    verts, faces, H, tris0 = szilassi_arr()
    rng = random.Random(seed)
    labs = labelings_torus7()
    res = dict(arr=0, sat=0, sat_vs_bf_dis=0, lemma_dis=0, enc_dis=0, ok_labelings=0, nonok=0)
    for i in range(N):
        rel = [0.02, 0.1, 0.2, 0.3, 0.5][i % 5]
        arr = Arrangement(perturb(H, rel, rng))
        if not arr.check_general_position(): continue
        res["arr"] += 1
        enc = geomsat.GeomEncoding(arr, hard_triples=False)
        S = Solver(name="glucose4", bootstrap_with=enc.clauses)
        anyok = False
        for tris in labs:
            r = check_embedding(arr, tris)
            tset = set(tris)
            assum = [v if T in tset else -v for T, v in enc.tv.items()]
            assert S.solve(assumptions=assum)
            m = {abs(l): l > 0 for l in S.get_model()}
            ok_enc = not any((m[abs(v)] if v > 0 else not m[abs(v)]) for v in enc.viol.values())
            res["lemma_dis"] += r["ok_triples"] != r["ok_pairs"]
            res["enc_dis"] += ok_enc != r["ok_triples"]
            res["ok_labelings"] += r["ok_pairs"]; res["nonok"] += not r["ok_pairs"]
            anyok |= r["ok_pairs"]
        S.delete()
        st, tr, info = geomsat.solve_sat(arr)
        res["sat"] += st == "SAT"
        res["sat_vs_bf_dis"] += (st == "SAT") != anyok
        print(i, rel, st, anyok, res, flush=True)
    return res

def fractions(N, dists, seed):
    out = {}
    for dist in dists:
        rng = random.Random(seed)
        t0 = time.time(); sat = 0; dis = 0
        for _ in range(N):
            arr = random_planes(7, dist, rng)
            st, tr, info = geomsat.solve_sat(arr)
            if st == "SAT":
                sat += 1
                if "DISAGREEMENT" in info or not info["direct_ok_pairs"]:
                    dis += 1
        out[dist] = dict(N=N, sat=sat, frac=sat / N, direct_disagreements=dis, secs=round(time.time() - t0, 1))
        print(dist, out[dist], flush=True)
    return out

def robustness(N, seed):
    verts, faces, H, tris = szilassi_arr()
    rng = random.Random(seed)
    out = {}
    for rel in [1e-4, 1e-3, 1e-2, 3e-2, 0.1, 0.2, 0.3, 0.5]:
        sat = own = n = 0
        for _ in range(N):
            a = Arrangement(perturb(H, rel, rng))
            if not a.check_general_position():
                continue
            n += 1
            own += check_embedding(a, tris, do_pairs=False)["ok_triples"]
            st, _, _ = geomsat.solve_sat(a, verify=False)
            sat += st == "SAT"
        out[rel] = dict(n=n, sat=sat, own_triangulation_ok=own)
        print("rel", rel, out[rel], flush=True)
    return out

if __name__ == "__main__":
    which = sys.argv[1]
    d = ["sphere_unif", "tangent", "near_tangent", "gauss", "pts3", "small_off"]
    res = {}
    if which == "cv":
        res = crossval(int(sys.argv[2]), d, 7)
    elif which == "cvp":
        res = crossval_pert(int(sys.argv[2]), 17)
    elif which == "frac":
        res = fractions(int(sys.argv[2]), d, 11)
    elif which == "rob":
        res = robustness(int(sys.argv[2]), 13)
    json.dump(res, open(os.path.join(SCRATCH, "exp_n7_%s.json" % which), "w"), indent=1)
