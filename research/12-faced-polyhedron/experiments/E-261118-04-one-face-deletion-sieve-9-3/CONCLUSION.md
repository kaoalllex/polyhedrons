# E-261118-04: conclusion

Concluded on the pilot by the owner's decision (2026-11-18): the pilot gate failed on price, and the pilot already
answers H1. No long run.

* **Runs**: session pilot on commit 500eb8e8 (pre-registration), kissat 4.0.4, NO_PROOF, cap 300 s; no `manifest.txt`
  (direct `sieve.py` calls, not `run.sh`). Recorded solver seconds: controls 79.0 (`results/pilot-controls/controls.json`),
  map 0 2700.3 (`results/pilot/*/results.jsonl`), map 29 771.1 (session transcript; per-face times in PLAN.md
  amendment, models and solver logs in `results/pilot29/`); bridge 4 stages of at most 120 s each, times not recorded.
  About 1.0 core-h solver time + at most 0.13 core-h bridge.
* **Formula**: the S5 (9, 3) map formula (ALL_OPTS) with the own conditions of one face S dropped and plane S kept
  (owner's option (a), PLAN.md). A model is a planar but possibly defective face S on eight faces that satisfy all their
  conditions, not the curved face of I-261118-04.
* **Controls**: passed. Positive: Roest-Vigh's planes pinned, all 8 deleted formulas SAT. Negative: the shifted
  planes, all 8 UNSAT-SOLVER; full formulas of maps 29, 66, 20 UNSAT-SOLVER (28 / 31 / 20 s). Eval violation counter
  calibrated on both sides (`test_sieve.py`). Monotonicity by construction (prefix test).
* **Outcome**: map 0, all 9 faces TIMEOUT. Map 29: faces 5 and 8 SAT (2.9 s, 0.4 s), the other 7 UNSAT-SOLVER
  (53-174 s). The bridge did not realize either SAT model: two-stage then hinge, 6 restarts, best 1 wrong sign (face 8)
  and 4 (face 5) (`results/pilot29/map29_del{8,5}.bridge.json`). No final-polynomial test was run.
* **Prediction vs outcome**: P1 (controls pass) held; P2 (deleted formulas slower than the full ones) held: map 0 at
  2700 s, map 29 at 771 s against 28 s for its full formula; P3 (a SAT) held on the second map tried. The projection
  for 1827 units was 40-150 core-h against the budget of <= 1 core-h, so the gate failed.
* **Exact verification**: SAT models checked against their clauses by `pilot.solve`. No candidate: the models are
  relaxation objects (S defective by design), unrealized, and never S5 candidates, so `candidate-check` does not apply.
* **What may be claimed**: EXACT at formula scope: the deleted formulas of map 29 with S = 5 and S = 8 are SAT,
  i.e. at OM level the refutation of map 29's full formula needs the own conditions of face 5 and of face 8.
  UNSAT-SOLVER (ranking only): the other seven faces of map 29.
* **What may NOT be claimed**: anything about curved-face quasi-polyhedra (not encoded); that the SAT models are
  realizable or non-realizable (the bridge failed, no final polynomial); anything about the other 202 maps
  (map 0 timed out, the rest were not run); any negative result (no proofs).
* **Hypotheses**: H-261101-07 unchanged (a relaxation result on one map; it neither excludes nor produces a
  (9, 3) object). I-261118-04 stays open: its curved-face reading is untested.
* **Verdict**: OPEN-LOW@1.1 core-h, 2 maps of 203 (map 0 undecided): the obstruction of map 29 depends on single
  faces; a full sieve costs 40-150 core-h.
* **Next step**: none in the queue. For the lead: a curved-face encoder (free vertices on the lines L_XY, a
  non-uniform chirotope, a soundness note) if the lead wants the owner's idea tested as stated; whether the two
  unrealized map-29 models deserve a final-polynomial test. Week item 2 (N1b, E-261118-01) next.
* **Rows updated**: `STATUS.md` 3az, `ROADMAP.md` State done, `experiment-log.md` (2026-11-18), H-261101-07 note,
  README.
