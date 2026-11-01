---
id: E-261101-26
title: Engine benchmark ladder - tasks with known answers on which every construction engine is scored before the target
date: 2026-11-01
status: planned
direction: [DR1, DR7, DR17]
origin: [I-261101-22, E-261030-01, E-261030-03, E-261101-25]
tests: [H-261101-17, H-261101-10]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 2 2 | budget: 1-2 days of harness code, then one laptop night per engine. Before
> any compute: `PLAN.md` (skill `experiment-start`).

## Goal

A fixed ladder of tasks with known answers and a score vector (success rate, median time to exact success) for every
construction engine the project has (genus ladders, solid-first, normals-first, chirotope-first, later Farkas descent
and arrangement-first), so that a new engine or variant is compared on observable progress, not on the open target.

## Next

Stop rule: all engines scored on all rungs, or the first rung where every engine fails (then that rung is the
research problem, and the target is not yet in reach). The ranking goes into `STATUS.md` as a new table; the ROADMAP
order of construction items follows it (I-261101-22).

## Starting point

* Rungs (exact success only, `ladder_exact.verify` or a DRAT): R1 Szilassi from random planes (n = 7); R2 the
  Roest-Vigh and Mizhaev objects from their own 8 planes (inner step, doubled runs allowed) and R3 from random D2 / C4
  two-orbit planes; R4 a type-15 genus-3 witness map from random planes; R5 the same from its genus-2 parent in the
  archive; R6 k-face sub-instances of types 0, 15, 58 for k = 7, 8, 9 (a realized partial object, or an UNSAT with
  proof); R7 the full type (the open target, reported but not scored).
* Harness: one JSON task list, one runner per engine with a fixed wall-clock budget per rung and per seed, one
  `scores.json` per engine; the exact checker is the only judge.
* Controls: every rung R1-R5 has a known solution, so an engine that fails a rung is measurably weaker there.
* Counter calibration: the score is a success count and a median time, not a float energy; report the number of
  seeds and the budget so that "0 of 20 in 10 minutes" is read as a power statement.
