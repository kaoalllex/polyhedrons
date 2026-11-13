# E-261110-05: immersion-only and segment-free formulas on two (8, 2) and six (9, 3) maps

Pre-registration, 2026-11-13 (lab session, week item 3 of the owner-approved plan). No solver run before this commit.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (T + D = 4), explore. Origin I-261110-04.
* **Question**: which clause family refutes the plain formulas of the two (8, 2) maps and the six (9, 3) maps?
* **Hypotheses moved**: H-261110-01 (multiple-adjacency constraints carry the S5 negatives), by the readings below.
* **H1 / H0**: H1: V2 is SAT on some map whose plain formula is UNSAT-VERIFIED. H0: V2 is UNSAT on all eight.
* **Why**: every admissible (8, 2) and (9, 3) plain formula is UNSAT-VERIFIED (STATUS 3d); if the refutation needs
  the segment clauses, the S5 ladder says little about S0, which has no multiple adjacency (I-261110-04).
* **Method**: maps of the E-261103-01 census: (8, 2) #0, #1; (9, 3) #40, 43, 10, 30, 48, 5 (the E-261109-03 set).
  Encoder `code/omsat.build` with `ALL_OPTS` (the plain formula, `from_links`, not `submap`), two relaxations:
  * V1 immersion-only: `triples=False` (no TRIPLE and no SEGMENT_DISJOINT; INCONS, RFCONS, REFLEX1, POC kept);
  * V2: `no_segment_disjoint=True`, a new default-off option that skips only the SEGMENT_DISJOINT block (the block
    is emitted only under `triples`, `omsat.py` lines 561-568); default formulas unchanged (control c1).
  Solver: kissat rel-4.0.4, no proofs (`NO_PROOF=1`), cap 900 s per unit (12 x 900 s = 3 core-h at most for the run).
  Runner `units.py` through `run.sh`: controls, then the units of the shard. Counters (SPEC §4): SAT /
  UNSAT-SOLVER / TIMEOUT per (map, variant), solver seconds, clause-family counts.
* **Controls** (every shard, before any unit; a failure stops the shard): c1 the plain formula of each map rebuilds
  to its recorded CNF SHA-256 (E-261103-03 records); c2 the family counts: V2 = plain minus SEGMENT_DISJOINT only
  (plain has SEGMENT_DISJOINT > 0 on every target), V1 without TRIPLE and SEGMENT_DISJOINT, V2 byte-identical to plain
  on the single-adjacency convex f9 map; c3 positive: the pinned Roest-Vigh and Mizhaev chirotopes (E-261103-02)
  SAT under V1 and V2 (both relaxations of a formula they satisfy); c4 negative: the convex f9 planes pinned on its
  swapped map UNSAT-SOLVER under V2 (V1 recorded without expectation).
* **Stages**: (1) prep, in this session: the four (8, 2) units (V2 first, as the week plan asks), `CASE=8_2`, 2
  shards, recorded as results under `results/prep-8-2/`; they double as the pilot. (2) owner launch: the twelve
  (9, 3) units on 10 shards, queued after E-261113-02 (`launch.sh 13-02 10-05 start`).
* **Pilot gate**: controls pass and the (8, 2) units end. The run starts unchanged; if both (8, 2) V2 units time out,
  the (9, 3) run waits for the owner (a pilot at its cap can stop a run, STRATEGY).
* **Predictions**: (P1, ~50 %) V2 SAT on at least one (8, 2) map; (P2, ~60 %) V1 SAT on both (8, 2) maps;
  (P3, ~40 %) at least 10 of 12 (9, 3) units decided within 900 s.
* **Grid**: one setting; the relaxations are the variable. **Budget**: prep (seconds to minutes) + <= 3 core-h,
  10 shards, laptop, owner launch.
* **Power**: detects a SAT relaxed formula kissat finds within 900 s on these eight maps; a TIMEOUT says nothing; an
  UNSAT-SOLVER answer moves H-261110-01 only for planning, not as a claim; eight maps of 205 are not a census.
* **Proofs**: none. The README asked for DRAT on the (8, 2) units, but no outcome below is a negative claim for a
  note or a STATUS exclusion (owner rule 2026-11-13, `PROTOCOL.md` §5); a proof replay of a V1 UNSAT runs only if
  the core mining of the follow-up needs it as a claim, on the owner's word.
* **Calibration**: no float diagnostic enters any reading (statuses and exact hashes only). `summary.py --selftest`.
* **Scenario move**: none on the decision-point credences; H-261110-01 moves by the readings.
* **Outcomes**: SAT: about the relaxed formula only, never a geometric object; UNSAT-SOLVER: likely UNSAT, planning
  only; TIMEOUT: no information. Near-miss: not applicable.
* **Follow-up tree** (`summary.py` readings): V2 SAT on a map -> H-261110-01 supported, one theory paragraph; V1
  UNSAT-SOLVER on an (8, 2) map -> one session of core mining on the (8, 2) formulas; V1 SAT and V2 UNSAT-SOLVER on a
  map -> H-261110-01 weakened. A failed control stops the item (escalate).
* **Stop rule**: all 16 units recorded, a failed control, or the cap (900 s per unit, 3 core-h for the run).
* **STATUS / ROADMAP**: a STATUS 3 section with the 8 x 2 table and readings; H-261110-01 evidence line; ROADMAP to
  done.

## Amendments
