---
id: I-261108-04
title: Grooved-box positive control - an embedded polyhedron in which one face pair shares three or four collinear segments
date: 2026-11-08
status: open
direction: [DR19]
origin: [E-261103-02, E-261103-03]
---

## Idea

A box with k V-grooves cut across one edge has two faces (top and front) that share k + 1 collinear segments. With the
groove walls tilted to general position it is a cubic genus-0 polyhedron with 6 + 3k faces (12 for k = 2). Its own map,
encoded through the `submap=True` path with the planes pinned, must be SAT; the same planes on a map with one segment
pairing swapped must be UNSAT-VERIFIED.

## Why it might help

No positive control of the S5 encoder has a pair with multiplicity >= 3: the run controls are convex, and Roest-Vigh
and Mizhaev have only doubled pairs. 18 admissible (9, 3) maps, one (8, 2) map and 109 (10, 4) maps have such a pair
(EXACT counts), so 128 S5 formulas rely on clauses that no real object has tested. Untested.

## Cheapest test

k = 2 (tripled pair) and k = 3 (quadrupled pair), exact rational planes, `ladder_exact` / `verify_solid`, then the
pinned formulas: one session, minutes of CPU.

## Source

Lead review 2026-11-08d, §6 idea N1 and audit A1; week item 1.
