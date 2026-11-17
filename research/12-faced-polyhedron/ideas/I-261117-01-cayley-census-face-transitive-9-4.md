---
id: I-261117-01
title: Cayley census - every face-transitive cubic (9, 4) map is a Cayley map of Z9 or Z3 x Z3; list them and decide each
date: 2026-11-17
status: open
direction: [DR19]
origin: [I-261030-18, I-261101-15, E-261103-01]
---

## Idea

A cubic nine-face genus-4 map whose orientation-preserving group is transitive on the faces has a Sylow 3-subgroup
of order 9 acting regularly (face stabiliser divides 10, index <= 2, nine odd), so it is a Cayley map of Z9 or
Z3 x Z3 (PROVED-1 sketch, dialogue 2026-11-16-strategy, A3). Enumerate the dual rotations (a cyclic order of ten slots:
the eight non-identity elements and one inverse pair repeated, all faces triangles; at most about 2.2e6) and decide
each map by the plain formula at 10 elements and the free-C3 uniform formula.

## Why it might help

A complete list of one natural slice of S1 at nine faces that needs no full census; the known (8, 3) objects
(Roest-Vigh's map) are of this kind one rung below. It covers patterns 9 and 3+3+3 of the equivelar slice
(I-261101-15). Face transitivity alone gives only g = 1 mod 3; g = 7 is not enumerated. Untested proposal.

## Cheapest test

The rung below: the five groups of order 8 at (8, 3), valency 9; Roest-Vigh's map must appear (a map automorphism,
not a geometric symmetry). Then Z9 and Z3 x Z3 at (9, 4); raw rotations, valid maps, distinct maps; 1 core-h.

Source: `reviews/dialogue-2026-11-16-strategy.md` §2 row 1, Appendix A3 (N1). Nearest: I-261030-18.
