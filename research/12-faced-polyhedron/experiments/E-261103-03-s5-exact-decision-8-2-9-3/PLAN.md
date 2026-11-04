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

### 2026-11-04: autonomous follow-through, 60/300-second plain grid

Owner authorization: continue this experiment autonomously. This amendment changes the target-call
cutoff and freezes a stopping decision; it does not silently repeat the same pilot. T+D=4 remains
above gate. Target S5 (9,3); no S0, new census, fixed-face symmetry or model enumeration.

* Panel: unresolved plain maps 0,1,40,48, purposively covering the earlier short/interrupted calls
  and two nonsymmetric extra-edge patterns, including tripled adjacency. Reuse recorded 60-second
  cells of maps 40/48. Map 0 gets its first 60-second cutoff; map 1 gets its first uninterrupted
  60-second call. Then each still-unresolved map gets one 300-second call. No rerun of SAT or
  UNSAT-VERIFIED cells; at most six new solver calls. Retain earlier C3 decisions as comparison
  only; do not rerun them or infer a median speedup from censored pairs.
* H1/prediction: at least two of four selected plain maps decide by 300 seconds with valid checked
  evidence; H0/rival: fewer than two, or proof checking prevents use of the decisions. At least one
  new decision is a weaker secondary prediction. These concern affordability, not non-existence.
* Budget: one worker, nice priority, all numerical threads pinned to one. Computation hard cap
  3300 seconds plus 300 seconds reporting reserve. New solver/checker worst case 2640 seconds
  (2x60 + 4x300 each), below 0.8 core-hours; controls <=300 seconds. Prior grid baseline cells are
  reused evidence, not charged again as new computation. Sum all manifests for cumulative experiment
  accounting. At most one target SAT is processed, with three <=120-second stages; no night launch.
* Controls: the existing pinned positives, warm reconstructions (required), unseeded reconstructions
  (construction power), checked cross-map negative, inadmissibility and malformed-pairing guards,
  rebuilt/replayed (8,2) evidence, exact nine-plane predicate/GP positive and free-C3 arrangement
  positive all run before targets. The same hard limits and failure gates apply. These do not supply
  a positive S5 (9,3) embedding or a runtime distribution for target maps.
* Exact outputs/counters: clause-validated SAT, UNSAT-VERIFIED only with retained checked CNF/DRAT,
  TIMEOUT, ERROR, exact sign match, EMBEDDED. No float diagnostic contributes to a verdict. Record
  solver and checker budgets/durations separately. The checker has the cell's cap too; all processes
  are bounded by the remaining global deadline. A decision at 60 skips its 300-second cell.
* SAT: stop further dispatch, save/check the full assignment, try both existing realizers then final
  polynomial, <=120 seconds each. An exact candidate invokes candidate-check and verify_candidate
  --target S5, with F=9,g=3, (V,E,F,chi)=(26,39,9,-4). Sign invariance does not certify a rotation.
  A nonrealizable model leaves its map open. Numerical failure or timeout gives no mathematical negative.
* Stop: control mismatch, invalid model, ERROR, unchecked/failed proof, first processed SAT, exhausted
  grid or hard deadline. All timeout/partial proofs and CNFs are retained and hashed; completed proofs
  are compressed without loss and versioned. Large partial proofs stay local with hashes.
* Decision after the grid: fewer than two checked new decisions, or dominant proof cost, stops the
  unchanged full-sweep route at this budget. Conclude it as LOW-YIELD@the measured budget, leaving
  unrun maps and geometric existence explicitly unresolved; changing solver/encoding needs a new
  rationale, not more identical seeds. If at least two complete, assess a costed tranche with the
  unresolved tail and the strategy review's explore-before-tranche gate; do not extrapolate an easy
  median or start a multi-hour session run. A first SAT with no witness ends this affordability stage
  and makes a bounded model-level study the next task, not collecting more models.
* Provenance: results/grid_9_3, immutable original pilot directories, census hash, map identities,
  identical clause hashes across cutoff cells, baseline summary hash, source commit/dirty state,
  dependencies, platform, exact wall/core durations and full/partial evidence. No push, PR or release.


### 2026-11-04: activate bounded new-map coverage after E-261103-05

The owner requested continuation from CONTINUE_PROMPT. E-261103-05's registered explore
prerequisite has concluded (STATUS 3g). Continue on Codex/s5-coverage-tranche from 9f9f898,
retaining the completed explore dependency and every previous artifact. T D F G R remain
2 2 2 2 2. This amendment supersedes the proposal's activation status, not earlier evidence.

* Target: S5 (9,3), plain uniform embedding formulas only. H1: cheap exact decisions extend
  beyond the purposive pilot panel; rival: the new-map tranche mostly times out. Prediction:
  at least 20 of the frozen 80 maps become UNSAT-VERIFIED or yield a clause-checked first SAT.
  This tests affordability, not existence; no median extrapolation from completed calls.
* Freeze tranche_queue.json before compute: first 80 admissible census maps in saved order
  excluding every previously dispatched plain map. Store census/baseline/canonical hashes.
  Preserve the seven unresolved attempted maps; no retries of that hard tail or new census.
* Budgets: solver <=60 seconds, checker <=120 seconds, one numerical thread per worker,
  1..8 simultaneous single-worker shards. Each shard has at most 180 seconds per assigned
  map plus 300 seconds controls, 360 seconds first-SAT processing and 300 seconds setup/report.
  At eight shards this is 22080 seconds = 6.133334 conservative core-hours (<6.2).
  A persistent shared reservation ledger caps all attempts at 22319 seconds (<6.2 core-hours),
  including restarts; a killed attempt retains its reservation conservatively. Exhausting it
  stops unresolved work; a new budget requires a committed amendment. No automatic git writes.
* Checkpoint: append/fsync one record per completed map; skip recorded TIMEOUT and verified
  decisions across all shards when repartitioning. In-flight attempts use fresh directories;
  never overwrite their CNF, partial proof or logs. A torn final JSONL line is ignored, then
  repaired before appending; corrupt interior lines block resume. Changed source/queue/input
  identities block resume. Per-shard locks prevent duplicate starts; shared dispatch/SAT lock
  makes first-SAT stopping visible across shards. Interrupted attempts are unresolved.
* Gates before each shard dispatches targets: the existing positive pinned known objects,
  warm realizers, checked cross-map negative, inadmissibility/malformed pairing guards,
  rebuilt saved (8,2) proof replays, nine-plane exact predicate/GP positive and free-C3
  arrangement positive. Controls <=300 seconds through the existing pilot path; a failed
  control, invalid model, ERROR or unchecked proof sets a shared stop. Unseeded realizer
  outcomes describe construction power separately. No geometric (9,3) positive is available.
* Same-path session pilot: one shard, the first two frozen maps (8,9), same 60/120-second
  limits, same controls and coordinator as production; separate results/coverage_pilot.
  Resume that pilot once to verify completed units are skipped. Target work plus controls
  is <=660 seconds plus bounded reporting. An additional synthetic SAT/UNSAT/process test
  exercises the first-SAT latch and corruption/error paths without a target solve.
* Long-run gate: controls and checkpoint/first-SAT tests pass, target calls bind on intended
  time/completion limits, no proof checker failure; the >=20 prediction remains uncertain.
  A tiny pilot is not an estimate of population yield. First SAT or a gate failure blocks
  a coverage launch pending its bounded model-level outcome and a written decision.
* First SAT: save and clause-check the full assignment, atomically stop further dispatch
  across shards (already running units may finish); process only the first model through
  hinge, two-stage and final polynomial, each <=120 seconds. A saved SAT latch survives
  restart; unfinished processing resumes under a global lock and within remaining budget.
  Exact signs and embedding precede CANDIDATE; verify_candidate --target S5 and candidate-check
  remain required. NONREALIZABLE-EXACT concerns one model, never the map. No model enumeration.
* Counters: SAT, UNSAT-VERIFIED, TIMEOUT, ERROR, UNSAT-UNCHECKED, exact sign match, EMBEDDED.
  No float diagnostic enters a verdict. Keep and hash all CNFs, full/partial DRAT, models,
  raw transcripts, tool versions, source/input identities and per-attempt wall/core seconds.
  Solver/checker durations and binding limits are separate. All waits/deadlines use monotonic
  time; setup/build/proof handling are bounded by the shard cap. Append manifests on restart.
* Interpretation: EXACT applies only to checked saved formulas. Geometric interpretation
  remains PROVED-1 conditional on encoder/census/general-position arguments; no CERTIFIED
  upgrade. Timeouts/unchecked proofs and numerical failures give no negative information.
  SAT without realization stops collection and prioritizes the realizability bottleneck.
  Otherwise report coverage and cost, retaining every unresolved/unattempted map explicitly.
  Existence hypotheses and scenario credences do not move from a bounded partial exclusion.
* Implementation plan (existing Python/shell patterns; no dependencies):
  1. Add failing regressions for queue identity, checkpoint resume, independent checker cap,
     shared first-SAT stop, interrupted attempts and bounded subprocess cleanup.
  2. Extend pilot.solve with a distinct checker cap and SAT callback; add controls-only mode.
     Implement experiment-local tranche.py and register its job in run_overnight.py.
     Reuse command/stage, JSON checkpoint and manifest patterns; do not change old evidence.
  3. Extend run.sh with numeric shards and an explicit coverage-pilot mode using activated
     python3; reject invalid modes/shard counts. Keep old pilot/paired/grid modes intact.
  4. Run focused regressions and the registered same-path pilot, record its conclusion and
     gate verdict, run verify_all.py --quick, update handover and supply the exact laptop
     launch/status/stop commands. Do not launch the tranche, push, open a PR or upload proofs.
