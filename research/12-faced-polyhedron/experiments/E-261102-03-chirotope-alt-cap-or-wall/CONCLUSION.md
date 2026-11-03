# E-261102-03: conclusion (laptop, night 7, 2026-11-02/03)

* **Runs**: commit `9de14b8` (branch `experiment/E-261101-25-chirotope-first`, 3 dirty files: untracked `results/` and
  `launch.pids`), `tasks.json` hash in every manifest, unchanged. Two segments, both through `overnight/launch.sh`:
  1. 2026-11-02T17:18:56Z, `SHARDS = 10` as pre-registered; all 10 shards ended at 18:12:33Z (`exit_status: 0` from
     the exit trap; the night log does not say why, presumably `launch.sh stop`). No unit finished in these 54 min
     (each shard's first unit was a 120-min full-map unit), so this segment produced **no record**: 10 x 0.894 = 8.9
     core-h lost.
  2. Restarted at 18:57:29Z with `SHARDS = 8` (shards 0-7; `results/8` and `results/9` hold only the lost segment).
     Shards ended 20:54Z-23:54Z, all `exit_status: 0`. From 18:57Z the laptop ran 8 + 4 processes (this run and
     E-261102-04) on 14 cores, not the 14 processes the PLAN amendment expected.

  All 20 units ran, 20 distinct (task, seed), no duplicate, no HARD-CAP, no CRASH. Core-hours from
  `results/*/manifest.txt`: **35.9** in total, of which 27.0 in segment 2 (8.9 lost), against the 40-45 core-h
  budget. Scores: `results/scores.json` over shards 0-7 (`ladder.py score ... --cutoffs 40 120`).
* **Controls**: positive: the `tasks.json` controls (hash unchanged); the replay control R6k k = 9 seed 1 succeeded
  again after 6 alternations (80 s), as in E-261101-26, so the harness and the override reproduce a known trajectory;
  the R6k rungs went 8/8, so the engine reaches success when the answer is in reach. Negative: the judge rejects
  random planes on every task (`tasks.json`), and the 12 full-map records were judged failures through the same code
  path.
* **Outcome** (counter: exact success per (task, seed); 4 seeds per task, 120 min each, `--alt 100000 --timeout 300`):

  | Task | Rung | Successes at 40 / 120 min | Median time to success | Unit ended by | Highest k realized per seed |
  |---|---|---|---|---|---|
  | type-15 genus-3 map from random planes | R4 | 0/4, 0/4 | - | TIME-CAP 2, SAT TIMEOUT 2 | 9, 10, 8, 7 |
  | type-0 genus-3 map from random planes | R4 | 0/4, 0/4 | - | TIME-CAP 3, SAT TIMEOUT 1 | 9, 8, 10, 8 |
  | type-15 genus-3 map from its genus-2 parents | R5 | 0/4, 0/4 | - | TIME-CAP 2, SAT TIMEOUT 2 | 10, none, 9, 9 |
  | type-15 map, first 8 faces | R6k | 2/4, 4/4 | 28.6 min | success | - |
  | type-15 map, first 9 faces | R6k | 3/4, 4/4 | 27.8 min | success | - |

  With the cap at 20 alternations (E-261101-26, same seeds among 10) the R6k cells were 1/10 and 1/10 at 20 min.
* **Where the full-map units stopped**: the face ladder climbed past E-261101-26's furthest point (k = 9) in 7 of
  12 units (they worked on k = 10), and 3 realized k = 10 (R4 type-15 seed 1, R4 type-0 seed 2, R5 seed 0); those 3
  worked on k = 11, and none realized it. The binding limit was the time budget in 7
  units (100-101 % used) and the 300-s per-call SAT timeout in 5 (at k = 10 or 11, after 59-102 % of the budget).
  SAT time per alternation (engine record): median 3-5 s at every k, but the 90th percentile rises from 5 s (k = 7)
  and 10 s (k = 9) to 99 s at k = 10, with calls of 200-315 s at k = 10 and 11. Realized steps per alternation, all
  units (engine label `realized_wrong_signs = 0`, NUMERICAL): k = 7: 11/1455, k = 8: 14/1214, k = 9: 11/1288,
  k = 10: 3/222, k = 11: 0/39. On R6k the successes came after 22, 183, 31, 270 (k = 8) and 284, 6, 91, 92 (k = 9)
  alternations: spread like a geometric count at ~1 % per alternation (descriptive, n = 8).
* **Prediction vs outcome**:
  * P1 (R6k k = 8 and 9: >= 5 of 8 at 120 min, >= 2 of 8 at 40 min): **holds**, 8/8 and 5/8.
  * P2 (R4 and R5: 0 of 12 full-map successes at 120 min): **holds**, 0/12.
  * P3 (median highest k realized on the 8 R4 type-15 and R5 units >= 8): **holds**, median 9 (values 7, 8, 9, 9, 9,
    10, 10 and one R5 unit with no k realized).
  * P4 (as amended before the night: every failure ends by TIME-CAP with >= 95 % of the budget, or by a solver status
    reported as the unit's binding limit; no HARD-CAP, no CRASH): **holds as amended**; 5 of 12 failures ended on the
    SAT timeout, so in the original wording P4 would fail.
* **H1 / H0**: H0 (0/12 full-map units at 120 min).
* **Exact verification** (`candidate-check`): no R4 / R5 success, so no new genus-3 realization and no candidate. The
  8 R6k successes re-judged in a fresh process (`ladder.judge`: integer planes in general position, chirotope
  satisfies the task's CNF): 8/8. They are k-face partial objects of a map with an archived realization (known-answer
  controls), not witnesses; nothing goes into `witnesses/witnesses.json`. No UNSAT is used as evidence.
* **What may be claimed**:
  * NUMERICAL (engine score, scope: these 5 tasks, seeds 0-3, 120 min, `--alt 100000 --timeout 300`, 20 units):
    chirotope-first with the alternation cap lifted realizes the first 8 and the first 9 faces of the type-15 genus-3
    map in 4/4 and 4/4 seeds (median ~28 min), and neither full genus-3 map from random planes nor the type-15 map
    from its genus-2 parents (0/12). The face ladder realizes k = 10 in 3 of 12 full-map units; past k = 9 single SAT
    calls take minutes.
  * Answer to the question of the row: for the k-face rungs the 20-alternation cap was a cap (1/10 -> 4/4 per rung);
    for the full maps the frontier did not move at 120 min, and the new binding limits are time and the SAT cost at
    k = 10-11.
  * Power: 0/12 bounds the per-unit full-map success rate at 120 min below ~22 % (95 %, one-sided); 0/4 per task below
    ~53 %.
* **What may NOT be claimed**: that the full map is unreachable for this engine (longer budgets, a longer SAT timeout,
  restarts and other settings were not run; 5 units stopped on the timeout, not on the time); anything about the
  target types; that the per-alternation process is memoryless (n = 8 successes, consistent with it only); that
  any statement holds on maps other than these two.
* **Hypotheses**: H-261101-17 (open, weakened further): with the cap lifted, 0/12 on full genus-3 maps with known
  realizations at 120 min; its "small, fast cores" part holds up to k = 9 and fails at k = 10-11, where single calls
  take 100-300+ s. I-261102-01: the R6k data support "longer chains help" for this engine (the cap, not the seed, was
  the limit at k <= 9); see its file.
* **Scenario move**: none (pre-registered; the ladder scores an engine, not the target).
* **Verdict**: chirotope-first, no alternation cap: **FRONTIER at R4 / R5 unchanged**, LOW-YIELD@35.9 core-h (27.0
  productive) for full genus-3 maps, 0/12 at 120 min, 4 seeds per task; R6k k = 8, 9: 4/4, 4/4 at 120 min (2/4, 3/4 at
  40 min). Not REFUTED (no proof); not UNDERPOWERED (the positive controls passed in the same configuration).
* **Consequence for E-261102-02** (pre-registered outcome "0 R4 / R5 successes, R6k rising"): the full map is a wall
  for this engine at <= 120 min, and E-261102-02 is **killed** in its full-map form. Its pre-registered k = 7 form is
  also not run: on a known map k = 7 to k = 9 now succeed with near certainty in 120 min, so a realized k = 7 model on
  a target type is expected rather than informative (the pilot-gate objection of its 2026-11-02 amendment stands).
  Killed, not re-planned; a target run of this engine waits until some engine passes R4.
* **Next step**: no new row from this experiment. If the chirotope-first engine is continued, the open knob is the
  SAT cost at k >= 10 (a longer per-call timeout or incremental solving across alternations), tested on R4 first; the
  ROADMAP order goes to the exact side (E-261101-06).
* **Rows updated**: `STATUS.md` 3b (new row), DR8, section 7, "As of"; `ROADMAP.md` E-261102-03 done, E-261102-02
  killed; `experiment-log.md` (2026-11-03); `hypotheses/H-261101-17`; `ideas/I-261102-01`; night report
  `reports/NIGHT_REPORT_2026-11-03.md`.
