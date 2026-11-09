#!/usr/bin/env python3
"""Censored projection P(lambda) of PLAN.md (E-261108-03).

Usage: projection.py --selftest | projection.py [RESULTS_RUN_DIR]
Strata: A = (1^4,2) N 520 (map 96), B = 1^6 N 237 (map 85), C = others N 360 (maps 146, 845).
A unit is decided if its status is SAT/UNSAT-SOLVER and its solver seconds <= cap. The registered report uses cap = tau =
3600 s; the second report uses the measured times (cap = the 14400 s solver cap, tau = 3600 s for censored units).
"""
import glob, json, sys
from pathlib import Path

N = {"A": 520, "B": 237, "C": 360}
STRATUM = {96: "A", 85: "B", 146: "C", 845: "C"}
TAU = 3600.0


def project(units, lam, cap, tau=TAU):
    """units: {stratum: [(decided, seconds)]}. Returns (P, sum B); inf if a stratum has no units."""
    total = sum_b = 0.0
    for h, n_h in N.items():
        u = units.get(h)
        if not u:
            return float("inf"), float("inf")
        done = [s for ok, s in u if ok and s <= cap]
        p = len(done) / len(u)
        mu = sum(done) / len(done) if done else 0.0
        b = n_h * (p * mu + (1 - p) * tau) / 3600
        total += b + n_h * (1 - p) * (lam - 1) * tau / 3600
        sum_b += b
    return 1.25 * total, sum_b


def selftest():
    cens = {h: [(False, TAU)] for h in N}
    fast = {h: [(True, 60.0)] for h in N}
    p4 = project(cens, 4, TAU)[0]
    f4 = project(fast, 4, TAU)[0]
    assert abs(p4 - 5585.0) < 0.5 and p4 > 1000 > 160, p4  # all censored: above both thresholds
    assert abs(f4 - 23.27) < 0.01 and f4 < 160, f4  # all decided at 60 s: below both
    assert project({"A": [(True, 1.0)]}, 4, TAU)[0] == float("inf")
    print(f"selftest OK: all censored P(4) = {p4:.0f}, all decided at 60 s P(4) = {f4:.1f}")


def load(run):
    out = {}
    for root in sorted(glob.glob(f"{run}/*-B")):
        units = {}
        for f in glob.glob(f"{root}/*/results.jsonl"):
            for line in open(f):
                d = json.loads(line)
                m = d["map_index"]
                if m in STRATUM:
                    units.setdefault(STRATUM[m], []).append(
                        (d["status"] in ("SAT", "UNSAT-SOLVER"), d["seconds"]))
        out[Path(root).name] = units
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit()
    run = sys.argv[1] if len(sys.argv) > 1 else "results/run"
    for name, units in load(run).items():
        for label, cap in (("registered cap 3600", 3600.0), ("measured cap 14400", 14400.0)):
            for h in "ABC":
                u = units.get(h, [])
                k = [s for ok, s in u if ok and s <= cap]
                print(f"{name} [{label}] stratum {h}: n={len(u)} k={len(k)} mu={sum(k)/len(k) if k else 0:.0f}s "
                      f"censored={[round(s) for ok, s in u if not (ok and s <= cap)]}")
            p4, b = project(units, 4, cap)
            p16, _ = project(units, 16, cap)
            print(f"{name} [{label}] P(4)={p4:.0f} P(16)={p16:.0f} sumB={b:.0f} core-h")
