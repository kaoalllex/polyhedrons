---
id: E-261113-04
title: Cube-and-conquer pilot on (10, 4) maps 96 and 85 - do segment-order cubes cut the summed kissat time?
date: 2026-11-13
status: running
direction: [DR19, DR8]
origin: [I-261031-02, E-261108-03, E-261110-06]
tests: [H-261101-06]
produces: []
preregistered: true
---

> Running (pre-registered in `PLAN.md`), explore. Week item 4 of the 2026-11-13 plan, the gate of E-261110-06.
> Scores T D F G R: 1 2 2 2 2 | budget: one prep session + <= 3 core-h, 10 shards. No proofs.

## Goal

Does splitting the plain S5 formula into cubes cut the summed kissat core-seconds on the two slow (10, 4) maps measured
by E-261108-03, 96 (stratum A, 1073 s) and 85 (stratum B, 2749 s)? march_cu could not be built in this session (the
session's permission system refused to build downloaded third-party code), so the cubes are the segment-order cubes
the row names as the fallback: three order literals per doubled pair, three pairs per map, 512 cubes per map.

## Next

Controls, readings and stop rule: `PLAN.md`. Kill: summed cube time >= 0.7x monolithic on both maps -> park
cube-and-conquer at this budget. <= 0.5x on both -> the eight (10, 3) maps without symmetry (Lutz #3, 5, 7, 9, 10, 11,
13, 18) with cubes are proposed to the owner; (10, 4) strata A + B stay behind them under the rule of E-261110-06.
