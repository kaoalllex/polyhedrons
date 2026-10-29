#!/usr/bin/env python3
"""Build data/k12_triangulations.json from the output of enum_k12 (CLASS lines).

Usage: python3 build_json.py ENUM_OUTPUT.txt OUT.json
Each class is relabelled to its canonical labelling (the rotation system of the stored
triangulation IS the canonical code).  The C canonical code is re-derived in Python.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k12_tools as K  # noqa: E402


def dump_entries(entries, path):
    """JSON list, one key per line, lists on one line (compact but readable)."""
    with open(path, "w") as f:
        f.write("[\n")
        for i, e in enumerate(entries):
            f.write(" {\n")
            keys = list(e)
            for j, k in enumerate(keys):
                f.write(f"  {json.dumps(k)}: {json.dumps(e[k], separators=(',', ':'))}")
                f.write(",\n" if j < len(keys) - 1 else "\n")
            f.write(" }" + (",\n" if i < len(entries) - 1 else "\n"))
        f.write("]\n")


def main():
    src, out = sys.argv[1], sys.argv[2]
    classes = []
    for line in open(src):
        if line.startswith("CLASS"):
            t = line.split()
            d = dict(zip(t[0::2], t[1::2]))
            classes.append((d["code"], int(d["aut"]), int(d["aut_op"]), int(d["hits"])))
    entries = []
    for idx, (hexcode, aut, aut_op, hits) in enumerate(classes):
        code = "-".join(hexcode[i * 11:(i + 1) * 11] for i in range(12))
        succ = K.succ_from_code(code)
        K.check_rule_delta(succ)
        e, cs = K.entry_from_succ(succ, idx)
        assert e["canonical"] == code, "Python canonical differs from C canonical"
        assert e["aut_order"] == aut and e["aut_orient_preserving_order"] == aut_op
        assert hits * aut == 264
        entries.append(e)
    assert [e["canonical"] for e in entries] == sorted(e["canonical"] for e in entries)
    dump_entries(entries, out)
    print(f"wrote {len(entries)} entries to {out}")


if __name__ == "__main__":
    main()
