---
id: E-261108-03
title: (10,4) speed-up benchmark - kissat and CaDiCaL --unsat against the recorded default-CaDiCaL runs
date: 2026-11-08
status: done
concluded: 2026-11-09
verdict: OPEN@8.59 core-h (kissat winner, P(4) = 475 core-h without DRAT, no 10x; (10,4) maps 96/85/146/845 UNSAT-SOLVER)
direction: [DR19]
origin: [E-261103-07, E-261103-03, I-261031-02, I-261108-05]
tests: [H-261101-07]
produces: []  # no FD / W / C; UNSAT-SOLVER is not a negative result
preregistered: true
---

> Week plan item 2 (`ROADMAP.md`, lead review 2026-11-08d, amended by review 2026-11-08e), cut down by the owner on
> 2026-11-08 21:30 for one launch tonight. Scores T D F G R: 1 2 2 2 2. Design and deviations: `PLAN.md`.

## Goal

Is there a solver variant that makes the (10,4) plain S5 formulas of the E-261103-02 encoder >= 10x cheaper, measured
on (10,4) maps? Tonight: V1 = kissat (pinned release), V2 = CaDiCaL `--unsat`; Phase A correctness screen on six known
(9,3) maps, Phase B on (10,4) maps 96, 85, 146, 845. The holdout and cube-and-conquer are separate later launches.

## Results

Launch 2026-11-08 22:21 local, 8.59 core-h, 2.38 h wall, controls pass everywhere, 0 SAT. kissat decides all four (10,4) maps
(189-2749 s), `--unsat` also (367-8420 s, slower than default), default CaDiCaL decides 96 and 85 (1970, 6454 s); best
measured ratio 2.35x, goal 10x not met. Winner kissat, P(4) = 475, P(16) = 475 core-h (`projection.py`). See `CONCLUSION.md`.

## Next

Follow-up tree: Actions calibration (I-261108-07); the lead review decides.
