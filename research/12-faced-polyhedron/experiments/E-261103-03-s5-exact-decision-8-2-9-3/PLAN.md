# E-261103-03: bounded (8,2) decision pilot

Pre-registration, 2026-11-03. Focus S5 (9,3); this stage is S5 (8,2).

* ROADMAP scores: T D F G R = 2 2 2 2 2; T + D = 4.
* Tests: H-261103-03, H-261103-02, H-261101-07.
* H1: an admissible (8,2) map has a geometric realization; H0: neither does.
* Method: reuse E-261103-01 census and E-261103-02 predicates. Build plain and free-C2 formulas for each of the two maps. No fixed-face C2/D3 exclusions, nonuniform extension, new census or (9,3) solve.
* Controls: own Roest-Vigh and Mizhaev pinned formulas SAT, exact recovery of their supplied chirotopes through both existing realizers (warm-start and unseeded recovery reported separately). Cross-map pinned formula UNSAT with checked proof; all 37 inadmissible (9,3) maps rejected. No target solve after a required control fails.
* Pilot: one worker, 900 s hard wall budget; controls <=480 s, four target SAT calls <=60 s each, remaining time for proof checking/model processing. All subprocesses use the remaining deadline. Solver timeout, not a model/iteration cap, is intended to bind target calls.
* Prediction: at least one plain target formula finishes in 60 s (uncertain; failure means a longer-budget grid, not an exclusion). Controls are expected to finish; failure blocks target solving and calls for repair/calibration.
* Grid: pilot uses 60 s per formula; a later run uses 300/900/3600 s, not more seeds at the same cutoff. That run requires a committed amendment after this pilot.
* SAT handling: save and check the full model against every CNF clause; try both existing realizers at F planes, one restart each with deterministic seeds, then final polynomial <=120 s within remaining time. Exact rational signs must match before geometry verification.
* UNSAT handling: retain CNF and DRAT, check with drat-trim; unchecked proofs remain UNSAT-UNCHECKED. Preserve partial proofs on timeout too.
* Critical scope: NONREALIZABLE-EXACT excludes one model only, never its map. No model enumeration or map-wide nonrealizability claim in this pilot. Symmetric UNSAT excludes only the uniform symmetry ansatz. Plain UNSAT is scoped to the formula, with geometric interpretation conditional on PROVED-1 encoder soundness.
* Power: 60 s probes affordability, not completeness. Both realizers must recover each known chirotope with supplied planes; unseeded failure is UNDERPOWERED for target construction. Timeout/UNKNOWN/ERROR/LP-TIMEOUT give no negative mathematical information.
* Counters/calibration: SAT, UNSAT-VERIFIED, TIMEOUT, ERROR, exact chirotope match and EMBEDDED; no float threshold contributes to a verdict. Record seconds, budget fraction and binding limit per unit.
* Scenario move: verified geometric (8,2) witness supports existence for that case only; both plain UNSATs support H-261103-03 conditional on encoding soundness. One nonrealizable model or timeout leaves the map unresolved and credences unchanged. Symmetric-only decisions do not change asymmetric existence credence. No arbitrary fractional update by number of maps.
* Stop: failed required control, hard deadline, or completion of four target calls plus bounded model processing. A candidate uses candidate-check and verify_candidate --target S5, with F=8,g=2 confirmed. Focus (9,3) is unchanged.
* Artifacts: original maps/planes, CNFs/models/proofs/checker output, hashes, parameters, source commit and dirty state, dependencies, measured wall/core seconds. Never overwrite an existing result directory.
* Ledger: record a pilot conclusion and leave the experiment running if the wider queue remains undecided. No long run, push, PR or subagent is part of this stage.

## Amendments
