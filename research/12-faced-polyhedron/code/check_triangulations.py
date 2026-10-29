#!/usr/bin/env python3
"""Independent checker for neighborly orientable 12-vertex genus-6 triangulations.

Usage: python3 check_triangulations.py FILE.json [--no-pairs] [--selftest]
  --selftest: positive control -- every entry is randomly relabelled and mirrored (seeded);
              the copy must pass all checks, be found isomorphic to the original, and have
              the same invariant and the same canonical string.

Uses ONLY the "triangles" field to derive everything (links, orientation, automorphisms);
the other fields are compared against the recomputed values.  Does not import k12_tools.

Checks per entry:
  1. 44 triangles, entries are 3 distinct vertices in 0..11, no repeated triangle (simplicial)
  2. every pair of the 12 vertices is an edge (66 edges), every edge in exactly 2 triangles
  3. every vertex link is a single 11-cycle (closed surface, vertex links connected)
  4. coherent orientation: the 132 directed boundary edges of the listed oriented
     triangles are pairwise distinct (each edge traversed once in each direction)
  5. Euler characteristic V - E + F = -10 (=> genus 6, orientable)
  6. 'links' field: consecutive l[i], l[i+1] give the oriented triangle [v, l[i], l[i+1]]
  7. automorphism group orders recomputed by brute force over the 264 flag maps
     (a simplicial map determined by the image of vertex 0, of one link neighbour and of
     the direction around the link), compared with 'aut_order',
     'aut_orient_preserving_order', 'chiral' (chiral := no orientation-reversing automorphism;
     an automorphism is orientation preserving iff it maps oriented triangles to oriented
     triangles up to cyclic rotation)
  8. 'canonical' recomputed by an independent implementation of the definition
Across entries:
  9. pairwise non-isomorphism: an isomorphism-invariant (multiset of sorted link-distance
     triples over all 220 vertex triples) and, for EVERY pair, a brute-force search over
     all 264 candidate vertex bijections (independent of the invariant).
"""
import json
import sys
from collections import Counter
from itertools import combinations

N = 12
HEX = "0123456789ab"


def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)


def cyc_norm(t):
    """oriented triangle up to cyclic rotation"""
    i = t.index(min(t))
    return tuple(t[i:]) + tuple(t[:i])


def link_cycle(tris, v):
    """Cycle of the link of v as a list, from the unoriented triangles only."""
    adj = {}
    for t in tris:
        if v in t:
            a, b = [x for x in t if x != v]
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    if sorted(adj) != [u for u in range(N) if u != v]:
        fail(f"link of {v} does not contain all other vertices: {sorted(adj)}")
    for a, nb in adj.items():
        if len(nb) != 2:
            fail(f"link of {v}: vertex {a} has degree {len(nb)}")
    start = min(adj)
    cyc, prev, cur = [start], None, start
    while True:
        nxt = adj[cur][0] if adj[cur][0] != prev else adj[cur][1]
        if nxt == start:
            break
        cyc.append(nxt)
        prev, cur = cur, nxt
        if len(cyc) > N:
            fail("link walk overflow")
    if len(cyc) != N - 1:
        fail(f"link of {v} is not a single 11-cycle (component of length {len(cyc)})")
    return cyc


def check_entry(e, k):
    tris = e["triangles"]
    if len(tris) != 44:
        fail(f"entry {k}: {len(tris)} triangles")
    for t in tris:
        if len(t) != 3 or len(set(t)) != 3 or not all(0 <= x < N for x in t):
            fail(f"entry {k}: bad triangle {t}")
    sets = [frozenset(t) for t in tris]
    if len(set(sets)) != 44:
        fail(f"entry {k}: repeated triangle")
    ecount = Counter()
    for t in tris:
        for a, b in combinations(t, 2):
            ecount[frozenset((a, b))] += 1
    if len(ecount) != 66:
        fail(f"entry {k}: {len(ecount)} edges, not 66 (K12)")
    if any(c != 2 for c in ecount.values()):
        fail(f"entry {k}: some edge not in exactly 2 triangles")
    links = {v: link_cycle(tris, v) for v in range(N)}
    darts = [(t[0], t[1]) for t in tris] + [(t[1], t[2]) for t in tris] + [(t[2], t[0]) for t in tris]
    if len(set(darts)) != 132:
        fail(f"entry {k}: orientation of the listed triangles is not coherent")
    V, E, F = N, len(ecount), len(tris)
    if V - E + F != -10:
        fail(f"entry {k}: Euler characteristic {V - E + F}")
    # oriented successor: [v,a,b] oriented => at v, a -> b
    succ = {v: {} for v in range(N)}
    for (a, b, c) in tris:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            succ[x][y] = z
    if "links" in e:
        for v in range(N):
            l = e["links"][str(v)]
            if sorted(l) != [u for u in range(N) if u != v]:
                fail(f"entry {k}: links[{v}] not a permutation of the other vertices")
            for i in range(N - 1):
                if succ[v][l[i]] != l[(i + 1) % (N - 1)]:
                    fail(f"entry {k}: links[{v}] inconsistent with oriented triangles")
    otris = set(cyc_norm(t) for t in tris)
    return {"tris": tris, "sets": set(sets), "links": links, "succ": succ, "otris": otris}


def flag_maps(T1, T2):
    """All 264 candidate bijections f with f(link of 0 in T1) = link of f(0) in T2."""
    c1 = T1["links"][0]
    for w in range(N):
        c2 = T2["links"][w]
        for s in range(N - 1):
            for d in (1, -1):
                f = [None] * N
                f[0] = w
                for i in range(N - 1):
                    f[c1[i]] = c2[(s + d * i) % (N - 1)]
                yield f


def isomorphisms(T1, T2, first_only=False):
    out = []
    for f in flag_maps(T1, T2):
        if all(frozenset(f[x] for x in t) in T2["sets"] for t in T1["tris"]):
            # orientation preserving iff oriented triangles go to oriented triangles
            # (for an automorphism of a connected oriented surface: all or none do)
            imgs = [cyc_norm([f[x] for x in t]) in T2["otris"] for t in T1["tris"]]
            if any(imgs) and not all(imgs):
                fail("isomorphism neither preserves nor reverses orientation")
            op = all(imgs)
            out.append((f, op))
            if first_only:
                break
    return out


def canonical_independent(T):
    """lex-min over all flag labellings of rot(0)+...+rot(11) (see README)."""
    best = None
    pred = {v: {b: a for a, b in T["succ"][v].items()} for v in range(N)}
    for v in range(N):
        for a in range(N):
            if a == v:
                continue
            for S in (T["succ"], pred):
                L, inv, cur = {v: 0}, {0: v}, a
                for k in range(1, N):
                    L[cur], inv[k] = k, cur
                    cur = S[v][cur]
                code = []
                for xn in range(N):
                    x = inv[xn]
                    y = inv[1 if xn == 0 else 0]
                    for _ in range(N - 1):
                        code.append(L[y])
                        y = S[x][y]
                if best is None or code < best:
                    best = code
    s = "".join(HEX[c] for c in best)
    return "-".join(s[i * 11:(i + 1) * 11] for i in range(N))


def invariant(T):
    pos = {v: {u: i for i, u in enumerate(T["links"][v])} for v in range(N)}

    def d(x, y, z):
        q = abs(pos[x][y] - pos[x][z])
        return min(q, N - 1 - q)

    return tuple(sorted(Counter(tuple(sorted((d(a, b, c), d(b, a, c), d(c, a, b))))
                                for a, b, c in combinations(range(N), 3)).items()))


def main():
    path = sys.argv[1]
    do_pairs = "--no-pairs" not in sys.argv
    data = json.load(open(path))
    if isinstance(data, dict):
        data = [data]
    Ts = []
    for k, e in enumerate(data):
        T = check_entry(e, k)
        isos = isomorphisms(T, T)
        aut = len(isos)
        aut_op = sum(1 for _, op in isos if op)
        chiral = (aut_op == aut)
        if "aut_order" in e and e["aut_order"] != aut:
            fail(f"entry {k}: aut_order {e['aut_order']} != recomputed {aut}")
        if "aut_orient_preserving_order" in e and e["aut_orient_preserving_order"] != aut_op:
            fail(f"entry {k}: aut_orient_preserving_order mismatch ({aut_op})")
        if "chiral" in e and e["chiral"] != chiral:
            fail(f"entry {k}: chiral flag mismatch")
        if "canonical" in e and e["canonical"] != canonical_independent(T):
            fail(f"entry {k}: canonical string mismatch")
        if "id" in e and e["id"] != k:
            fail(f"entry {k}: id {e['id']}")
        T["aut"], T["aut_op"] = aut, aut_op
        Ts.append(T)
    if all("canonical" in e for e in data) and len(data) > 1:
        cs = [e["canonical"] for e in data]
        if cs != sorted(cs):
            fail("entries not sorted by canonical form")
    print(f"OK: {len(Ts)} entries pass all per-entry checks "
          f"(44 triangles, K12 edge graph, each edge in 2 triangles, links 11-cycles, "
          f"coherent orientation, chi=-10, simplicial, aut orders, canonical strings)")
    if do_pairs and len(Ts) > 1:
        invs = [invariant(T) for T in Ts]
        ninv = len(set(invs))
        for i in range(len(Ts)):
            for j in range(i + 1, len(Ts)):
                if isomorphisms(Ts[i], Ts[j], first_only=True):
                    fail(f"entries {i} and {j} are isomorphic")
        print(f"OK: all {len(Ts)} entries pairwise non-isomorphic (brute force over "
              f"264 flag maps for every pair); distance-triple invariant separates "
              f"{ninv} classes")
    if "--selftest" in sys.argv:
        import random
        rng = random.Random(12345)
        for k, e in enumerate(data):
            p = list(range(N))
            rng.shuffle(p)
            mirror = rng.random() < 0.5 or k % 2 == 0
            tris = [[p[t[0]], p[t[2]], p[t[1]]] if mirror else [p[x] for x in t]
                    for t in e["triangles"]]
            rng.shuffle(tris)
            T2 = check_entry({"triangles": tris}, f"selftest-{k}")
            if not isomorphisms(T2, Ts[k], first_only=True):
                fail(f"selftest {k}: relabelled copy not recognised as isomorphic")
            if invariant(T2) != invariant(Ts[k]):
                fail(f"selftest {k}: invariant not invariant")
            if "canonical" in e and canonical_independent(T2) != e["canonical"]:
                fail(f"selftest {k}: canonical string not invariant")
        print(f"OK: selftest ({len(data)} random relabellings, mirrored ones included) passed")
    print("aut orders:", Counter(T["aut"] for T in Ts))
    print("chiral (no orientation-reversing automorphism):",
          sum(1 for T in Ts if T["aut"] == T["aut_op"]), "of", len(Ts))


if __name__ == "__main__":
    main()
