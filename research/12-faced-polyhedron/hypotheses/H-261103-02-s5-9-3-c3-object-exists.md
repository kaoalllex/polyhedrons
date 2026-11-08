---
id: H-261103-02
title: A (9, 3) polyhedron exists with a 3-fold rotational symmetry, on one of the 8 admissible maps with a free C3
date: 2026-11-03
status: weakened
origin: [owner, H-261101-07, I-261030-07, L:roestvigh2026, L:mizhaev2026]
---

## Statement

Some maximal face-neighbourly polyhedron with 9 faces and genus 3 is invariant under a rotation of order 3 (axis through
its two fixed vertices, the three doubled pairs one orbit or a triangle), realized on one of the 8 admissible (9, 3) maps
whose automorphism group contains a free order-3 element (`reviews/strategy-review-2026-11-03.md` section 2.1).

## Rival

No (9, 3) polyhedron has the specified free-face C3 symmetry. Other symmetry groups and asymmetric realizations remain possible; absence of every (9, 3) object is a stronger rival.

## Evidence so far

None geometric. Prior: both known face-neighbourly polyhedra beyond Szilassi are symmetric (D2 and C4), Szilassi has a C2,
and Bokowski-H. 2025 report that every embedding they found has a geometric symmetry (CLAIMED, regular maps). Against: a
free C3 on 9 faces leaves about 7 parameters, a small space.

## What would move it

E-261103-03 (b): a realized model with C3 clauses proves it; 8 UNSAT-VERIFIED instances with C3 clauses, plus sound equivariant coverage and normalization arguments, exclude the C3
form conditionally (the asymmetric form stays open until (d)). E-261103-05: a C3 solid with 36 pairs proves it.

## 2026-11-04 paired-pilot evidence

E-261103-03 CONCLUSION reports checked UNSATs for every tested uniform free-C3 formula
(EXACT instances). This weakens the uniform ansatz; the hypothesis stays open pending a
sound equivariant general-position/coorientation and family-coverage argument (PROVED-1 at best
until reviewed). C3-invariant signs alone would also not certify a geometric rotation.
No asymmetric non-existence claim follows; possible realizations with other symmetry groups remain open.

The experiment CONCLUSION now contains a conditional free-C3 coverage draft (PROVED-1), with
explicit coorientation, equivariant genericity, orbit/mirror gauge and subgroup arguments.
Independent exact determinant controls check its arrangement and reflection identities. This
single-author draft is an external-review input; the hypothesis status is not promoted on its basis.

## 2026-11-04 explore calibration

E-261103-05 passes its disk-aware solid-first R2/R3 controls (CONCLUSION / STATUS 3g).
The exact auxiliary recovery is at (8,3), not maximal S5 (9,3), and supplies no focus existence
or C3 conclusion. This is engine-power evidence; the hypothesis remains open.

## 2026-11-04 new-map tranche

E-261103-03 completed its registered bounded coverage tranche (STATUS 3i / CONCLUSION).
EXACT decisions concern saved formulas only; geometric interpretation remains conditional
PROVED-1. No target SAT or geometric candidate. This hypothesis retains its preceding status;
partial coverage and timeouts do not decide existence.

## 2026-11-04 ladder representation gate

E-261103-04 CONCLUSION / STATUS 3j diagnose a PROVED-1 limitation of the legacy
triangle-to-links conversion on parallel-edge maps. Geometric recovery has not
been attempted by this stage. The hypothesis retains its preceding status.

## 2026-11-04 conditional ladder calibration

E-261103-04's conditional failed-level grid concluded UNDERPOWERED (CONCLUSION /
STATUS 3n). PROVED-1 supplied-input checks reject all saved cell outputs. The
scope covers auxiliary intermediate maps from frozen parents. This hypothesis
retains its preceding status and credence.

## 2026-11-08 lead review

Status weakened (conditional): all 8 uniform free-C3 formulas are UNSAT-VERIFIED (EXACT instances); the geometric
family exclusion rests on the PROVED-1 coverage draft in E-261103-03 CONCLUSION, not reviewed. No further C3-only work
is queued (`reviews/strategy-review-2026-11-08.md` §5.1, M2).
