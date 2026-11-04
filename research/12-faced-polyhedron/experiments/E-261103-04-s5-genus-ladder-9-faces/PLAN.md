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
