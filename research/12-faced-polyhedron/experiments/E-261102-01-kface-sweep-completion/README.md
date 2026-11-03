---
id: E-261102-01
title: Completion of the k-face sweep - the types night 6 did not reach, with a time-limited final-polynomial LP
date: 2026-11-02
status: done
verdict: LOW-YIELD@4.2 core-h (exclusion, greedy face set, k <= 9); UNDERPOWERED (realization, no positive control)
direction: [DR8, DR11]
origin: [E-261101-23, I-261101-18]
tests: [H-261101-15, H-261101-02, H-261101-12]
produces: [C:final_polynomial]
preregistered: true
---

> Done 2026-11-02 (laptop, daytime, 8 shards, 40 min wall). k = 8 SAT for all 32 types, k = 9 SAT for 18 and
> TIMEOUT for 14; 0 UNSAT, 0 realized models, no hang; two more exact final polynomials stored (type 57 k = 8,
> type 53 k = 9), not yet independently checked. Numbers, claims and scope: `CONCLUSION.md`.

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
