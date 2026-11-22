# E-261119-02: symmetric nine-face census (C3 3+3+3, C2 4 x 2 + 1), then per-map symmetric formulas

Pre-registration of stage A (2026-11-19), at most 80 lines. Stage B is registered by an amendment after the stage-A gate
and the per-stratum pricing (week plan item 2). Amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 1 G 2 R 2; week item 2, explore, J 2, the main investment.
* **Question (stage A)**: which admissible (9, 4) dual maps carry a rotation acting on the faces as C3 3+3+3 or as
  C2 4 x 2 + 1, listed exactly within 1 core-h?
* **Hypotheses moved**: H-261101-07 only through stage B (a realized nine-face map). I-261030-18 and I-261119-01 tested
  (the symmetric census route). Stage A moves no credence: maps are not polyhedra.
* **H1 / H0**: H1 = a family's list is complete within the budget and passes its controls (that family goes to stage B);
  H0 = it times out or fails a control (UNDERPOWERED or repair).
* **Why**: the uniform symmetric families left are C3 3+3+3 (standard chart) and C2 4 x 2 + 1 (moved chart; I-261118-02,
  STRATEGY §1); per-map formulas at 10 elements are what decided (8, 2), (9, 3), (10, 4) and (11, 5) on the laptop.
* **Method**: `symcensus.py`, one enumerator for a prescribed vertex rotation rho (generalises
  `E-261103-01/c3_crosscheck.py`, written anew; uses the census's TriMap, check, canonical codes). Per excess vector of
  the pair orbits (multiplicity <= 3; up to the normaliser of <rho>: C3 324 elements, 18 classes of 352 at (9, 4)) and
  per choice of fixed triangles (C3: b distinct supports with (30 - b) = 0 mod 3, so b in {0, 3}, any orientation; C2:
  none possible): every exact cover of the directed-pair-orbit demands by triangle orbits (each orbit at most once,
  distinct supports; orbits with two triangles on one support excluded), every gluing commuting with rho (built from one
  matching per pair orbit, propagated, conflicts rejected), the one-cycle-per-vertex check and `census.review.check`.
  Completeness PROVED-1 (module docstring). Deadline checks inside the cover and the gluing loops. Recorded per unit
  (config, demand class, fixed choice): complete flag, nodes, covers, gluings tried, map hits, seconds, and per map the
  canonical code, b, fixed edges and rho on canonical darts; per stratum (b, multiplicity pattern) the sums.
* **Independent checks**: each recorded action is re-checked on the canonical code alone (commutes with step and alpha,
  order p, the family's number of fixed vertices); `review.check` on every map; codes compared with the census below.
* **Controls (exact equalities, from saved E-261103-01 data)**: C3 (9, 3) = the census's 8 admissible maps with a
  vertex-free order-3 automorphism = `c3-crosscheck.json`; C2 4 x 2 + 1 at (9, 3) = the census's admissible maps with an
  involution fixing exactly one vertex; free C2 at (8, 2) = the census's maps with a vertex-free involution; C2 3 x 2 + 1
  at (7, 1) = Szilassi's map (the only (7, 1) class); free C2 at (8, 3) holds both known maps (Roest-Vigh, Mizhaev; no
  (8, 3) census exists, so containment only; the full list is stage B's rung). Negative: the action check rejects a
  wrong fixed count, a transposed action and the identity (unit test).
* **Unit tests** (`test_symcensus.py`, run on this commit by shard 0 of the launch before any census unit): normalisers 324 / 384 / 384 / 48; C3 (9, 4) 12 pair orbits,
  352 excess vectors, 18 classes, 9 fixed choices, (9, 3) 12; C2 4 x 2 + 1: 4 excluded orbits, no fixed triangle;
  (7, 1) and (8, 2) controls exact; the action check on both sides.
* **Run** (owner launch after E-261119-01 ends, `launch.sh 261119-02 start`): shard 0 runs the unit tests (the others
  wait; a failure stops all), then 10 shards x 360 s on a shared ordered unit list with O_EXCL claims, controls and C3
  first, then C2; <= 1 core-h by construction. Then the session: `symcensus.py summary results/stageA`.
* **Gate per family**: C3 passes if its (9, 3) control is exact, 18 classes, every action checks and every C3 (9, 4) unit
  completed; C2 passes if its four controls hold, every action checks and every C2 (9, 4) unit completed. A passing
  family goes to stage B even if the other times out.
* **Predictions**: (P1) every control holds (0.85); (P2) the C3 family completes (0.75); (P3) the C2 family completes
  (0.45); (P4) the C3 (9, 4) list is non-empty (0.85); (P5) the free-C2 (8, 3) list holds a third map besides the two
  known ones (0.5).
* **Grid**: none; the census is exhaustive per family. One cap (1 core-h, the row's).
* **Budget**: stage A <= 1 core-h (the row), session; stage B <= 10 core-h owner run (amendment).
* **Power**: a complete list is exhaustive for its family (EXACT computation, coverage PROVED-1); an incomplete one says
  nothing about the maps not reached. Nothing about other actions (mirrors, C2 3 x 2 + 3) or other genera.
* **Proofs**: none (no SAT in stage A).
* **Counter calibration**: no float diagnostic; all counters are integers or booleans with controls on both sides.
* **Scenario move**: none in stage A.
* **Outcomes**: complete + controls -> the list (EXACT, PROVED-1 coverage), per-stratum counts, then the pricing of one
  map per multiplicity stratum and the stage-B amendment. Timeout -> that family UNDERPOWERED@1 core-h, to the lead (no
  extension without the owner). Control failure -> repair once. An empty complete list -> that family has no (9, 4)
  map: stage B for it is void; genus 5 (E = 51) per the tree.
* **Follow-up tree**: as the week plan: a family all UNSAT-SOLVER in stage B -> genus 5 for it, priced the same way;
  neither family advances -> item 3 (P6); a SAT -> bridge, `--all-pairs`, `candidate-check`, escalate.
* **Stop rule**: a control failure; the 1 core-h deadline; or both families complete.
* **STATUS / ROADMAP**: after stage A, one STATUS line per family (count or timeout); the row stays running until stage
  B concludes.
* **Deviations from the row**: (1) a new enumerator instead of an edit of `c3_crosscheck.py` (the census folder's
  evidence stays as recorded); (2) the free-C2 (8, 2) control is added (an exact census equality for the C2 code path
  without a fixed face); (3) the unit tests run inside the launch on this commit, not in the session, because
  E-261119-01 holds all 10 cores while this is registered (the owner launches stage A, 2026-11-19).

## Amendments

**Amendment 1 (2026-11-20, launch defect, no data).** The owner launch of 2026-11-20 09:24Z ran no census unit: `run.sh`
read its cap as `${SECONDS:-360}`, and `SECONDS` is bash's built-in seconds-since-start counter (always set, 0 at
start), so every shard got a 0 s budget (manifests: `seconds 0`, empty `claims/`, no `results.jsonl`); only the unit
tests ran (6 OK, 8 s). Repair: the cap is now `BUDGET` (the name other runners use); nothing else changed. Smoke on
shard 0 with `BUDGET=25` (single core, pilot folder, deleted): the manifest records 25 s and 201 units ran before the
deadline. Note for the gate: building the 808-unit list takes about 9 s of each shard's budget. The defective
launch stays in `results/stageA-defective-0s/` (raw, not committed); stage A is relaunched unchanged by the owner.

**Amendment 2 (2026-11-20, before any stage-B solver run): pricing and the rung.** Stage A passed both gates (STATUS 3be).
The owner chose a two-pass stage B (2026-11-20): pass 1 every map of both lists at a short cap set by this pricing, pass
2 the pass-1 UNKNOWNs at 600 s; no subset by a guessed predictor. The cap and the budget go to amendment 3, with the owner.
* **Inputs** (`stageb.py`, from the committed stage-A records): one record per map and rotation group; links keyed by
  the canonical code's labels (32 of 32 (9, 3) records equal the census's links, every generator a rotation of them);
  C3 and free C2 uniform in the standard chart, C2 4 x 2 + 1 plane-only in a moved chart (`tranche.submap_formula`).
* **Pricing**: 3 maps per stratum (deviation: the row says one; a short cap needs a decided fraction per stratum), frozen
  seed 2611200201: 12 C3 and 21 C2 records (`queue_pricing.json`). **Rung**: the 8 C3 and 24 C2 4 x 2 + 1 (9, 3) classes
  (`queue_rung_9_3.json`; all must be UNSAT-SOLVER, 3d: every (9, 3) plain formula UNSAT-VERIFIED); Roest-Vigh's map
  under its 3 free-C2 groups and Mizhaev's under its 1 (`queue_rung_8_3.json`; at least one SAT per map, realized,
  `--all-pairs` PASS).
* **Run**: `run_b.sh` (the E-261103-03 runner, imported-map mode), kissat seed 0, cap 600 s, bridge 360 s on a SAT, no
  proofs, 10 shards each, the three queues in turn: rung (9, 3), rung (8, 3), pricing; pinned convex f9 controls on
  every shard of the nine-face queues, the runner's pilot controls on every shard. Owner launch (`launch.sh 261119-02
  start`; `run.sh` now defaults to these queues, stage A is `STAGE=A`), <= 1.5 h wall; solver
  <= 11.5 core-h only if every unit times out. One code change: `tranche.bridge` calls `verify_candidate.py --all-pairs`
  for the target `all-pairs` (STRATEGY §1), otherwise unchanged (`test_tranche` 28 OK).
* **Controls not run here**: the moved-chart plane-only path is the E-261118-03 Szilassi chain (recorded pass, same
  runner and formula code); the nine-face generic pinned positive and the wrong-action negative go to amendment 3.
* **Recorded**: per record status, solver seconds, unit wall, formula size; per stratum the fraction decided by 30, 60,
  120, 600 s. **Projection** for pass 1: sum over strata of size x mean min(t, cap) plus the per-unit overhead.
* **Predictions**: (Q1) the rung holds (0.8); (Q2) every C3 pricing record decides within 600 s (0.7); (Q3) at least
  half of the C2 records decide within 60 s (0.5); (Q4) no (9, 4) SAT (0.9).
* **Stop / tree**: a (9, 3) SAT, a failed pinned control or no SAT on a known (8, 3) map -> stop, repair before stage B.
  A (9, 4) SAT -> bridge, `--all-pairs`, `candidate-check`, escalate. Otherwise amendment 3 (pass 1 cap, budget,
  controls) to the owner.

**Amendment 3 (2026-11-20, before any pass-1 run): pass 1 of the two-pass stage B.** Amendment 2's owner launch
(2026-11-20 12:12Z, 31 s wall, < 0.1 core-h): every pilot and pinned f9 control passed on every shard. The rung held (Q1):
the 32 (9, 3) classes were UNSAT-SOLVER (<= 1.3 s); Roest-Vigh's map was SAT under 2 of its 3 groups and Mizhaev's under its
1, all three realized with `--all-pairs` PASS. Pricing: 33 of 33 UNSAT-SOLVER in <= 0.29 s; the fraction decided by
30, 60, 120 and 600 s is 1.0 in all 11 strata (Q2, Q3 held; Q4 holds so far). README "Stage B".
* **Controls added** (all 33 pricing records C2f decide UNSAT in under 0.3 s, and no nine-face positive exists for the
  moved-chart path: suspect until controlled): `controls_b.py` (the `E-261118-03/controls_12.py` pattern). The record's
  formula with only the GP, symmetry and gauge clauses (mirror and orbit-flip gauge as stage B). Per record, 5 draws:
  random integer planes symmetric under the record's rotation (C2f: half-turn, moved chart; C3: standard chart) gauged and
  pinned, must be SAT; planes symmetric under a conjugate t g t != g instead, must be UNSAT; the unpinned formula SAT.
  Result on this commit (`results/controls_b.json`, 8 s): 165 of 165 SAT, 165 of 165 UNSAT, 33 of 33 SAT, PASS. Formula
  level, the same code builds every pass-1 formula, so it is not repeated per shard. Every shard keeps the pinned f9
  controls and the runner's pilot controls.
* **Pass 1**: `queue_pass1.json`, every (9, 4) map of both lists: 12562 records (118 C3, 12444 C2f; one group each), in
  stage-A order (C3 first). Kissat seed 0, cap 30 s (100 x the priced maximum), bridge 360 s on a SAT, no proofs, 10
  shards, `BUDGET` 36000 s (the row's 10 core-h as a hard ceiling; pass 1 + pass 2 stay within it unless the owner
  extends). `maps/pass1.json` (7.7 MB, SHA-256 `82faa3402b1d64a4eb1249604060629e1e4d4612e03f3a5419eeb99121be58a7`) is not committed: `stageb.py` rebuilds it
  deterministically (two builds agree), and the runner refuses a file whose hash differs from the queue's. The 33 pricing
  records are re-run inside pass 1: any status change stops the reading (replication check).
* **Projection**: the pricing sum over strata gives ~2260 solver-s, ~1.4 core-h with the unit overhead. Smoke on this
  commit (10 shards, 50 s, then stop; folder deleted): 821 records, all UNSAT-SOLVER, max 0.45 s, 0.51 s wall per unit
  under full load, so ~1.8 core-h, ~11 min wall. About 0.5 GB of raw output goes to `../polyhedrons-data` (`move_raw.py`).
  Tail risk: with 3 maps per stratum the pooled 95% upper bound on the undecided share is ~9% (33 of 33 decided), up to +9 core-h
  at 30 s, which the ceiling cuts. Units not dispatched stay pending (resumable).
* **Run**: owner launch `launch.sh 261119-02 start` (`run.sh` now defaults to pass 1, `STAGE=B` keeps amendment 2) ->
  `results/stageB-pass1/<s>/`.
* **Predictions**: (R1) every pass-1 record decides within 30 s (0.85); (R2) no (9, 4) SAT (0.9); (R3) pass 1 <= 3 core-h
  (0.9).
* **Readings / tree**: a failed control or a replication mismatch -> stop, repair. A SAT -> bridge, `--all-pairs`,
  `candidate-check`, escalate. UNKNOWNs -> pass 2 at 600 s: owner launch inside the row's remaining budget if <= 5% (628
  records), else the pass-2 price goes to the owner first. A family with every record UNSAT-SOLVER -> that family's
  uniform symmetric (9, 4) formulas are UNSAT-SOLVER; per the tree, genus 5 for it, priced the same way.
* **Power / scope**: an UNSAT-SOLVER holds for its exact formula (uniform symmetric, C3 standard chart, C2f plane-only
  moved chart) and is never a negative result without a checked replay. Nothing about non-symmetric realizations of these
  maps, other actions (mirrors, C2 3 x 2 + 3), or other genera.
* **Deviations**: a 30 s pass-1 cap instead of the row's 600 s (two-pass, owner 2026-11-20); 3 priced maps per stratum
  instead of 1 (amendment 2).

**Amendment 4 (2026-11-20, before any genus-5 run): the census at (9, 5).** Pass 1 left both families all UNSAT-SOLVER at
(9, 4) (STATUS 3bf), so per the tree genus 5 (E = 51) for both, priced the same way. Owner choice (2026-11-20, after the
price below): the C3 census now in the session, the C2 census as one owner night with a 40 core-h hard cap; stage B at
genus 5 goes to amendment 5 after the gate.
* **Bookkeeping** (EXACT, session): V = 34 triangles, k = 15 extra edges; multiplicity <= 3 still holds (2m distinct
  corner triples on a pair out of 7). C3: 12 pair orbits, 3432 excess vectors, 83 classes; 34 - b = 0 mod 3 forces b = 1
  (one fixed triangle, on one of the 3 face orbits, 2 orientations): 6 fixed choices, 498 units. C2 4 x 2 + 1: 20 pair
  orbits (4 of size 1), 1330768 vectors, 12288 classes, no fixed triangle: 12288 units. Every class count, the recorded
  (9, 3), (8, 3) and (9, 4) ones included, equals an independent Burnside count over the normaliser (`burnside_classes`).
* **Code** (`symcensus.py`, `run.sh`, `test_symcensus.py` 7 OK): `demand_reps` makes one pass per normaliser orbit (the
  old loop is 384 x 1.3M at (9, 5)); same representatives in the same order: `summary results/stageA` rebuilt with the new
  code equals the committed `summary-brief.json`. New configs C3_9_5, C2f_9_5; stages A5c3 (C3 (9, 3) control + C3_9_5)
  and A5c2 (the four C2 controls + C2f_9_5), each gated alone; `run.sh` takes `STAGE`, default A5c2, results in
  `results/stage<STAGE>/`. The enumerator itself (covers, gluings, checks) is unchanged.
* **Price** (session pilot, 10 processes, frozen sample seed 2611200401): 60 C3 units all complete in <= 0.03 s, no map;
  300 C2 units mean 3.53 s (5 cut at 30 s, rerun to completion in <= 67 s), max 135 s over the first 10 demand classes
  (the heaviest cluster at low indices, which the claim order runs first). Projection: C2 census 12.1 core-h (bootstrap
  95% 9.2-15.3), ~1.1M map classes (+-0.3M), ~1.6 GB of records. The pilots (price, tail, a 10-shard 40 s smoke of the
  A5c2 path, folders deleted) used ~0.85 core-h, booked to the A5c2 budget.
* **Run**: A5c3 in the session after this commit (`STAGE=A5c3 BUDGET=300`, 10 shards, seconds). A5c2: owner launch
  `launch.sh 261119-02 start` (`launch.results` -> `results/stageA5c2`), 10 shards x 14400 s = 40 core-h hard cap,
  ~1.3 h wall projected; shard 0 runs the unit tests first. Then `symcensus.py summary results/stageA5c2 A5c2`. The
  per-unit records are not committed (size): they go to `../polyhedrons-data` (`move_raw.py`); git keeps the brief
  summary, per-stratum counts and the SHA-256 of every shard's `results.jsonl`.
* **Gate per family**: C3 passes if the C3 (9, 3) control is exact, its classes equal the Burnside count, every action
  checks and all 498 units complete; C2 passes if its four controls hold, the Burnside count matches, every action checks
  and all 12288 units complete.
* **Predictions**: (G1) every control holds (0.9); (G2) the C3 (9, 5) list is empty (0.6); (G3) the C2 census completes
  within 40 core-h (0.9); (G4) the C2 list has 0.8M-1.4M classes (0.6).
* **Readings / tree**: a control failure -> repair once. An empty complete C3 list -> no C3 3+3+3 (9, 5) map (EXACT,
  coverage PROVED-1): stage B void for C3. A non-empty one or a complete C2 list -> amendment 5: per-stratum pricing
  (3 maps per stratum, as amendment 2) and the pass-1 price to the owner (at the (9, 4) per-record cost ~1.1M C2 records
  are ~170 core-h and ~45 GB raw: no subset by a guessed predictor without the owner). C2 timeout -> UNDERPOWERED@40
  core-h, to the owner.
* **Power / scope**: a complete list is exhaustive for its family at (9, 5); maps are not polyhedra; nothing about
  mirrors, C2 3 x 2 + 3 or other genera.
* **Deviations**: the C2 census budget exceeds the row's stage-A 1 core-h (owner, 2026-11-20: 40 core-h cap); stages
  split by family; per-unit records kept out of git.

**Amendment 5 (2026-11-22, before any genus-5 solver run): lean runner, (9, 5) pricing.** Amendment 4's gate passed:
C3 3+3+3 (9, 5) is empty (STATUS 3bg; stage B void for C3); C2 4 x 2 + 1 (9, 5) has 978228 map classes in 12 strata (3bh).
Per the tree: per-stratum pricing as amendment 2, then the pass-1 price to the owner; pass 1 is amendment 6.
* **Inputs** (`stageb.py --g5`): the A5c2 records are read by streaming from `../polyhedrons-data/<same path>`, every
  shard file checked first against `results/stageA5c2/SHA256SUMS`. Two passes: the stratum of every map by its canonical
  SHA-256 (one stratum per map, asserted), then the drawn maps. 3 per stratum, frozen seed 2611220501, drawn from the
  sorted canonical SHA-256 of the stratum (deviation from amendment 2's sorted codes: the first pass keeps no codes):
  36 records, one rotation group each (`maps/pricing_9_5.json`, `queue_pricing_9_5.json`). Formula as at (9, 4) for C2f:
  uniform symmetric, plane-only, moved chart (`tranche.submap_formula`).
* **Lean runner** (owner, 2026-11-22: no raw data nobody needs): a queue flag `lean_unsat` in `tranche.py`; a non-control
  UNSAT-SOLVER unit keeps only its fsync'ed `results.jsonl` line (status, seconds, variables, clauses, `cnf_sha256`,
  `formula_sha256`, scope, canonical SHA-256) and its unit folder is removed once that line is written; SAT, TIMEOUT,
  errors and controls keep everything; resume reads only the line (`test_tranche` 28 OK, the flag test extended).
  At (9, 4) a unit folder held 5 files (239 MB on disk for pass 1); at (9, 5) that would be ~5M files.
* **Summary** (owner, same day): `symcensus.py summary` streams the records and writes only `summary-brief.json`
  (controls, gate, per-config counts and strata), no code list; the claim markers are removed once every planned unit is
  recorded. Check on this commit: the stage A and A5c3 briefs equal the old code's text; the A5c2 brief rebuilt from the
  data copy equals the committed one (85 s, 0.75 GB RSS; the old code peaked at 21 GB). `test_symcensus` 7 OK.
* **Controls**: (a) the amendment-3 formula controls on the 36 records (`controls_b.py results/controls_b_9_5.json
  maps/pricing_9_5.json`, 5 draws each): every positive SAT, every wrong-action UNSAT, every unpinned SAT. (b) Lean
  replication: `queue_pricing_lean.json`, the committed (9, 4) pricing queue with the flag (same maps file); every one of
  its 53 units must match the committed `results/stageB-pricing` records in status, `cnf_sha256` and `formula_sha256`, no
  folder may remain for an UNSAT-SOLVER record and every control keeps its folder. (c) Every shard keeps the pinned f9 and
  the runner's pilot controls.
* **Run** (session, seconds, < 0.1 core-h): `STAGE=B5 bash run.sh s` for the 10 shards: (b) then the (9, 5) pricing,
  kissat seed 0, cap 600 s, bridge 360 s on a SAT, no proofs -> `results/stageB5-<queue>/`; (a) single process.
* **Recorded**: per record status, solver seconds, unit wall, formula size; per stratum the fraction decided by 30, 60,
  120, 600 s; bytes left per lean unit. **Projection** for pass 1: as amendment 3 (sum over strata of size x mean
  min(t, cap) plus the measured per-unit overhead), with disk. Known cost to price: one 978228-record maps file is ~0.6 GB
  and `tranche.imported_maps` loads it in every unit, so pass 1 needs chunked maps files and queues (amendment 6).
* **Predictions**: (S1) the formula controls pass (0.9); (S2) the replication is exact (0.95); (S3) every (9, 5) pricing
  record decides within 30 s (0.8); (S4) no (9, 5) SAT (0.9).
* **Readings / tree**: a failed control or a replication mismatch -> stop, repair. A SAT -> bridge, `--all-pairs`,
  `candidate-check`, escalate. Otherwise the pass-1 price (core-h, wall, disk) goes to the owner; pass 1 needs amendment 6
  and the owner's budget (the row's 10 core-h stage-B cap does not cover it); no subset by a guessed predictor without
  the owner.
* **Power / scope**: a price, not a result about any stratum; an UNSAT-SOLVER holds for its exact formula only and is
  never a negative result. Nothing about non-symmetric realizations, mirrors, C2 3 x 2 + 3 or other genera.
* **Deviations**: the draw by sorted hashes; the lean mode and the brief-only summary (owner); the replication queue.

**Amendment 6 (2026-11-22, before any pass-1 run at (9, 5)): pass 1 on a random 10% first.** Amendment 5 passed (README
"Stage B at genus 5"): lean replication exact, formula controls pass, 36 of 36 priced records UNSAT-SOLVER in <= 0.23 s;
pass 1 priced ~143 core-h. Owner choice (2026-11-22): first a uniformly random 10% of the 978228 maps, then decide between
the other 90% and a lemma for the common obstruction (item 4).
* **Order and chunks** (`stageb.py --g5-pass1`, streamed from the hash-checked data copy): the sorted canonical SHA-256
  of every map, shuffled with the frozen seed 2611220601, cut into 100 contiguous chunks of 9783 maps (the last 9651);
  chunks 0-9 (97830 maps, one rotation group each) are the 10%. A random order, not a predictor: the rest is chunks 10-99
  of the same order. Chunk maps files and queues (~6 MB each, `maps/pass1_9_5/`) are not committed; `pass1_9_5.json`
  pins the order hash and every chunk's maps and queue SHA-256 (two builds agree; the runner refuses a changed file).
* **Run**: per chunk the amendment-5 runner (`run_b.sh`, lean, kissat seed 0, no proofs), cap 5 s (20 x the priced
  maximum; owner), bridge 360 s on a SAT; every shard keeps the pilot and pinned f9 controls per chunk. `STAGE=B5p1`
  (`run.sh` default): the chunks in turn per shard, each chunk ledger 18000 s; a shard stops at a chunk that ends other
  than SHARD-COMPLETE, and before a chunk once the ledgers hold 20 core-h (hard cap; projected ~14.3 core-h, ~1.5 h wall).
  Owner launch `launch.sh 261119-02 start` (`launch.results` -> `results/stageB5-pass1`), `stop` at any time, resumable.
* **Checks before the launch** (session, recorded in README): (a) SAT units in the lean mode: `queue_rung_8_3_lean.json`
  (the amendment-2 (8, 3) rung with the flag; `STAGE=B5`) must repeat the recorded statuses and hashes of
  `results/stageB-rung_8_3`, every SAT unit keeping its folder with the model and the bridge's `--all-pairs` PASS;
  (b) a 10-shard smoke of the B5p1 path on chunk 0 (`PILOT_DIR`, ~60 s, then stop, folder deleted): per-unit wall under
  full load, statuses, no folder left for UNSAT-SOLVER units.
* **Predictions**: (T1) every one of the 97830 records decides within 5 s (0.85); (T2) no SAT (0.9); (T3) the 10% stays
  within 20 core-h (0.9).
* **Readings / tree**: a failed control -> stop, repair. A SAT -> bridge, `--all-pairs`, `candidate-check`, escalate.
  TIMEOUTs -> pass 2 at 600 s on them after the 10% (priced first if > 5% of it). All UNSAT-SOLVER -> the 10% read as a
  price and as a sample (with 0 of 97830 undecided, the 95% upper bound on the undecided share is ~3e-5); the owner
  decides between chunks 10-99 (~129 core-h) and the lemma.
* **Power / scope**: an UNSAT-SOLVER holds for its exact formula only and is never a negative result; the 10% says
  nothing about the 90% beyond the sampling bound. Nothing about non-symmetric realizations, mirrors, other genera.
* **Deviations**: a 10% stage before the full pass (owner); cap 5 s instead of amendment 3's 30 s (owner).
