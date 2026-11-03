# E-261102-04: conclusion (laptop, night 7, 2026-11-02/03)

* **Runs**: commit `9de14b8` (branch `experiment/E-261101-25-chirotope-first`, 4 dirty files: untracked `results/`,
  `launch.pids` and the other runs' folders), `tasks.json` hash in every manifest, unchanged. Two segments through
  `overnight/launch.sh`:
  1. 2026-11-02T17:19:15Z, `SHARDS = 4` as pre-registered, until 18:15:26Z (`exit_status: 0` from the exit trap,
     presumably `launch.sh stop`); the units finished by then are kept, the ones in progress were re-run.
  2. Restarted at 18:15:44Z with `SHARDS = 10`: shards 4-9 ran one 40-min unit each (ended 18:55:50Z), shards 0-3
     ran to 20:15Z-20:55Z. From 18:57Z E-261102-03 shared the laptop (8 + 4 processes on 14 cores).

  All 49 units of the grid ran, 49 distinct (task, seed, budget), no duplicate, no HARD-CAP, no CRASH. Core-hours
  from `results/*/manifest.txt`: **17.8** in total (budget at most 20.7). Scores: `results/scores.json` over all
  10 shards.
* **Controls**: positive: the `tasks.json` controls (hash unchanged); R1 (Szilassi from random planes) 20/20 in
  2-17 s. Negative: the judge rejects random planes on every task (`tasks.json`); every float zero went through the
  same judge, and none was rejected.
* **Outcome** (counter: exact success per (task, seed, budget); engine `genus_ladder.search` with the `archive_climb`
  floor):

  | Task | Rung | Budget | Successes / seeds | Time to success | Failures ended by |
  |---|---|---|---|---|---|
  | Szilassi from random planes | R1 | 5 min | 20/20 | 2-17 s (median 0.1 min) | - |
  | type-15 genus-3 map from its genus-2 parents | R5 | 6 min | 5/10 | 108-175 s (median 2.7 min) | TIME-CAP 5, best energy 2-3 |
  | same | R5 | 40 min | 3/5 | 114-179 s | TIME-CAP 2, best energy 1 |
  | type-15 genus-3 map from random planes | R4 | 40 / 120 min | 0/5, 0/2 | - | TIME-CAP, best energy 1-3 |
  | type-0 genus-3 map from random planes | R4 | 40 / 120 min | 0/5, 0/2 | - | TIME-CAP, best energy 1-3 |

* **The R5 cells are one experiment seen twice**: the unit's random stream comes from its tag, not from its budget,
  and every success came within the first 3 minutes (the annealing half of a 6-min unit). Seeds 0, 1 and 4 succeeded
  at both budgets with identical planes and 15-23 restarts; seeds 2 and 3 failed at both, and their 40-min units ran
  164-167 restarts without a float zero (best energy 1). So the 34 extra minutes per seed converted 0 of 2 failures;
  per seed the outcome was decided in the first ~3 min. Successes by seed kind: exact parents (seeds 0-2) 2/3,
  parents with noise 0.01 (seeds 3-9) 3/7.
* **Prediction vs outcome**:
  * P1 (R1 >= 18 of 20 at 5 min): **holds**, 20/20.
  * P2 (R5: >= 5 of 10 at 6 min and >= 4 of 5 at 40 min): **fails**, by one unit: 5/10 holds, 3/5 at 40 min does not.
    The pre-registered reading of a failure: the archive's success came from the choice of arms, not from the
    search, and the constructive queue does not move to this engine. The data add: the per-seed rate on this map is
    about one half at any budget >= 6 min, and a longer budget buys nothing for a seed that failed (above).
  * P3 (R4: at most 1 of 10 at 40 min and 1 of 4 at 120 min): **holds**, 0/10 and 0/4.
  * P4 (no HARD-CAP, no CRASH; failures by TIME-CAP with >= 95 % of the budget; every float zero passes the judge):
    **holds**: every failure used 100 % of its budget, 28 float zeros, 28 judged EMBEDDED.
* **H1 / H0**: neither as stated: R5 succeeds at both budgets (H1's first half), R4 has 0 of 14 (H0). The full
  genus-3 map from random planes is this engine's frontier too.
* **Exact verification** (`candidate-check`; planes saved from the records with the task's triangles):
  `verify_candidate.py` on the 20 R1 sets with `--all-pairs`: 20 PASS (V E F chi = 14 21 7 0, every pair adjacent
  once), with `--target S0`: 0 PASS (7 faces), as expected. On the 8 R5 sets (5 distinct, the 40-min sets are equal to
  the 6-min ones of the same seed) without a flag: 8 PASS, each EMBEDDED on the type-15 map with V E F chi =
  32 48 12 -4, 12 simple faces, points distinct; with `--target S0`: 0 PASS (genus 3, not every pair adjacent). They
  are new realizations of a map whose realizations are archived (known-answer controls, S3 on a known map), not
  witnesses; nothing goes into `witnesses/witnesses.json`, and they are not added to `verify_all`, so not labelled
  EXACT. No UNSAT is used as evidence.
* **What may be claimed**:
  * NUMERICAL (engine score, scope: these 3 tasks plus R1, the seeds and budgets of the grid, 49 units): the
    genus-ladder search with the `archive_climb` floor realizes Szilassi from random planes 20/20 (seconds), the
    type-15 genus-3 map from its genus-2 parents in 5/10 seeds at 6 min and 3/5 at 40 min (successes within 3 min),
    and neither full genus-3 map from random planes (0/10 at 40 min, 0/4 at 120 min).
  * Next to chirotope-first on the same tasks (STATUS 3b): this engine wins R5 (5/10 at 6 min against 0/10 at 40 min
    and 0/4 at 120 min); neither engine passes R4.
  * Power: 0/10 per map at 40 min bounds the per-seed R4 rate below ~26 % (95 %, one-sided); 0/4 at 120 min below
    ~53 %; the R5 rate (8/15 units, 5 distinct seeds of 10 succeeded) is about one half with wide intervals.
* **What may NOT be claimed**: that this engine cannot reach a full genus-3 map from random planes (other budgets,
  floors and seed counts were not run); that a longer budget never helps (2 failing seeds at 40 min); anything about
  other maps, the archive's arms or the target; that the R5 successes say anything about in-class handles (R5 is a
  handle step on a map known to be realizable).
* **Hypotheses**: H-261101-10: no move (as pre-registered: R5 is not an in-class handle of the target). H-261101-09
  (thin regions): not tested by design; noted only that random-plane starts reach best energy 1 and stop there on
  both maps, as in the archive runs. I-261101-22 (constructive queue ordered by the ladder): updated with both rows.
* **Scenario move**: none (pre-registered).
* **Verdict**: genus-ladder search scored: **FRONTIER at R4** (0/14 at 40 / 120 min, LOW-YIELD@17.8 core-h for full
  genus-3 maps from random planes); R5 5/10 at 6 min, 3/5 at 40 min; R1 20/20. Not UNDERPOWERED (R1 and R5 passed in
  the same configuration); not REFUTED (no proof).
* **Consequence**: with two engines scored, R4 (a full 12-face genus-3 map from random planes, 2 h per seed) is a
  rung where every scored engine fails. By the stop rule of E-261101-26 ("the first rung where every engine fails"),
  that rung is now the research problem on the construction side, not the target. The pre-registered consequence of
  the P2 failure (the constructive queue does not move to this engine) is applied; P3 holding leaves the queue
  order as it was.
* **Next step**: none from this experiment. For this engine the cheap knob is more seeds, not more minutes (the
  outcome per seed is decided in ~3 min). The ROADMAP order goes to the exact side (E-261101-06).
* **Rows updated**: `STATUS.md` 3b (new row), DR1, section 7, "As of"; `ROADMAP.md` E-261102-04 done, E-261101-26
  note; `experiment-log.md` (2026-11-03); `ideas/I-261101-22`; night report `reports/NIGHT_REPORT_2026-11-03.md`.
