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

### 2026-11-04: post-pilot hardening (no target rerun)

The recorded c48ab73 pilot finished in 35.58 s. Review found that a realizer fallback
could be misclassified if signs matched despite wrong_signs != 0. Require both checks;
all eight recorded recoveries have wrong_signs = 0, so this does not change their verdicts.
Add a main-process alarm as well as subprocess timeouts: the 900-s computation deadline
now covers Python formula building too. Final evidence hashing/reporting is outside the
alarm and its elapsed time is included in the manifest wall duration. The original run
had subprocess limits and a cooperative Python deadline, without the new alarm.
No amended target computation was run; old artifacts retain their original provenance.
Warm two-stage reconstruction uses two restart slots because the existing realizer only
uses supplied normals when k < restarts // 2; random-start controls use one slot.

### 2026-11-04: owner-requested paired C3/plain (9,3) affordability pilot

* Continue this experiment on its existing branch. T + D remains 4. This bounded pilot precedes any night;
  the separately due strategy review is not performed here.
* Target S5 (F=9,g=3). H1: free-C3 formulas decide substantially more cheaply than their plain partners;
  rival: symmetry yields no usable decision advantage at this cutoff. Existence H-261103-02 and H-261101-07
  move only after a verified geometric witness, or sufficient formula coverage plus soundness arguments.
* Deterministic sample: census indices 0..7, all eight admissible free-C3 maps, each C3 then plain;
  indices 8..11, the first four other admissible maps, plain only. Exactly 20 target formulas on 12 maps.
  Controls are separate from that target-formula count. Reuse the saved census; no new census or (8,2) solves.
  Recover C3 permutations from cyclic links and check order, absence of fixed faces and cyclic-link preservation.
* One worker, BLAS/OpenMP/Accelerate threads capped at one. Hard computation deadline 3300 wall seconds,
  with 300 seconds reserved for hashing/reporting, at most 1 core-hour conservatively as wall time x one worker.
  Controls <=480 seconds; each solver <=30 seconds and DRAT checker <=30 seconds, both bounded by remaining time.
  SAT postprocessing is after all formulas: hinge <=15 s, two-stage <=15 s, final-polynomial subprocess <=30 s/model.
  The existing internal LP limit of 120 s is superseded by that subprocess deadline. No enumeration or new seeds.
* Required controls before targets: pinned Roest-Vigh and Mizhaev SAT; warm exact recovery by both realizers;
  cross-map pinned negative UNSAT-VERIFIED; all inadmissible census maps rejected. Unseeded reconstructions
  are reported separately and failure means UNDERPOWERED for construction. Additional size-10-element C3
  control: exact uniform symmetric planes pinned in a GP + symmetry formula, SAT with clause-checked model.
  This calibrates symmetry, not existence of an S5 (9,3) embedding. No known geometric positive at (9,3).
* Predictions: at least four of eight C3 calls decide in 30 s; at least one paired plain call decides in 30 s.
  These are affordability predictions, not existence claims. Report paired decision counts, censored times,
  time fractions, and binding limits; do not replace timeouts by completed times or infer a median speedup
  from censored pairs. A longer campaign needs a committed budget grid and a separately passed long-run gate.
* Stop immediately on required-control failure, ERROR/invalid SAT model, failed or timed-out proof check,
  exact geometric CANDIDATE, hard deadline, or completion of all target calls and bounded model processing.
  A solver timeout alone continues to the next formula and carries no negative mathematical information.
* Retain CNF, full/partial DRAT, models, raw logs, original inputs, parameters and SHA-256 provenance;
  never overwrite results/paired_9_3. No floating diagnostic enters a verdict: exact signs and EMBEDDED only.
  An exact geometric candidate invokes candidate-check and verify_candidate --target S5, explicitly F=9,g=3.
* UNSAT-VERIFIED is EXACT for the saved formula; symmetry UNSAT concerns only the uniform free-C3 ansatz.
  A final polynomial excludes only its one model; numerical reconstruction failure excludes nothing.
  No symmetric-only UNSAT, nonrealizable model or timeout decides a map's asymmetric geometric existence.
* Decision: if both affordability predictions fail, stop this route at this budget pending strategy review;
  if C3 succeeds and plain stalls, retain C3 as the cheap ansatz and keep asymmetric existence unresolved;
  if plain decisions complete, consider a budget grid on the remaining admissible maps after review;
  if SAT models stall in realization/final polynomials, record the model bottleneck and do not buy a night.
  No automatic long run, push, PR or subagent work is authorized by this amendment.

### 2026-11-04: panel correction before continuation

The hand-over was stale: commit 69caae8 already contains the strategy review of 2026-11-04.
The first dispatch used the preceding amendment before that review was noticed. It was interrupted
by SIGINT during map1_plain; its manifest and partial proof remain untouched in results/paired_9_3.
This is an execution correction, not a mathematical outcome. No dispatched formula will be retried.
The interrupted call counts toward the 20-formula limit and remains unresolved.

For continuation, follow review section 4: pairs on maps 0 and 5, plain 10/30/40/48, then the other
six pairs in index order, skipping the already dispatched calls. This panel covers six excess patterns.
Use 60 s solver + 60 s checker for remaining formulas. Preserve the original 30-s cutoff and actual
interruption for earlier calls; mixed/censored timings do not estimate a speedup. Stop further target
dispatch on the first SAT, process that one model through both realizers and final polynomial, each
<=120 s, then stop even if no witness. Predictions become at least one plain completion and at least
six plain completions unless SAT interrupts; the interrupted plain is unresolved, not a timeout result.

Add the review's omitted control gates before continuation: rebuild and replay both saved (8,2)
proofs (no solver rerun), malformed pairing guard, and a deterministic nine-plane pinned definitions
+ GP positive with all evaluated predicates compared to direct exact geometry. These are arrangement
controls, not known (9,3) embeddings. Retest the selected free-C3 action. Controls <=300 s.
Record canonical-code hashes and the full group closure. Existing controls are repeated under the
same caps. Results go to results/paired_9_3_continued; inherited outcomes point to their original files.
The continuation's computation cap is 3300 seconds minus the first manifest's wall seconds, leaving
300 seconds total reserve for reporting. Both attempts together stay below 1 core-hour; all manifests
are summed. No night or repeated target call is authorized. A control failure ends the pilot.
