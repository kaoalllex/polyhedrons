# E-261116-09: conclusion

## Part A: lemmas (2026-11-22)

* **Runs**: no solver; `checks.py` (exact, < 1 s) -> `results/checks.json` PASS, on `1d93b962` + the session's edits.
* **Controls**: witness minima reproduce the Codex review (C3 3+3+3: 8; C2 4 x 2 + 1 moved: 44); free C2 at eight: 20, no
  zero. L6 local check: the six convex 4-faced cones are valid and keep the bounded cell out; opposite cones, the eight
  3-faced cones and a flipped far cell are rejected (both signs of the checker exercised).
* **What may be claimed** (`LEMMAS.md`, single AI author, unreviewed; all **PROVED-1**, theorem scope as stated there):
  L1 a cubic object perturbs to a uniform one with the same map; L2 the same equivariantly for C3 3+3+3 (standard
  chart), C2 4 x 2 + 1 (moved chart) at nine faces and free C2 at eight (witnesses EXACT); L3 a symmetric nine-face S1
  cubic object whose group is not Cs carries a C3 3+3+3 or C2 4 x 2 + 1 action; L4 an eight-face one carries a free
  half-turn unless its group is C1, Cs, C7 or C7v; L5 on the 3986 admissible (11, 5) maps every improper symmetry is a
  mirror (forced zero); L6 objects with vertices of degree <= 4 perturb to cubic ones with the same faces, genus and
  adjacencies plus one new edge per 4-valent vertex (local check EXACT: 288 vertex types x 2 signs, all with a valid
  patch).
* **What may NOT be claimed**: anything for vertices of degree 5 or 6 (k = 5, 6 not run); that the (8, 2) / (9, 3) note
  may drop "cubic" (it may say "vertices of degree <= 4"); any reviewed or CERTIFIED status; the encoder's and gauges'
  soundness (assumed, `SOUNDNESS.md`, PROVED-1, not re-proved); Cs, C7, C7v or asymmetric objects (plain formulas only).
* **Verdict**: FOUNDATION (scope lemmas, PROVED-1) for L1-L5; L6 partial (k = 4).

## Part B: family ablation of the E-261119-02 stage-B formulas (owner addition, amendment 1)

* **Runs**: pilots (session, discarded, ~0.5 core-h) and the run `results/ablation/` on `ac0e0c72`: 10 workers, 588 s wall
  of 720, 5012 solver-s (1.4 core-h; total part B ~1.9 of 2 core-h), kissat 4.0.4, 105 records (33 + 36 priced, 4 rung
  (8, 3), 32 rung (9, 3)) + 27 stratum representatives; nothing skipped. `parity.py` (no solver, 11 s) ->
  `results/parity.json`.
* **Controls**: every record's formula hash equals stage B's; 105 of 105 records: 5 pinned symmetric draws SAT, 5
  wrong-action draws UNSAT; the three SAT (8, 3) rung units SAT with all families, models satisfy every clause. The GF(2)
  results agree with kissat on every comparable set (0 mismatches over 105 probes and 27 enumerations).
* **Outcome**: (1) symmetry is not needed: dropping SYM (or any single family) leaves all 69 priced formulas UNSAT; the
  plain formula (SYM and both gauges off) is UNSAT-SOLVER within 5 s on 36 of 36 (9, 5) and 23 of 33 (9, 4) records
  (10 UNKNOWN), against 0 of 32 on the (9, 3) rung (UNKNOWN, where SYM is what makes stage B fast). (2) No common small
  set: minimal sets of size <= 3 vary by stratum; 5 of 23 priced representatives and all 4 (9, 3) ones have none
  (sets of size 3 at cap 2 s, some UNKNOWN). (3) A linear obstruction:
  SEGMENT_DISJOINT, SYM and the gauges are linear over GF(2) in the chirotope bits; SEGMENT_DISJOINT alone is
  inconsistent on 3 of 36 (9, 5) records (certificates of 10-12 equations), SEGMENT_DISJOINT + SYM on 12 of 36 (9, 5) and
  5 of 21 C2 (9, 4) records (9-29 equations); never on C3, on the (9, 3) rung or on a SAT (8, 3) unit (the UNSAT (8, 3)
  unit is SEGMENT_DISJOINT + SYM inconsistent).
* **Lemma P (collinear-segment parity), PROVED-1, certificates EXACT** (`parity.py`): in a uniform realization each
  endpoint P_XYV of one collinear XY segment lies outside the other (sd(XYA, V) = sd(XYC, V), Cramer), so an
  inconsistent system excludes the map: no cubic embedded realization of the 3 maps at all (L1; any symmetry, chart),
  and none of the 17 (map, action) pairs with that action (L2). The formula-level UNSAT of those stage-B formulas is
  EXACT (a re-checked GF(2) certificate), not UNSAT-SOLVER. Scope: these records; nothing about the other 52.
* **Predictions**: P1 (one map family on top of the symmetry) failed (SYM is not needed); P2 (no common C3/C2 set) held;
  P3 ((9, 3) shows the same sets) failed.
* **What may NOT be claimed**: any statement on unpriced maps; the plain or ablation UNSATs beyond UNSAT-SOLVER; a
  human-reviewed exclusion; that the remaining 90 % of pass 1 is decided.
* **Verdict**: no single common obstruction; PROMISING for an exact parity prefilter (no solver) on the full lists.
* **Next step**: for the lead (`CONTINUE_PROMPT.md`): a parity pass over all (9, 4) and (9, 5) maps against the
  remaining 90 % of the symmetric pass 1, and the plain formula as the test that matters.
* **Rows updated**: `STATUS.md` 3bi, `ROADMAP.md` E-261116-09 done, `experiment-log.md` (2026-11-22), `paper/OUTLINE.md`
  B5, B8, ideas I-261116-07, I-261108-09, I-261118-02.
