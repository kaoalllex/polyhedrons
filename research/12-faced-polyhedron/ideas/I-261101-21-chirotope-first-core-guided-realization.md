---
id: I-261101-21
title: Chirotope first - core-guided incremental SAT with geometric assumptions, then realize the model
date: 2026-11-01
status: tried
direction: [DR8, DR9, DR17]
origin: [FD2, FD8, I-261101-18, I-261029-57, I-261029-11, L:schewe2010]
---

## Idea

Search in the space of oriented matroids, where "embedded" is a logical constraint (FD2), and let geometry enter only
as a seed and as a realization. Seed: the rank-3 signs chi(X, Y, Z, inf) of a plane set (the combinatorics of its
normals) are passed to the SAT solver as assumptions; with the normals fixed the remaining problem is the offsets
(FD8), so the solver is fast. If the assumptions contradict embedding, the UNSAT core names the normal signs that
must change; release exactly those and re-solve (core-guided relaxation, as in MaxSAT). A model is a full chirotope
satisfying every embedding clause; realize it by hinge-loss descent on the 715 signed determinants with analytic
gradients, round to integers, recompute the exact chirotope and run `ladder_exact.verify`: by Lemma 5.1 a realized
model is a polyhedron. A model that does not realize blocks its rank-3 part (CEGAR; biquadratic final polynomials
would give sharper cuts). The face ladder (I-261101-18) is the same loop on k-face sub-instances with the previous
realization as the next seed.

## Why it might help

Every engine so far optimised an intersection count or a float energy in geometry and plateaued (DR1, DR6); here the
solver chooses the combinatorial type of the whole arrangement and the only continuous problem is sign fitting.
Cross-field: core-guided MaxSAT, CEGAR from model checking, Bokowski-Richter-Gebert realizability of small oriented
matroids, Schewe's OM + SAT for the vertex version (used there only for UNSAT).

## Cheapest test

E-261101-25: n = 7 from random planes must end EMBEDDED; the realizer must recover known 12-plane chirotopes from
random starts; then the full type-0 instance from class seeds with a 2-minute timeout per solve.

## Source

Strategy review follow-up 2026-11-01 (algorithm v2).
