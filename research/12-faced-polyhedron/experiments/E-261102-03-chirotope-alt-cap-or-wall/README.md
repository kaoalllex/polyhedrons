---
id: E-261102-03
title: Chirotope-first on the full-map rungs with the alternation cap lifted - is the R4 / R5 frontier a cap or a wall?
date: 2026-11-02
status: running
direction: [DR8, DR17]
origin: [E-261101-26, I-261102-01]
tests: [H-261101-17]
produces: []
preregistered: true
---

> Planned 2026-11-02 from `../E-261101-26-engine-benchmark-ladder/CONCLUSION.md`; pre-registered in `PLAN.md` (two pilots in its Amendments). Scores
> T D F G R: 1 2 2 1 2.

## Goal

In E-261101-26 every failure of the chirotope-first engine stopped at `--alt 20` (20 alternations per face-ladder
step) after 15-39 % of its time budget. Per alternation the successes looked memoryless (about 2 % at k = 7).
This experiment lifts the cap so that the time budget binds, and asks whether the full genus-3 maps (R4, R5) then
become reachable, or stay at 0 while the k-face rungs improve.

## Next

`experiment-start`: `PLAN.md` with the new pilot gate (PROTOCOL §2.4). Day pilot: one R4 type-15 seed at 40 min
with the cap lifted (`--alt` large). It must show that time, not alternations, ends the unit, and how far the face
ladder climbs. Night: a grid over the budget per seed (40 and 120 min) with a few seeds per cell. Tasks R4 (both
maps), R5, R6k k = 8, 9; harness `../E-261101-26-engine-benchmark-ladder/ladder.py` with the same `tasks.json`
(needs an option to override `ENGINE['alt']`). Decision:
* R4 / R5 successes: E-261102-02 is amended with that setting;
* 0 on R4 / R5 with the R6k rates rising: the full map is a wall for this engine at <= 120 min, and E-261102-02 is
  killed or cut down;
* R6k not rising either: the alternation cap was not the limit.
