---
id: H-261101-10
title: Handles are the wrong move - no genus-3 realization space reaches an in-class handle
date: 2026-11-01
status: open
origin: [I-261101-11, E-261030-06, E-261101-07]
---

## Statement

No connected component of the realization space of an archived genus-3 polyhedron contains a plane set at which
some handle has k_tau = -1. Equivalently, in normal space the realization region of M and the Gauss class of
M + tau are disjoint for every arm.

## Rival

Such plane sets exist; the nights-4/5 drift missed them because its energy asked `hemisphere_margin` for a
value the function cannot return (artefact, `reviews/strategy-review-2026-11-01.md` 5.1).

## Evidence so far

k_tau = 0 on all 21 type-0 arms at the realizations' own normals (E-261030-06) and in 40 random projective charts of
one witness (strategy review, Appendix A.1, EXACT on that instance). The drift evidence of nights 4-5 is void.

## What would move it

E-261101-19 (barrier continuation with a correct measure): a path to k_tau = -1 refutes it; none on 40 realizations
supports it; a proof makes handle ladders REFUTED. E-261101-16 (a higher-genus solid on an archived arrangement)
also refutes it.
