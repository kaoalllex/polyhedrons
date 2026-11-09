# E-261109-05: conclusion (2026-11-09)

**Verdict: PARK I-261108-06 (kill rule met, LOW-YIELD@0.052 core-h).** 0 of the 203 admissible (9, 3) plain formulas is
UNSAT on the rank-3 contraction at any one face (needed: >= 27 for a pass, < 20 parks). Scope: one-face contraction
sub-formulas (`PLAN.md` method), cap 20 s, these 203 maps; 2030 map sub-formulas, all SAT, 0 TIMEOUT, slowest 0.11 s.

* **Runs**: commit `ea9e70c` (pre-registration `42dcff8`), 10 shards, 18-20 s wall each, 0.052 core-h (sum of the 10
  manifests), laptop.
* **Controls**: C0 full formula SAT and every con(X) SAT (pass); C1 UNSAT-VERIFIED exactly at 4, 5, 6 and INF (pass);
  C2 fires at face 1 only (descriptive: the measure moves on a non-planted contradiction). The null on the maps is
  therefore not a constant artefact of the measurer.
* **Prediction vs outcome**: P1 (< 20 killed) held, 0; P2 (con(INF) SAT on all 203) held; P3 (no TIMEOUT) held.
* **Exact verification**: no map UNSAT was used as evidence. The five control UNSATs are UNSAT-VERIFIED (drat-trim,
  CNF and proof SHA-256 plus checker log in the unit folders). Formula hashes: 198 of 203 equal a recorded
  E-261103-03 `formula_sha256`; maps 5, 6, 30, 40, 48 have no local `result.json` record (40, 48 are in the grid
  summary, see E-261108-02); no mismatch (a mismatch stops the run).
* **What may be claimed** (EXACT per sub-formula, instance scope): for each of the 203 maps and each face X, the clauses
  of the plain formula whose chirotope signs all contain X are satisfiable. In this encoding, no (9, 3) map is excluded
  by the conditions of one face's polygon alone. Obstructions come only from clauses that couple three faces (TRIPLE,
  REFLEX1), which no contraction contains (structure count, `PLAN.md`).
* **What may NOT be claimed**: anything about (10, 4) maps, about unions of two or more contractions, or about other
  groupings; that one-face polygon conditions are realizable (a SAT sub-formula is an OM-level statement only).
* **Hypotheses**: H-261101-07 not moved (the answers were known). H-261101-11 (S0, few-face core): no support from
  this grouping at (9, 3); together with E-261108-02 (no core on <= 7 face-indexed faces), the (9, 3) UNSATs look global.
* **Next step**: none for the sieve. The (10, 4) sweep stays unsieved; queue order is N2's question (lead review
  2026-11-09). A union-of-two-contractions sieve would still miss TRIPLE, so it is not proposed.
* **Data**: `results/` keeps the 206 `result.json`, the manifests and the five control UNSAT logs. The 2055 SAT models of
  sub-formulas (not candidate models) and their solver logs were deleted after aggregation, as in E-261108-02.
* **Rows updated**: `STATUS.md` 3ac, `ROADMAP.md` State done, `experiment-log.md` (2026-11-09), I-261108-06 parked.
