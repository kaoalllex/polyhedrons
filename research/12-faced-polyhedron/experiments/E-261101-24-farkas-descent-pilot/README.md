---
id: E-261101-24
title: Farkas-certificate descent on the normals - pilot on the 80 radius-0 seeds and a perturbed witness
date: 2026-11-01
status: planned
direction: [DR2, DR4, DR17]
origin: [I-261101-19, E-261030-11, E-261029-16]
tests: [H-261101-16, H-261101-09]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 1 2 | budget: 1 day of coding, about 5 core-h. Parked methods DR2 / DR4 are
> involved; what is different: the normals move along the exact dual gradient of the offset LP, not by annealing or
> random radii. Before any compute: `PLAN.md` (skill `experiment-start`).

## Goal

Whether guided moves of the normals turn UNSAT offset problems into SAT ones: trajectories of the infeasibility
measure from the 80 in-class seeds of nights 4-5 and from a genus-3 witness perturbed by 0.1 (the nights-4/5 control
is UNSAT there), with an exact decision at every SAT.

## Next

Stop rule: 50 steps per seed, 5 core-h, or the first exact S3 object at a level where sampling found none. The
positive control (the perturbed witness returns to SAT) must pass before the seeds are run.

## Starting point

* Inner LP: `code/fixed_normals_gauge.py` decides the offsets exactly (z3 / LRA). For the gradient use an LP phase-1
  formulation with HiGHS (`scipy.optimize.linprog`): minimise the sum of slacks s subject to A(n) d + s >= 1, s >= 0;
  the dual solution y of that LP is the Farkas certificate when the optimum is positive.
* Gradient: the entries of A(n) are 3x3 and 4x4 determinants of plane rows (FD8); differentiate them with respect to
  the normals analytically (or by automatic differentiation on the float copy) and take g = y^T dA/dn as the step
  direction on the normals, projected to the unit spheres; step size by backtracking on the phase-1 objective.
* Which sign cell: start from the cell the seed's own gauge and the Gauss gate prescribe (`gauss_gate`); if the cell
  changes along the way (a determinant crosses zero), re-derive it from the current float configuration.
* Report per seed: phase-1 objective per step, number of cell changes, final exact verdict; for SATs run
  `candidate-check` with the level's target.
