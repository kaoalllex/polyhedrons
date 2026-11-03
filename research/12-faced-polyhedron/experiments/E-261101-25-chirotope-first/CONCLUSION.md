# E-261101-25: conclusion (night run 1 = night 6, 2026-11-01/02)

* **Runs**: commit `1bbe052` (branch `experiment/E-261101-25-chirotope-first`), shards 0-3 of the 10 slices of the 149
  class seeds (14 + 15 + 15 + 15 = 59 seeds scheduled; shards 4-9 were not part of night 6), started
  2026-11-01T17:41Z under `caffeinate -dimsu`, all four ended by the owner's `stop` at 2026-11-02T04:42Z.
  Core-hours from `results/*/manifest.txt`: 44.10 in total (11.02 per shard plus restart lines of 0.003-0.004).
  Productive time (start to the last `progress.jsonl` line): shards 0-2 under 5 minutes each, shard 3 about 1.45 h,
  of which one step took 81 minutes; the rest of the 44 core-h was spent inside hung steps.
* **Why the night stopped producing**: in every shard the last line of `progress.jsonl` is an alternation step with
  an unrealized model (shard 0: seed type18-kd_92b7df10c4 after 3 steps; shard 1: type44-kd_017a10a854 after 3;
  shard 2: type34-kd_1a185650d1 after 14; shard 3: type29-kd_fab21b9a23 after 2), and the next call in
  `one_run` is `final_polynomial`. The same HiGHS `linprog` without a time limit was reproduced hanging in
  E-261101-23 (see its `CONCLUSION.md`); here the cause is inferred from the code path, not reproduced. The per-seed
  cap (`--seed-minutes 75`) is checked only between steps, so it could not stop a step that never returned; in shard 3
  one such LP did return after about 80 minutes (seed type39-kd_4aecd06992, between steps 17 and 18), and that seed
  was then recorded as TIME-CAP. Fixed after the night: `final_polynomial(..., time_limit=120)` -> `LP-TIMEOUT`.
* **Controls**: positive controls passed in the session pilot through the same engine (n = 7 from random planes ->
  exact EMBEDDED; known 12-plane chirotopes recovered by the realizer). No positive control exists for the k = 7
  step at n = 12 (no k-face model with a known realization was tried), so a failure to realize at k = 7 is not
  evidence about realizability.
* **Outcome** (counters: core-guided status, released signs, realized wrong signs; seeds = class seeds):

  | | value |
  |---|---|
  | seeds started / recorded | 27 / 23 (4 hung) |
  | result `ROUNDS` at the first step (12 core-guided rounds used up, 117-409 of 715 assumptions still on) | 21 |
  | seeds that reached a k = 7 model | 6 |
  | alternation steps with a model | 42 |
  | released signs per model (minimal correction set) | median 12, range 4-679 |
  | wrong signs after realization | median 9, range 3-30; 0 realized |
  | final polynomials (19 recorded) | 13 FEASIBLE, 5 NONREALIZABLE-NUMERICAL, 1 NONREALIZABLE-EXACT (135 brackets, became a sound cut) |
  | EMBEDDED / k > 7 reached | 0 / 0 |

  Cores were 3-110 literals and solved in under a second; the round budget, not the solver, ended 21 of 27 seeds:
  the night setting `--rounds 12` (the PLAN's Method said 40) is too small once SIMPLE clauses are on, because the
  cores are small and 12 of them do not release enough signs.
* **Prediction vs outcome**: P1 (every seed's k = 7 step reaches a model within the round budget): false, 6 of 27,
  and a budget artefact (`--rounds 12`). P2 (at least 30 % of unrealized k = 7 models get an exact final
  polynomial): false, 1 of 19 recorded (5 %); the 4 hung LPs gave nothing. P3 (at least one k = 7 model realizes):
  false, 0 of 42, best 3 wrong signs. P4 (no seed reaches k = 12): true.
* **Exact verification**: no candidate (nothing EMBEDDED, no realized model); `candidate-check` had nothing to run
  on. The exact final polynomial's multipliers were not stored, so it is not reproducible from the files.
* **What may be claimed**:
  * NUMERICAL: with these settings the k = 7 sub-instance under the rank-3 signs of a class seed returns UNSAT cores
    of 3-110 literals in under a second; for 6 of 27 seeds a model was reached, 4-679 signs (median 12) away from the
    seed's signs; none of the 42 models realized with the two-stage and hinge realizers (6 restarts).
  * NUMERICAL (exact computation inside the run, not reproduced by `verify_all.py`): one k = 7 model (seed
    type39-kd_4aecd06992, step 3) is a non-realizable chirotope by a biquadratic final polynomial.
* **What may NOT be claimed**: anything about the full 12-face instance or any type (k = 7 only, 27 of 149 seeds);
  that the models are non-realizable (13 of 19 have no biquadratic final polynomial, which proves nothing either way);
  that the engine cannot reach models (21 of 27 failures are the round budget); that H-261101-17 is weakened.
* **Hypotheses**: H-261101-17 stays open (evidence: small cores, fast solves and small minimal correction sets at
  k = 7, supporting its "small cores" part; no full-instance run). H-261101-12: no move (k = 7 models only).
  H-261101-01: no move.
* **Scenario move**: none of the pre-registered moves applies (no realized model, no full-instance result); the
  credences in `ROADMAP.md` stay unchanged.
* **Verdict for the direction**: UNDERPOWERED@44.1 core-h (under 2 productive; 27 of 59 scheduled seeds, k = 7
  only, `--rounds 12`, a hang in the final-polynomial LP). Not LOW-YIELD. The PLAN's "What each outcome changes" for
  P2 false says invest in the realizer rather than cuts; with 4 of 23 LPs lost and the round budget binding, that
  reading is premature.
* **Next step**: ROADMAP row E-261102-02 (night run 2 of the engine with the LP time limit, `--rounds 40`, a step-level
  cap, all 10 seed slices, final-polynomial certificates stored), after the engine is scored on the benchmark ladder
  E-261101-26 (PROTOCOL 8a), which also gives the missing k-face realizer control.
* **Rows updated**: `STATUS.md` DR8 and the "As of" line, `ROADMAP.md` E-261101-25 State done and row E-261102-02,
  `experiment-log.md` (2026-11-02), `hypotheses/H-261101-17`, `reports/NIGHT_REPORT_2026-11-02.md`.
