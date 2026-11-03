---
id: I-261103-05
title: Spectral start for embedded-first - a Tutte / Colin de Verdiere type 3D drawing of the cubic 1-skeleton as the initial embedded surface
date: 2026-11-03
status: open
direction: [DR17, DR19]
origin: [I-261103-01]
---

## Idea

I-261103-01 needs an embedded surface with the target map as its starting point. Build it from the graph: a vector
representation of the cubic 1-skeleton (26 vertices for (9, 3)) in R^3 by a nullspace / low-eigenvector embedding of a
Laplacian-type matrix with the face cycles as constraints (Tutte-style barycentric drawing generalised to three
dimensions, Lovasz-Schrijver and Colin de Verdiere nullspace representations) gives straight edges and face polygons that
are near-planar by construction; triangulate the faces and start the barrier planarisation from there. Algebraic graph
theory, untried here.

## Why it might help

The starting surface decides whether the planarisation has a chance; a spectral drawing already minimises a quadratic
non-planarity and respects the map's symmetry when the matrix does. CONJECTURE.

## Cheapest test

The Szilassi map's spectral drawing: measure its planarity energy and whether it is embedded; then the Roest-Vigh map.
Minutes with numpy.

## Source

Strategy review 2026-11-03 (`reviews/strategy-review-2026-11-03.md` section 4, idea 4).
