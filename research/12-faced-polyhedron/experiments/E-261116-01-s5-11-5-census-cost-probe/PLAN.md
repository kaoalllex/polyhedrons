# E-261116-01: S5 (11,5) census and normalised cost probe

Pre-registration, 2026-11-16; week item 1, exploit, jump 2. Commit before compute.

* **ROADMAP / scores**: T 2 D 2 F 2 G 2 R 2; origin I-261114-03, E-261103-01, E-261110-06.
* **Question / H1 / H0**: does the normalised (11,5) family fit one laptop night (H1),
  or is it too expensive at this scale (H0)? H-261101-07 gets planning evidence only.
* **Target / counters**: SPEC S5, F=11, g=5, V=38, E=57, adjacent_pairs=55;
  EMBEDDED, nonsimple_faces, bad_pairs, multiplicities; SPEC §4 solver statuses and timings.
* **Census**: unchanged E-261103-01/census.py 11 5, 540 s enumerator cap, full manifest;
  compare complete/exhausted, canonical-code digest and distributions with the lead's
  strategy-review-2026-11-16-census-11-5.json. Verify every Euler/link/admissibility record.
  Reuse the unchanged saved 59-map S0 census control and its exact correspondence test.
* **Method**: freeze random.Random(26111601).sample within each census-ordered pattern:
  [1,1,1,1]: five; [1,1,2]: four; [2,2]: one. Queue binds census, encoder and control hashes.
  Reuse E-261110-06 s5ab dispatch; ALL_OPTS, symbreak=True, mirror=True, kissat seed 0.
* **Controls**: validate saved E-261114-01 invariance/positive/negative source, Python,
  dependency and solver hashes via E-261110-06/prep.controls; do not repeat unchanged solves.
  New size: convex f11 from control_f9.build(faces=11), exact topology; normalised pinned
  and unpinned formulas must be SAT (60 s). Negative: different convex map at the same
  pinned planes must be UNSAT-SOLVER (60 s). Ten shards; stop on a failed control.
* **Pilot**: actual launch.sh 16-01 start/status/stop/start with a fixture of ten sampled
  target maps at 0.01 s; verify intended dispatch, checkpoint preservation and resume.
  This tests startup, not discovery power; short timeouts cannot kill the 3600 s probe.
* **Pilot gate / prediction**: controls pass, census matches, startup reaches all ten units;
  the intended day binding limit is 3600 s or cumulative budget. Predict fewer than five
  timeouts (uncertain; failure sends the route to the registered symmetric slice).
* **Grid**: one cap, 3600 s, because this is a price probe; the startup cap is not a price sample.
* **Budget**: prep one session (census <=540 s plus checks); owner day run ten shards,
  <=36000 cumulative worker seconds, <=10 cores, on AC under caffeinate, no session launch.
  Per-shard build/bridge overhead shares the budget; solver cap is reduced to remaining
  time if needed and its actual cap is recorded. A shorter timeout is right-censored.
* **SAT**: check Boolean assignment, preserve model; existing bridge (hinge/two_stage/fp,
  120 s each), up to 30 solver-seed models within budget. An unfinished bridge or model
  set stays pending for review, not complete; no unbudgeted continuation. Any exact
  --target S5 PASS at (11,5) -> candidate-check, stop and escalate to the owner.
* **Proofs**: none; UNSAT-SOLVER, exact formula scope only, never geometric exclusion.
* **Power**: ten stratified maps price a sample, not all maps. No known target discovery
  rate; no detection-probability claim. Recovery controls do not establish discovery power.
* **Counter calibration**: no float geometry diagnostic decides success. Runtime thresholds
  use recorded monotonic seconds; summary logic is checked on artificial timed/censored rows.
* **Pricing**: population-weighted stratum means, timeouts replaced by their actual cap as
  lower bounds; report censoring explicitly. One night = 10 cores x 8 h = 80 core-h.
  Report the sample median with its censoring flag; element-count 9..12 comparisons use
  existing normalised records only and disclose selection/solver differences.
* **Follow-up**: SAT has priority; then >=5 TIMEOUT or price >4 nights -> no sweep, only
  I-261116-04; <=1 night with uncensored price -> owner sweep, fastest pattern first;
  1..4 nights or an uncertain/censored boundary -> lead. An uncensored median <=1200 s
  enables E-261116-03 (owner already approved). Never use a censored lower bound to pass it.
* **Outcomes / scenario move**: checked witness establishes existence for S5 (11,5);
  SAT without realization leaves existence open. UNSAT-SOLVER only prices this formula
  sample; timeout/UNKNOWN, ERROR and near-miss establish nothing. H-261101-07 and S0
  A/B/C credences unchanged without a new lead decision; no quantitative credence update.
* **Stop / ledger**: census mismatch, failed control, first verified candidate, ten map
  records or budget. Prep PASS -> running/ready for owner; mismatch/failure -> escalate.
  Day verdict and registered follow-up go in CONCLUSION and the ledger, not a family negative.

## Amendments

### 2026-11-16: preparation record

Census matches; its review digest serializes newline-joined sorted str(code), not JSON arrays.
The initial comparison failed only on that serialization; rechecked hash-bound saved output,
without rerunning the enumerator. Corrected probe.py; positive-control code is unchanged.
Size controls PASS; inherited controls reused after source/environment hash checks.
Actual ten-shard start/status/stop/start fixture PASS at 0.01 s; checkpoints unchanged.
The hard budget includes validation, map loading, building, solving and bridging inside run().
Production capped solves and all target follow-ups remain for the owner; prep is not a price sample.
