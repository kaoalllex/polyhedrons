# E-261116-07: conclusion

**NO MODEL, BUDGET STOP (UNDERPOWERED@5.5 core-h, caps 225 / 450 / 560 s per cube, one seed)**: the census-free
formula passed every stage-A control and found the K7 torus map unpinned at seven faces in 8 s, but at eight and nine
faces all 48 stage-B units ended at their caps with CP-SAT status UNKNOWN: no (8, 30) or (9, 39) cube decided, no
(8, 36) model. Cube 5 of L3 contains Roest-Vigh's and Mizhaev's chirotopes (stage-A gauge check) and was not solved
either, so the positive control never succeeded under the stage-B budget. The gate is not passed; by the PLAN's
tree the method is parked with its cause recorded.

* **Runs**: pre-registration `55f26432`, stage A and pilot `557fd08f` (amendment: no change). Stage A in the session
  (`run.sh stage_a` -> `results/controls/`, 39 s wall on eight processes, at most 0.09 core-h; the manifest records
  wall only). Pilot `results/pilot/0/` (shard 0 at 60 s per unit, 300 s, 0.08 core-h). Stage B on the laptop (AC),
  `overnight/launch.sh 16-07 start`, 10 shards, 48 units, 15:56:44-16:34:14 UTC (37.5 min wall against about
  35 planned; the longest shard ran 2244 s of units). Every shard's manifest is present (`dirty_files: 1` is the
  output directory, `ortools` 9.15.6755); each shard's wall equals the sum of its units within 6 s, so there was no
  sleep gap. Stage B 19 762 core-s = 5.49 core-h; total about 5.66 core-h within the 6 core-h cap.
* **Controls** (`results/controls/controls.json`, all PASS): L0 240 / 240 K13 verdicts matched (17 OPTIMAL and
  `EMBEDDED` (24, 36, 8, -4)); Roest-Vigh, Mizhaev and perturbed Szilassi OPTIMAL and `EMBEDDED`; raw Szilassi
  OUT-OF-DOMAIN; tetrahedron at E = 7 and Roest-Vigh with one GP-breaking sign INFEASIBLE; gauge reachability:
  Roest-Vigh and Mizhaev, reoriented and mirror-normalised, both in cube 5, OPTIMAL with chi pinned. L1 (7, 21)
  unpinned with the gauge: OPTIMAL in 8.0 s, GP-valid, `decode`d to the K7 map; its bridge (hinge, 0.8 s) realized it
  and `verify_candidate.py --all-pairs` passed (a recovery of Szilassi's type, not a new object).
* **Unit tests (deviation)**: the PLAN states that `test_p3.py` passed before the pre-registration commit. At
  `55f26432` two of its six tests failed (`test_annulus`, `test_disk_plus_annulus`) on their first assertion: the
  test helper `pinned` pins the chirotope of fixture planes that are not reoriented into the gauge, while `Formula`
  has the gauge on by default, so the pinned model is INFEASIBLE before the Euler or connectivity blocks matter. With
  the gauge off in the helper (the only change, in the test; `p3.py` unchanged, so the stage A and B evidence stands)
  all six pass, including the INFEASIBLE assertions on the annulus and on disk + annulus that were never reached
  before. `test_p3.py` is now a `verify_all` line; `verify_all.py --quick` ALL PASS at the conclusion.
* **Stage B** (`python3 p3.py summary results`; every unit's solve used 99.6-100.2 % of its cap):

| Rung | Cubes | Cap per cube | Ended by cap (UNKNOWN) | Decided | Models | Core-h |
|---|---:|---:|---:|---:|---:|---:|
| L2 (8, 30) | 16 | 225 s | 16 | 0 | 0 | 1.00 |
| L2 (9, 39) | 16 | 450 s | 16 | 0 | 0 | 2.00 |
| L3 (8, 36) | 16 | 560 s | 16 | 0 | 0 | 2.49 |

  Build time 0.4 s at eight faces, 1.0 s at nine; the per-unit cap was the binding limit everywhere, as the pilot
  gate required. The status is CP-SAT's own: the same `Formula.solve` returned OPTIMAL and INFEASIBLE on the stage-A
  controls, and an UNKNOWN that consumed the full cap is a solver budget stop, not a measuring artefact.
* **Prediction vs outcome**: P1 (L1 OPTIMAL, ~70 %) held. P2 (all (8, 30) cubes INFEASIBLE, ~50 %) failed: none
  decided. P3 (all (9, 39) cubes INFEASIBLE, ~30 %) failed: none decided. P4 (L3 >= 10 models, ~50 %) failed: 0.
  P5 (>= 1 L3 model passes `--all-pairs`, ~30 %) failed. H0 holds in its budget form: no realized L3 model within
  the cap.
* **What may be claimed** (labels `SPEC.md` §5): the stage-A regressions and controls EXACT per instance (formula
  scope: uniform, cubic, one disk face per plane); the L1 model and its realization EXACT (a known type). NUMERICAL,
  one host, one seed, these caps: the unpinned formula with the gauge decides (7, 21) in 8 s, while at eight faces no
  1/16 cube of (8, 30) or (8, 36) is decided in 225 or 560 s, including the cube that contains two known solutions.
* **What may NOT be claimed**: anything about the existence or absence of (8, 3), (9, 4) or other S1 objects; that
  (8, 30) or (9, 39) are UNSAT for this formula (no UNSAT-SOLVER was produced; STATUS 3d's (8, 2) decision is
  untouched); that the formula is wrong or the method dead (the controls passed; only the budget was exhausted);
  any scaling law or forecast of the time to a model at eight or nine faces (one cap per rung, no decision to fit).
  Not run: longer caps, other seeds, more workers, solution hints, partial pinning, the nine-face run.
* **Hypotheses**: H-261101-07 (in `tests`): unchanged, open (no model, no decision). I-261103-02: tested at its
  cheapest-test rungs; seven faces passed, the eight-face rung stopped at the budget; parked.
* **Verdict**: UNDERPOWERED@5.5 core-h (stage B; 16 cubes per rung, caps 225 / 450 / 560 s, one seed): no model and
  no decision; the gate (one unpinned eight-face model realized with `--all-pairs` PASS) is not passed. Method
  parked, not refuted.
* **Cause recorded (tree branch "no model")**: the jump from seven to eight faces. The (7, 21) formula solves in
  seconds, but CP-SAT on one worker finds no model of the (8, 36) formula within 560 s in any cube, including cube 5
  with the two known objects inside, so the search does not reach known solutions at this scale and budget. A new
  run must change the search, not repeat it (ROADMAP "Parked methods").
* **Next step**: week item 4 (P4 probe, E-261117-03), starting with `candidate-check` of the 16 S6 (10, 2) files. The
  coupled P3 + P4 test (tree branch "models but no bridge") is not triggered. For the lead: whether a P3 rerun earns
  a row, measured first on cube 5 alone (time to a model with Roest-Vigh as a solution hint or partly pinned, more
  workers, a longer cap) before any eight- or nine-face sweep.
* **Rows updated**: `STATUS.md` 3aw and header, `ROADMAP.md` (row done, week item 3, parked-methods row),
  `experiment-log.md`, README, H-261101-07 and I-261103-02 notes, `test_p3.py` fix and its `verify_all.py` line.
  `paper/OUTLINE.md`: no item added, strengthened, weakened or removed.
