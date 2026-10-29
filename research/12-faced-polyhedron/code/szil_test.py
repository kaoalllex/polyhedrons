from szilassi import *
import time
verts, faces, H, tris = szilassi_arr()
arr = Arrangement(H)
# which degeneracies?
bad = 0
for t in combinations(range(7), 3):
    try: arr.tp(*t)
    except DegenerateArrangement as e: print("inf:", e); bad += 1
vecs = list(H) + [(0,0,0,1)]
zero = [t for t in combinations(range(8), 4) if det4(*(vecs[i] for i in t)) == 0]
print("zero 4x4 dets:", len(zero), zero[:10])
rng = random.Random(5)
for rel in [1e-6, 1e-5, 1e-4, 1e-3]:
    Hp = perturb(H, rel, rng)
    a = Arrangement(Hp)
    gp = a.check_general_position()
    if not gp: print(rel, "not GP"); continue
    r = check_embedding(a, tris)
    print("rel", rel, "direct (own triangulation): ok_triples", r["ok_triples"], "ok_pairs", r["ok_pairs"], violation_profile(a, tris))
    st, tr, info = geomsat.solve_sat(a)
    print("   SAT:", st, info.get("direct_ok_triples"), info.get("direct_ok_pairs"), "time %.3f" % info["t_total"], "DIS" in str(info), tr == tris if tr else None)
