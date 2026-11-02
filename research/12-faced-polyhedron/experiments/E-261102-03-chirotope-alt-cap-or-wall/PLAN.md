# E-261102-03: chirotope-first on the full-map rungs with the alternation cap lifted - cap or wall?

Pre-registration (2026-11-02, before the night run; the predictions were written before the pilot finished).
Amendments at the end.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3).
* **Question**: in E-261101-26 every failure of chirotope-first stopped at `--alt 20` after 15-39 % of its budget.
  With the cap lifted, so that time binds, does the engine reach the full genus-3 maps (R4, R5) within 40 or
  120 min per seed, and do the k-face rungs (R6k k = 8, 9) rise as a memoryless per-alternation rate predicts?
* **Hypotheses moved**: H-261101-17 (chirotope-first reaches models). A full-map success supports its "some models are
  realizable" part on maps where a realization exists; 0 full-map successes with R6k rising makes the full map a
  wall for this engine at <= 120 min; R6k not rising says the alternation chain stalls (the cap was not the limit).
* **H1 / H0**: H1 = at least one exact R4 or R5 success at 120 min; H0 = 0 of 12 full-map units.
* **Why this**: PROTOCOL §2.4 (the lesson of E-261101-26): a run whose binding limit was a cap measured the cap. The
  per-alternation success rates of E-261101-26 (type 15 from random planes: k = 7 7/352, k = 8 1/223, k = 9 1/186)
  project, if memoryless, a k = 8 or k = 9 success per 120-min unit with ~85 % probability, a full map with < 10 %.
  E-261102-02 is blocked on this answer.
* **Method**: harness `../E-261101-26-engine-benchmark-ladder/ladder.py` and its `tasks.json` unchanged, plus the new
  option `run --alt A` (overrides `ENGINE['alt']`, recorded per unit) and `score --cutoffs M ...` (successes within M
  minutes; per unit the limit that ended it, the budget fraction used, the alternations, the highest k realized).
  Engine configuration = E-261101-26 except `--alt 100000` (no cap: time binds). Tasks: R4 type-15 map, R4 type-0
  map, R5 type-15 from its genus-2 parents, R6k type-15 k = 8 and k = 9; seeds 0-3 of each (20 units), 120 min each,
  hard cap 135 min. The seeds and tags are those of E-261101-26, so each unit continues a trajectory that failed at
  the cap there (paired; `PYTHONHASHSEED=0` fixes the realizer seed; the SAT timeouts are wall-clock, so the replay
  is close, not exact). Target: S3 (genus-3 maps) and k-face partial objects; counter: exact success per unit and
  time to success (monotonic).
* **Judge (exact, the only one)**: as E-261101-26: full map `ladder_exact.verify` EMBEDDED; k-face task: integer
  planes in general position whose normalised chirotope satisfies the task's CNF. Every full-map success goes
  through `candidate-check` and `verify_candidate.py --all-pairs` before it is called a result.
* **Controls**: positive: `tasks.json` controls (every reference is judged and in its CNF, checked by `ladder.py
  build` in E-261101-26; the file is unchanged, its hash is in each manifest); R6k k = 9 seed 1 succeeded in
  E-261101-26 after 6 alternations, so it should succeed again early (a replay check of the harness under the
  override, not guaranteed because of the wall-clock SAT timeouts). Negative: the judge rejects random planes on
  every task (`tasks.json` controls).
* **Pilot**: R4 type-15 seed 0, 40 min, `--alt 100000`, same code path (`ladder.py run`), in a session; results kept
  in `pilot/0/`. It can expose: a run that ends on another limit (the core-guided solver's status at a k step, an
  UNSAT of the CNF plus the accumulated heuristic blocks, a hard cap), a hang, or a cost per alternation that grows
  so fast that time buys no alternations.
* **Pilot gate** (PROTOCOL §2.4): the long run starts only if the pilot unit ends with `TIME-CAP` after >= 95 % of
  its budget (time binds, not alternations, rounds or the solver), and its projected outcome leaves P1 or P2 a real
  chance to fail. If it ends otherwise (a solver status, UNSAT of CNF + blocks), the PLAN gets an amendment first
  (for example `--block 0`) or the run is dropped.
* **Predictions** (written before the pilot result):
  * (P1) R6k k = 8 and k = 9 together: at least 5 of 8 successes at 120 min (memoryless projection ~85 % per unit,
    ~6.8 of 8); at 40 min at least 2 of 8. Real chance to fail: the chain may stall (the blocks accumulate, the
    trajectory stays near one bad region). Fails -> the alternation chain is not memoryless; the engine needs
    restarts, not a longer chain (I-261102-01 direction), and E-261102-02 is killed.
  * (P2) R4 and R5: 0 of 12 full-map successes at 120 min (projection < 10 % per unit). Fails -> E-261102-02 is
    amended with the cap lifted and the budget at which the success came.
  * (P3) median highest k realized on the 8 R4 type-15 and R5 units at 120 min: >= 8 (a type-15 unit spends ~50
    alternations, ~15 min, to pass k = 7 if memoryless).
  * (P4) every failure ends by `TIME-CAP` with >= 95 % of the budget used; no HARD-CAP, no CRASH.
* **Grid** (PROTOCOL §2.5): the budget per seed, {40, 120} min, plus the alternation-capped cell of E-261101-26
  (`--alt 20`, same seeds). The engine uses its budget only as a deadline (`one_run`: `deadline`, and the final
  polynomial's time limit `min(120 s, time left)`), so a 120-min unit truncated at 40 min is a 40-min unit up to that
  last-two-minutes time limit: the 40-min cell is scored with `score --cutoffs 40 120` from the same units. Fewer
  seeds per cell than E-261101-26 (4 per task instead of 10), more time per seed.
* **Budget**: 20 units x 120 min = 40 core-h, at most 45 core-h with the hard caps; laptop night, `overnight/launch.sh
  start experiments/E-261102-03-chirotope-alt-cap-or-wall 10` (2 units per shard, about 4-4.5 h wall). Pilot 40 min.
* **Power statement**: 0/12 full-map units bounds the per-unit success rate at 120 min below ~22 % (95 %, one-sided);
  0/4 per task below ~53 %. It cannot detect a full-map rate of a few percent per 2-hour unit, and says nothing about
  longer budgets, other engine settings (`--block 0`, restarts) or the target types.
* **Counter calibration**: no float diagnostic enters the verdict: exact pass / fail, times, alternation counts,
  integer k. Both sides of the judge are reachable on every task (`tasks.json` controls). `realized_wrong_signs` is
  reported, not used.
* **Scenario move**: none on A / B / C (the ladder scores an engine, not the target).
* **Outcomes and their meaning**:
  * an R4 / R5 success: a new exact genus-3 realization (S3, after `candidate-check`); the engine reaches the full map
    with the cap lifted; E-261102-02 is amended with that setting;
  * 0 R4 / R5 successes, R6k rising (P1 holds): the full map is a wall for this engine at <= 120 min; E-261102-02 is
    killed in its full-map form;
  * 0 R4 / R5 successes, R6k not rising (P1 fails): the cap was not the limit, the chain stalls; E-261102-02 is
    killed and the engine change (restarts / adaptive seed time, I-261102-01) gets a row;
  * TIME-CAP / NOT-REALIZED / HARD-CAP: a failure of that seed at that budget, no information about the target;
  * an UNSAT of a k step (CNF plus heuristic blocks): not a non-realizability statement (the blocks are not sound
    cuts); recorded as the limit that ended the unit;
  * a near-miss (a model with few wrong signs): not a result.
* **Stop rule**: all 20 units, or the first R4 / R5 success (`candidate-check` before anything else).
* **STATUS / ROADMAP changes**: STATUS 3b engine-score table gets a "chirotope-first, no cap, 40 / 120 min" row per
  task; ROADMAP E-261102-03 concluded, E-261102-02 amended or killed by the outcome above.

## Amendments
* 2026-11-02 pilot 1 (session, commit `dc3d7ae` plus the uncommitted `--alt` option; `pilot/0/`): R4 type-15 seed 0,
  40 min, `--alt 100000`, otherwise the E-261101-26 configuration. The unit climbed the face ladder: k = 7 realized
  after alternation 27, k = 8 after 16 more, k = 9 after 49 more (94 alternations in ~34 min; median SAT time 3 s).
  At the first alternation of k = 10 a SAT call (round 7, 47 assumptions left) hit `--timeout 60` and the engine
  ended with `TIMEOUT` after 2048 s, 85 % of the budget. **Gate not passed**: the binding limit was the per-call
  solver timeout, not time. The k = 10 CNF had no heuristic blocks yet (they are per k step), so the hard call is the
  k = 10 instance under partial assumptions, not an artefact of accumulated blocks. Per alternation the pilot did
  better than the E-261101-26 rates (k = 9: 1 of 49 against 1 of 186), so P3 now looks likely to hold.
  Amendment: `--timeout 300` (configuration only, the engine code is unchanged; new harness option
  `ladder.py run --timeout S`, recorded per unit) and a re-pilot of the same seed (`pilot-t300/0/`) under the same
  gate before the night.
* 2026-11-02 pilot 2 (session, same code plus the uncommitted `--timeout` option; `pilot-t300/0/`): the same unit with
  `--alt 100000 --timeout 300`. The trajectory replayed pilot 1 exactly up to k = 9 (realized after alternations 27,
  43, 92, so the pairing with E-261101-26 seeds is a real replay), then 12 alternations at k = 10 (SAT calls up to
  125 s, the call that timed out in pilot 1 now finished; wrong signs after realization 2-29), and the unit ended
  with `TIME-CAP` after 2400 s, 100 % of the budget. **Gate passed**: time binds. Projection for 120 min: this seed
  spends ~34 min on k = 7-9 and ~30 s per alternation at k = 10, so ~170 more alternations at k = 10 and beyond;
  P1 and P3 look likely to hold, P2 (0 of 12 full maps) has a real chance to fail. The night runs the PLAN with
  `--timeout 300` (in `run.sh`); a SAT call can overrun the deadline by up to 300 s plus a final polynomial of up to
  120 s, inside the 15-min hard-cap margin. P4 now reads: every failure ends by `TIME-CAP` with >= 95 % of the budget
  used, or by a solver status that is reported as the binding limit of that unit.
* 2026-11-02 (before the night, nothing run since the pre-registration): E-261102-04 shares the night on 4 more
  shards, so 14 processes run on 10 performance and 4 efficiency cores. Budgets are wall-clock, so the compute per
  unit depends on the core the scheduler gives it (not recorded); the pairing with E-261101-26 (8-10 processes) is
  close, not exact, after the first divergence.
