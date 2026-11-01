---
id: E-261101-19
title: Barrier continuation from genus-3 realizations towards an in-class handle (replaces E-261101-07)
date: 2026-11-01
status: planned
direction: [DR17, DR3]
origin: [I-261101-11, E-261101-07, E-261030-11, E-261030-06]
tests: [H-261101-10, H-261101-03]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 1 2 2 | budget: one laptop night (40 realizations x about 1 core-h) after a
> 1-core-hour pilot. Before any compute: `PLAN.md` (skill `experiment-start`).

## Goal

Whether the handle normals of any arm can be pushed out of every open hemisphere (k_tau = -1) while the base
genus-3 polyhedron stays exactly embedded; and, where they can, whether the offsets of M + tau are then SAT.

## Next

Stop rule: 40 realizations (7 of type 0, 33 of type 53) x all extendable arms, or the first exact genus-4 object
(then `candidate-check`). Either outcome is a `theory/theory-notes.md` note: a path (the ladder is alive) or a
written argument why none exists (H-261101-10 towards a lemma).

## Starting point

* Do not use `gauss_gate.hemisphere_margin` as an objective: it returns 0 for every set not in an open hemisphere
  (`reviews/strategy-review-2026-11-01.md` 5.1 and Appendix A.3). Use the cosine of the smallest enclosing spherical
  cap of the six gauge normals (candidates: midpoints of pairs, circumcentres of triples; take the centre whose
  largest angular distance is smallest). It is negative exactly when the six normals are not in an open hemisphere.
  Calibrate: the octahedron axes must give about -0.58, a tight cluster a value near 1.
* Feasibility: `ladder_exact.verify` of the base map at every accepted step (exact). Barrier: -sum log(margin) over
  the float margins of the base map's forbidden-triple conditions (`code/fastviol.py` gives the triples; the margin is
  the distance of P_XYZ to the relevant edge or face boundary), step by line search that never leaves the feasible
  set, as in intersection-free simulation (IPC).
* When k_tau = -1 (`gauss_gate.k_tau`), decide the offsets of M + tau exactly at those normals and at 20 jittered
  copies (`code/fixed_normals_gauge.py`, radius 0.01).
* Pilot: type-0 realization A, arm (0,5,8)-(2,6,7), 1 core-hour; the margin trajectory must move (if it does not,
  the step rule is wrong).
* Positive control: on the genus-2 parent of a genus-3 realization, the same procedure must reach the class of the
  known child (its handle), since the child exists. Negative control: a non-extendable arm must not be offered.
* Outcomes: a SAT offset problem = a genus-4 candidate (candidate-check); k_tau = -1 reached but offsets UNSAT
  everywhere = the class is reachable and insufficient (moves H-261101-03 down); never reached on 40 realizations =
  H-261101-10 supported, write the argument.
