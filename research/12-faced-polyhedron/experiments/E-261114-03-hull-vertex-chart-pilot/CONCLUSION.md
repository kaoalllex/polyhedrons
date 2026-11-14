# E-261114-03: hull-vertex chart pilot (2026-11-14)

* **Verdict: UNRESOLVED / OPEN, solver-limited.** The small-pilot gate closes the full pilot;
  no launch is prepared. H-261101-06 and A/B/C remain unchanged. Next: week item 2, E-261110-06.
* **Lemma:** SOUNDNESS.md, PROVED-1 and unreviewed; inward orientations and a nonzero old-INF
  perturbation preserve finite vertices. Coverage is geometric, not a partition of abstract OM models.
* **Controls:** all 23 saved geometric inputs pass at every hull vertex: 131 exact rational
  re-chartings, verifier PASS and pinned normalized-CNF SAT with checked models. The remaining 391
  vertices have exact convex-combination certificates. All 23 reversed-orientation controls violate
  the selector and return UNSAT-SOLVER on the pinned selector-only CNF. No new focus witness.
* **Prediction vs outcome:** five cubes each on Lutz #1 and #2, ten shards, all TIMEOUT at the
  intended 10 s cap (fractions 1.0007-1.0015); no SAT, UNSAT-SOLVER or ERROR. Predicted completion fails.
* **Comparison:** no complete vertex cover, so no speedup or kill ratio is established. Both saved
  monolithic baselines remain censored at 1200 s; their rebuilt CNF hashes match. The full 56-cube
  pilot and its timing-threshold calibration were not run. No geometric negative (SPEC section 4).
* **Runs (NUMERICAL timing):** pre-registration a46658fe; ten shards each for controls and small
  pilot, elapsed wall 34.217 / 11.818 s; recorded worker-hours 0.028640 / 0.030222, below the reserved
  0.4 / 0.1 core-h caps. Worker CPU deltas total 196.000369 s; parent preparation CPU is unrecorded.
  No positive endpoint sleep gap recorded; no heartbeat trace. The resumed pilot used AC and caffeinate.
* **Verification:** unchanged E-261114-01 gates/environment reused by hash; saved output hashes and
  PASS transcripts validated in results/validation.json. No solver or geometry replay. The unchanged
  shared-code quick check from E-261114-02 is reused; this standalone runner's controls cover its new code.
* **Execution:** the first resume command failed before workers on a temporary environment's missing
  numpy; retry in the existing research environment passed. No solver budget was spent by that failure.
* **Lead:** reopening needs an explicit decision. No proofs; correctness controls do not measure discovery power.
