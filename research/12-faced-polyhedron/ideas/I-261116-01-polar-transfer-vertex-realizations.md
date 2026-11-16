---
id: I-261116-01
title: Polar transfer - the polar planes of the vertex realizations of the (10, 3) maps, tested in every affine chart
date: 2026-11-16
status: open
direction: [DR5, DR19]
origin: [L:hlz2010, I-261110-02]
---

## Idea

Hougardy, Lutz and Zelke give small-integer realizations of 17 of the 20 vertex-minimal genus-3 triangulations with
10 vertices (vertex version, CLAIMED). Polarity sends a face plane to a vertex, a triple point to a triangle plane
and an edge line to an edge line, exactly; only embeddedness differs. Take the polar planes of each realization and
test every affine chart (each feasible sign pattern of the hyperplane at infinity, exact LP) with
`verify_candidate.py --target S6`.

## Why / cheapest test

`literature/README.md` says the vertex result does not transfer by duality: a general statement, not a test of these
objects in all charts. The test is finite, exact and takes seconds. Control: the polar of a cube is an octahedron.
If the coordinates cannot be obtained: Szilassi's seven planes as points against the Csaszar torus instead.
Kill: no chart of any object passes. Untested proposal.

Source: `reviews/strategy-review-2026-11-16.md` §5 (N1).
