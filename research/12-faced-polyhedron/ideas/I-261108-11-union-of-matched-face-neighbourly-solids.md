---
id: I-261108-11
title: Boolean union of two projectively matched face-neighbourly solids - a direct genus source for (10, 4) and, in stage 2, for the 12-face target
date: 2026-11-08
status: open
direction: [DR19]
origin: [owner, L:szilassi1977, L:mizhaev2026, L:roestvigh2026]
---

## Idea

Take two exact known solids P1 (F1 faces, genus g1) and P2 (F2, g2), map P2 by a projective transformation whose
pole misses both solids so that k of its face planes coincide with k face planes of P1, and take the boundary of the
union. If the solids intersect in j disjoint balls, glued as ordinary boundary patches, the union is a handlebody of
genus g1 + g2 + j - 1 (PROVED-1, conditional on that intersection pattern), with F1 + F2 - k planes. PGL(4) acts
simply transitively on 5 planes in general position, so k <= 4 leaves 15 - 3k continuous parameters and k = 5 is
rigid (finitely many correspondences); k >= 6 is generically impossible. Copy 2 may also be deformed inside its own
realization space with the k matched planes fixed (more freedom for a follow-up search).

Budget per target (counting heuristics, untested): the (F1 - k)(F2 - k) pairs of exclusive faces of different
copies must be created on the seams; the simplest overlap (a corner of each solid inside the other) gives a hexagonal
seam with up to 6 such pairs. Pieces with multiple adjacencies import extra adjacencies that the target cannot afford
(it allows 3 at (10, 4), 2 at (11, 5), 0 at (12, 6)); Mizhaev and Roest-Vigh carry 8 each, Szilassi and the
tetrahedron none.

| Target | Pieces | k | j | parameters | pairs needed / seam budget | imported extras |
|---|---|---:|---:|---:|---|---:|
| (10, 4) | Szilassi + Szilassi | 4 | 3 | 3 | 9 / 18 | 0 |
| (10, 4) | Szilassi + tetrahedron | 1 | 4 | 12 | 18 / 24 | 0 |
| (10, 4) | Mizhaev or Roest-Vigh + tetrahedron | 2 | 2 | 9 | 12 / 12 | 8 |
| (10, 4) | Szilassi + Mizhaev or Roest-Vigh | 5 | 1 | rigid | 6 / 6 | 8 |
| (10, 4) | Mizhaev + Roest-Vigh | 6 | - | impossible | - | - |
| (12, 6) | Szilassi + Szilassi | 2 | 5 | 9 | 25 / 30 | 0 |
| (12, 6) | Mizhaev + Roest-Vigh | 4 | 1 | 3 | 16 / 6 | 16 |
| (9, 3) control | Szilassi + Szilassi | 5 | 2 | rigid | 4 / 12 | 0 |

Stage 2, the 12-face form: Szilassi + Szilassi with k = 2 and five balls; pairs 21 + 21 - 1 + 25 = 66 = C(12, 2), so
every pair is accounted for exactly once if each copy keeps its own adjacencies and the seams create the 25 cross
pairs without doubling. A cheap combinatorial filter comes first: does any of the 59 K12 types decompose as two
7-vertex torus pieces sharing two vertices and joined by five tubes?

**The pieces need not be known, or face-neighbourly** (owner's question, 2026-11-08). The union boundary consists of
patches of each solid's boundary outside the other; two faces of the same piece meet in the union only along an edge
that piece already had, and only faces of different pieces meet on the seams (elementary, general position). So the
real condition is weaker: in each piece the faces that are not on a matched plane must be pairwise adjacent; faces on
matched planes may gain adjacencies through the other piece. The clique is bounded by Heawood for the piece's genus
(4 on the sphere, 7 on the torus, 8 at genus 2, 9 at genus 3), and a piece may carry extra faces beyond its clique if
they lie on matched planes (k <= 5 in total). This opens three families:

* genus-0 pieces: any polyhedral sphere with 3 pairwise adjacent faces (every vertex has them) or 4; e.g. Szilassi +
  a combinatorial cube matched on 3 planes, the cube's free corner giving its 3 exclusive faces (10 faces, four
  balls for genus 4, 6 projective parameters plus the cube's own shape); the tetrahedron source is the simplest case;
* modified known objects: Szilassi with a truncated corner (8 faces, genus 1, the 7-clique kept), the new face used
  as a matched plane;
* bootstrapping: every union that passes becomes a piece for the next union. Szilassi + Szilassi with k = 5 and three
  balls gives (9, 4), and Szilassi + tetrahedron with k = 2 and four balls gives (9, 4) with 9 parameters: candidates
  for the first face-neighbourly polyhedron with 9 faces (none in print, CLAIMED). The rigid k = 5 list is the same
  enumeration as the (9, 3) cross-check.

## Why it might help

It is a direct genus source with few parameters, not a handle ladder and not a free cell selection; it reaches the
target genus in one step (jump). The rigid (9, 3) row is a geometric cross-check of the (9, 3) negative: any embedded
cubic (9, 3) boundary from it would contradict the UNSATs and stop the note. Untested: the union must also have
simple connected faces (the shared planes merge two faces into one), cubic vertices and all pairs adjacent; the
topology alone does not give them. Low probability, high payoff.

## Cheapest test

Stage 1 is week item 5 of `ROADMAP.md` (2026-11-08): the two clean (10, 4) sources, a Boolean control (two identical
copies return Szilassi), 128 frozen samples per source, exact union boundary from the cells of the plane arrangement,
at most 1 session and 1 core-h. Stage 2 (12-face filter on the 59 types, minutes of CPU) and the rigid (9, 3)
cross-check (finite list) are separate later items.

## Source

Review `reviews/strategy-review-2026-11-08e.md` Follow-up Q5 (Szilassi + Szilassi at (10, 4)); the lead's extension
to other pieces and to the 12-face target after the owner's question "why only Szilassi?" (2026-11-08).

## Stage 1 result (2026-11-09)

E-261109-04: 0 of 128 Szilassi + Szilassi (k = 4) and 0 of 128 Szilassi + tetrahedron (k = 1) samples give 10 simple faces with genus 4; both sources parked at this resolution (STATUS 3ab).
