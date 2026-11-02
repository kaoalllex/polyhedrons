---
id: E-261102-01
title: Completion of the k-face sweep - the types night 6 did not reach, with a time-limited final-polynomial LP
date: 2026-11-02
status: planned
direction: [DR8, DR11]
origin: [E-261101-23, I-261101-18]
tests: [H-261101-15, H-261101-02, H-261101-12]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: one laptop night, 6 shards. Before any compute: `PLAN.md` (skill
> `experiment-start`). What is different from E-261101-23: the final-polynomial LP has a time limit, so the
> sweep reaches the types night 6 never reached (numbers: `../E-261101-23-k-face-subinstances-face-cegar/CONCLUSION.md`).

## Goal

The verdict (SAT / UNSAT / timeout) of the k = 8, 9 sub-instances on the greedy face set for the types E-261101-23
did not reach; DRAT for every UNSAT; final-polynomial certificates (multipliers) stored so that an exact one can be
re-checked by an independent script.

## Starting point

* Runner: `../E-261101-23-k-face-subinstances-face-cegar/kface_sweep.py` with `--types` restricted to the missing
  types (list in that experiment's `CONCLUSION.md`); `final_polynomial(..., time_limit=120)` returns `LP-TIMEOUT`.
* Store the Farkas multipliers of every NONREALIZABLE-EXACT result in the record (or a side file with its SHA-256).
* k = 10: every night-6 run timed out at 20 minutes; either a 60-minute timeout on a few types or drop it.
* A second face set per type when k = 9 is SAT (one face set per (type, k) says nothing about the others).
* Realizer positive control on k-face sub-instances of known realizations (from E-261101-26) before reading
  "0 realized" as anything.
