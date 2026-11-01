---
id: E-261101-21
title: The Gauss map as a fold map - find the identity on the controls, then add it to the rank-3 encoding
date: 2026-11-01
status: planned
direction: [DR9, DR3]
origin: [I-261101-13, E-261030-10, E-261101-06]
tests: [H-261101-14]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 2 2 | budget: one session of theory plus minutes of compute. Before any compute:
> `PLAN.md` (skill `experiment-start`).

## Goal

For every control (tetrahedron, cube, Szilassi, Roest-Vigh, the 247 archived realizations): the number of convex
vertices c, the fold-locus length E_CS (edges between a convex and a saddle vertex), the number k_X of convex runs
around each face, chi of the convex and saddle regions, and the degree; then the identity that holds on all of
them, with its proof sketch; then the effect of adding it to E-261101-06 (model counts with and without).

## Next

Stop rule: one session. Outcome either way goes to `theory/theory-notes.md`: an identity with proof (PROVED-1) and
its clause form, or a written statement that the local identities already imply everything found.

## Starting point

* Vertex types from `gauss_gate.own_gauge` and `sign_tables` (convex iff the gauge determinant is positive, F3);
  the regions are subcomplexes of T; chi(C) = (faces with a convex corner) - (edges in a convex triangle) + c.
* Known smooth fact to adapt (CLAIMED from memory, verify in the source): for a stable map between closed oriented
  surfaces, deg * chi(target) = chi(M+) - chi(M-) + (signed cusps) (Quine 1978).
* Negative control: a random sign vector with the right counts (c, s) that is not the gauge of any realization should
  violate the identity in most cases, otherwise the identity has no pruning power.
