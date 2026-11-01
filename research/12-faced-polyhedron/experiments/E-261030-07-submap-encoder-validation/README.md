---
id: E-261030-07
title: Validate the exact offset solver on sub-maps
date: 2026-10-30
status: done
direction: [DR2]
origin: [E-261029-07, E-261030-03]
tests: []
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

The offset SMT must work for the ladder sub-maps, in both directions.

## Method

`omsat.Triangulation(..., submap=True)`, `code/submap_validate.py`, `fixed_normals_gauge.solve_gauge`.

## Results

5/5 realizations SAT at their own normals (96-173 s, exactly EMBEDDED); 3/3 genus-4 maps at genus-3 normals UNSAT, as the degree theorem requires; negative controls flag the attempts.

## Conclusions

EXACT: tool validated.

## Next

Normals first (E-261030-08).
