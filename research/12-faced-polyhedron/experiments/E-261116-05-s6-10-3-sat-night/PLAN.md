# E-261116-05: normalised S6 SAT-oriented owner night

* ROADMAP: week item 2, registered follow-up of E-261116-02; exploit, jump 2.
  T D F G R = 1 2 2 1 2, T + D = 3. Owner requested preparation on 2026-11-16.
* Question: can the pilot-winning monolithic kissat --sat decide the remaining
  normalised Lutz (10,3) formulas in one laptop night?
* Tests: H-261110-03. H1: another map is decided; H0: none is decided.
* Target: S6 at ten faces, genus three; the unchanged uniform submap=True formula,
  symbreak=True and mirror=True (E-261114-01). No target weakening.
* Changed setup: E-261116-02 decides both pilot maps; monolithic --sat costs less
  than lookahead cubes on each. This follows the approved success branch.
* Queue: Lutz #3 through #20 in catalogue order, immutable links and source hashes.
  Reuse #1/#2 monolithic decisions from E-261116-02, bound by audit and CNF hashes;
  do not rerun decided maps. Fresh records and reused decisions stay distinguishable.
* Budget: <=80 worker core-h including controls, builds and interrupted reservations;
  reserve 1 worker-h for preparation and 79 for production including restarts;
  ten single-worker shards, <=8 active hours each, owner laptop on AC under caffeinate.
  Each map has a 13800 s solver cap; two units fit a standard shard with overhead.
  Dispatch only a complete unit allocation; exhausted time/budget leaves work OPEN.
  In-flight killed attempts retain their charged reservation on restart.
* Counters: SAT, UNSAT-SOLVER, TIMEOUT, ERROR; solver/worker/CPU seconds,
  checked assignment and completed maps. Timings NUMERICAL, SPEC §4 instance scope.
* Controls: reuse normalisation invariance, positive and negative gates after source,
  Python, dependency and solver identity validation in every shard (prep.controls).
  Reuse E-261116-02 known-SAT --sat model and cover-negative gate after hash checks.
  Prep checks both signs through the same new queue path on small control formulas;
  no rediscovery or proof replay of unchanged evidence.
* Pilot: no further long target solve. Existing two target decisions are the method
  pilot; bounded startup uses ten shards through launch.sh, tiny caps in scratch output.
  Exercise start/status/stop/start, checkpoint survival, full-cap refusal and first-SAT
  dispatch latch. No startup TIMEOUT is a target conclusion.
* Gate: controls and startup PASS, queue and inherited decisions hash-consistent,
  no production units before the owner start; T + D unchanged. Failure blocks launch.
* Power: decisions only within this frozen queue and cap. Positive recovery does not
  establish discovery power. No scaling law, speedup claim or geometric negative.
* Proofs: none; UNSAT-SOLVER only, never UNSAT-VERIFIED or an exclusion.
* Calibration: exact Boolean clause checks; no floating geometric diagnostic.
* SAT: check every original clause, save the model, latch a shared stop before further
  dispatch; other in-flight work may finish. Thirty models and the frozen submap bridge
  are a subsequent bounded stage, then verify_candidate.py --target S6 and candidate-check.
* UNSAT-SOLVER: decide this formula for planning only. TIMEOUT or missing record: OPEN.
  ERROR/control failure: shared stop and investigate; no blind retry.
* Stop: first target SAT, failed control, owner stop, budget/deadline, or queue exhausted.
  Stop/resume skips completed units across all shards; no automatic change of caps.
* Follow-up: any SAT -> registered thirty-model bridge stage, escalate on exact PASS;
  no SAT -> park the remaining undecided S6 queue, record solver-level decisions for
  planning. No further long-cap campaign without owner/lead direction.
* Credences: H-261110-03 status and S0 A/B/C unchanged for solver outcomes.
  Only an exactly verified S6 witness can move existence claims.
* Ledger: preparation changes launch readiness only; conclusion owns counts/costs.

## Amendments
