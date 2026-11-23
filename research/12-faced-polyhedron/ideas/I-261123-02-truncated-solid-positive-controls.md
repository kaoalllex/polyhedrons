---
id: I-261123-02
title: An unaided positive control at every new element count - truncate a convex vertex of a known solid
date: 2026-11-23
status: open
direction: [DR19]
origin: [I-261101-20, E-261117-04]
---

## Idea

Cutting one convex vertex of a known face-neighbourly solid by a new plane gives an embedded polyhedron with F + 1
faces, the same genus and the same doubled pairs, plus a triangle adjacent to three faces. Its map is realized, so its
plain sub-map formula at F + 2 elements must be SAT unaided. Both known (8, 3) solids have four convex vertices
(I-261101-20), so each yields nine-face genus-3 controls with eight doubled pairs: (V, E, F, chi) = (26, 39, 9, -4),
23 single, 8 double and 5 absent pairs (`--all-pairs` fails by design; the bare verifier is the check).

## Why it might help

About 111 thousand nine-face formulas are UNSAT-SOLVER (STATUS 3bf, 3bm, 3bn), while the only 10-element SAT controls
were a convex genus-0 solid (f9) and convex runner controls, and the symmetric formula controls test GP, symmetry and
gauge clauses only (`E-261119-02/controls_b.py`). A constant diagnostic needs a control on the measuring function
(`CLAUDE.md`). The same construction serves any later element count.

## Cheapest test

Done as a session check in the cross-review of 2026-11-23 (check A): Roest-Vigh cut by (7, 14, 21, -57), face-8 link
(2, 6, 3); Mizhaev cut by (1, 2, 3, -1113), link (3, 2, 0); both plain formulas SAT in 0.08 s with a clause-checked
model, both bridged to embedded files. Not ledger evidence until E-261123-01 step 0 registers them as fixtures.

Source: `reviews/strategy-review-2026-11-23.md` §5 N2, `-codex.md` check A, `-final.md` points 1-2 (owner-approved 2026-11-23).
