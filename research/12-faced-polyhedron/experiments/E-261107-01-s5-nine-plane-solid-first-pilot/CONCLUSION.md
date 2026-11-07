# E-261107-01: conclusion

2026-11-07. Explore pilot at S5 (9, 3). Scope (`SPEC.md` §4): 30 uniform 9-plane arrangements, exact CP model
(36 pairs, E = 39, <= 3 runs per pair). Not an S5 witness, not a 12-face result.

* **Runs**: commit 9fbea2a (clean tree), one shard, 10 workers, wall 166 s. Core-hours 0.38 (sum of the 34 unit
  wall times; 0.46 is the workers x wall upper bound in `manifest.json`), against the 2 core-h budget. No manifest
  missing. Models are kept gzipped in `results/0` (hashes in each `*.result.json`); the draws are deterministic
  (`nine.py planes`).
* **Controls**: all four as stated: tetrahedron E = 7 and nine-plane E = 33 INFEASIBLE; Roest-Vigh and Mizhaev SOLID
  with the known map and 28 pairs in Phase B. The pair count is calibrated only at its saturation point 28.
* **Prediction vs outcome**: (1) controls pass - yes. (2) most INFEASIBLE units finish inside the cap (~50 %) - yes,
  stronger than predicted: all 30 completed, 5.9-21.0 s (mean 13.5 s) against the 180 s cap, no timeout or
  UNKNOWN. (3) no SOLID in 30 units (~85 %) - yes.
* **Exact verification**: no candidate, so no `candidate-check` and no `verify_candidate.py` run. No shared code
  changed; no `verify_all` run.
* **What may be claimed**: EXACT computation (re-solved CP models, no DRAT): for each of the 30 exact integer
  arrangements the hard model is INFEASIBLE, so no 36-pair disk-face solid exists on those 30 arrangements. The
  geometric reading rests on the PROVED-1 encoding argument of E-261103-05. Phase B pair counts (raw solver
  values, max 32, distribution 27: 10, 28: 3, 29: 15, 30: 1, 32: 1) are diagnostic only; none reaches 33.
* **What may NOT be claimed**: any exclusion of a symmetry family, of C3 or D2 solids, or of S5 at (9, 3); a
  success rate (30 purposive seeds, fixed-face C2/D3 and S4/C4 families not run). The solid need not share the
  arrangement's symmetry, so `c3` and `d2p1` say nothing about C3/D2 solids as a class.
* **Verdict for the direction**: LOW-YIELD@0.38 core-h, 30 arrangements (this configuration). H-261103-02 and
  H-261101-07 unchanged; no credence moves.
* **Observation (to the lead)**: the engine is cheap at nine planes (about 13 s per exact decision), unlike what the
  8-plane scale suggested. Coverage is then limited by the number of arrangements, not by the solve time; a broader
  sample or a smarter arrangement source (not a longer cap) is the open design question.
* **Next step**: no follow-up branch fires (no embedded output, no >= 33-pair solid, controls pass). Park this
  configuration; week plan item 2 (E-261103-06 R1 pilot).
* **Rows updated**: `STATUS.md` 3t, `ROADMAP.md` E-261107-01 `done`, `experiment-log.md` 2026-11-07, README `done`.
