---
id: E-261029-16
title: Period-defect search over all 59 types
date: 2026-10-29
status: done
direction: [DR4]
origin: [E-261029-14, I-261029-17]
tests: [H-261029-11]
produces: []
verdict: LOW-YIELD@night 2
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Find Gauss-admissible normals whose faces close up (zero period defect), per type.

## Method

Laptop night 2, job `pdefect` (closure MILP inside an annealer), later with a simplicity check.

## Results

170 records, 161 positive defects, 9 zero-defect normal sets - all false positives (11 or 12 of 12 faces must be non-simple; three checked by hand, six flagged automatically). Best positive: type 11, 1.20 (not scale-normalized). Records: `results/pdefect/`.

## Conclusions

NUMERICAL: zero closure defect is necessary, not sufficient; closure-first does not reach simple faces.

## Next

Parked (STATUS DR4); simplicity must be inside the model.
