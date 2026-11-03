---
id: I-261103-06
title: Z3 fundamental piece - build a C3-symmetric (9, 3) polyhedron as three copies of a planar-faced patch whose boundary matches its rotated image
date: 2026-11-03
status: open
direction: [DR19, DR12]
origin: [I-261030-18, I-261030-04, H-261103-02]
---

## Idea

For the 8 admissible (9, 3) maps with a free C3, the quotient is a torus map with 3 vertices, 13 edges, 8 triangles and 2
branch points (the two fixed polyhedron vertices, on the axis). Build the polyhedron as three copies, under a 120-degree
rotation, of one fundamental piece: three planes, one third of the surface, a planar-faced surface with boundary whose
boundary arcs match those of the rotated copy. The search variables are the three planes and the piece's cell selection;
the matching conditions are exact incidences along the boundary. This is how crystallographers build a unit cell, and it
turns the symmetric ansatz into a boundary-matching problem for a small patch.

## Why it might help

Fewer variables than the full symmetric arrangement, a direct use of the quotient structure, and every solution is
C3-symmetric by construction (legal for S5). CONJECTURE.

## Cheapest test

Recover the Roest-Vigh object from one D2 piece (two planes, a quarter of the surface) by the same matching conditions;
then the first C3 (9, 3) map of `reviews/strategy-review-2026-11-03-maps.json`.

## Source

Strategy review 2026-11-03 (`reviews/strategy-review-2026-11-03.md` section 4, idea 5).
