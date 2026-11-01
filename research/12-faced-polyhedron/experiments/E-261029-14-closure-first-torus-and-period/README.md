---
id: E-261029-14
title: Closure first: period defects, flat 3-torus, simple faces
date: 2026-10-29
status: done
direction: [DR4]
origin: [I-261029-17, I-261029-03]
tests: [H-261029-11]
produces: [FD9]
verdict: LOW-YIELD@1 session
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Is the fixed-normal obstruction only the handle periods (closure), or also face simplicity?

## Method

`code/period_defect.py`: closure MILP with periods; flat 3-torus relaxation (periods in a lattice); `torus_simple` with simple faces; period-defect annealing in R^3.

## Results

With a general lattice the closure defect is exactly 0 for types 0 and 58 (configurations in `results/torus/`), but faces are not simple; with simple faces the same problems are INFEASIBLE (116 s, 392 s). R^3 annealing: 17.6 -> 8.5.

## Conclusions

NUMERICAL: closure alone can be met on the torus; face simplicity is an independent strong part of the obstruction (FD9).

## Next

Night-2 period-defect sweep (E-261029-16).
