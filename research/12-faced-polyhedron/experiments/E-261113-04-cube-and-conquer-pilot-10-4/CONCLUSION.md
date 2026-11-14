# E-261113-04: conclusion

2026-11-13. One owner laptop launch (`launch.sh 13-04 start`), 10 shards, commit `62521be5` (pre-registration `ba9a0886`,
pilot amendment `da276d95`), one attempt per shard, no restart.

* **Runs**: 10 shards, all `exit_status: 0`, wall 370-410 s each. Core-hours from the ten `manifest.txt`: **1.083 core-h**
  (cap 3), plus 0.006 for the pilot. `dirty_files: 13` in every manifest: the three untracked owner notes at the repo
  root and the ten shard folders of this run, no tracked file. Solver `~/bin/kissat` in every record (SHA-256
  `4bc06993...`, as in E-261108-03), `NO_PROOF=1`.
* **Controls**: `CONTROLS-PASS` in all 10 shards (c1 the plain CNFs of 96, 85, 845 equal the recorded hashes; c2 nine
  distinct unfixed order literals and the 512-cube cover on both arms; c3 the pinned Roest-Vigh chirotope gives exactly
  one SAT cube of eight, the one read off its model, and that cube is SAT unpinned). Calibration: map 845 monolithic
  UNSAT-SOLVER in 173.7 s against 188.38 s recorded, ratio **0.922**, inside [0.75, 1.33]: calibrated.
* **Results** (`summary.py results`; r = summed cube solver seconds / recorded monolithic seconds):

  | map | monolithic s | cubes run | UNSAT-SOLVER | TIMEOUT | SKIPPED-ARM-CAP | summed s | r | median cube s | cubes < 1 s |
  |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
  | 96 `(1^4,2)` | 1073.5 | 125 | 123 | 2 (cubes 73, 78, at 107 s) | 387 | 1146.8 | **>= 1.068** | 0.1 | 64 |
  | 85 `1^6` | 2748.9 | 39 | 39 | 0 | 473 | 2534.8 | **>= 0.922** | 65.5 | 0 |

  0 SAT cubes. Both arms hit the arm cap (first skip at 755 s and 1954 s of recorded cube time), so both r are lower
  bounds. Reading: **PARK** (r >= 0.7 on both arms; calibrated).
* **Not registered, for planning only**: the cubes run are the lowest indices (96: 0-206, 85: 0-45), not a random
  sample. On 85 every cube cost 2-4 % of the monolithic time (39 cubes, 49-109 s), so 512 cubes would cost about 12x;
  on 96 half the cubes are refuted at once (the order bits clash with other clauses) and the rest carry the cost (mean
  9.2 s, about 4.4x for 512). Fixing the segment order of the doubled pairs barely simplifies the hard part of the
  formula on these maps.
* **Prediction vs outcome**: P1 (r <= 0.5 on 85, ~50 %): **failed**. P2 (CUBES-WIN, ~35 %): **failed**. P3 (PARK, ~25 %):
  **holds**. P4 (a cube under 1 s on each arm, ~70 %): **failed** on 85 (none of 39), holds on 96. H0 (>= 0.7x on both)
  holds; H1 rejected.
* **Exact verification**: no SAT, no candidate, no `candidate-check`. Every UNSAT is UNSAT-SOLVER and none is used as
  evidence for anything but cost.
* **What may be claimed** (NUMERICAL, instance scope): on the plain uniform S5 formulas of (10, 4) maps 96 and 85, the
  512 segment-order cubes (three order literals per doubled pair) cost kissat rel-4.0.4 at least 1.07x and 0.92x the
  monolithic solver time on this laptop at 10 shards, before covering 125 and 39 of the 512 cubes.
* **What may NOT be claimed**: anything about march_cu cubes, other cube variables, other solvers, other maps or other
  map families ((10, 3) included); that cube-and-conquer cannot pay (only these cubes at this budget); anything about
  the existence of a (10, 4) object (no map was decided here).
* **Hypotheses**: H-261101-06 (per-type decision cost): no status change; evidence line added (simple cubes on the
  doubled-pair order do not lower the cost on two (10, 4) maps).
* **Verdict for the direction**: DR8 cube-and-conquer with segment-order cubes: **PARKED@1.08 core-h** (two maps,
  r >= 0.92 and >= 1.07). Not a refutation of cube-and-conquer.
* **Next step**: by the registered tree, cube-and-conquer is parked at this budget; under the rule of E-261110-06 the
  (10, 4) strata A + B become one explore night at most (<= 80 core-h, fastest stratum A maps first), only when a lead
  review schedules it; no further (10, 4) night without a new lead decision. The eight asymmetric (10, 3) maps get no
  cube proposal from this pilot. For the lead: march_cu (the first choice of the row) was built by the owner after the
  run (`~/bin/march_cu`, CnC commit `705b60c6`, SHA-256 `f3554726...`); a march_cu cube pilot on the same two maps would
  be a changed set-up (D > 0), not a rerun, and needs a lead decision and its own PLAN.
* **Rows updated**: `STATUS.md` 3aj and "As of", DR8 row; `ROADMAP.md` week item 4, E-261113-04 and E-261110-06 rows;
  `experiment-log.md` (2026-11-13); `hypotheses/H-261101-06`; README.
