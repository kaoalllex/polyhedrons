---
id: I-261101-16
title: Close the FD6 gap - no polyhedral immersion has a mirror or point-reflection symmetry
date: 2026-11-01
status: open
direction: [DR11]
origin: [E-261029-15, I-261031-06]
---

## Idea

The 25 immersion instances encode `det rho(g) = eps(g) = +1`, i.e. proper rotations only (`code/omsat_sym.py`).
For embeddings that is complete (an improper isometry preserves the solid and so reverses the surface orientation;
no type has such an involution). For immersions a mirror or a point reflection may induce an orientation-preserving
involution, and that case was never run; it cannot be encoded uniformly either (15 quadruples {a, g a, b, g b} are
forced to zero). Lemma [P, reviewer, unreviewed]: (i) a point reflection iota sends plane a to a parallel plane, but
a and iota(a) are adjacent faces and must share an edge; (ii) for a mirror sigma, the line a cap sigma(a) is
sigma-invariant, hence either perpendicular to the mirror (then sigma(a) = a, excluded since the action on faces is
free) or inside the mirror and fixed pointwise; the edge e_{a, sigma a} lies on it, sigma maps the triangle
{a, sigma a, c} to {sigma a, a, sigma c}, so sigma c is the third face at the other endpoint and the two endpoints
are swapped by sigma; both are fixed, so they coincide: a zero-length edge. Rotoreflections of order 4 have a proper
half-turn as square (covered); orders 5, 7, 11 do not occur in any automorphism group.

## Why it might help

With the lemma reviewed, FD6 holds as stated ("any non-trivial isometry"); without it the statement must say
"rotation". The write-up E-261101-10 needs one or the other.

## Cheapest test

A second reader of the twelve lines (a human; the `adversarial-verifier` agent only as a filter).

## Source

`reviews/strategy-review-2026-11-01.md` section 5.2 and Appendix A.4.
