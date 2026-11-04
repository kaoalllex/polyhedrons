# E-261103-04: nine-face genus ladder, representation gate

Pre-registration, 2026-11-04. Commit this plan before executing the audit or any search.
At the owner's request this work stays on the current local branch, without creating a new branch.
The first activated stage is the bounded representation audit below. A geometric pilot and a
night require a dated, committed amendment after this gate passes.

* **ROADMAP row / scores**. T 1, D 2, F 2, G 1, R 2. T + D = 3. Explore.
* **Question**. Can the existing genus-ladder path preserve the supplied multi-adjacency maps
  before its recovery power is measured on known eight-face objects?
* **Hypotheses moved**. H-261101-07 concerns existence of maximal face-neighbourly polyhedra.
  H-261103-02 concerns geometric free-C3 symmetry at (9,3). This stage moves neither
  hypothesis. An eventual S5 witness would settle the corresponding existence case.
  Geometric C3 symmetry would require a separate exact certificate.
* **H1 / H0**. H1 for this gate is that the current triangle-to-links conversion preserves
  all admissible focus maps and both eight-face controls. H0 is that a representation
  mismatch prevents the proposed unmodified pipeline from reaching its intended inputs.
* **Difference from parked DR1**. The intended search targets S5 (9,3), below the
  genus-3-to-4 barrier, using nine planes and multiple adjacencies. This audit tests the
  representation prerequisite specific to that change. It repeats no S0 search.
* **Method**. Load the frozen E-261103-01 census, retain admissible maps, reconstruct their
  dart pairings with `census.from_code`, and extract the oriented corner triples. Compare
  `gauss_degree.links_from(gauss_degree.coherent_triangles(triples), n)` with the original
  dart map, using `census.from_links` and equality of canonical dart codes. Exceptions,
  missing edge copies, changed cycles, or changed codes fail the gate. Retain each outcome
  and source/input hashes. Test both eight-face references by the same conversion.
  Do not call `genus_ladder.chain` or search on a map that fails this gate.
* **Controls**. Positive combinatorial control is the single (7,1) Szilassi census map,
  which must round-trip to the same canonical dart code. Negative control is a supplied
  eight-face map with parallel edges. Its directed edge-label multiplicity must exceed
  one and the legacy conversion must reject it or fail exact round-trip equality.
  The negative control diagnoses this conversion, without deciding geometric existence.
* **Pilot and binding limit**. One serial representation audit, at most 120 seconds wall
  time, including the focus census and the two reference maps. Report elapsed time,
  budget fraction, and stop reason. No stochastic search, SAT call, or proof replay.
* **Prediction**. At least one admissible focus map fails the legacy conversion. This is
  a source-derived prediction, without a claimed 30-70 percent failure probability.
  No night can be activated on this prediction. A later recovery pilot must register an
  uncertain prediction and the 3/10-minute per-level grid before a night is considered.
* **Gate decision**. A failed positive control or any focus/control map mismatch stops
  the unmodified ladder path. Record an implementation limitation, retain the experiment
  as running, and prepare an explicitly scoped dart-preserving amendment. Passing this
  audit permits preparation of the geometric recovery pilot, without authorizing a night.
* **Intended subsequent geometric controls**. R1 Szilassi, then both known (8,3) maps
  through the same sphere-to-genus-3 ladder. Verify every level exactly and use
  `verify_candidate.py --target S5` only for maximal targets. Register recovery budgets,
  seeds and stop rules in an amendment before execution. A sphere must have the required
  simple triangulation and connected vertex links before convex realizability is invoked.
* **Budget / grid**. Current stage is one shard, one core, at most 0.033334 core-hours.
  One setting suffices for a deterministic round-trip audit. The ROADMAP night budget
  remains a ceiling for a future separately activated stage.
* **Power statement**. Exact equality detects loss of the supplied dart pairings in this
  conversion. Failure does not rule out dart-preserving handle surgery, another ladder,
  another representation, or any geometric realization. Tube decomposition coverage and
  recovery probability are unmeasured by this stage.
* **Counters / calibration**. Integer edge-copy counts, exact canonical-code equality,
  per-map conversion exceptions, and elapsed time only. No float diagnostic enters the
  verdict. Geometric `EMBEDDED`, `nonsimple_faces`, `bad_pairs`, and `adjacent_pairs`
  (SPEC section 4) are reserved for the later recovery pilot.
* **Scenario move**. A exists / B all OM-UNSAT / C OM-SAT but non-realizable all retain
  their preceding credences. A representation failure changes implementation readiness.
* **Outcomes**. ROUNDTRIP-PASS preserves this input map. ROUNDTRIP-FAIL identifies a
  conversion mismatch on this input. ERROR or timeout leaves the unprocessed scope open.
  No SAT, UNSAT, near-miss, geometric witness, or existence conclusion is produced.
* **Stop rule**. Complete the serial audit or stop at 120 seconds. Any failed gate
  prevents geometric search. Preserve partial records on failure.
* **Ledger**. On pre-registration set the README and ROADMAP to running. Record this
  stage in CONCLUSION and the chronology with its exact scope and evidence labels.
  Mathematical claims stay at PROVED-1 until human review. No FD/witness row changes.

## Amendments

* 2026-11-04, after the first audit on commit `040562a`. The audit stopped with
  `ValueError: links do not uniquely identify parallel-edge pairing; use dart code`
  while loading the Mizhaev control. Its supplied face cycles are not coherently
  oriented. Reuse the existing `review.coherent` helper on the supplied controls
  before `census.from_links`. Preserve the failed attempt and repeat the bounded
  audit into `results/representation-audit-oriented` using the runner's `OUT`
  override. This rerun addresses the failed control-loading step. No search is
  activated. The declared input hashes include the helper's source file.

### 2026-11-04. Dart-preserving surgery gate

Commit this amendment before implementing or executing its bounded audit. The first
representation audit and its correction remain historical evidence. This stage
tests a replacement for tube removal, using the same frozen census and controls.
T + D remains 3. A successful surgery gate permits planning recovery calibration.
Geometric search still requires a separate committed amendment.

**Question and scope.** Can six-triangle annulus removal produce checked chains
from the supplied maps to simple sphere triangulations while retaining every
surviving edge copy? H1 predicts such a chain for Szilassi and both eight-face
controls. H0 predicts an obstruction in this restricted surgery or representation.
Report focus-map coverage separately, without requiring every focus map to pass.
No existence hypothesis or scenario credence changes at this gate.

**Representation and implementation.** Reuse `census.from_code`, `review.TriMap`
and `TriMap.canon`. Extend the experiment-local audit and its runner with an
explicit surgery stage. Preserve the legacy audit invocation and immutable
outputs. Keep changes local to this experiment. Operations use triangle and dart
identities throughout. Vertex-label triples may filter a proposed annulus, but
must never determine which parallel edges are paired.

**Surface validation.** Check that every live dart occurs in exactly one oriented
triangle, `alpha` is a fixed-point-free involution on precisely the live darts,
paired darts have reversed endpoints, and the triangle/alpha traversal is connected.
The permutation `alpha(prv(d))` must have exactly one cycle for each of the original
face labels. Reject loops, repeated labels inside a triangle, and repeated unordered
corner triples. Require the intended Euler characteristic and unchanged label set.
Reuse the applicable checks from `review.check`, but its complete-adjacency condition
applies only to the supplied top maps. Lower ladder levels lose adjacencies.
Retain a label-preserving serialization alongside the unlabelled canonical code.

**Surgery.** Enumerate connected sets of six triangle identities through their
actual alpha adjacency, in deterministic order. Accept a removable patch only when
it is an orientable annulus with six distinct boundary labels, no interior vertices,
and exactly two vertex-disjoint boundary cycles of length three. Check patch vertex
links and Euler characteristic zero. Its complement must remain connected after
capping. For each boundary dart in the patch, retain its pairing with the outside
dart and place that boundary dart in the coherently oriented cap triangle. Delete
only internal patch darts and their alpha pairs. Keep all outside triangle cycles,
tails and alpha pairs unchanged. Validate the capped map and require genus to
decrease by exactly one. Store the removed triangles, internal pairings and boundary
identities so that reversing the surgery restores the entire labelled dart map.
Check this inverse at every step and compare canonical codes as an additional check.

**Chain search and endpoint.** Use deterministic depth-first search over validated
surgeries with canonical-code deduplication for reachability. Retain one complete
labelled path for each accepted endpoint, including the original top map. At genus
zero require no loops or parallel edges, distinct triangles, the surface checks
above, and the expected sphere Euler characteristic before naming the endpoint a
simple sphere triangulation. An exhausted restricted search records only that no
chain using these six-triangle surgeries reached such an endpoint. It does not
exclude other surgeries or realizations. Save a partial chain when a cap binds.
Report both canonical top-map equality and exact restoration of its labelled data.

**Controls.** Run Szilassi first, followed by coherently oriented Roest-Vigh and
Mizhaev from the same inputs as the corrected audit. All three must reach checked
simple sphere endpoints for the recovery gate to open. In addition, enumerate one
Szilassi removal with the legacy tube finder and match its capped map up to canonical
code as a compatibility control on a simple input. Check the independent structural
validator with a broken alpha involution and with a mismatched tail label. Check
patch rejection on the two disjoint cap triangles produced by a valid removal.
Each malformed control must fail its designated check. Reversal must reproduce
each valid control's top data, including parallel-edge pairings. Record missing
fixtures or an unexpected outcome as CONTROL-FAIL and stop before the focus maps.

**Budget and stop rule.** One core, at most 300 seconds wall time for the complete
audit, including controls and provenance, and at most 256 expanded states per map.
The per-map wall cap is 5 seconds, measured across enumeration, validation and chain
search. Check deadlines within patch enumeration as well as between states. Stop a
map on the first checked sphere endpoint or its cap. Process admissible focus maps
in frozen census order after all controls pass. A global timeout leaves remaining
maps unprocessed. This stage has no night, stochastic seeds or parameter grid.

**Outcomes and power.** CHAIN-PASS means a checked reversible chain to a simple
sphere for that input. NO-CHAIN means exhaustion of the declared restricted search.
STATE-CAP and TIMEOUT leave reachability unresolved. INVALID-INPUT, CONTROL-FAIL
and ERROR stop the gate and retain diagnostics. The stage can expose lost edge
copies, invalid capping and unsuitable endpoints. It measures no geometric recovery
probability and supplies no LOW-YIELD verdict on the geometric engine. Counters are
integer state/patch counts, reached genus, canonical and labelled equalities, and
elapsed time. No float geometric diagnostic enters its verdict.

**Evidence and decision.** Preserve every supplied input hash, source hash, plan
hash, commit, environment, limits, elapsed time, stop reason and output hash using
the existing manifest pattern. Use a fresh `results/surgery-audit` directory and
exercise the bounded stage through the actual `run.sh 0` entry point with its
explicit stage selection. Record the exact command once implemented. Compare saved
steps with a separate direct permutation/edge-incidence check rather than relying
only on the surgery routine's acceptance. These checks have no external human
review. Claims remain PROVED-1 until the SPEC requirements for promotion are met.
If any control fails, repair only through a documented committed amendment before
rerunning affected scope. If controls pass, register R1 and both (8,3) geometric
recovery budgets and seeds next. Focus geometry remains gated on their success.

### 2026-11-04. Bounded geometric recovery pilot

Commit this amendment before implementing or executing the pilot. The surgery gate
and its saved checker evidence are reused unchanged. This stage registers controls
only. T + D remains 3 because a successful recovery would establish that the
replacement representation can feed the geometric engine at genus three.

**Question and prediction.** Can the dart-preserving ladder recover R1 Szilassi and
both supplied (8,3) controls from their saved sphere endpoints? H1 predicts all three
recoveries within this pilot. H0 is failure to recover at least one under these
limits. The prediction is uncalibrated. A failure with passing deterministic
controls is UNDERPOWERED at this budget, with the failed level identified. It does
not refute the engine or move H-261101-07, H-261103-02 or the A/B/C credences. A pass
permits preparation of a focus amendment. Any night still requires its own committed
plan and an uncertain, decision-linked prediction under PROTOCOL section 2.

**Frozen inputs and representation.** Read only the `szilassi`, `roest_vigh` and
`mizhaev` rows of `results/surgery-audit/audit.json.gz`. Bind the decompressed input
hash to its original manifest and bind these rows to the named source maps. Reuse
the recorded successful saved-chain check when its code and inputs are unchanged.
Do not rerun the surgery search. Reverse the saved level order to genus zero first.
For each level, export neighbour cycles by walking the saved dart permutations,
retaining the original face labels, repeated neighbours and cycle orientation.
Reconstruct with `census.from_links`, compare canonical codes, and require a
label-preserving isomorphism that maps oriented triangle cycles and alpha pairs.
Record that isomorphism and check it directly. Numeric dart IDs may change during
reconstruction. Any ambiguous parallel-edge pairing, changed label or edge copy,
or failed round trip is REPRESENTATION-FAIL before energy evaluation. Do not use
`coherent_triangles` to reconstruct the multi-adjacency levels.

**Surface checks.** Reuse the validated direct surface conditions at every level,
including connected vertex links, the intended genus and unchanged label set. At
genus zero require a simple sphere triangulation. Require complete adjacency only
on the three top maps. Lower levels use `require_all_pairs=False` for exact
geometric verification. Record expected V, E, F and chi from each saved map and
compare them with each exact geometric report.

**Deterministic geometric controls.** Before optimization, feed the published
Roest-Vigh planes from `control_rost_vigh.build`, the supplied Mizhaev planes from
`literature/mizhaev2026-planes.json`, and the Szilassi planes from
`experiments/E-261101-25-chirotope-first/szilassi_control.json` through the same
export and verification path. Derive and check an explicit labelled map isomorphism
for any plane-label permutation. All three must be EMBEDDED with complete adjacency
and their expected topology. Check Szilassi with `--target S5`, and the two (8,3)
objects with `--all-pairs`. The latter are auxiliary controls under SPEC S1.
They do not satisfy the maximal S5 face count at genus three. Duplicate one plane
in each fixture to produce a degenerate negative input. It must receive a recorded
rejection before entering optimization. A controlled rejection of singular input
may be an explicit invalid-input outcome. An unhandled exception is ERROR.
A failed positive or unexpectedly accepted negative control stops the pilot.

**Search contract.** Reuse `genus_ladder.search`, with its half-annealing,
half-CMA-ES allocation and honest `pair_energy`. Set `EXTRA=None` explicitly and
retain the default `DEPTH_W=0.01`. No new penalty or degeneracy floor is introduced.
Use one serial unit for each control, ordered Szilassi, Roest-Vigh and Mizhaev. Seeds are respectively 10401, 10402 and 10403, using
NumPy `default_rng(100 * seed + genus)` independently at each level. Start the
sphere from random planes. Seed each higher level only with the preceding exactly
accepted plane set under the unchanged labels. The published top planes serve
only the deterministic controls. They never seed the recovery search.

At every visited level, save and exactly check the best returned planes regardless
of the energy value, including when the optimizer stopped below its 0.5 threshold.
Use `ladder_exact.verify` and the saved-file `verify_candidate.py` entry point.
Only an exact PASS and the expected topology allow ascent. For the Szilassi top
use `--target S5`. For both (8,3) tops use `--all-pairs`. For intermediate levels
use the default embedded target. Stop that unit at its first unaccepted level,
then process the next control, unless an infrastructure/control error stopped the
whole pilot. A float zero remains a CANDIDATE until exact acceptance. Apply the
`candidate-check` skill to any accepted recovery before reporting it as a result.
Preserve rejected outputs and exact reports. An exact verifier exception is ERROR,
with its traceback retained, and cannot count as a search failure.

**Budget, limits and startup.** One shard, one core, one seed per control, 45 seconds
of optimization per visited level. The maximum ten levels consume at most 450
seconds of requested optimizer time. Enforce a 600-second outer wall cap including
imports, JIT warm-up, controls, verification and manifest finalization. Reserve
finalization time within that cap, checkpoint each completed level, and record
partial progress on timeout. Run the pilot through an explicit `STAGE=recovery`
selection of the existing `run.sh 0`, with a fresh default output directory
`results/recovery-pilot`. Preserve the default legacy and surgery dispatches.
The command is a planned interface until implementation and bounded startup have
been checked. No owner launch is pending at registration.

Record optimization wall time separately from JIT, controls and exact checks.
For each level record requested/actual time, budget fraction, restart count and
binding stop reason, including early energy threshold, requested time, outer cap,
exact rejection or error. A wall cap is TIMEOUT with remaining scope unresolved.
A short readiness pilot uses one fixed budget. The original 3/10-minute per-level
grid remains reserved for a separately registered calibration expansion, with
explicit seeds and total costs, if this pilot leaves a decision worth testing.
Do not silently extend this pilot or activate that grid.

**Counters, power and decisions.** Verdicts use only exact EMBEDDED,
`nonsimple_faces`, `bad_pairs`, `adjacent_pairs`, topology, round-trip equality and
accepted levels. `pair_energy`, elapsed time and restart counts describe the
optimizer. The 0.5 threshold stops optimization early in the reused engine,
and never certifies acceptance. Evaluate and retain the objective on the positive
and degenerate negative fixtures to expose diagnostic errors. Degenerate inputs
may yield a nonfinite value or a controlled exception. Neither is evidence for a
geometric claim. No verdict depends on a floating diagnostic threshold, and no
new float acceptance threshold is calibrated by this pilot.

RECOVERY-PASS requires every level of all three controls to pass exactly.
Partial recovery reports its exact accepted levels and the remaining unprocessed
or rejected scope. A completed unsuccessful search is UNDERPOWERED at this budget.
CONTROL-FAIL, REPRESENTATION-FAIL and ERROR stop implementation readiness and
require a documented, committed correction before repeating affected scope.
TIMEOUT does not measure nonexistence. Even a pass estimates no reliable recovery
probability from one seed. These limits can detect representation/dispatch errors
and rapid recoveries. They cannot justify LOW-YIELD or select a production budget.
A pass leads to a new focus/calibration plan, and an underpowered pilot leads to a
costed expansion proposal or a different approach. Neither launches a focus run.

**Provenance and evidence.** Keep the existing manifest fields, all supplied input,
plan and source hashes, the implementation commit, dependency versions, seeds,
limits, stop reasons and every output hash. Preserve stdout/stderr and saved exact
verifier transcripts, including negative controls. Refuse to overwrite an attempt.
Implement only the experiment-local recovery path, reusing the shared optimizer
and exact verifiers. Before behavioral changes use the recorded structural checks
for unchanged surgery code and register the smallest affected recovery checks.
Record the actual bounded entry-point command and outcome in CONCLUSION. Saved
recoveries remain PROVED-1 supplied-input computations until the requirements for
another SPEC evidence level are met. No FD/witness row or existence claim changes
merely because known control geometry is recovered.

### 2026-11-04. Reflected reference alignment correction

The first recovery attempt at implementation `5643bc5` stopped before geometric
verification or optimization with REPRESENTATION-FAIL while aligning the Szilassi
top to its reference. Retain `results/recovery-pilot` unchanged. Its exported
Szilassi levels passed the labelled round trips. The rooted isomorphism lookup
compared tails even when its target triangle traversal was reversed. For that
traversal a dart's tail is the original head, so the proposed label mapping split
vertices and rejected the reflected reference.

Correct the alignment lookup to use the head as tail for reflected traversals,
and check both endpoints, triangle successor/predecessor and alpha explicitly.
Add a reflected-map fixture using reversed triangle cycles and swapped endpoints;
it must admit a directly checked isomorphism before reference alignment. This
changes only reference alignment. Label-preserving round trips still require the
original orientation and identity on labels. Commit this correction before the
next affected check. Repeat the bounded entry point with
`OUT=.../results/recovery-pilot-oriented`, retaining the same controls, seeds,
per-level budgets and outer cap. No search seed or attempted optimization is
repeated because the first attempt stopped before geometry. Both attempts enter
the resource total. No focus run or calibration expansion is activated.

### 2026-11-04. Conditional failed-level calibration grid

**Decision and scope.** Select the costed grid proposed in CONCLUSION, rather than
repeat the full pilot. T + D remains 3 (T=1, D=2): this tests whether either saved
bottleneck can be crossed at the original short/night budget choices. Unlike the
completed pilot, no sphere search or ascent is repeated. This amendment registers
the implementation and bounded startup only; the owner must authorize the full
grid under the standing long-run rule before launch. Commit before implementation.
No focus geometry, night or alternative-chain search is authorized.

**Frozen units and paired seeds.** Use only the saved Roest-Vigh genus-one and
Mizhaev genus-two maps exported by `results/recovery-pilot-oriented/recovery.json`.
Start each cell independently from `roest_vigh-g0.json` or `mizhaev-g1.json` in that
attempt, respectively. Check the input bytes against the original manifest; match
the parent's labelled links and saved exact PASS to its current exported level.
Reuse the source-bound two-scale independent acceptance and successful transcript
for these unchanged parents. A mismatch is ERROR, never a reason to regenerate a
parent. Do not initialize from rejected planes or any other grid cell.

Use RNG seeds 1040201 and 1040302, respectively, unchanged from the failed levels,
paired across 180- and 600-second cells. Order cells by budget, then Roest-Vigh,
Mizhaev. Keep one worker and the existing thread limits. Use the unchanged
`genus_ladder.search`, EXTRA=None, DEPTH_W=0.01 and its half-annealing/half-CMA-ES
allocation. Equal seeds pair initialization, not identical trajectories: wall-time
phase boundaries depend on hardware and budget. Results need not be monotone.

**H1/H0 and decisions.** H1 predicts that at least one failed level passes exact
checking within this grid; H0 is no accepted cell under these limits. This is an
uncalibrated prediction, not a justified 30-70 percent success estimate. A pass
establishes conditional level recovery only (PROVED-1 supplied-input computation)
and selects the cheapest observed passing budget for a separately registered
full-control continuation. A pass at 600 but not 180 seconds supports retaining
both budgets in that continuation, not an estimated speed threshold. If no cell
passes, retain UNDERPOWERED and reassess intermediate-map realizability or chain
selection before proposing further geometry. Do not simply increase the cap.
All cells run even after a conditional success; no ascent follows a cell.
No outcome opens the full eight-face gate or changes any existence hypothesis,
FD/witness row or scenario credence. Scenario move: none.

**Controls and acceptance.** Reuse the existing deterministic positive and
duplicate-plane negative controls and labelled round trips through the actual
recovery worker before any grid cell. Stop on CONTROL-FAIL, REPRESENTATION-FAIL
or ERROR. These controls test infrastructure; they do not establish search power
at the intermediate maps. Save and exactly check every cell's best planes,
regardless of its objective, using the same in-process and saved-file verifiers
and expected topology. Require only the embedded target at these auxiliary levels.
Retain rejected candidates and transcripts. Accepted cells require candidate-check
before a result claim. Counters: exact EMBEDDED, nonsimple_faces, bad_pairs,
adjacent_pairs, topology and accepted levels. Counter calibration: unchanged
objective controls; no verdict uses a floating threshold. Time, objective and
restarts remain diagnostics. TIMEOUT and exact rejection do not decide map
realizability; no LOW-YIELD or nonexistence interpretation is available.

**Budget and provenance.** Four cells request at most 1560 optimizer seconds
(26 minutes) on one core. The outer wall limit is 1800 seconds including at most
237 seconds for startup, deterministic controls, saved-input checks and exact
verification, and three seconds reserved for termination/finalization. Record
requested/actual cell seconds, budget fraction, restarts, optimizer stop reason,
exact outcome, all source/input/output hashes and dependency versions. Checkpoint
before and after every cell; retain partial output on timeout. Fresh default OUT
is `results/recovery-grid`; never overwrite an attempt. Preserve all older modes.
The outer cap bounds the attempt; it does not guarantee that every cell runs.

**Bounded startup and affected checks.** Add `STAGE=calibration` to the existing
`run.sh 0` and a `STARTUP_ONLY=1` switch valid only for that stage. Startup uses the
same dispatch, controls, exports, parent validation and worker, with a 120-second
outer cap and no optimization. It records four planned cells and returns
STARTUP-PASS, with conditional/full recovery flags false. Exercise this once in
`results/recovery-grid-startup` after implementation; it cannot count as a grid
outcome. Check Python/shell syntax, cell budget/seed/parent identity and rejection
of unsupported stage/startup combinations. Reuse the recorded shared-code suite
and saved surgery acceptance: no shared algorithm is changed. No owner launch
command is ready until this startup passes. The full grid then awaits explicit
owner authorization, even though its plan is committed.

### 2026-11-04. Bounded intermediate-map feasibility audit

**Decision and registration.** Follow the completed grid's no-success branch:
test the two frozen intermediate maps with the existing exact submap encoding
before considering any further geometry. T + D remains 3 (T=1, D=2). A checked
formula obstruction changes which chain can be pursued; SAT leaves geometry
open and requires a separate realization proposal; timeout identifies an
unresolved exact question without earning a larger cap. This is a bounded audit,
not a new recovery grid, chain search or focus night. Commit this amendment
before formula construction, solving or proof checking. Preserve all previous
attempts, especially `results/recovery-grid`, unchanged.

**Frozen inputs.** All four JSON files below are in
`results/recovery-pilot-oriented/`. Use their labelled `links` without relabelling
or changing cyclic order or parallel-edge pairing. Bind them to the same labelled
exports and checked surgery chain in `recovery.json`; canonical equivalence alone
does not preserve the association with supplied planes.

| Role | File | SHA-256 of file bytes |
|---|---|---|
| Unpinned target, Roest-Vigh genus one | `roest_vigh-g1.json` | `c26ff6f254c9ff8fab5b58949be71dcdbba76e45de9ea095de084a444b49832b` |
| Unpinned target, Mizhaev genus two | `mizhaev-g2.json` | `45d961c197548c94f074400f491dd2b13cd8e604add133d80ada5875d30c1980` |
| Pinned positive, Roest-Vigh genus zero | `roest_vigh-g0.json` | `75607a1793514a6edc9572ccd02e404e37ed336658a80663c54695df8a83967f` |
| Pinned positive, Mizhaev genus one | `mizhaev-g1.json` | `c1446ff315c9369b9d8f541f30afb0481d1008f09d140137e9aa67c11a5d3f7a` |

The exports file `recovery.json` has SHA-256
`57bf8ce5247aef6cb515f7265375a145d2b9cce554c9d522d013ff3a86e119cd`.
Reuse the parents' saved exact acceptance and independent two-scale acceptance:
`results/recovery-review/report.json`, SHA-256
`96123d22ee993888d42a6fc29a4619c064987f4621e8c218e9808bccc9e5e573`,
and successful `check-saved.txt.gz`, SHA-256
`52c5a7a6b9d52a1a52af86e858967004526678c2b08a978259fdaeee8da9d65c`.
A hash, labelled-link or pairing mismatch is ERROR; do not regenerate an input.

**Formula and target scope.** Construct each map with
`Triangulation(n, triangles, links=labelled_links, submap=True)`. Derive corner
triples from the supplied cyclic links and check preservation of the labelled
segment pairings. Do not use the default-full-map `test_encoder.from_links`
helper. Build the plain uniform rank-4 oriented-matroid relaxation on eight face
elements and infinity with `build(..., ALL_OPTS)`, recording the actual options
and clause-family counts. Use no symmetry, symmetry breaking or mirror clauses.
Absent pairs have `E=False` and no prescribed segments; retain all non-corner
TRIPLE and parallel SEGMENT_DISJOINT constraints. For an absent pair the compact
intersection on the two planes' line has no permitted boundary endpoints, so an
embedded realization must have empty intersection. The encoding soundness and
uniform-perturbation interpretation remain PROVED-1, with the existing argument
in `../E-261103-02-s5-omsat-multi-adjacency-encoder/SOUNDNESS.md`.

These are auxiliary eight-face maps in preparation for S5 (9,3), not S5 targets.
The free target formulas fix neither supplied planes nor a parent chirotope.
Target order is Roest-Vigh genus one, then Mizhaev genus two. No other maps,
chains, seeds, symmetry families, realization or optimization are in scope.

**H1/H0 and controls.** H1 predicts that both unpinned target formulas are SAT;
H0 is at least one verified UNSAT formula. Unresolved units distinguish neither.
This is a falsifiable audit prediction, not a calibrated probability estimate.
Before any free target decision, require the following controls through the same
submap construction, clause options, solver and saved-evidence path:

* For each accepted parent, rationalize every plane coefficient to an integer
  row using `int(round(1e9 * coefficient))`. Save these integer rows and use
  exactly those rows both for `chirotope_from_planes` and `compare_direct`.
  Passing the original float rows to `Geometry` would truncate them with
  `int(x)` and is invalid. Require uniformity, no Eval violations, agreement of
  all named predicates with direct geometry, and SAT of the chi-pinned CNF.
  Save the model and check that it satisfies every clause of the stored DIMACS
  and every pinned chirotope sign. Roest-Vigh g0 exercises absent pairs;
  Mizhaev g1 exercises absent pairs and parallel segments together.
* Use the frozen rejected `roest_vigh-g1.json` as a meaningful negative
  fixed-chirotope fixture, rationalized by the identical integer-row rule.
  Require uniformity, its saved exact rejection, agreement with direct
  geometry and nonzero Eval violations before solving. Its chi-pinned formula
  must be UNSAT with retained CNF and proof accepted by an independent proof
  checker. For a unit-refutable formula, retain an empty-clause RUP certificate
  and independently replay unit propagation on the stored DIMACS. Otherwise
  retain DRAT and its independent checker transcript. A missing or unchecked
  proof is not control success. Do not replace a failed fixture with an
  artificial contradiction or a duplicate-plane degeneracy.

Any control timeout, mismatch, nonuniformity, unexpected solver answer or failed
certificate check stops the stage before free targets. The old complete-map
cross-fixture in E-261103-02 is reusable background evidence, not a substitute
for these submap controls. There is no floating diagnostic threshold in a
verdict; objective values and elapsed time are diagnostics only.

**Budget and stopping.** One shard, one worker, existing single-thread limits,
180 seconds outer wall time (at most 0.05 core-hours), with three seconds reserved
for termination/finalization. All worker operations share a monotonic deadline
at 177 seconds, including imports, formula construction, input/control checks,
model checking and metadata. Each positive-control solver call has at most
10 seconds. The negative-control solver has at most 10 seconds and its proof
check at most 10 seconds. Each free-target solver has at most 45 seconds and
its proof check at most 15 seconds. Clip every subordinate limit to the common
remaining time; these maxima do not guarantee all units complete. Do not raise
any limit or transfer unused time by increasing another unit's cap. The parent
watchdog terminates the entire worker process group at the deadline and finalizes
the manifest within the outer cap. Checkpoint before and after each unit and
retain partial CNF/proof/model/log output on interruption. Record requested/actual
unit time, solver/checker time, budget fraction and binding stop reason
(completed, solver timeout, checker timeout, outer cap, control failure or error).
Run both targets after successful controls even if the first returns SAT,
verified UNSAT or timeout; stop immediately on ERROR or outer cap.

**Evidence and decisions.** Save fresh immutable evidence in
`results/submap-feasibility-audit`; refuse to overwrite an attempt. Record
generating commit/dirty state, dependencies, source and input hashes, integer
rows, maps, clause options/counts, CNF hashes, solver answers, models/proofs,
independent checks and full stdout/stderr. SAT requires exact satisfaction of
the saved CNF by the saved model. UNSAT-VERIFIED requires a retained formula,
certificate and successful independent proof check; a bare solver UNSAT is
UNVERIFIED, not a negative result.

* SAT yields only an abstract oriented-matroid candidate. It neither establishes
  geometric realizability nor explains recovery failure. Both SAT outcomes
  permit preparation of a separately registered realization question only.
* UNSAT-VERIFIED excludes that exact formula. Conditional on the PROVED-1
  encoding and uniform-perturbation argument, reassess the affected intermediate
  map or chain before proposing geometry. Do not generalize to another chain,
  the published control, a focus census or an existence theorem.
* UNKNOWN/timeout/UNVERIFIED leave feasibility open. ERROR invalidates the
  affected computation; control failure invalidates the target stage. Neither
  justifies increasing the cap or repeating geometry by default.

No outcome opens the full-eight-face recovery gate, authorizes a night, changes
an existence hypothesis or scenario credence, or supplies an S5 result. Evidence
claims remain PROVED-1 unless an applicable stronger SPEC evidence chain is
actually completed. This audit contains no realizability extension.

**Affected verification.** After implementation, exercise this bounded actual
entry point once, with controls before target decisions. Review Python/shell
syntax, hashes, labelled map identities, deadline handling and saved evidence.
Reuse unchanged surgery/parent acceptance and the recorded shared-code quick
suite; do not rerun previous recovery attempts or an integrated suite merely
to refresh this report. Any later amendment requires registration before its
new computation.

### 2026-11-04. Alternative first-step Mizhaev chains

**Question and decision.** The frozen Mizhaev genus-two intermediate formula is
UNSAT-VERIFIED in `results/submap-feasibility-audit`; its published genus-three
top is embedded. Reassess the first removal rather than increasing any recovery
budget. T=1, D=2: a different SAT intermediate changes which chain deserves a
descendant audit; exhausting the exact finite removal scope with checked UNSATs
would reject this particular removal route. This stage authorizes no geometry,
descendant search, focus-map search or night. Commit this amendment before any
enumeration or formula construction.

**Frozen scope.** Restore the `mizhaev` row's labelled `levels[0]` from
`results/surgery-audit/audit.json.gz` (SHA-256
`7abf382cf134792b897cdeb9854ddfb75e1444b35b2e0772951534b12f1c2fcc`).
Keep its dart/face labels, published-top alignment and inverse surgery witnesses.
The existing `recovery.json` frozen above binds the old labelled exports to this
chain. The known rejected class is that row's `levels[1]`, whose labelled export
must equal the frozen `mizhaev-g2.json` links.

Enumerate the top's connected six-triangle subsets on at most six face labels
in existing `patches` order; valid patches require exactly six labels. The
complete scope is six-label annular removals accepted by `patch_caps` and the
checks below. Apply `patch_caps`, `remove_patch`, `check_surface`,
`check_step`, exact `reverse_step` equality and `recovery.export_level` without
relabelling the parent. Require a valid eight-vertex genus-two triangulation,
distinct corner triples and uniquely preserved parallel-edge pairing. The raw
subset bound is C(24,6)=134596; the number of valid distinct children is unknown.
Deduplicate by canonical map code, retaining one full labelled representative,
its removal step and inverse per class. If its code matches the old rejected
class, require an explicit checked map isomorphism before attaching the old
CNF/proof decision. Do not infer map identity from genus or adjacency counts.
Save class multiplicities and the number of valid patches separately.

The decision queue is the first eight OTHER canonical classes in first-encounter
order. Finish enumeration if possible even after eight classes are discovered;
save every discovered class but solve only this registered prefix. Record
`enumeration_complete` separately from `tested_prefix_complete`. A 20-second
enumeration cap can leave a deterministic discovery prefix, which is not a full
first-step census. A smaller complete queue does not justify filling a night.

**Controls and representation gates.** Reuse the just-passed positive/negative
submap controls and certificates from `results/submap-feasibility-audit`:
manifest SHA-256 `11c8599ce486b981d52810678035d843bbb5ba1502b0e5e0e8fb23f1a4f164af`,
summary SHA-256 `d647563830d257468da5f7b07c5786c6bdd29dff61f11b0929107fd28e624db4`.
Check their saved output hashes, successful statuses, relevant unchanged core
source/input hashes, Python/dependency/tool identities and thread limits. The
existing formula, model-checking and proof-checking path is unchanged; do not
rerun these controls merely to refresh them. A mismatch stops the stage for
review rather than silently rerunning controls. Reuse saved parent/surgery
acceptance and shared-code quick-suite baseline. Newly exercised representation
requires the per-child labelled export/inverse checks above and matching the
old genus-two export, not a fresh geometric recovery.

**Formula and limits.** Use the same plain `submap=True`, `ALL_OPTS` formula,
with no pinned planes, symmetry, symmetry breaking or mirror clauses. One shard,
one worker; outer cap 180 seconds, three seconds for termination/finalization,
all worker operations sharing the 177-second monotonic deadline. Enumeration
has at most 20 seconds; each selected class has at most 10 solver seconds and
five proof-checker seconds, clipped to the common remaining time. Keep every
CNF, model, proof and transcript; SAT requires exact satisfaction of saved
DIMACS, UNSAT-VERIFIED a successful independent proof check. An unresolved class
does not block later prefix classes; ERROR or outer cap stops the stage.

Checkpoint the discovered queue and witnesses after each distinct class and
each solver unit. A restart of the same output directory resumes unfinished
units without repeating recorded decisions or replacing their evidence. A
partially enumerated queue may be deterministically rebuilt under the same
20-second cap, checking equality of already saved discovery records. Record
each invocation separately, actual/maximum times, binding limits and cumulative
work. Restart is a recovery mechanism, not authorization to expand this pilot.
Use `STAGE=alternatives`, output `results/mizhaev-first-step-audit`; preserve all
earlier stages and outputs unchanged.

**Predictions and interpretation.** H1: at least one of the first eight other
classes is SAT; H0: every class in that prefix is UNSAT-VERIFIED. An empty prefix
tests neither; unresolved classes prevent H0, while any checked SAT establishes
H1. Alternative SAT permits only a separately
registered g1-descendant assessment. A complete enumeration with every class
decided UNSAT-VERIFIED rejects only this finite six-triangle first-removal scope
of this labelled top, conditional on the PROVED-1 encoding; a prefix verdict
never excludes the untested remainder. Timeout/UNVERIFIED leave feasibility
open. Only measured queue size and throughput can justify a later bounded
remaining-queue run; no automatic three-hour or overnight run. No outcome is a
geometric S5 result or a theorem about all chains.

**Verification.** Review the amendment before its registration commit. Before
execution, review the minimal stage implementation and Python/shell syntax.
After release, exercise this entry point once, checking queue order, class
identity, completeness flags, reused-control provenance and saved evidence.
Do not rerun the first submap audit, recovery grids or integrated suite.
