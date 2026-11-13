---
id: H-261110-01
title: The multiple-adjacency constraints are what refutes the (8, 2), (9, 3) and (10, 4) formulas
date: 2026-11-10
status: weakened
origin: [E-261103-03, E-261109-06, I-261108-01, I-261110-04, I-261110-02]
---

## Statement

The plain S5 formulas at (8, 2), (9, 3) and (10, 4) are UNSAT because of the constraints that only multiple
adjacencies bring (`SEGMENT_DISJOINT` and the collinear-segment geometry of a pair with two or more boundary runs),
not because of a global obstruction at these genera. Consequence if true: the negative ladder of S5 says little about
S0, which has no multiple adjacency.

## Rival

The obstruction is global (genus / covering): formulas without multiple adjacencies at comparable size are refuted
as well, and the S5 negatives are evidence about S0.

## Evidence so far

* E-261110-05 (2026-11-13, STATUS 3ai; UNSAT-SOLVER, planning evidence): without SEGMENT_DISJOINT (V2) all eight
  (8, 2) / (9, 3) formulas stay UNSAT; the immersion-only formula (V1) is SAT on five (9, 3) maps and UNSAT on both
  (8, 2) maps -> weakened in its stated form: at (9, 3) the global triples carry the refutation, at (8, 2) a local one.
* (9, 3) solve times split by multiplicity pattern (NUMERICAL, STATUS 3d): concentrated patterns `(1,2,3)`,
  `(2,2,2)` in 22-76 s, spread-out `1^6` in 523-914 s. Suggestive only: a time is not a cause.
* E-261108-02 found no UNSAT sub-formula on <= 6 faces of the 24 11-gon maps (its grouping, cap 20 s): the
  refutation is not small in faces.
* E-261110-02 (2026-11-13): the 20 (10, 3) formulas all TIMEOUT at 3600 s, so the comparison with (10, 4) has no
  data point; no move (STATUS 3af).
* Nothing else beyond these. The statement is the judgment of one AI session (2026-11-10).

## What would move it

* E-261110-05: plain without `SEGMENT_DISJOINT` (V2) SAT on maps whose plain formula is UNSAT -> supported; V2 UNSAT
  on all eight maps -> weakened in this form. Immersion-only (V1) UNSAT -> the obstruction is local; V1 SAT and V2
  UNSAT -> the global triples carry it without the segment clauses, weakened.
* E-261110-02: SAT models at (10, 3) (no multiple adjacency, same element count as (10, 4)) while (10, 4) stays
  without one -> supported; 20 UNSAT at (10, 3) -> weakened (the rival predicts it).
