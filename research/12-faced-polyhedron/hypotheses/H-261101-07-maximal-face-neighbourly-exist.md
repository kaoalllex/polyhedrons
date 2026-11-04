---
id: H-261101-07
title: Maximal face-neighbourly cubic polyhedra with few doubled pairs exist for genus 2-5
date: 2026-11-01
status: open
origin: [L:mizhaev2026, L:roestvigh2026]
---

## Statement

Maximal face-neighbourly cubic polyhedra with few doubled pairs exist for genus 2-5.

## Rival

They stop below genus 6.

## Evidence so far

8-face genus-3 objects exist (Mizhaev, Roest-Vigh). (8,2) was tried only by black-box engines at session budgets
(E-261029-19: plateau at 1-2 violations, no symmetric ansatz, no attempts saved), so it is underpowered, not
untested; (9,3), (10,4), (11,5) are untested geometrically. For 12 faces the smallest S1 relaxation has 3 doubled pairs and genus 7
(d = 6g - 36). Literature check of 2026-11-03 (`literature/review-2026-11-03.md`): no (8, 2), (9, 3), (10, 4) or (11, 5)
object in print (CLAIMED). E-261103-01 has since exhausted the maximal-case map families, with controls
(EXACT computation, coverage PROVED-1; `STATUS.md` section 3c). This supplies geometric inputs
but does not move the existence hypothesis; its status remains open.

## What would move it

E-261103-03 (exact decision per map): a realized model at (8, 2) or (9, 3) proves the case; all maps of a case
UNSAT-VERIFIED refutes it for that case. E-261103-04, -05, -06 (searches): an S5 PASS proves the case; a failed run moves
nothing.

## 2026-11-04 update

E-261103-03 decides both plain (8,2) formulas UNSAT-VERIFIED (EXACT); the geometric
interpretation is conditional PROVED-1, see its CONCLUSION and STATUS section 3d.
The genus-2 case is excluded at that level; genus 3-5 remain open, so the umbrella status stays open.

## 2026-11-04 explore calibration

E-261103-05 passes its disk-aware solid-first R2/R3 controls (CONCLUSION / STATUS 3g).
The exact auxiliary recovery is at (8,3), not maximal S5 (9,3), and supplies no focus existence
conclusion. This is engine-power evidence; the hypothesis remains open.

## 2026-11-04 new-map tranche

E-261103-03 completed its registered bounded coverage tranche (STATUS 3i / CONCLUSION).
EXACT decisions concern saved formulas only; geometric interpretation remains conditional
PROVED-1. No target SAT or geometric candidate. This hypothesis retains its preceding status;
partial coverage and timeouts do not decide existence.
