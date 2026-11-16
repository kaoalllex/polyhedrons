# E-261114-01: normalised S6 prep (2026-11-14)

* **Soundness gate:** PROVED-1 geometric normalisation argument in `SOUNDNESS.md`; bounded
  exact-arithmetic tests in `results/invariance/`: 300 uniform configurations, 2800 reorientation/mirror
  comparisons, no mismatch. Each shard detects an intentionally corrupted GP sign. Not a theorem about
  arbitrary nonrealizable OMs; no new exact witness is asserted.
* **Positive gate:** 73/73 pinned/unpinned SAT, every solver model checked against its CNF, no retry:
  the three named polyhedra, convex f9/f10, grooved k2/k3, sixteen realized (10,2) objects and fifty maps.
* **Negative gate:** 205/205 admissible (8,2)/(9,3) formulas UNSAT-SOLVER, plus three (10,4) timing controls.
  Instance scope only (SPEC §4), no proofs and no negative geometric claim.
* **Timing (NUMERICAL):** normalized solver seconds for (10,4) #845/#96/#85: 4.619/23.981/203.839;
  speedups over the saved plain runs: 40.78/44.76/13.49. All three plain CNF hashes match the baselines.
* **Runs:** ten shards per gate; positive CPU counters sum to 0.02040 core-h, negative to 0.25336.
  These are cumulative worker counters, not deduplicated CPU billing. Invariance recorded wall time
  only; its CPU total is unavailable. Environment and input hashes: `results/environment.json`.
  AC was checked during the pilot; caffeinate was attached during it, not at its start. No sleep-gap detector.
* **Execution failure:** first negative-gate launch failed before solving because spawned workers
  imported a namesake controls module. The local import path was fixed; the recorded rerun passes.
* **Bridge control:** chained E-261114-02 is ADEQUATE; see its CONCLUSION. At least thirty models
  per target SAT map remain mandatory. H-261110-03 and A/B/C have not moved from these controls.
* **Verification:** focused seed regression and `verification/verify_all.py --quick` ALL PASS;
  archive replay skipped. This reuses the shared successful check saved under E-261114-02/results/.
* **Provenance:** PLAN pre-registration `ada4ee1c`; results retain model/formula hashes and exact
  control transcripts. No (10,3) or S0 witness is claimed from the prep controls.

## Pilot decision

* **Verdict: NO-DAY-RUN (OPEN, solver-limited).** Lutz #1 and #2 both TIMEOUT at the 1200 s solver
  cap, budget fraction approximately 1.0 each; no SAT, UNSAT-SOLVER, ERROR or target candidate.
  The registered prediction that at least one pilot finishes fails. Both units stopped at the intended limit.
* The day gate is closed: no twenty-map run, no launcher prepared or exercised. Only these two
  normalized target formulas were run; the other eighteen were not run. No negative claim (SPEC §4).
* **Next:** week item 4, E-261114-03 hull-vertex chart normalisation, before a day run or item 2.
  This is the registered follow-up, not an improvised extension. H-261110-03 and A/B/C remain unchanged.
* **Evidence:** `results/pilot/summary.json`, per-shard `results.json` and `manifest.json`;
  no processes left in flight. Passing prep and integration checks above are reused.
