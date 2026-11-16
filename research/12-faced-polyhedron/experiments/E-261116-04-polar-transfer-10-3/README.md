---
id: E-261116-04
title: Polar transfer - polar planes of the Hougardy-Lutz-Zelke (10, 3) realizations in every affine chart
date: 2026-11-16
status: planned
direction: [DR5, DR19]
origin: [I-261116-01]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, explore, jump 2. Scores T D F G R: 1 2 2 1 2 | budget: one session, seconds of compute.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 5 (`ROADMAP.md`). Is some affine chart of the polar of a known vertex realization of a (10, 3) map an S6
object?

## Next

Obtain the coordinates of the 17 general-position realizations (literature data, untrusted: read, never run). Polar
planes of each; every feasible sign pattern of the hyperplane at infinity (exact LP), each chart through
`verify_candidate.py --target S6`. Control: the polar of a cube is an octahedron. Coordinates not obtainable ->
Szilassi's planes as points against the Csaszar torus. Follow-up: PASS -> `candidate-check`, escalate; none -> park
I-261116-01 with the count of charts tried.
