# E-261114-04: face-grouped immersion cores

* ROADMAP: week item 5, explore; T D F G R = 2 1 2 2 2.
* Question: do the normalised V1 formulas of (8,2) maps #0 and #1 have cores on <=6 face groups?
* Tests: H-261101-15 (local obstruction), H-261029-06 (immersion obstruction).
  These are eight-face analogues, not tests of the twelve-face statements themselves.
* H1: a core uses <=6 groups; H0: every such restriction is SAT.
* Target: immersion-only relaxation of S5 (8,2), not an embedded object.
* Method: retain all eight plane elements, GP, definitional circuits and reorientation/mirror units.
  Group INCONS by its first face, RFCONS and POC by their face, REFLEX1 by its pair of faces.
  A constraint is enabled only if all its owning faces are selected. Predicate definitions may
  reference unselected planes; a small group core is not a standalone polyhedron on fewer planes.
* Enumerate all 256 face subsets per map, round-robin in 10 shards. Save formula hashes,
  checked SAT assignments and solver logs; compute inclusion-minimal UNSAT-SOLVER subsets.
* Controls: full grouped formula equals standard normalised V1 as a clause multiset;
  empty groups SAT; re-gauged pinned Roest-Vigh V1 SAT; contradictory units UNSAT-SOLVER.
  Reuse item 1's soundness controls; no new invariance claim.
* Pilot: shard 0, including controls. Failed controls stop the experiment.
* Grid: all subsets, no sampling; cap 5 seconds per solve, including controls.
* Budget: <=1 core-h, one session, 10 shards on owner's laptop, no unattended run.
  Worst solver budget 512*5 + 10*3*5 = 2710 seconds; allow <=800 seconds overhead.
* Power: exhaustive if all queries finish; timeouts make affected minimality unresolved.
* Prediction: neither map has a core on <=6 groups (planning prediction).
* Proofs: none; every negative solver response is UNSAT-SOLVER, instance scope only.
* Counters: selected face groups, clause counts, SAT/UNSAT-SOLVER/TIMEOUT; no float verdict.
* SAT means only a model of the selected restriction, validated against every CNF clause.
  No geometry or candidate claim follows. Timeout gives no information.
* Scenario move: A/B/C unchanged for every outcome; only prioritise a possible local lemma.
* Follow-up: any <=6-group core -> one theory session; otherwise park. Unresolved
  restrictions -> report solver-limited and escalate, no extra run.
* Stop: controls fail, registered grid exhausted, or budget exhausted.
* Ledger: record completion and follow-up in STATUS / ROADMAP, never a geometric exclusion.

## Amendments
