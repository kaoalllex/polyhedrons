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
