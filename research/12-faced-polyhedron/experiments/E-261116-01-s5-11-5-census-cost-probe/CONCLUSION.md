# E-261116-01: preparation; owner price run pending

## Preparation (2026-11-16)

* **Verdict: READY**, not a completed price probe. No new focus witness or geometric negative;
  H-261101-07 and S0 A/B/C unchanged. SPEC §4 instance scope, NUMERICAL startup/control timings;
  census coverage and encoder soundness retain their existing PROVED-1 status.
* **Census:** complete/exhausted, 4099 classes, 3986 admissible; patterns [1,1,1,1]/[1,1,2]/[2,2]
  have 2474/1478/34 maps; 24 symmetric. Euler/admissibility, distributions and canonical-code
  digest match the lead check (`results/census-check.json`, compressed full output in `results/census/`).
* **Controls:** inherited E-261114-01 gates reused after Python/dependency/solver/source checks;
  new convex f11 pinned/unpinned SAT, wrong-map pinned UNSAT-SOLVER; assignments checked.
  `results/controls/summary.json` preserves original provenance; census-only source correction
  leaves control functions unchanged (`results/validation.json`). No proofs produced or replayed.
* **Runs:** census 116.93 s (0.03248 worker-h) against a 540 s enumeration cap; size controls
  total 1.209 worker-s (CPU unrecorded). Two startup launches total 29.270 worker-s, 20.788 CPU-s;
  endpoint clock-gap values are in shard manifests, not a continuous sleep audit.
* **Startup:** actual `launch.sh 16-01 start/status/stop/start`, ten shards, 0.01 s cap;
  ten TIMEOUT records survive restart unchanged (`results/startup.json`). Not discovery-power data.
* **Checks:** final runner tests 3 PASS, pricing tests 6 PASS; shell/compile checks PASS;
  integrated `verify_all.py --quick` ALL PASS, archive skipped (`results/quick.log`).
  Initial digest comparison failed on serialization; saved output rechecked without re-enumeration.
  An initially wrong pricing-test expectation was corrected; final boundary tests pass.
* **Next:** owner on AC: `bash research/12-faced-polyhedron/overnight/launch.sh 16-01 start`;
  after completion run `summary.py`, then conclude the production stage by PLAN. No day solve yet.
