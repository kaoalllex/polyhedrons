# E-261101-26: conclusion, first scope - the chirotope-first engine (laptop, daytime, 2026-11-02)

* **Runs**: commit `73b6515` (branch `experiment/E-261101-25-chirotope-first`, 2 dirty files: untracked `results/`
  and `launch.pids`), `tasks.json` SHA-256 `2dd87b6a...` (unchanged since `build`, so the controls stored in it hold
  for this run). Started through `overnight/launch.sh` at 2026-11-02T10:03:16Z, daytime, not night 7. **8 shards
  instead of the pre-registered 10**: the owner passed 8 to `launch.sh start` as a core count, but `run.sh` partitions
  the units into `SHARDS = 10`, so shards 8 and 9 never started. Run: 64 of 80 units; **not run**: R1 seeds 8, 9,
  18, 19 and seeds 8, 9 of every other task (16 units). All 8 shards `exit_status: 0`, wall 30-54 min. Core-hours
  from `results/*/manifest.txt`: 5.34 in total (0.50-0.90 per shard), against the ~31.7 core-h budgeted for 80 units.
* **Controls**: positive: in `tasks.json` (built and checked before the run, hash unchanged) the judge accepts every
  task's reference and the reference chirotope satisfies the task's CNF; in the run, R1 16/16 and R6k k = 7 4/8, so
  the engine and the judge reach success when the answer is in reach. Negative: the judge rejects random planes on
  every task (`tasks.json`), and 58 of the 64 records were judged failures through the same code path. No HARD-CAP,
  no CRASH.
* **Outcome** (counter: exact success per (task, seed); `results/scores.json` over all 8 shards):

  | Task | Rung | Budget | Successes / seeds | Median time to success | Wall used of the budget |
  |---|---|---|---|---|---|
  | Szilassi from random planes | R1 | 5 min | 16 / 16 | 0.2 s | 0 % |
  | type-15 genus-3 map from random planes | R4 | 40 min | 0 / 8 | - | 19 % |
  | type-0 genus-3 map (the extendable witness map) from random planes | R4 | 40 min | 0 / 8 | - | 16 % |
  | type-15 genus-3 map from its genus-2 parents | R5 | 40 min | 0 / 8 | - | 15 % |
  | type-15 map, first 7 faces | R6k | 20 min | 4 / 8 | 3.2 min | 32 % |
  | type-15 map, first 8 faces | R6k | 20 min | 1 / 8 | 0.6 min | 29 % |
  | type-15 map, first 9 faces | R6k | 20 min | 1 / 8 | 1.3 min | 39 % |

* **What stopped the failures: the alternation cap, not the time budget.** Every failed unit ended `NOT-REALIZED`
  after exactly 20 alternations of one face-ladder step (`--alt 20`), in 3.6-15.2 min of a 20-40 min budget; every
  SAT call returned SAT. The time budget never bound, so a longer `--seed-minutes` changes nothing in this
  configuration. Wall time was 30-54 min per shard, not the 3.5-4.5 h of the PLAN.
* **Per-alternation realization rate** (descriptive, NUMERICAL; the engine's own `realized_wrong_signs = 0` on an
  intermediate step, exact judge only at the end of a unit): type-15 map from random planes, same face order on R4
  and R6k: k = 7: 6 of 281 alternations (2.1 %), k = 8: 1 of 183 (0.5 %), k = 9: 1 of 146 (0.7 %); type-0 map:
  k = 7: 2 of 137, k = 8: 1 of 26, k = 9: 0 of 20; R5 (parent seeds), k = 7: 0 of 160. On R4 the face ladder got
  furthest on the type-0 map, seed 0: k = 7 and k = 8 realized, then 20 alternations without success at k = 9.
  Successes on R6k came after 3-16 alternations (8, 6, 16, 14, 3, 6), so a larger `--alt` would probably have
  added successes (two came after alternation 13).
* **Prediction vs outcome**: P1 (R1 >= 18/20 in 5 min): holds as a rate, 16/16 on the seeds that ran; the count of
  20 cannot be checked. P2 (R6k k = 7 >= 3/10, falling with k): holds, 4/8, then 1/8 and 1/8 (not strictly falling
  from k = 8 to k = 9). P3 (R4 <= 2/10 per map): holds, 0/8 and 0/8. P4 (R5 >= R4 type 15): holds only trivially
  (0 = 0); per alternation the parent seeds did worse at k = 7 (0/160 against 6/281). P5 (no HARD-CAP, no CRASH):
  holds.
* **H1 / H0**: H0. R4 (both maps) and R5 have 0 successes, so the **frontier of this engine configuration is the
  full 12-face genus-3 map**, from random planes and from genus-2 parents. It is the frontier of this configuration
  (`--alt 20`) only, not of the engine.
* **Exact verification** (`candidate-check`): the 16 R1 planes sets, saved from the records, pass
  `verify_candidate.py --all-pairs` (S4, Szilassi: V E F chi = 14 21 7 0, every pair adjacent once) and fail
  `--target S0` (7 faces), as expected. The 6 k-face successes re-judged in a fresh process: 6/6 in general position
  with the chirotope satisfying the task's CNF. All are known-answer controls (7-face Szilassi; 7-, 8- and 9-face
  partial objects of a map with an archived realization), not new witnesses; nothing goes into
  `witnesses/witnesses.json`. No R4 or R5 success, so no new genus-3 realization. No UNSAT is used as evidence.
* **I-261102-01 (adaptive time per seed), its cheapest test on this data**: (1) time to success is not the variable,
  since no unit used its time budget; per alternation the success count looks roughly memoryless (successes after
  3-16 alternations, hazard about 2 % per alternation at k = 7). If so, a longer run of one seed is worth about as
  much as more seeds, and successive halving has nothing to select on. (2) The wrong-sign trajectory does not
  separate successes from failures: in their first three alternations the 6 R6k successes reached a minimum of
  0-4 wrong signs, and the failures reached 1-9. Many failures drop to 1-2 and never reach 0 (R6k k = 8 seed 7: 1
  at alternations 2, 3 and 19). Descriptive only, at n = 6 successes. The final-polynomial label shows no pattern
  either (FEASIBLE on most steps of both kinds).
* **What may be claimed**:
  * NUMERICAL (engine score, this configuration, scope: these 7 tasks, these seeds, 64 units): chirotope-first with
    the E-261102-02 settings realizes Szilassi from random planes 16/16 and the first 7 / 8 / 9 faces of the type-15
    genus-3 map 4/8, 1/8, 1/8 within 20 min; it realizes neither full genus-3 map from random planes (0/8 each) nor
    the type-15 map from its genus-2 parents (0/8) within 40 min. Every failure was cut by the 20-alternation cap,
    not by the time budget.
  * Power: 0/8 bounds the per-seed success rate on R4 / R5 below ~31 % (95 %, one-sided) in this configuration.
* **What may NOT be claimed**: that the engine cannot reach a genus-3 map (other `--alt`, more seeds and other
  configurations were not run); anything about the target types; anything about R2 / R3 (not expressible in the
  encoder) or about the 16 units that did not run; that the wrong-sign signal is useless in general (n = 6
  successes).
* **Hypotheses**: H-261101-17 (open, weakened): on full 12-face maps whose realizations are known, the engine reached
  no embedding model within 20 alternations per step. Its "small, fast cores" part holds (every SAT call returned SAT
  quickly), and its "reaches models of the full instance in minutes" part fails on R4 in this configuration.
  H-261101-10: no move (as pre-registered).
* **Scenario move**: none (pre-registered); the ROADMAP order of the construction items follows the score.
* **Verdict**: first scope (one engine): chirotope-first with `--alt 20` scored. FRONTIER at R4 / R5: 0/24 at 40 min
  (LOW-YIELD@5.3 core-h for full genus-3 maps, 8 seeds per task, alternation cap binding); R1 16/16; R6k 4/8, 1/8, 1/8
  (k = 7, 8, 9). Not REFUTED (no proof); not UNDERPOWERED (the positive controls passed in the same configuration).
* **Consequence for E-261102-02** (by the pre-registered rule "goes ahead unchanged if R4 or R6k k = 9 has a
  success"): R6k k = 9 has 1/8, so the rule lets it go ahead unchanged. Its scope is k = 7 on the target, and k = 7 is
  the rung where the engine has a positive control (4/8 at 20 alternations). Two observations for the owner before
  its launch, not applied: (a) its seeds will mostly end at the 20-alternation cap long before `--seed-minutes 40`,
  so the night will be short unless `--alt` is raised (a change that needs an amendment); (b) at k = 7 the engine now has a realizer positive
  control, on one map. 0 realized out of 149 target seeds would therefore say more than night run 1 did, but it is
  not established that the rate on one map carries over to other maps.
* **Next step**: optionally the 16 missing units (`launch.sh start ... 10` resumes: shards 0-7 skip their recorded
  units, shards 8, 9 run; ~1 h wall), appended here as an amendment. Then the next engine on the same `tasks.json`.
  A chirotope-first variant with `--alt` filling the budget would test whether R4 is a cap or a wall. Then
  E-261102-02.
* **Rows updated**: `STATUS.md` (new table "engine scores", DR8, "As of"), `ROADMAP.md` E-261101-26 (open, first scope
  done), `experiment-log.md` (2026-11-02), `hypotheses/H-261101-17`, `ideas/I-261102-01`. Daytime run, so no night
  report.
