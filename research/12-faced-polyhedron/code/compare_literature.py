#!/usr/bin/env python3
"""Compare our enumeration (data/k12_triangulations.json) with external lists.

Usage (external files are untrusted data; only parsed as text, nothing executed):
  python3 -I compare_literature.py OURS.json --hackerpoet topologies.txt \
          --lutz k12_g6_lutz.txt [--out MAP.json]

Each external triangulation is checked (via check_triangulations.check_entry after a BFS
orientation), mapped to our id by the canonical form of k12_tools, and the match is
confirmed by brute-force isomorphism (check_triangulations.isomorphisms).
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_triangulations as C  # noqa: E402
import k12_tools as K  # noqa: E402
from classify_enum2 import orient  # noqa: E402


def parse_hackerpoet(path):
    out = []
    for line in open(path):
        t = line.split()
        if not t:
            continue
        name = t[0]
        tris = [tuple(K.HEX.index(ch) for ch in w) for w in t[1:]]
        out.append((name, tris))
    return out


def parse_lutz(path):
    txt = open(path).read()
    out = []
    for m in re.finditer(r"(manifold_lex_d2_n12_o1_g6_#\d+)\s*=\s*(\[\[.*?\]\])", txt, re.S):
        name = m.group(1).split("_")[-1]
        tris = [tuple(x - 1 for x in t) for t in json.loads(m.group(2))]
        out.append((name, tris))
    return out


def succ_of(otris):
    succ = {v: {} for v in range(12)}
    for (a, b, c) in otris:
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            succ[x][y] = z
    return succ


def match_list(ours, ext, label):
    canon_to_id = {e["canonical"]: e["id"] for e in ours}
    reps = [C.check_entry(e, k) for k, e in enumerate(ours)]
    mapping = {}
    for name, tris in ext:
        assert len(tris) == 44, (label, name)
        ot = orient(tris)
        T = C.check_entry({"triangles": ot}, name)
        code = K.code_str(K.canonical(succ_of(ot))[0])
        if code not in canon_to_id:
            C.fail(f"{label} {name}: canonical form not in our list")
        i = canon_to_id[code]
        if not C.isomorphisms(T, reps[i], first_only=True):
            C.fail(f"{label} {name}: brute-force isomorphism to our id {i} not confirmed")
        mapping[name] = i
    ids = sorted(mapping.values())
    print(f"{label}: {len(ext)} entries; mapped to {len(set(ids))} distinct ids of ours;"
          f" bijection with our {len(ours)}: {ids == list(range(len(ours)))}")
    return mapping


def main():
    args = sys.argv[1:]
    ours = json.load(open(args[0]))
    res = {}
    if "--hackerpoet" in args:
        res["hackerpoet"] = match_list(ours, parse_hackerpoet(args[args.index("--hackerpoet") + 1]),
                                       "HackerPoet topologies.txt")
    if "--lutz" in args:
        res["lutz"] = match_list(ours, parse_lutz(args[args.index("--lutz") + 1]),
                                 "Lutz-format k12_g6_lutz.txt")
    if "--out" in args:
        table = []
        inv = {k: {v: n for n, v in m.items()} for k, m in res.items()}
        for e in ours:
            row = {"id": e["id"]}
            if "hackerpoet" in inv:
                row["hackerpoet_no"] = inv["hackerpoet"].get(e["id"])
            if "lutz" in inv:
                row["lutz_no"] = inv["lutz"].get(e["id"])
            row["aut_order"] = e["aut_order"]
            table.append(row)
        with open(args[args.index("--out") + 1], "w") as f:
            f.write("[\n" + ",\n".join(" " + json.dumps(r) for r in table) + "\n]\n")


if __name__ == "__main__":
    main()
