---
id: I-261101-14
title: Tight (minimal total absolute curvature) realizations - excluded for trivalent polyhedra of positive genus
date: 2026-11-01
status: parked
direction: [DR3]
origin: [FD7, L:banchoff1967, L:kuehnel1995]
---

## Idea

The covering condition of FD7 is the Chern-Lashof inequality in polyhedral form: total absolute curvature
TAC = sum |delta_v| = 2 (integral of p) + 4 pi (g - 1) >= 4 pi (g + 1), with equality iff the convex corners' normal
cones tile the sphere once (p = 1 almost everywhere: a *tight* surface). A tight Szilassi-12 would be a natural
ansatz: the convex triangles would form a spanning sub-sphere of T with exactly 20 triangles, the normals the radial
projection of a simplicial 12-vertex polytope, the offsets linear (FD8).

## Why it is parked

The ansatz is empty. Lemma [P, reviewer, unreviewed]: for a trivalent polyhedral surface in general position, tight
implies convex. Proof: let v = (X, Y, C) be a convex corner and v' = (X, Y, C') its neighbour along e_XY. Crossing
the arc n_X n_Y of the tile Delta_v at a generic point, the multiplicity p changes from 1 to 0 + [v' convex], because
by general position the only tiles with that arc on their boundary are those of v and v'. Since p >= 1 everywhere,
v' is convex. The edge graph is connected, so every vertex is convex, every vertex contributes +1 to the degree,
deg = 1 and g = 0. Consequences for Szilassi-12: p(m) >= 2 on a set of positive measure next to every arc of a
convex-saddle edge, and sum of delta over convex corners is strictly greater than 4 pi.

## Cheapest test

Exact p(m) on sampled directions for the 247 archived realizations: never identically 1 (sanity check of the
lemma); and a look at Kuehnel 1995 for a prior statement.

## Source

Strategy review 2026-11-01, follow-up work by the reviewer (cross-field: tight polyhedral surfaces, Banchoff;
Kuehnel).
