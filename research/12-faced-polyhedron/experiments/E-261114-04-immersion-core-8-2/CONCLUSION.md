# E-261114-04: park the small-core route

* Prediction met: neither map has a core on <=6 face groups.
* Runs: 10 shards, 512 distinct restrictions, 0.0222 core-h against <=1 core-h;
  pilot wall 9.05 s, remaining batch <=11.14 s per shard. No timeouts or errors.
* Each map: 255 SAT proper restrictions, one UNSAT-SOLVER full restriction;
  all 28 six-group restrictions SAT. The unique inclusion-minimal solver core
  is [0,1,2,3,4,5,6,7] for both maps. See results/summary.json.
* Controls: full grouped V1 equals standard normalised V1 as clause multisets on
  every build; pinned re-gauged Roest-Vigh SAT, contradictory units UNSAT-SOLVER,
  empty restriction SAT on every shard. SAT assignments checked by pilot.solve.
* Provenance/coverage audit PASS (results/audit.json); source, solver, CNF and output
  hashes retained. Cached invariance input hashes match. Cached positive summary
  not reused: pilot.py changed; this run's fresh controls passed instead.
* NUMERICAL planning evidence, SPEC section 4 instance scope: UNSAT-SOLVER only,
  no DRAT or geometric verification. SAT restrictions are Boolean models, not
  polyhedra. Predicate circuits still use all eight planes; face-group size is
  not the number of planes in a standalone obstruction.
* H-261101-15: this eight-face analogue does not support a small face-group lemma;
  its twelve-face statement stays open. H-261029-06 unchanged: no immersion found
  or excluded geometrically. A/B/C unchanged.
* Verdict: completed; park under week item 5's follow-up tree. No theory session
  triggered, no additional compute. Next: lead review of the unresolved focus routes.
