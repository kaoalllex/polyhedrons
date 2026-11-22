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

2026-11-17, E-261117-01: no face-transitive cubic (9, 4) map is admissible (EXACT, coverage PROVED-1); the slice was
empty before any geometry, so the status is unchanged (open). Genus 4 maps without face transitivity are untouched.

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

## 2026-11-14 (10,4) strata A+B

E-261110-06 completes the normalized A+B queue (CONCLUSION / STATUS 3ao): UNSAT-SOLVER only,
no checked proofs, no candidate. NUMERICAL timing evidence supports the one-night cost gate;
instance solver answers do not exclude geometric realizations. Status and credence remain unchanged.

## 2026-11-16 (11,5) cost probe

E-261116-01 (CONCLUSION / STATUS 3aq) completes the registered formula sample, with no SAT or candidate.
NUMERICAL, instance scope: censored costs close the full-sweep gate; only I-261116-04 remains for this target.
No geometric exclusion or measured discovery power; hypothesis status and credence remain unchanged.

## 2026-11-17 census-free formula

E-261116-07 (CONCLUSION / STATUS 3aw): the census-free formula decided (7, 21) but produced no model and no decision at
(8, 30), (9, 39) or (8, 36) within 5.5 core-h (UNKNOWN at every cap). A budget stop: no geometric exclusion, no new
object; status and credence remain unchanged.

## 2026-11-18 one-face deletion sieve

E-261118-04 (pilot only, STATUS 3az): on map 29 the refutation needs the own conditions of faces 5 and 8 (their deleted
formulas are SAT, models unrealized). A relaxation result on one map: status and credence unchanged.

## 2026-11-18 face-transitive (8, 3) formulas

E-261118-01 (STATUS 3ba): of the six face-transitive (8, 3) classes only Roest-Vigh's has a SAT formula (the other five,
both orientations, UNSAT-SOLVER at formula scope). No new eight-face object: status and credence unchanged.

## 2026-11-19 equivariant census-free formula

E-261118-02 (STATUS 3bb): the D2 / S4 formulas return the two known eight-face objects unaided; C3 3+3+3 at nine faces
UNKNOWN at 1 h per E (UNDERPOWERED). No new object: status and credence unchanged.

## 2026-11-19 (11, 5) plane-only C2 slice

E-261118-03 (STATUS 3bc): the plane-only C2 formulas of all 20 (11, 5) Aut+ = 2 maps UNSAT-SOLVER (planning only, no
proof). No object: status and credence unchanged.

## 2026-11-20 symmetric (9, 4) per-map formulas

E-261119-02 stage B pass 1 (STATUS 3bf): the uniform symmetric formulas of every map on both (9, 4) lists (C3 3+3+3
118, C2 4 x 2 + 1 12444) UNSAT-SOLVER (planning only, no proof). No object: status and credence unchanged.

2026-11-22 (E-261116-09): scope only; the priced nine-face stage-B UNSATs do not need the symmetry, and 3 (9, 5)
maps are excluded exactly by collinear-segment parity (STATUS 3bi). Status unchanged.
