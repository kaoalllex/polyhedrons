---
id: I-261114-05
title: Geometry of realization spaces - regions, quotients and transitions instead of single coordinate solutions
date: 2026-11-14
status: open
direction: [DR10, DR13, DR17]
origin: [owner, I-261101-05, I-261101-09]
---

## Idea

Owner's proposal of 2026-11-13 (three local notes, not in the repository): look for the rare polyhedra through the
structure of the space of face-plane configurations (chirotope chambers, degenerate boundaries, transitions,
obstructions) instead of coordinate optimization; an external review proposed a pilot on dependency sets of violated
predicates with a hitting-set lower bound.

## Why / cheapest test

Lead review 2026-11-14 (Recommendation): the space is the face-plane space the project already uses; e-means does
not apply; the hitting-set pilot is below the gate, because conflict analysis in the SAT solver derives stronger
statements from the same predicates plus the Grassmann-Pluecker clauses; fixed-normal convexity is FD8 and Farkas
transfer is E-261101-24. Actionable parts: which transformations to quotient out (I-261114-01, I-261110-06) and
transitions from a realized parent (I-261114-04). A datum: E-261113-03 found two far-apart chirotope cells of one map
over the same seven planes. The literature list of the notes is not checked (CLAIMED).

Source: `reviews/strategy-review-2026-11-14.md` §3, §6 (N5).
