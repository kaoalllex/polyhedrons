---
id: I-261117-02
title: Move infinity, not the planes - plane-only symmetry clauses in a generic chart make fixed-face half-turn families uniform
date: 2026-11-17
status: open
direction: [DR18, DR12]
origin: [I-261113-04, I-261030-12, I-261029-15, owner]
---

## Idea

For a half-turn fixing face X and swapping pairs (A, B), the forced zero chi(X, A, B, infinity) depends on the chart
(`experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/SOUNDNESS.md`, "Isometry clauses"). In a generic rational
chart disjoint from the solid the chirotope is uniform if the planes are in general position; the symmetry clauses
act on plane-only bases (determinant +1). The owner's projective idea B1, made concrete.

## Why it might help

It reopens the symmetry classes that uniform formulas could not take: C2 4 x 2 + 1 at nine planes (sampling on the
frozen engine with a far plane as infinity), the (9, 4) maps with an involution fixing one face, and the 20 (11, 5)
maps with Aut+ = 2 (I-261116-04) as a new registration. Plane-only symmetry is a necessary relaxation: a SAT model
need not carry a projective half-turn; the equivariant perturbation step is unproved (lemma session E-261116-09).
Several fixed faces can force plane-only zeros. Untested proposal.

## Cheapest test

Szilassi control chain: exact plane-only determinants; a rational chart missing the whole solid; exact transformed
signs and embedding; the pinned SAT control with the correct gauge (`symbreak` normalises against infinity: check).
Then the seven-plane rung 3 x 2 + 1 must recover Szilassi (planted and unaided recovery apart). 1 core-h.

Source: `reviews/dialogue-2026-11-16-strategy.md` §2 row 2, §3 (B1), Appendix A4 (N2). Nearest: I-261113-04.
