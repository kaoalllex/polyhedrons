"""Run grow (C leaf emitter), canonicalise with enum_growth.canon, compare with E-261103-01 maps_F_g.json."""
import json, subprocess, sys
from pathlib import Path
from enum_growth import canon, admissible

F, g, exe = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
census = json.load(open(Path(__file__).resolve().parent.parent / f"E-261103-01-s5-map-census/results/maps_{F}_{g}.json"))
recs = census.get("maps") or census.get("records")

def mine_from_leaf(line):
    a, b = line.split("|")
    x = list(map(int, a.split())); p = list(map(int, b.split()))
    T = len(x) // 3
    return {(t, i): divmod(p[3 * t + i], 3) for t in range(T) for i in range(3)}, [tuple(x[3*t:3*t+3]) for t in range(T)]

def mine_from_code(code):
    step = [c[0] for c in code]; alpha = [c[1] for c in code]
    tri, seen = [], set()
    for d in range(len(code)):
        if d not in seen:
            t = [d, step[d], step[step[d]]]; tri.append(t); seen.update(t)
    pos = {d: (k, i) for k, t in enumerate(tri) for i, d in enumerate(t)}
    return {pos[d]: pos[alpha[d]] for d in pos}

out = subprocess.run([exe, str(F), str(g)], capture_output=True, text=True, check=True).stdout.splitlines()
mine = {}
for line in out:
    P, tris = mine_from_leaf(line)
    c, aut, refl = canon(P, len(tris))
    mine.setdefault(c, (aut, refl, admissible(tris)))
theirs = {}
for r in recs:
    P = mine_from_code(r["code"])
    c, aut, refl = canon(P, len(P) // 3)
    theirs[c] = (r["aut_plus"], r["reflexible"], r["admissible"])
print(dict(F=F, g=g, leaves=len(out), mine=len(mine), theirs=len(theirs),
           only_mine=len(set(mine) - set(theirs)), only_theirs=len(set(theirs) - set(mine)),
           attr_mismatch=sum(mine[c] != theirs[c] for c in set(mine) & set(theirs)),
           mine_admissible=sum(v[2] for v in mine.values())))
