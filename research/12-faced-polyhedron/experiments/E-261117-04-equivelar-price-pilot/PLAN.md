# E-261117-04: P6 stage A, the equivelar (8, 3) rung and the enrichment control

Pre-registration (2026-11-22), at most 80 lines; stages B and C (week items 3, 4) come as amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2 (T + D = 4); week item 1, explore, J 0 (lead review 2026-11-22 §3).
* **Question**: does the plain per-map formula pipeline recover both known eight-face solids unaided from the complete
  equivelar (8, 3) census, and do SAT maps cluster in the equivelar slice or also appear among non-equivelar maps?
* **Hypotheses moved**: H-261101-07. Only the known maps SAT and realized: the rung passes, P6 proceeds (item 3).
  A non-equivelar map realized: P6's premise "realizable means equivelar" fails at (8, 3). A new equivelar object: a
  third eight-face S1 object (owner decision O4). **H1**: SAT maps lie only in the equivelar slice. **H0**: some of
  the 745 non-equivelar maps are SAT (formula scope) or realized.
* **Why**: both known (8, 3) solids are equivelar (Roest-Vigh 4+4, Mizhaev 8, not face-transitive: 3au); equivelar
  (E = F (F + 1) / 2) fixes the extra-edge multigraph to 2-regular, a small slice (expected 97 classes, 51 admissible).
* **Coverage (PROVED-1)**: at (8, 3) E = 36 = 28 + 8, so every face is a 9-gon iff each face has 2 extra edge-ends,
  i.e. the extra-edge multigraph (multiplicity - 1 per face pair, loopless) is 2-regular on 8 vertices: a disjoint
  union of cycles covering all vertices, a 2-cycle being one pair of multiplicity 3. Isomorphism types = partitions
  of 8 into parts >= 2 (seven). `enum_multi.c` is exhaustive for one labelled input (E-261103-01, PROVED-1) and the
  face labels are interchangeable, so one cycle-union input per partition (`p6.cycle_union`) covers every equivelar
  map; canonical codes (up to reflection) merge duplicates. Not `extra_graphs`, not symcensus with the trivial group.
* **Method**: `p6.py census` (`census.run` with explicit inputs; the only census change is that optional argument,
  `test_census` 9 OK), `p6.py build` (records, queue, pinned control, census controls), `run.sh SHARD` (10 shards;
  E-261119-02 `run_b.sh`: E-261103-03 runner, imported-map mode, kissat 4.0.4 seed 0, `NO_PROOF=1`, lean UNSATs).
  Formula: `tranche.submap_formula` without a generator, 9 elements (8 planes + infinity), on the 51 admissible census
  classes and the 745 non-equivelar maps of the 790 free-C2 (8, 3) list (E-261119-02 stage A; the 45 equivelar ones
  are census classes): 796 units, cap 60 s. One orientation per class (the code's): a realization of the mirror map
  is the reflection of one of the map, and the formula is sound for every realization of its map, so either formula
  is SAT if the class is realizable; UNSAT-SOLVER statements name that orientation. Each SAT model: the bridge
  (hinge, two_stage, fp; 120 s each), EMBEDDED -> `verify_candidate.py --all-pairs`. Target S1, eight faces, genus 3
  (never S5 or S0). Counters (SPEC §4): status per unit, solver seconds, bridge outcome, V_E_F_chi.
* **Census controls (stop on failure)**: all seven inputs complete; every class equivelar; both known codes, the six
  face-transitive (8, 3) classes of 3au (E-261117-01) and the 45 equivelar free-C2 codes present; every admissible
  class with a free half-turn (order-2 Aut+ element fixing no face) in the 790. Counts 97 / 51 expected, a session
  check, not a control truth: a different count is recorded, then the lead before any formula.
* **Formula controls**: positive: Roest-Vigh's planes pinned on his links SAT; negative: his planes pinned on another
  admissible census class of his pattern relabelled onto his doubled face pairs (same multiplicities, other map)
  UNSAT-SOLVER; both in every shard, plus the runner's convex controls. Deviation from the week plan ("a wrong
  pairing"): no relinking by one transposition in each link of a doubled pair is an admissible (8, 3) map other
  than his (0 of 10368, session prototype), so the same-multigraph map replaces it. In-run positive: both known maps
  SAT unaided and realized, (V, E, F, chi) = (24, 36, 8, -4). Consistency: E-261118-01 classes 1-5 UNSAT-SOLVER
  (another build of the plain formula; a SAT is recorded and goes to the lead, no stop).
* **Unit tests** (`test_p6.py`, 9 OK before this commit): partitions, the 2-regular inputs, census input-size guard,
  known patterns {4+4, 8}, 790 / 45 free-C2 maps, free half-turn flag, pinned calibration, queue layout, plain formula.
* **Counter calibration**: no float diagnostic in the verdict. Eval violation counts are integers, both sides in the
  tests (0 on Roest-Vigh's own links, > 0 on the negative); bridge `wrong_signs` is an integer and a failed bridge
  decides nothing.
* **Pilot**: the census (seconds), then shard 0 alone (its pinned pair, ~80 units). Exposes: a census path fault, a
  control-file path fault, plain records read as symmetric, bridge or verifier crashes.
* **Pilot gate**: controls pass, no ERROR, every unit ended by its own status; shards 1-9 only if the projection of
  the rest is <= 1 core-h minus the used time and <= 50 min wall.
* **Predictions**: (P1) census controls pass and 97 / 51 reproduced (0.9); (P2) both known maps SAT (0.85), each
  realized by its first model (0.5; else the 30-model step); (P3) no SAT among the 745 non-equivelar maps (0.6);
  (P4) no SAT among the 49 other equivelar classes (0.7); (P5) every unit decided within 60 s (0.9).
* **Grid**: one cap; the outcome depends on the map only.
* **Budget**: <= 1 core-h including census, bridges and follow-ups; <= 50 min wall; 10 shards; laptop, session-run
  after a one-line owner permission (10 cores, 50 min). Expected ~0.3 core-h (3ba: ~1 s per (8, 3) formula).
* **Power**: decides what kissat decides in 60 s (600 s on retry); one model per SAT first. Nothing about
  non-realizability, nor that the two known solids are alone (README); the 745-map control covers only maps with a
  free half-turn, so the non-equivelar SAT rate is that slice's rate.
* **Proofs**: none. Every UNSAT is UNSAT-SOLVER (ranking, planning); no negative claim.
* **Scenario move**: S0 credences A / B / C unchanged in every outcome (S0 parked). Nine-face credence 0.35: no
  automatic move; a realized non-equivelar map or a new object goes to the lead.
* **Outcomes**:
  * SAT: an OM model of that formula, not a polyhedron; realized and `--all-pairs` PASS -> `candidate-check` before
    any claim. Not realized: SAT-NOT-REALIZED, open.
  * UNSAT-SOLVER: that formula, that orientation; not an exclusion.
  * TIMEOUT: no information; one 600 s pass (`p6.py followup`, `Q=stageA_retry`).
  * near-miss: not applicable (exact statuses only).
* **Follow-up tree** (week plan): a failed control -> one repair, then the lead. A SAT not realized -> 30 seeded
  models (`Q=stageA_models`, seeds 1-30, inside the 1 core-h; models not reached are priced for the lead). Only the
  known maps SAT -> record both rates (SAT of 51 equivelar, of 745 others; formula scope), go to item 3. A
  non-equivelar map realized -> `candidate-check`, escalate; the lead re-plans. A new equivelar object ->
  `candidate-check`, escalate (O4); item 3 continues. More than two maps SAT but unrealized -> bridge pricing to the
  lead before stage C. Maps of the 790 left UNKNOWN or SAT-unrealized -> week item 2.
* **Stop rule**: all 796 units and the follow-ups recorded; a failed census control or count mismatch; a failed
  formula control after one repair; or 1 core-h (the session writes `results/<Q>/stop.requested` at 6 min wall with
  10 shards running; recorded units kept, the rest pending).
* **STATUS / ROADMAP**: a new STATUS section with the census counts (EXACT, coverage PROVED-1), both rates (formula
  scope) and the realized objects; the ROADMAP row to done (stage A) or blocked (failed control); item 2's input list.

## Amendments

**Amendment 1 (2026-11-22, week item 3, before any (9, 4) compute): stage B, the equivelar (9, 4) census** (J 2).
* **Coverage (PROVED-1)**: E = 45 = 36 + 9: 2-regular extra edges, eight partitions of 9, one `cycle_union` each; guards
  raised to 9 (90 darts <= MAXD, multiplicity <= 10 < MAXN). Unit (pattern, offset 0-29) seeds the roots numbered offset
  mod 30; each root's search undoes itself, so the union by canonical code is the unsplit census.
* **Method**: `p6.py census-b 9 4` (10 workers, 600 s per unit, aggregate core-s budget with one cap reserved per
  running unit, wall, `stop.requested`; `run.jsonl`), `p6.py merge 9 4 [--prune]` -> `maps_9_4.json`, `census.json`.
* **Controls (stop on failure)**: `census-b 8 3` (stride 3) equals `results/census_8_3` record for record; at (9, 4)
  every class equivelar and in its unit's pattern, duplicates identical; both 3au classes present, inadmissible; the 111
  symmetric equivelar codes present (in a timed-out pattern: unresolved) with their rotation; every admissible class
  with a C3 3+3+3 or C2 4 x 2 + 1 rotation in that list.
* **Probe, gate**: offset 0 of each pattern (`--offsets 0-0`, <= 10 min), projection 30 x its core-s (D3 session check:
  ~15000 core-s; 3+2+2+2 has 11 classes; no pattern below D3's partial count, else the lead). No error or timeout, <= 12
  core-h, rest <= 50 min on 10 workers -> lab-run; longer -> owner day run; > 12 core-h -> lead. A timeout: one 1800 s
  `--retry`, then the lead. Stop: error, failed control, 12 core-h.
* **Predictions**: (P6) controls pass (0.85); (P7) all units complete at 600 s (0.7); (P8) <= 8 core-h (0.75).

**Amendment 2 (2026-11-22, week item 4, before any stage-C compute): stage C, the plain (9, 4) pass** (J 2).
* **Question**: is the plain formula of any admissible equivelar (9, 4) class SAT, and is it realized (S1, nine faces,
  genus 4, (V, E, F, chi) = (30, 45, 9, -6))?
* **Records** (`p6.py build-c`): 1071, one per admissible class of `results/census_9_4/maps_9_4.json` (canonical codes
  merge mirror images; the stage-A orientation argument applies), `tranche.submap_formula` without a generator at 10
  elements, kissat 4.0.4 seed 0, cap 60 s, lean, 10 shards (`run.sh`, `Q=stageC_c0|stageC_c1`); each SAT: the bridge,
  then `--all-pairs`.
* **Chunks**: chunk 0 (91): the ten K2 maps (the lowest-SHA-256 code per pattern of the 111 symmetric equivelar codes,
  then pricing records 2 and 4), then a frozen draw (seed 2611220402) of up to 12 others per pattern (3+3+3, 3+2+2+2
  whole). Chunk 1 (980): the rest, patterns by descending trivial-Aut+ share (9, 5+4, 4+3+2, 6+3, 5+2+2, 7+2).
* **Controls (stop on failure)**: build: census complete with its controls, K2 distinct and admissible, the chunks
  partition the admissible set, every pattern in chunk 0, f9 violations 0 / > 0; run: the f9 pinned pair (positive SAT,
  negative UNSAT-SOLVER) and the convex controls in every shard of both queues. Consistency: the ten K2 maps
  UNSAT-SOLVER again (a SAT: bridge, then the lead; a TIMEOUT: the 600 s pass).
* **Price, gate** (`p6.py price`, NUMERICAL, planning only): chunk 1 = per pattern mean solver-s of chunk 0 (TIMEOUT at
  its cap) x count, scaled by ledger / solver-s; wall = core-s / 10 x 1.5. Chunk 1 is lab-run under the same one-line
  permission if chunk 0's controls pass, no ERROR, every unit ended by its own status and the wall is <= 50 min; else
  an owner night (`BUDGET` from the price, hard cap 80 core-h; above 2 h per shard the runner needs a relaunch, so the
  night script comes from `overnight-run-script`). Expected from K2 (8.1 s mean): ~2.4 core-h, ~20 min wall.
* **Follow-ups**: TIMEOUT -> one 600 s pass (`p6.py followup --stage stageC`, `Q=stageC_retry`), lab-run if <= 50 min,
  else in the night; SAT not realized -> 30 seeded models (`Q=stageC_models`), then the lead.
* **Tree** (week plan): realized and `--all-pairs` PASS with nine faces -> `candidate-check`, escalate. UNKNOWN after
  600 s -> open, listed. Cut by price -> completed patterns are reported, the rest to the lead (a miss is scoped to its
  patterns). All UNSAT-SOLVER -> "every admissible equivelar (9, 4) map has an UNSAT-SOLVER plain formula in its
  code's orientation" (formula scope, planning only); the lead re-plans, no automatic credence move.
* **Unit tests** (`test_p6.py`, 21 OK, 5 new): the K2 codes, a reproducible build (`build-c --check`) and its chunks,
  queue layout and controls, the 10-element formula, price / summary / retry on a synthetic result. Stage A
  `build --check` unchanged.
* **Predictions**: (P9) every control passes and the ten K2 maps are UNSAT-SOLVER (0.9); (P10) every unit decided
  within 60 s (0.8); (P11) no SAT among the 1071 (0.85); (P12) <= 5 core-h and a lab run (0.75).
* **Budget, stop**: hard cap 80 core-h; the lab part <= 50 min wall on 10 cores (chunk 0, chunk 1, retries;
  `stop.requested`). Stop: all 1071 units and follow-ups recorded, ERROR, a failed control after one repair, the cap.
* **Power**: what kissat decides in 60 s (600 s on retry), the code's orientation, one model per SAT first. Nothing
  about non-realizability or about non-equivelar (9, 4) maps. No proofs; every UNSAT is UNSAT-SOLVER.
