# E-261114-02: bridge recovery control

Pre-registration, 2026-11-14; chained week item 3. No compute before this commit.

* **Scores / hypothesis**: T 1 D 2 F 2 G 2 R 2; H-261110-03, planning only.
* **Question / H1 / H0**: does the frozen bridge recover >=80% of known-realizable chirotopes
  (H1), or <=30% (H0)? Intermediate outcomes are recorded without a new route.
* **Method**: the sixteen saved (10,2) objects of E-261113-02, rationalized at the verifier's
  1e-9 scale, exact chirotopes without coordinate warm starts; tranche.bridge, three optimizer
  seeds 26110303, 26110304, 26110305. Keep hinge/two_stage/fp, six restarts, 120 s per stage.
  Add only an optional payload seed, defaulting to the unchanged historical seed.
* **Discovery arm**: five lowest Lutz-number drawn maps of E-261113-02 that had no realization,
  thirty solver seeds 0..29 each, normalized ALL_OPTS submap formulas, 60 s solver cap;
  bridge each SAT with the historical optimizer seed. This arm is conditional on remaining budget.
* **Controls**: exact model satisfies its pinned formula; known input objects retain the saved
  successful --target S6 transcript. The bridge's exact sign match and --target S6 check must
  pass for each recovered object. A flipped bracket provides a sign-match negative control.
* **Counters**: SPEC §4 EMBEDDED, SAT, UNSAT-SOLVER, TIMEOUT, recovery fraction; solver and
  bridge times. Recovery means saved-file --target S6 PASS at (10,2), never a focus result.
* **Budget / stop**: strictly <1 core-h, ten shards, 350 s wall allowance per shard inclusive
  of all child stages; each operation is bounded by remaining shard allowance. Recovery arm
  first, then discovery. Stop at cap, failed correctness control, or all units recorded.
  Budget-censored units are TIMEOUT, not failures of realizability; incomplete recovery means
  UNDERPOWERED, do not apply the 0.3/0.8 thresholds to a selected completed subset.
* **Pilot / prediction**: reuse the known exact inputs and frozen bridge defaults; predict recovery
  above 0.3, uncertain before the run. A seed plumbing test must preserve the default stream.
* **Power / grid**: three optimizer seeds per known chirotope, thirty model seeds per new map;
  measures this implementation's recovery, not mathematical realizability or independence of seeds.
* **Proofs**: none. Counter calibration: exact booleans define recovery; float losses cannot decide it.
* **Scenario move**: no numerical credence update; high recovery supports many-model sampling for
  A/C, low recovery prioritizes realizer work; incomplete budget and intermediate recovery leave
  A/B/C unchanged. No negative statement about S6 (10,3).
* **Follow-up / ledger**: >=0.8 -> bridge adequate, thirty models per target SAT; <=0.3 -> one
  realizer session before judging target SAT; otherwise record. No new search route.
