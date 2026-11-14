---
id: E-261114-03
title: Chart normalisation at a hull vertex - lemma, re-charting controls and per-vertex cubes on the slowest normalised maps
date: 2026-11-14
status: planned
direction: [DR19, DR8]
origin: [I-261110-06, I-261114-01]
tests: [H-261101-06]
produces: []
preregistered: false
---

> Planned, explore, conditional. Scores T D F G R: 2 2 2 2 2 | budget: one session + <= 3 core-h, 10 shards.
> Runs only if E-261114-01 leaves > 20 % TIMEOUT or E-261110-06 is priced above one night. `PLAN.md` first.

## Goal

Week item 4 (`ROADMAP.md`). Remove the freedom in the choice of the plane at infinity: some convex vertex `a, b, c`
is a hull vertex, and with a plane just outside it sent to infinity the element INF is a positive combination of
the three outward planes, so `chi(i, j, k, INF)` is forced whenever the signs against `a`, `b`, `c` agree.

## Next

Write the lemma (PROVED-1 at most). Controls: exact re-charting of the control objects at every hull vertex
(verifier PASS; the new chirotope satisfies the formula and the selector clauses). Pilot: one cube per candidate
vertex on the two slowest normalised maps. Kill: summed cube time >= 0.7x the normalised monolithic time on both.
A wrong normalisation voids every UNSAT, so no target formula uses it before the controls pass.
