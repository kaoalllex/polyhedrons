"""Companion check of reviews/strategy-review-2026-11-13.md (no solver, seconds).

For each of the 20 imported (10, 3) maps: the orientation-preserving automorphisms of the
triangulation and, per conjugacy-free listing of cyclic subgroups, the necessary conditions for a
generator to act as a rotation of an embedded cubic polyhedron with planar faces (the dual):

* the fixed points on the surface (fixed vertices, reversed edges, rotated triangles) are the
  points where the axis meets the surface, so their number is even;
* two fixed vertices of the triangulation are two faces perpendicular to the axis, hence
  parallel, hence non-adjacent.

Combinatorial screening only: a passing subgroup is a candidate ansatz, not a realization.
Usage: python3 reviews/strategy-review-2026-11-13-symmetry.py
"""
import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "experiments/E-261110-02-face-minimal-10-3-decision/maps/maps_10_3.json"


def automorphisms(tris, n):
    nxt = {}
    for a, b, c in tris:
        nxt[(a, b)] = c
        nxt[(b, c)] = a
        nxt[(c, a)] = b
    assert len(nxt) == 3 * len(tris), "triangles are not consistently oriented"
    a0, b0 = tris[0][0], tris[0][1]
    auts = []
    for (a1, b1) in nxt:
        f = {}
        stack = [((a0, b0), (a1, b1))]
        seen = set()
        ok = True
        while stack and ok:
            (a, b), (x, y) = stack.pop()
            if (a, b) in seen:
                continue
            seen.add((a, b))
            for u, v in ((a, x), (b, y), (nxt[(a, b)], nxt[(x, y)])):
                if f.setdefault(u, v) != v:
                    ok = False
            c, z = nxt[(a, b)], nxt[(x, y)]
            stack += [((b, c), (y, z)), ((c, a), (z, x)), ((b, a), (y, x))]
        if ok and len(set(f.values())) == n:
            auts.append(tuple(f[i] for i in range(n)))
    return auts


def order(p):
    q, k = p, 1
    while any(q[i] != i for i in range(len(p))):
        q = tuple(p[i] for i in q)
        k += 1
    return k


def cycle_type(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            j, length = i, 0
            while j not in seen:
                seen.add(j)
                j = p[j]
                length += 1
            out.append(length)
    return tuple(sorted(out, reverse=True))


def main():
    data = json.loads(MAPS.read_text())
    for m in data["maps"]:
        tris = [tuple(t) for t in m["triangles"]]
        n = len(m["links"])
        adj = {frozenset(e) for t in tris for e in combinations(t, 2)}
        auts = automorphisms(tris, n)
        assert len(auts) == m["aut_plus"], (m["lutz"], len(auts))
        rows = {}
        for p in auts:
            k = order(p)
            if k == 1:
                continue
            fixed_v = [i for i in range(n) if p[i] == i]
            rev_e = sum(1 for e in adj if {p[i] for i in e} == set(e) and any(p[i] != i for i in e))
            rot_t = sum(1 for t in tris if {p[i] for i in t} == set(t) and p[t[0]] != t[0])
            fp = len(fixed_v) + rev_e + rot_t
            parallel_ok = all(frozenset(e) not in adj for e in combinations(fixed_v, 2))
            key = (k, cycle_type(p), len(fixed_v), rev_e, rot_t, fp % 2 == 0, parallel_ok)
            rows[key] = rows.get(key, 0) + 1
        print(f"Lutz #{m['lutz']:2d}  |Aut+| = {len(auts)}")
        for (k, ct, fv, re, rt, even, par), cnt in sorted(rows.items()):
            verdict = "candidate" if even and par else "excluded"
            print(f"    order {k}  faces {ct}  fixed faces {fv}  axis edges {re}  axis vertices {rt}"
                  f"  x{cnt}  even={even} parallel_ok={par}  -> {verdict}")


if __name__ == "__main__":
    main()
