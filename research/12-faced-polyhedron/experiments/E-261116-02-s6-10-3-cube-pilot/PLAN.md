# E-261116-02: S6 (10, 3) lookahead cube pilot

* ROADMAP: week item 2; exploit, jump 2; T D F G R = 1 2 2 1 2 (T + D = 3).
* Question: can march_cu splitting or kissat --sat decide normalised Lutz #1 or #2?
* Tests: H-261110-03. H1: at least one formula is decided within this pilot;
  H0: neither is decided. Solver outcomes affect planning only, not existence credences.
* Target: S6 (10 faces, genus 3), uniform submap embedding formula with
  symbreak=True, mirror=True, as E-261114-01. No target weakening.
* Changed from E-261113-04: real lookahead cubes, normalised S6 formulas,
  SAT-oriented monolithic arm; no segment-order cube fallback.
* Counters: SAT, UNSAT-SOLVER, TIMEOUT, ERROR (SPEC section 4); solver seconds,
  cube counts, checked assignment, cover status. Timings NUMERICAL, instance scope.
* Controls: unpinned known-SAT (10,2) Lutz #739 through the same cuber and conquer;
  formula plus the negation of every emitted cube must be UNSAT-SOLVER.
  A SAT assignment must satisfy every original clause, not just a simplified formula.
* Prep: preserve raw cubes and source CNF hash; parse only complete `a ... 0` lines,
  reject malformed literals, truncated output and unsuccessful cuber exits.
  Cover checks include the original CNF: cuber-refuted leaves need not be emitted.
* Depth grid: try 7, 8, 9, 10 in order; choose the first completed partition with
  100-500 cubes. Each cuber attempt and cover solve has a 60 s cap.
  No eligible partition, timeout or failed cover -> stop prep and escalate;
  do not replace march_cu with the old segment cubes.
* Pilot: ten shards, positive pipeline and both target partitions; at most five
  minutes per shard. Solve control cubes until a checked SAT is found (60 s each,
  aggregate 120 s). Check the negative cover control on each selected partition.
* Pilot gate: controls pass, both partitions eligible and covered; limits bind as
  registered, source formulas unchanged. A valid partition can still fail to decide
  its map; that uncertainty is the question, D remains 2. Otherwise no day launch.
* Prediction: at least one target arm decides its map. Failure parks this S6 queue;
  success selects that method for the registered twenty-map owner night.
* Day budget: <= 8 core-h including preparation and controls, 10 shards on laptop,
  AC and caffeinate. Reserve 2 core-h for two kissat --sat monolithic units
  (3600 s each); remaining budget for cubes (600 s each), truncated at budget.
  Charge all failed/restarted attempts and in-flight reservations; never silently
  overrun the aggregate cap. Stop/resume preserves completed units across shards.
* Power: detects a complete cube refutation or a SAT model within this budget;
  partial refutation and timeouts decide nothing. No claimed speedup from censoring.
* Proofs: none. Every UNSAT is UNSAT-SOLVER; no geometric negative claim.
* Calibration: no floating geometric diagnostic; exact Boolean assignment checks.
* Scenario move: A/B/C unchanged for solver timing or UNSAT-SOLVER; verified S6
  witness goes to the owner/lead before any change to the hypothesis.
* SAT: preserve checked model, stop target work, then obtain thirty models and
  use the frozen bridge and verify_candidate.py --target S6, candidate-check.
* UNSAT-SOLVER: map decided for planning only when all covered cubes are UNSAT,
  or monolithic solve is UNSAT. No proof, no exclusion.
* TIMEOUT/UNKNOWN: OPEN; no existence inference. ERROR/failed control: no launch.
* Near-miss: no result; only exact S6 PASS at (10,3) is a witness.
* Follow-up: map decided -> one owner night on all twenty by the winning method,
  <= 80 core-h. Neither decided -> park S6 (10,3), solver-limited at laptop scale.
  No long-cap night without the owner. Outside-tree prep failure -> lead.
* Stop: controls fail, malformed/incomplete cubes, aggregate cap, owner stop,
  first target SAT, both maps decided, or all scheduled units recorded.
* Ledger: prep leaves STATUS unchanged; ROADMAP records launch readiness or the
  blocker. Conclusion records scope, costs and the follow-up branch.

## Amendments
