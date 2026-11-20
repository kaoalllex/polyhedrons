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
