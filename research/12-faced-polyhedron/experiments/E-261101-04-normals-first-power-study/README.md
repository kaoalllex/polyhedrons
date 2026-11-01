---
id: E-261101-04
title: Power of normals first: how often is the control SAT at radius r?
date: 2026-11-01
status: planned
direction: [DR2]
origin: [I-261101-01, E-261030-08, E-261030-11]
tests: [H-261101-04, H-261029-09]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: ~10 core-h. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

Measure the SAT rate of the positive control per radius, so that the 12,202 UNSATs can be weighed.

## Next

Stop rule: 30 maps x 3 radii, or earlier if the rate is clear

## Starting point (moved from ROADMAP.md)

Hypothesis H0: at in-class seeds the offset problem is generically SAT near the realized normals, so 0 SAT in
12,202 means something. Test: `code/nf_control.py` on 30 realized maps (archive, several types) x r in {0.01,
0.02, 0.05}, z3 timeout 600 s. Outcomes: control SAT rate p >= 0.3 at some r -> the night-4/5 UNSATs at that r
are real evidence of an obstruction between levels (then E-261101-05 on them); p ~ 0 -> normals-first sampling is
blind, retire the UNSAT counts as evidence; timeouts dominate -> encoding cost problem, not geometry.
