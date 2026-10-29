#!/usr/bin/env python3
"""Combinatorial invariants of the 59 types (automorphism groups, orbits, fixed structures).

Usage: python3 k12_invariants.py data/k12_triangulations.json data/k12_invariants.json
Automorphisms are recomputed by brute force (check_triangulations.isomorphisms).
For each automorphism g we record: order, orientation character (+1 preserving,
-1 reversing), fixed vertices (= faces of the polyhedron mapped to themselves),
edges {u,v} with g{u,v}={u,v} (split into pointwise-fixed and swapped), and
triangles fixed as sets (= polyhedron vertices mapped to themselves).
"""
import json
import os
import sys
from collections import Counter
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_triangulations as C  # noqa: E402

N = 12


def compose(f, g):  # f o g
    return tuple(f[g[x]] for x in range(N))


def order(g):
    e, h, k = tuple(range(N)), g, 1
    while h != e:
        h, k = compose(g, h), k + 1
    return k


def group_name(elems):
    n = len(elems)
    orders = Counter(order(g) for g in elems)
    abelian = all(compose(a, b) == compose(b, a) for a in elems for b in elems)
    if n == 1:
        return "trivial"
    if n in (2, 3):
        return f"C{n}"
    if n == 4:
        return "C4" if orders[4] else "C2xC2"
    if n == 6:
        return "C6" if orders[6] else "S3"
    if n == 12:
        if orders[12]:
            return "C12"
        if abelian:
            return "C6xC2"
        if orders[2] == 7:
            return "D6 (dihedral, order 12)"
        if orders[2] == 3 and orders[3] == 8:
            return "A4"
        if orders[2] == 1:
            return "Dic3"
    return f"order {n} (unidentified)"


def orbits(elems, items, act):
    seen, out = set(), []
    for x in items:
        if x in seen:
            continue
        orb = {act(g, x) for g in elems}
        seen |= orb
        out.append(sorted(orb) if not isinstance(x, frozenset) else sorted(sorted(o) for o in orb))
    return out


def main():
    data = json.load(open(sys.argv[1]))
    out = []
    summary = []
    for e in data:
        T = C.check_entry(e, e["id"])
        isos = C.isomorphisms(T, T)
        elems = [tuple(f) for f, _ in isos]
        sign = {tuple(f): (1 if op else -1) for f, op in isos}
        op_elems = [g for g in elems if sign[g] > 0]
        tris = [frozenset(t) for t in e["triangles"]]
        edges = [frozenset(p) for p in combinations(range(N), 2)]
        vact = lambda g, x: g[x]  # noqa: E731
        sact = lambda g, s: frozenset(g[x] for x in s)  # noqa: E731
        vorb = orbits(elems, range(N), vact)
        vorb_op = orbits(op_elems, range(N), vact)
        eorb = orbits(elems, edges, sact)
        torb = orbits(elems, tris, sact)
        nontri = [frozenset(s) for s in combinations(range(N), 3) if frozenset(s) not in set(tris)]
        norb = orbits(elems, nontri, sact)
        el_info = []
        for g in elems:
            if g == tuple(range(N)):
                continue
            fv = [x for x in range(N) if g[x] == x]
            fe = [sorted(s) for s in edges if sact(g, s) == s]
            fe_fixed = [p for p in fe if g[p[0]] == p[0]]
            fe_swapped = [p for p in fe if g[p[0]] == p[1]]
            ft = [sorted(t) for t in tris if sact(g, t) == t]
            el_info.append({"perm": list(g), "order": order(g), "orientation": sign[g],
                            "fixed_vertices": fv, "fixed_edges_pointwise": fe_fixed,
                            "swapped_edges": fe_swapped, "fixed_triangles": ft})
        rev_inv = [x for x in el_info if x["orientation"] < 0 and x["order"] == 2]
        rec = {"id": e["id"], "aut_order": len(elems), "aut_orient_preserving_order": len(op_elems),
               "group": group_name(elems),
               "group_orient_preserving": group_name(op_elems),
               "element_types": sorted(Counter((x["order"], x["orientation"]) for x in el_info).items()),
               "vertex_orbits": vorb, "vertex_orbits_orient_preserving": vorb_op,
               "num_vertex_orbits": len(vorb), "num_edge_orbits": len(eorb),
               "num_triangle_orbits": len(torb), "num_nonface_triple_orbits": len(norb),
               "has_orientation_reversing_involution": bool(rev_inv),
               "elements": el_info}
        out.append(rec)
        summary.append(rec)
    with open(sys.argv[2], "w") as f:
        f.write("[\n")
        for i, r in enumerate(out):
            f.write(" " + json.dumps(r, separators=(",", ":")) + (",\n" if i < len(out) - 1 else "\n"))
        f.write("]\n")
    # summary table
    print("id |Aut| |Aut+| group  group+  v-orbits  e-orb t-orb  types(order,orient)  rev.inv")
    for r in summary:
        if r["aut_order"] == 1:
            continue
        print(r["id"], r["aut_order"], r["aut_orient_preserving_order"], r["group"], "|",
              r["group_orient_preserving"], "| vorb sizes", sorted(len(o) for o in r["vertex_orbits"]),
              "| e", r["num_edge_orbits"], "t", r["num_triangle_orbits"], "|", r["element_types"],
              "| rev-inv:", r["has_orientation_reversing_involution"])
    print("trivial group:", sum(1 for r in summary if r["aut_order"] == 1))


if __name__ == "__main__":
    main()
