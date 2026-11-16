# E-261114-03: hull-vertex chart pilot

Pre-registration, 2026-11-14. Week item 4, activated by E-261114-01's two target timeouts.

* **Scores / hypothesis**: explore; T 2 D 2 F 2 G 2 R 2; H-261101-06, solver cost only.
* **H1 / H0**: a hull-vertex chart reduces summed decision time below 0.7 of the normalized
  monolithic time on both pilot maps / it does not. No geometric negative is sought.
* **Target / formula**: S6 (10,3), Lutz #1 and #2, the two timed-out normalized pilot maps.
  Reuse ALL_OPTS, submap=True, symbreak=True, mirror=True, kissat, seed 0, no proofs.
  No ranking of the eighteen unrun maps is implied by "two slowest".
* **Lemma gate**: SOUNDNESS.md, PROVED-1 at most. Make the sketch precise: an outside plane
  needs a nonzero old-INF term; orient the three incident planes toward the local interior.
  INF is a sufficiently small perturbation of their positive combination, not that combination
  itself. Use only sign implications preserved by this perturbation. A failed argument or
  control blocks all target cubes; no alternative normalization in this experiment.
* **Cube**: one selected corner triple; its three face corners must be convex. Orient each
  incident plane using its value at the opposite edge neighbour. For each other face triple,
  if the nonzero determinants against the three inward planes agree, force that INF sign.
  Omit repeated-row determinants and the selected triple (all three determinants zero).
  Cubes may overlap; completeness is geometric, not a partition of abstract OM models.
* **Controls**: all 23 geometric inputs of E-261114-01's pinned gate, using its saved exact
  uniform planes. At every hull vertex, save an exact rational projective re-charting;
  verify_candidate.py must PASS, the full normalized formula and selected cube must hold,
  and the pinned CNF must be SAT. Certify every other vertex as a convex combination of
  other vertices; a floating hull classification alone is insufficient. Exact arithmetic
  checks the support plane, positive coefficients, finite vertices and all uniform brackets.
  On one hull vertex of each object, reversing the inward orientation must violate the
  selector and its pinned selector-only CNF must be UNSAT-SOLVER (no GP/base clauses).
* **Reuse**: unchanged invariance, positive and negative gates of E-261114-01; bind their
  source/input hashes. They do not substitute for the new re-charting controls.
* **Small pilot**: controls first, then at most one 10-second cube per shard, ten shards.
  Failure stops; all timeouts block the full pilot pending an owner/lead decision.
* **Full pilot**: only after the small pilot passes and owner launch. One cube per vertex
  on both maps, ten shards, 120-second solver cap. No automatic S6 day run.
* **Budget**: <=3 core-h total, including controls, formula construction and small pilot;
  <=0.4 core-h reserved for controls, <=0.1 for small pilot. Full target solver caps total
  56 x 120 s; remaining budget covers construction. Laptop on AC under caffeinate.
  Stop before exceeding the remaining budget; interrupted work is not a decision.
* **Counters / calibration**: SPEC §4 statuses, EMBEDDED, nonsimple_faces, bad_pairs,
  adjacent_pairs; solver seconds and worker CPU deltas, wall time and sleep gaps.
  Test timing decisions on synthetic complete/censored inputs on either side of 0.7.
* **Baseline censoring**: both saved monolithic runs are TIMEOUT at 1200 s, not measured
  decision times. Rebuild and hash-check them; do not rerun unchanged baselines. A complete
  cube cover below 840 s demonstrates the desired bound against those lower bounds.
  A sum >=840 s cannot establish the kill ratio against an unknown monolithic time:
  record UNRESOLVED-CENSORED, escalate this measurement limit, never label it PARK by ratio.
  A later uncensored baseline is outside this registered budget and needs lead approval.
* **Prediction / power**: at least one small-pilot cube finishes within 10 s; at least one
  map's complete cover costs <840 s. Two maps measure this chart only, not discovery power
  or geometric nonexistence. Partial covers/timeouts cannot establish a speedup.
* **Outcomes / follow-up**: failed control -> blocked, one implementation correction allowed,
  then escalate; both covers below the bound -> CUBES-WIN, propose continuation to the lead;
  incomplete or censored comparison -> UNRESOLVED, proceed to week item 2 after handover.
  SAT -> save and check model, stop target pilot and escalate for the registered thirty-model
  bridge recovery and --target S6/candidate-check; a SAT model alone is no construction.
  No SAT model is discarded. UNSAT-SOLVER ranks only its exact cube, never excludes a map.
* **Scenario move**: H-261101-06 receives scoped timing evidence; A/B/C unchanged unless
  an independently checked focus witness establishes A. No proof production or negative claim.
* **Stop / ledger**: failed gate, SAT, all units recorded or cap; record prep/pilot state,
  controls, censored comparisons and next action in CONCLUSION, STATUS, ROADMAP and handover.

## Amendments
