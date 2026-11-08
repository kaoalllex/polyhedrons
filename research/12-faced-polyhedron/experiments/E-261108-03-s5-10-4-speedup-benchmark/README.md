---
id: E-261108-03
title: (10,4) speed-up benchmark - kissat and CaDiCaL --unsat against the recorded default-CaDiCaL runs
date: 2026-11-08
status: running
direction: [DR19]
origin: [E-261103-07, E-261103-03, I-261031-02, I-261108-05]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Week plan item 2 (`ROADMAP.md`, lead review 2026-11-08d, amended by review 2026-11-08e), cut down by the owner on
> 2026-11-08 21:30 for one launch tonight. Scores T D F G R: 1 2 2 2 2. Design and deviations: `PLAN.md`.

## Goal

Is there a solver variant that makes the (10,4) plain S5 formulas of the E-261103-02 encoder >= 10x cheaper, measured
on (10,4) maps? Tonight: V1 = kissat (pinned release), V2 = CaDiCaL `--unsat`; Phase A correctness screen on six known
(9,3) maps, Phase B on (10,4) maps 96, 85, 146, 845. The holdout and cube-and-conquer are separate later launches.

## Next

Owner launch (`PLAN.md` § Launch), then `experiment-conclude`.
