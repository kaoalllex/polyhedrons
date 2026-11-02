---
id: E-261102-02
title: Chirotope-first engine, night run 2 - LP time limit, 40 core-guided rounds, cap inside each step, all seed slices
date: 2026-11-02
status: planned
direction: [DR8, DR9, DR17]
origin: [E-261101-25, I-261101-21, I-261101-22]
tests: [H-261101-17, H-261101-12, H-261101-01]
produces: []
preregistered: true
---

> **Blocked** 2026-11-02 until E-261102-03 decides (`PLAN.md` Amendments). Pre-registered 2026-11-02 (`PLAN.md`, `run.sh` with 10 shards); launch: one laptop night. Scores T D F G R:
> 2 2 2 2 2. Launch only after the benchmark ladder E-261101-26 has scored the engine (PROTOCOL 8a; `PLAN.md`
> Amendments). What is
> different from night run 1 (`../E-261101-25-chirotope-first/CONCLUSION.md`): the final-polynomial LP has a time
> limit, `--rounds 40` instead of 12, the per-seed cap also bounds each step, and all 10 seed slices run.

## Goal

The fraction of class seeds whose k = 7 step reaches a model when the round budget is not binding, the realization
rate of those models, and how many unrealized models carry an exact final polynomial (with stored certificates).

## Starting point

* Engine: `../E-261101-25-chirotope-first/chirotope_first.py`, settings from its `run.sh` with `--rounds 40`.
* The cap: pass the remaining seed time to `final_polynomial(..., time_limit=...)` and to the SAT calls, so
  `--seed-minutes` holds inside a step.
* Store the Farkas multipliers of exact final polynomials; write an independent re-check before calling one a result.
* Controls: the engine's n = 7 controls, plus the k-face realizer control from E-261101-26.
