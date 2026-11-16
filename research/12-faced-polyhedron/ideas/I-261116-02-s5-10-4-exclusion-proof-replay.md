---
id: I-261116-02
title: (10, 4) exclusion at formula scope - a checked proof replay of all 1117 admissible maps, LRAT first
date: 2026-11-16
status: parked
direction: [DR19, DR8]
origin: [E-261110-06, E-261109-06, owner]
---

## Idea

All 1117 admissible (10, 4) maps have UNSAT-SOLVER answers (stratum C plain, E-261109-06; strata A + B normalised,
E-261110-06). A checked replay would turn them into UNSAT-VERIFIED and allow the claim "no cubic maximal
face-neighbourly polyhedron with 10 faces at formula scope" (conditional on encoder soundness and census coverage,
PROVED-1), the third rung after (8, 2) and (9, 3) and a candidate for the deferred note.

## Why / cheapest test

LRAT (CaDiCaL `--lrat` with a linear checker) instead of DRAT: drat-trim on long solves did not fit 48 GB
(lead review 2026-11-09), normalised solves are 10-45x shorter. Cheapest test: one session pricing #85, #96, #926
(proof size, check time, peak memory); gate <= 2 nights and <= 200 GB transient disk. Stratum C must be re-solved
with the normalised formulas.

## Status

Parked by the owner on 2026-11-16: not now, kept for the note. Until then (10, 4) is UNSAT-SOLVER: it may skip or
rank maps in planning, never a negative result. A replay removes the solver risk only; encoder soundness and census
coverage remain PROVED-1. Untested proposal.

Source: `reviews/strategy-review-2026-11-16.md` §1 item 3, §5 (N2).
