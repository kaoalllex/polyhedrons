---
id: H-261103-02
title: A (9, 3) polyhedron exists with a 3-fold rotational symmetry, on one of the 8 admissible maps with a free C3
date: 2026-11-03
status: open
origin: [owner, H-261101-07, I-261030-07, L:roestvigh2026, L:mizhaev2026]
---

## Statement

Some maximal face-neighbourly polyhedron with 9 faces and genus 3 is invariant under a rotation of order 3 (axis through
its two fixed vertices, the three doubled pairs one orbit or a triangle), realized on one of the 8 admissible (9, 3) maps
whose automorphism group contains a free order-3 element (`reviews/strategy-review-2026-11-03.md` section 2.1).

## Rival

Every (9, 3) polyhedron, if any, is asymmetric (as FD5 forces for S0), or none exists.

## Evidence so far

None geometric. Prior: both known face-neighbourly polyhedra beyond Szilassi are symmetric (D2 and C4), Szilassi has a C2,
and Bokowski-H. 2025 report that every embedding they found has a geometric symmetry (CLAIMED, regular maps). Against: a
free C3 on 9 faces leaves about 7 parameters, a small space.

## What would move it

E-261103-03 (b): a realized model with C3 clauses proves it; 8 UNSAT-VERIFIED instances with C3 clauses refute the C3
form (the asymmetric form stays open until (d)). E-261103-05: a C3 solid with 36 pairs proves it.

## 2026-11-04 paired-pilot evidence

E-261103-03 CONCLUSION reports checked UNSATs for every tested uniform free-C3 formula
(EXACT instances). This weakens the uniform ansatz; the hypothesis stays open pending a
sound equivariant general-position/coorientation and family-coverage argument (PROVED-1 at best
until reviewed). C3-invariant signs alone would also not certify a geometric rotation.
No asymmetric non-existence claim follows; possible realizations with other symmetry groups remain open.
