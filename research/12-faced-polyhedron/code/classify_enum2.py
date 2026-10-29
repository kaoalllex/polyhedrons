#!/usr/bin/env python3
"""Classify the labelled solutions printed by enum2_k12 against data/k12_triangulations.json.

Usage: python3 classify_enum2.py ENUM2_OUTPUT.txt K12_JSON
Uses only the functions of check_triangulations.py (independent of enum_k12 / k12_tools):
for each labelled solution, orient it (BFS), compute the distance-triple invariant,
and confirm the isomorphism to the matching JSON entry by brute force over flag maps.
Verifies that class j receives exactly 264/|Aut_j| labelled solutions.
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_triangulations as C  # noqa: E402


def orient(tris):
    """Coherently orient a list of unoriented triangles by BFS (fails if impossible)."""
    edge_t = {}
    for i, t in enumerate(tris):
        for k in range(3):
            e = frozenset((t[k], t[(k + 1) % 3]))
            edge_t.setdefault(e, []).append(i)
    o = [None] * len(tris)
    o[0] = list(tris[0])
    queue = [0]
    while queue:
        i = queue.pop()
        t = o[i]
        for k in range(3):
            x, y = t[k], t[(k + 1) % 3]
            for j in edge_t[frozenset((x, y))]:
                if j == i:
                    continue
                u = list(tris[j])
                z = [w for w in u if w not in (x, y)][0]
                want = [y, x, z]          # neighbour must traverse y -> x
                if o[j] is None:
                    o[j] = want
                    queue.append(j)
                else:
                    if C.cyc_norm(o[j]) != C.cyc_norm(want):
                        raise ValueError("not orientable")
    return o


def main():
    sols_path, json_path = sys.argv[1], sys.argv[2]
    data = json.load(open(json_path))
    reps = [C.check_entry(e, k) for k, e in enumerate(data)]
    auts = [e["aut_order"] for e in data]
    inv_index = {}
    for k, T in enumerate(reps):
        inv_index.setdefault(C.invariant(T), []).append(k)
    hits = Counter()
    nsol = 0
    seen = set()
    for line in open(sols_path):
        line = line.strip()
        if not line:
            continue
        tris = [tuple(int(x) for x in w.split(",")) for w in line.split()]
        key = frozenset(frozenset(t) for t in tris)
        if key in seen:
            C.fail("duplicate labelled solution in enum2 output")
        seen.add(key)
        nsol += 1
        T = C.check_entry({"triangles": orient(tris)}, nsol)
        cands = inv_index.get(C.invariant(T), [])
        match = [k for k in cands if C.isomorphisms(T, reps[k], first_only=True)]
        if len(match) != 1:
            C.fail(f"solution {nsol}: matches {match}")
        hits[match[0]] += 1
    bad = [k for k in range(len(reps)) if hits[k] * auts[k] != 264]
    print(f"{nsol} labelled orientable solutions from enum2; classes hit: {len(hits)} of {len(reps)}")
    print("orbit-stabiliser (hits * |Aut| == 264) failures:", bad)
    if bad or len(hits) != len(reps):
        sys.exit(1)
    print("OK: enum2 reproduces exactly the 59 classes with the predicted multiplicities")


if __name__ == "__main__":
    main()
