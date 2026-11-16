# E-261116-01: census and cost probe

## Owner run conclusion (2026-11-16)

* **Verdict: NO-SWEEP-SYMMETRIC-SLICE@8.5331 CPU core-h.** NUMERICAL, SPEC §4 instance
  scope: sampled normalised formulas only. Existence is open; no geometric negative or witness.
* **Prediction vs outcome:** four UNSAT-SOLVER, six TIMEOUT, no SAT / ERROR; the prediction
  of fewer than five timeouts failed. All ten frozen maps recorded once in their assigned shards.
* **Runs:** commit e7d099cd, ten shards, 08:16:53–09:16:52 UTC, 3599.22 s elapsed;
  summed worker wall 8.5477 h against 10 h; CPU from all shard manifests, none missing.
  Maximum endpoint clock gap 0.074 s; no continuous sleep audit, so no claim of zero sleep gaps.
* **Price:** population-weighted, cap-substituted sample projection >=3314.54 worker-h,
  >=41.43 laptop nights; every stratum censored. This is a sample estimate, not a lower
  bound on the unsampled population or a confidence bound. Sample median >=3597.365 s,
  censored above; the uncensored <=1200 s gate for E-261116-03 is not met.
* **Element curve:** medians at 9/10/11 elements: 0.291/2.762/54.765 s; 12 elements is
  the censored sample above. Unequal populations and selection, not a scaling law or S0 price.
* **Controls / verification:** inherited invariance/positive/negative PASS reused after current
  source, Python, dependency and solver hash checks; size-control PASS bound by queue hash.
  Fresh coverage/checkpoint/log/provenance audit PASS (`results/run-audit.json`). No solves,
  CNF rebuild or DRAT replay; formula hashes retained, UNSAT-SOLVER is not UNSAT-VERIFIED.
* **Summary correction:** timeout lower bounds now use recorded caps, excluding shutdown
  overhead, as PLAN requires. Focused pricing tests: seven PASS; production summary regenerated.
  Existing census/runner checks reused; no integration concern requiring another quick suite.
* **Scope:** no SAT model to bridge or candidate to verify. Recovery is not discovery-power
  evidence; H-261101-07 status and S0 A/B/C unchanged. No LOW-YIELD or family exclusion.
* **Next:** no full sweep; only registered symmetric slice I-261116-04 remains for (11,5).
  Week item 2 next; item 4 parked by its failed gate. Evidence: `results/run/verdict.json`.

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
