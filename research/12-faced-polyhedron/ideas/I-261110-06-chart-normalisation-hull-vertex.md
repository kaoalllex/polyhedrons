---
id: I-261110-06
title: Chart normalisation at a hull vertex - fix the plane at infinity next to a convex-hull vertex
date: 2026-11-10
status: open
direction: [DR19, DR8]
origin: [I-261029-43, I-261030-12, I-261030-30]
---

## Idea

A projective map that sends a plane just outside a convex-hull vertex v = (X, Y, Z) to infinity keeps the polyhedron
bounded and keeps its map. So without loss of generality some vertex v with three convex edges is the triple point
nearest to infinity on each of the lines L_XY, L_XZ, L_YZ: the `lt` signs of the other F - 3 planes against v are
fixed on those three lines.

Encoding: one selector per candidate vertex, one clause "some selector", 3 (F - 3) implied order literals per
selector. It removes the freedom in the choice of the plane at infinity.

Status of the argument: **sketch only** (PROVED-1 at most once written). It must be written out (existence of a hull
vertex with three convex edges in a cubic polyhedron; that the re-charted object satisfies every clause family of the
encoder, the reorientation units `SB_REORIENT` / `SB_MIRROR` included) and checked on the pinned controls before any
formula uses it. A normalisation that is wrong turns UNSAT answers into non-results.

## Why it might help

The existing breakers (I-261029-43) fix the reorientation gauge only; the chart freedom is a separate, larger
symmetry of the formula. Relatives I-261030-12 and I-261030-30 move the plane at infinity as a search move; this
fixes it as a normalisation.

## Cheapest test

Three known (9, 3) maps with recorded times, with and without the selectors; the pinned positive controls must stay
SAT. Kill: < 1.5x on all three. Low priority, as I-261110-05.

## Update 2026-11-14

The plain S5 / S6 formulas did not carry the reorientation breakers (I-261114-01), so the sentence above held for the
S0 formulas only. Stronger form (lead review 2026-11-14, N2, sketch only): with the plane just outside the hull vertex
sent to infinity, INF is a positive combination of the three outward planes at the vertex, so `chi(i, j, k, INF)` is
forced whenever the signs of `i, j, k` against the three planes agree; that constrains all C(F, 3) signs with INF,
not 3 (F - 3). Planned as E-261114-03, conditional on E-261114-01.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §4 I-F). Untested.
