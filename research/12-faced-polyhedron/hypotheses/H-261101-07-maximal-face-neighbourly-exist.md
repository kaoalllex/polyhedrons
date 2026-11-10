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

## 2026-11-04 ladder representation gate

E-261103-04 CONCLUSION / STATUS 3j diagnose a PROVED-1 limitation of the legacy
triangle-to-links conversion on parallel-edge maps. Geometric recovery has not
been attempted by this stage. The hypothesis retains its preceding status.

## 2026-11-04 conditional ladder calibration

E-261103-04's conditional failed-level grid concluded UNDERPOWERED (CONCLUSION /
STATUS 3n). PROVED-1 supplied-input checks reject all saved cell outputs. The
scope covers auxiliary intermediate maps from frozen parents. This hypothesis
retains its preceding status and credence.

## 2026-11-08 item 5a

E-261103-03 item 5a: all 203 admissible (9,3) plain formulas UNSAT-VERIFIED (EXACT, formula scope); the geometric
reading excludes genus 3 at 9 faces, conditional PROVED-1 (census coverage, encoder soundness, one encoder, no human
review; STATUS 3d). Genus 2 and 3 are excluded at that level; genus 4-5 are untested, so the status stays open.

## 2026-11-10 (10,4) stratum C

E-261109-06: kissat reports UNSAT on the plain formula of all 360 admissible (10,4) maps outside `(1^4,2)` and `1^6`
(UNSAT-SOLVER, no checked proof, so not a negative result; STATUS 3ad). No SAT, no candidate; strata A (520) and B (237)
untested. Status stays open.
