---
id: E-261101-12
title: Maximal face-neighbourly cubic polyhedra per genus
date: 2026-11-01
status: planned
direction: [DR12, DR15]
origin: [I-261101-07, E-261030-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 2 2 | budget: literature 1 session; then 1 night per case. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

Focus target of the project since 2026-11-03 (`STRATEGY.md`): an S5 polyhedron at **(9, 3)**, then the stretch
target **(10, 4)**. Which of (8,2), (9,3), (10,4), (11,5) exist; start with the literature check.

## Starting point (2026-11-01)

First task (one file, no compute): `code/control_mizhaev.py` modelled on `control_rost_vigh.py`, from
`literature/mizhaev2026-planes.json` (planes, face walks, derived links), added to `verify_all` CHECKS as the second
positive control with doubled adjacencies (expected: EMBEDDED, 20 single + 8 doubled pairs, degree -2, 20 saddles).
Then the (8, 2) case with a two-orbit symmetric ansatz calibrated on both 8-face objects.

## Next

Stop rule: (9, 3) found (`--target S5` PASS, `candidate-check`) or every map tried UNSAT with a power statement; then
(10, 4) under the same rule
