"""Final lead review 2026-11-22, check K1: free orientation-preserving involutions of the 790 free-C2 (8, 3) stage-A maps vs the stage-B records.

Usage: python3 -I k1_free_half_turns_8_3.py <E-261119-02 dir>. Own automorphism search from the canonical dart code (step = nxt, alpha); not TriMap.automorphisms."""
import json
import sys
from collections import Counter
from pathlib import Path

E = Path(sys.argv[1])
sys.path.insert(0, str(E))
import stageb as B  # noqa: E402

S = B.S


def autos(step, alpha, reverse):
    nd = len(step)
    prv = [0] * nd
    for d, e in enumerate(step):
        prv[e] = d
    target_step = prv if reverse else step
    out = []
    for r in range(nd):
        f = {0: r}; todo = [0]; ok = True
        while todo and ok:
            d = todo.pop(); e = f[d]
            for a, b in ((step[d], target_step[e]), (alpha[d], alpha[e])):
                if a in f:
                    if f[a] != b:
                        ok = False; break
                else:
                    f[a] = b; todo.append(a)
        if ok and len(f) == nd and len(set(f.values())) == nd:
            out.append(tuple(f[d] for d in range(nd)))
    return out


data = B.maps_of('C2_8_3')
codes = sorted(data)
F = 8
tot_inv = 0; tot_rec = 0; miss_lab = 0; miss_plus = 0; miss_full = 0
maps_miss_lab = set(); maps_miss_full = set(); nonconj_classes_full = 0
ex = None
for k in codes:
    code = json.loads(k)
    step = [c[0] for c in code]; alpha = [c[1] for c in code]
    M = S.census.from_code([tuple(x) for x in code])
    tail = M.tail; head = [M.head(d) for d in range(len(code))]
    plus = autos(step, alpha, False); minus = autos(step, alpha, True)
    def vperm(f, rev):
        g = [None] * F
        for d in range(len(code)):
            v = head[f[d]] if rev else tail[f[d]]
            assert g[tail[d]] in (None, v)
            g[tail[d]] = v
        return tuple(g)
    Gp = {vperm(f, False) for f in plus}; Gm = {vperm(f, True) for f in minus}
    Gfull = Gp | Gm
    ident = tuple(range(F))
    inv = set()
    for f in plus:
        if all(f[f[d]] == d for d in range(len(code))) and any(f[d] != d for d in range(len(code))):
            g = vperm(f, False)
            if all(g[v] != v for v in range(F)):
                inv.add(g)
    recs = B.records_for('C2_8_3', [k], data=data)
    listed = {tuple(r['sym_generator']) for r in recs}
    assert listed <= inv, ('listed generator not a free involution', k[:40])
    tot_inv += len(inv); tot_rec += len(recs)
    conj = lambda G, L: {tuple(h[g[hinv[v]]] for v in range(F)) for h in G for g in L
                         for hinv in [tuple(sorted(range(F), key=lambda v: h[v]))]}
    m1 = inv - listed; m2 = inv - conj(Gp, listed); m3 = inv - conj(Gfull, listed)
    miss_lab += len(m1); miss_plus += len(m2); miss_full += len(m3)
    if m1: maps_miss_lab.add(k)
    if m3:
        maps_miss_full.add(k)
        # number of Gfull-conjugacy classes of free involutions not represented
        rest = set(m3);
        while rest:
            g = rest.pop(); cl = conj(Gfull, [g]); rest -= cl; nonconj_classes_full += 1
        if ex is None:
            ex = (B.code_sha(code)[:12], sorted(m3)[0])
print(dict(maps=len(codes), free_involutions=tot_inv, records=tot_rec, missing_labels=miss_lab,
           maps_missing=len(maps_miss_lab), missing_after_aut_plus_conj=miss_plus,
           missing_after_full_conj=miss_full, maps_missing_full=len(maps_miss_full),
           unrepresented_classes_full=nonconj_classes_full, example=ex))
