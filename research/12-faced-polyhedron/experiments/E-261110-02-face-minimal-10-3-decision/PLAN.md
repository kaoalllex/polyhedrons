# E-261110-02: (10, 3) face-minimal decision (single adjacencies, kissat with DRAT)

Pre-registration, 2026-11-10 (lead session; proposed week plan item 2). The night starts only after the owner
approves it and after amendment 1 (prep: input hashes, pilot outcome) is committed.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (T + D = 4), jump 2.
* **Question**: does the dual of any of the 20 vertex-minimal 10-vertex triangulations of the orientable genus-3
  surface have a SAT plain formula, and does a model realize?
* **Hypotheses moved**: H-261110-03 (realized SAT proves its (10, 3) part; 20 UNSAT-VERIFIED refutes it at formula
  scope), H-261110-01 (SAT here with none at (10, 4) supports it; 20 UNSAT weakens it).
* **H1 / H0**: H1: at least one of the 20 formulas is SAT. H0: all 20 are UNSAT.
* **Why**: the only ladder with S0's zero slack (I-261110-02); 20 maps fit one night; nothing on the face version in
  print (CLAIMED, web search 2026-11-10).
* **Method**: target = proposed S6 at (F, g) = (10, 3): V, E, F = 28, 42, 10, 42 adjacent pairs, all single, 3
  non-adjacent pairs. Maps: Lutz's list of the 20 triangulations, stored under `literature/` as untrusted data and
  parsed with `python3 -I`, never executed. `code/lutz_import.py` converts each to oriented triangles and dual
  `links` and checks: closed, orientable, simplicial, (V, E, F) = (10, 42, 28), pairwise non-isomorphic, count 20.
  Formula: E-261103-02 encoder through the E-261103-03 runner (`pilot.build`, `ALL_OPTS`, `from_links`) with
  `submap=True`, 11 elements. Solver: kissat rel-4.0.4 (the binary hash of E-261108-03) with DRAT; drat-trim checks
  each proof in the run, CNF and proof SHA-256 and the checker transcript are recorded, proofs are then deleted
  (`PROTOCOL.md` §5). Solver cap 3600 s per map; 10 shards, 2 maps each; no first-SAT stop (all 20 answers are
  wanted); every SAT model is checked against the clauses in the run.
  Counters (SPEC §4): SAT / UNSAT-VERIFIED / UNSAT-SOLVER / TIMEOUT per map, solver and checker seconds, CPU seconds.
* **Controls**: (a) converter, no solver: the 7-vertex torus gives the Szilassi map; the 59-type Lutz-format file
  gives the classes of `data/k12_triangulations.json`; (b) (7, 1) through the same path with `submap=True`: SAT,
  pinned on Szilassi's planes and unpinned; (c) every shard, first in its queue: the pinned convex 10-face positive
  (SAT, model checked) and its swapped-map negative (UNSAT-VERIFIED), as in E-261109-06, with `submap=True`;
  (d) a pinned genus-3 S3 witness of STATUS §2 (non-adjacent pairs present) through `submap=True`: SAT.
* **Pilot** (prep, scratch results): controls, then two of the 20 maps at a 1200 s cap. It reports per unit the limit
  that ended it and, for any UNSAT, the peak memory and time of the DRAT check.
* **Pilot gate**: binding limit = the 3600 s solver cap. The night starts if every control passes. If a pilot proof
  does not fit memory, the night runs only with the owner's word, and such maps are UNSAT-SOLVER (no negative claim).
* **Predictions**: (P1, ~50 %) all 20 decided within the cap; (P2, ~25 %) at least one SAT; (P3, ~60 %) the median
  decided time is below 10 minutes; (P4, ~70 %) every UNSAT proof is checked within 48 GB.
* **Grid**: one setting; solver and cap come from E-261108-03 and E-261109-06.
* **Budget**: 1 prep session; one owner night, 10 shards, <= 80 core-h, <= 10 h wall (`launch.sh` entry point of the
  prep; 20 solver-hours at the cap plus proof checking).
* **Power statement**: detects a SAT formula that kissat finds within 3600 s. A TIMEOUT says nothing. An UNSAT holds
  for its formula; the geometric reading needs census coverage (CLAIMED from Lutz's list until re-enumerated here),
  encoder soundness with `submap=True` (PROVED-1) and general position, and covers cubic polyhedra only.
* **Counter calibration** (`summary.py --selftest`): 5 of 20 timeouts escalates, 4 does not; median 599 s proposes
  (11, 4), 601 s does not; no float diagnostic enters the verdict.
* **Scenario move** ("(10, 3) exists" 0.25, CONJECTURE): realized SAT -> 1; 20 UNSAT-VERIFIED -> 0.03; SAT models
  that do not realize in one session -> 0.25 stays, C-type evidence recorded; timeouts -> no move. S0 table: no move.
* **Outcomes**:
  * SAT: a CANDIDATE only; follow-up tree. An OM model alone is not a result.
  * UNSAT-VERIFIED on all 20: "no cubic single-adjacency polyhedron with 10 faces and genus 3" at formula scope,
    geometric reading PROVED-1 and conditional as above; not CERTIFIED, not reviewed.
  * UNSAT-SOLVER: not a negative result; listed for a replay.
  * TIMEOUT: no information. Near-miss: not applicable.
* **Follow-up tree**: any SAT -> exact model check, realization with the saved-OM tools of E-261103-04, then
  `verify_candidate.py` (EMBEDDED, 10 faces, genus 3, 42 adjacent pairs, all single; `--target S6` once the owner
  approves the SPEC entry), `candidate-check`, escalate; not realized in one session -> final polynomials
  (I-261029-45), escalate. 20 UNSAT-VERIFIED -> H-261110-03 weakened at genus 3; (11, 4) is proposed only if the
  median is below 10 minutes. Timeouts on > 20 % of the maps -> record, escalate.
* **Stop rule**: all 20 maps recorded, a control failure (stop that shard, escalate), or the 80 core-h cap.
* **STATUS / ROADMAP**: a new STATUS 3 section with the per-map table and the verdict; the ROADMAP row to done; the
  proposed credence table; a SAT goes through `candidate-check` before any wording.

## Amendments
