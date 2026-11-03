---
id: I-261103-03
title: Interval branch-and-bound over the C3 ansatz - a complete decision of the symmetric (9, 3) case by validated numerics
date: 2026-11-03
status: open
direction: [DR19, DR18]
origin: [I-261030-07, I-261101-08, H-261103-02]
---

## Idea

A C3-symmetric (9, 3) polyhedron has about 7 free parameters (three orbit representatives of planes, the axis fixed).
Every realizability condition is the sign of a polynomial in them (determinants of planes and triple points). Cover a
compact parameter box by interval boxes: a box is discarded when, by interval arithmetic, some sign is constant on it and
wrong for every admissible C3 map; otherwise it is split; a leaf on which every sign is decided and consistent with some
map is an exact candidate (then `candidate-check`). The outcome is either an object or a proof "no C3-symmetric (9, 3)
polyhedron with parameters in the box"; with a projective normalisation the box can be made to cover everything.

## Why it might help

It is the computer-assisted-proof technique of validated numerics (Tucker-style), untried here; it decides the symmetric
case *completely*, which no sampler or annealer does, and it transfers to S0's loophole (I-261101-08: symmetric
arrangements with asymmetric solids, with the solid chosen by the inner solver per leaf). CONJECTURE.

## Cheapest test

A 2-parameter slice of the Roest-Vigh D2 family (their two free planes with the others fixed) must isolate a leaf containing
their solution; count the boxes and the time. If the slice needs more than ~10^6 boxes, the 7-parameter case is out of
reach and the idea is parked.

## Source

Strategy review 2026-11-03 (`reviews/strategy-review-2026-11-03.md` section 4, idea 2).
