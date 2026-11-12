---
id: E-261109-06
title: (10,4) first-witness sweep, stratum C - 358 maps of the six fastest patterns, kissat, no DRAT
date: 2026-11-09
status: done
concluded: 2026-11-10
verdict: OPEN@63.84 core-h (stratum C 360/360 UNSAT-SOLVER, 0 SAT; f = 7.16, A + B = 6.06 laptop nights -> Actions route)
direction: [DR19]
origin: [E-261108-03, E-261103-07, E-261103-03, E-261103-01]
tests: [H-261101-07]
produces: []  # UNSAT-SOLVER is not a negative result; a SAT goes to candidate-check
preregistered: true
---

> Exploit. Week plan item 1 (lead review 2026-11-09, owner-approved). Pre-registered in `PLAN.md`.

## Goal

Decide the plain S5 formula of every admissible (10,4) map outside the patterns `(1^4,2)` and `1^6` (360 maps; 146 and
845 reuse their E-261108-03 records) with kissat in one laptop night, stop at the first SAT, and price strata A and B
with the measured per-pattern factor.

Files: `make_queue.py` (frozen `queue.json`, `--check`), `run.sh` (E-261103-03 runner, kissat, `NO_PROOF=1`),
`progress.sh` (`launch.sh status`), `summary.py` (per-pattern table and the registered verdict, `--selftest`).

## Results

Launch 2026-11-09 23:02 local, 63.84 core-h, 6.87 h wall, controls pass in all 10 shards. All 358 maps UNSAT-SOLVER
(148-2041 s), 0 SAT, 0 TIMEOUT; with 845 and 146 all 360 of stratum C decided. Measured factor f = 7.16 prices A + B at
6.06 laptop nights, so the follow-up tree sends A and B to Actions after week item 2. See `CONCLUSION.md`.

## Next

Week item 2 (Actions calibration, GitHub's terms first); item 3 (cube-and-conquer) may lower the A/B price.
