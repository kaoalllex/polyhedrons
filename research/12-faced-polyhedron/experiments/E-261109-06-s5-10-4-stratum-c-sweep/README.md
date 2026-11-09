---
id: E-261109-06
title: (10,4) first-witness sweep, stratum C - 358 maps of the six fastest patterns, kissat, no DRAT
date: 2026-11-09
status: running
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

## Next

Owner launch from the repo root, on AC power: `bash research/12-faced-polyhedron/overnight/launch.sh 09-06 start`
(then `status`, `stop`). After the night: `python3 summary.py`, then `experiment-conclude`.
