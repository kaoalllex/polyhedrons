# E-261118-01: conclusion

**COMPLETE-UNSAT-SOLVER@0.004 core-h (classes 1-5), all 20 formulas decided**: no face-transitive (8, 3) class other than Roest-Vigh's has a
SAT plain or normalised formula (UNSAT-SOLVER, formula scope); Roest-Vigh's class SAT and realized in every formula.

* **Runs**: pre-registration `0667a897`; session pilot (controls into `results/pilot-controls/`, shard 0 into
  `results/0/`) at `0667a897`; owner launch `launch.sh 261118-01 start` at `a2781796`, 2026-11-18 19:42:38-43 UTC,
  10 shards, every `exit_status: 0` (shard 0 had no unit left). `dirty_files` 1 and 11 are the untracked result
  files themselves; sources unchanged between the two commits. Cost from the records: 9.8 solver-s + 2.6 bridge-s
  (controls 6.7 s wall); about 0.004 core-h against the expected 0.2. Kissat 4.0.4 (SHA-256 in every manifest).
* **Controls** (all passed): Roest-Vigh's planes pinned on his own map SAT (plain), his gauge representative pinned
  SAT (normalised); his planes pinned on classes 1-5 UNSAT-SOLVER. In-run positive: class 0 SAT in all four
  formulas (map and mirror, plain and normalised), 0.1 s each.
* **Results** (`results/<shard>/results.jsonl`): classes 1, 2, 3 (map and mirror) and 4, 5 (map; reflexible): all 16
  formulas UNSAT-SOLVER in 0.1-2.9 s; no TIMEOUT, no ERROR.
* **Prediction vs outcome**: P1 (controls, class 0 SAT) held; P2 (all decided) held; P3 (classes 1-5 all
  UNSAT-SOLVER) held; P4 (class 0's single model realized, 0.4) held for all four models.
* **Exact verification**: the four class 0 models were realized by the bridge's first stage (`hinge`, 0 wrong signs)
  and `verify_candidate.py --all-pairs` gives PASS on each saved `class0_*.candidate.json` ((V, E, F, chi) =
  (24, 36, 8, -4)). These are realizations of Roest-Vigh's known class, the registered positive control and bridge
  calibration; no claim beyond that is made, so `candidate-check` does not apply. No proofs (UNSAT-SOLVER only).
* **What may be claimed**: for each of the five face-transitive (8, 3) classes other than Roest-Vigh's, in both
  orientations of the chiral ones, the S1 formula at 9 elements (`ALL_OPTS`, plain and with the `symbreak` + `mirror`
  units) is UNSAT-SOLVER (kissat 4.0.4; instance scope, SPEC §4; ranking only). Roest-Vigh's class: SAT, realized,
  `--all-pairs` PASS (EXACT; known object).
* **What may NOT be claimed**: that classes 1-5 are not realizable (no checked proof; the encoder's completeness for
  multi-adjacent maps is PROVED-1); anything about non-face-transitive (8, 3) maps, other genera, or nine faces.
* **Hypotheses**: H-261101-07 unchanged (no new eight-face object; Roest-Vigh's class stays the only face-transitive
  one with a model).
* **Verdict for the direction**: the face-transitive (8, 3) slice is closed for planning: Roest-Vigh's class is the
  only one with a SAT formula. COMPLETE-UNSAT-SOLVER@0.004 core-h. Side result: the bridge realizes his class from a random
  model in under 1 s, so it is a cheap rung control for E-261118-02.
* **Next step**: week item 3, P3-sym (E-261118-02). No follow-up row.
* **Rows updated**: `STATUS.md` 3ba and header, `ROADMAP.md` State done, `experiment-log.md` (2026-11-18), README,
  H-261101-07 note, `paper/OUTLINE.md` B7.
