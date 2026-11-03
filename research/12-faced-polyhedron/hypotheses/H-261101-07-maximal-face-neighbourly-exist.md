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
object in print (CLAIMED). Candidate maps sampled 2026-11-03 (`STATUS.md` 3c; H-261103-01): 2 at (8, 2), 240 at (9, 3)
of which 203 admissible and 8 with a free C3, >= 113 at (10, 4); so the maps exist and the question is geometric.

## What would move it

E-261103-03 (exact decision per map): a realized model at (8, 2) or (9, 3) proves the case; all maps of a case
UNSAT-VERIFIED refutes it for that case. E-261103-04, -05, -06 (searches): an S5 PASS proves the case; a failed run moves
nothing.
