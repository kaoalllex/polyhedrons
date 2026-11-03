# E-261103-01: Exhaustive S5 map census

Pre-registration. Commit this plan before enumeration; append dated amendments after runs.

* **ROADMAP scores:** T 2 D 2 F 2 G 2 R 2; the first open row.
* **Question:** Are the sampled S5 candidate-map lists complete up to isomorphism and mirror?
* **Hypotheses:** H-261103-01 (sample completeness); H-261101-07 (candidate combinatorics only,
  no geometric existence inference). H1: the census agrees with the sampled list; H0: additional classes exist.
* **Region:** S5 dual maps at (7,1), (8,2), (9,3), (10,4); S0 (12,6) is a control only.
* **Method:** Enumerate the underlying multigraphs K_F plus k extra edges, up to vertex relabelling.
  For each graph, enumerate root-vertex rotations, then complete triangular rotation systems by the
  existing `enum_k12.c` triangle-assignment/MRV method generalized to identified darts. Reject premature
  vertex cycles; canonicalize completed maps by rooted dart BFS in both orientations. No admissibility
  pruning: repeated corner triples must be retained and flagged. Export full dart data as well as `links`;
  `links` alone can lose edge-pairing information on inadmissible maps. Reuse the review sampler's
  `TriMap`, `check`, canonical codes, invariants and automorphism reports as a second check.
* **Coverage argument (PROVED-1 until reviewed):** Every loopless complete underlying multigraph is
  K_F plus k edges. Unlabelled extra-edge augmentation covers these graphs inductively. A vertex of
  maximum extra degree can be labelled 0. Its incident darts can be cyclically anchored at a dart to
  vertex 1; permutations of isolated extra-graph vertices and parallel-edge identities remove only
  redundant labels. Enumerate every remaining root rotation. Every unfilled directed dart belongs
  to a triangle; branching over both other darts includes that triangle. A partial vertex cycle shorter
  than its valence cannot extend to a one-cycle rotation. Completed connected rotation systems therefore
  cover the requested family; rooted BFS removes only combinatorial duplicates.
* **Counters:** Exact combinatorial nodes, leaves, classes, admissible classes, automorphism orders,
  and completion flags. SPEC section 4 geometric counters are not applicable: no planes are constructed.
  No float diagnostic enters a mathematical verdict; elapsed time is scheduling information only.
* **Controls:** (7,1): one chiral class with |Aut+|=42; (12,6): 59 classes and matching FD3
  automorphism orders if its bounded control finishes, otherwise explicitly unrun/incomplete.
  Every sampled class must be contained in a finished census. If (8,3) is attempted and finishes,
  both published maps must be contained. Negative controls: corrupt alpha, disconnected vertex links,
  wrong Euler characteristic, and a repeated corner triple rejected as admissible.
  Relabelling and mirroring must preserve the canonical class. Independently cross-check the C3
  sub-list by voltage lifts before treating that part as fully validated; defer explicitly if not implemented.
* **Pilot:** Unit tests first, then a bounded complete (7,1) run and at most 60 seconds each for
  (8,2) and (9,3). Record nodes, completed graph/root cases, wall time, binding limit and used budget.
* **Pilot gate:** Positive/negative controls must pass. A timeout must be reported as partial. A longer
  run requires a useful completion projection, a time limit as the intended binding limit and owner approval.
* **Predictions / decisions:** (7,1) should finish in seconds; failure blocks the pipeline.
  (8,2) should finish within the pilot; if not, improve pruning before a long run.
  Whether (9,3) completes within 60 seconds is uncertain; completion enables comparisons, failure
  triggers a written runtime projection rather than an unchanged hours-long launch.
* **Grid:** 10/60-second caps if an instance times out; exhaustive output is independent of the cap.
* **Budget:** Two implementation sessions; interactive pilots at most five minutes per command,
  one core. No multi-hour launch or subagents. Owner approval required for any longer computation.
* **Power:** Exhaustion decides the combinatorial census. Partial output is a lower bound only;
  neither exhaustion nor failure to finish decides geometric realizability.
* **Counter calibration:** Integer invariants checked against the controls above; no float thresholds.
* **Scenario move:** No change to A (exists), B (all OM-UNSAT), C (OM-SAT/non-realizable) from
  combinatorics alone. Additional maps enlarge the inputs of E-261103-03; disagreement blocks geometry.
* **Outcomes:** Found maps are combinatorial objects, not geometric candidates. Exhausted empty
  family excludes that combinatorial family only. SAT/UNSAT and near-miss do not apply to this enumerator.
  Timeout/UNKNOWN means no completeness conclusion; preserve partial classes and progress counters.
* **Stop rule:** All four cases and controls, or a documented reason why a case does not finish.
  Do not mark the experiment done merely because a session ends.
* **Ledger:** Set ROADMAP/README running at pre-registration. Update STATUS counts only after
  validated completed cases, with SPEC labels and coverage caveats. Record partial work in the handover.

## Implementation checklist

- [x] Add focused failing tests for a one-class control, parallel darts, mirror invariance, and timeouts.
- [x] Add a bounded C enumerator beside the experiment and a Python driver reusing review checks.
- [x] Run focused tests, then the registered pilots; save manifests and input/output hashes.
- [x] Compare finished cases with sampled maps, record limitations and prepare the next command.
- [x] Re-run `verify_all.py --quick` and `trace.py`; leave unrelated files unchanged.

Scope: this folder and its README, ROADMAP state, generated research graph, and session handover.
Existing `enum_k12.c`, geometric encoders, witnesses and the public viewer remain unchanged.

## Amendments

* 2026-11-03: Baseline `verification/verify_all.py --quick`: ALL PASS; archive check skipped by
  quick mode. Base a037d4e (merged strategy review); local branch `experiment/E-261103-01-s5-map-census`.
  Work in the existing checkout per owner instructions. No additional dependencies or subagents.
* 2026-11-03, after the first pilot: (7,1), (8,2) and (9,3) exhaust their graph families
  within the registered caps; focused controls pass. Attempt (10,4) with a 60-second enumeration
  cap, on one core, to measure its runtime frontier. If incomplete, retain its partial list and
  do not infer a total count or launch an unchanged longer run. Run the (12,6) control with
  the same 60-second cap. No geometry or long computation is authorized by this amendment.
* 2026-11-03, symmetry cross-check: use a separate triangle-orbit exact cover rather than
  a second dart-rotation search. Fix rho=(012)(345)(678), enumerate invariant admissible triangle
  sets and every rho-equivariant pairing of parallel edges. This enumerates Z3 lifts implicitly:
  there are three quotient vertices, thirteen quotient edges, eight triangle orbits and two fixed
  triangles (branch points). A free C3 action on an admissible nine-vertex map has at most three
  invariant unordered triples; Riemann-Hurwitz gives r=5-3h, hence exactly r=2 and quotient genus h=1.
  This coverage argument is PROVED-1. Compare canonical codes, not just the number of maps.
  Budget: 60 seconds, one core; timeout leaves this control incomplete and the experiment running.
* 2026-11-03, conclusion: all four cases and the K12 control exhausted; code-set and automorphism
  comparisons pass. The C3 control used the amended exact-cover method, not an explicit voltage-table
  generator. The optional (8,3) census was not attempted. No subagents or long jobs were used.
  Final tests also cover refusal to overwrite an occupied output directory. ASan/UBSan completed
  the (9,3) enumeration with the same class count and no diagnostics. See CONCLUSION.md for all counts.
