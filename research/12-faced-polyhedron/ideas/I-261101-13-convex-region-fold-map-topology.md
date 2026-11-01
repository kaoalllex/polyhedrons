---
id: I-261101-13
title: The Gauss map as a fold map - topology of the convex region as rank-3 clauses
date: 2026-11-01
status: open
direction: [DR9, DR3]
origin: [FD7, I-261029-16, L:quine1978, L:bgm1982]
---

## Idea

In the gauge the PL Gauss map T -> S^2 preserves orientation on the convex-corner triangles C, reverses it on the
saddle triangles Sigma, and folds along the edges between them (the fold locus, boundary of C). For smooth fold maps
the degree obeys Quine's formula deg = (chi(M+) - chi(M-) + cusp terms) / 2. Derive the PL analogue for the Gauss
map (vertex corrections at normals the fold passes through), check it on every control (tetrahedron, cube, Szilassi,
Roest-Vigh, the 247 archived realizations), and turn it into clauses on the 44 vertex-type bits for the rank-3 SAT
(E-261101-06): constraints on c, on the fold-locus length E_CS (chi(C) = 12 - c/2 - E_CS/2 when every face has a
convex corner) and on the number k_X of convex runs around each face.

## Why it might help

Degree -5 and >= 13 saddles use only counts; the topology of the convex region is an exact, unused constraint, and it
is a rank-3 statement, so it prunes the normal-level search where the project wants to split (cube-and-conquer on
the rank-3 contraction). Cross-field: singularity theory of fold maps (Quine 1978), cusps of Gauss mappings
(Banchoff-Gaffney-McCrory 1982).

## Cheapest test

Compute (c, E_CS, k_X, chi(C), chi(Sigma), deg) on the 247 realizations and the controls; look for the identity;
one session.

## Source

Strategy review 2026-11-01, follow-up work by the reviewer.
