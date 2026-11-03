# E-261102-04: the genus-ladder search scored on the benchmark ladder

Pre-registration (2026-11-02, before the night run; the predictions were written while the pilot ran, before its
results). Amendments at the end.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3).
* **Question**: on the full-map rungs with a known answer (R1, R4, R5), how often and how fast does the genus-ladder
  search, the engine that produced the 94 archived genus-3 realizations, reach an exactly verified realization, next
  to chirotope-first's row (E-261101-26; E-261102-03 runs the same night)?
* **Hypotheses moved**: H-261101-10 (handles are the wrong move): R5 is a handle step on a map known to be
  realizable, not an in-class handle of the target, so no move in either direction; stated so that the score is not
  read as one. The score orders the constructive queue (I-261101-22): the engine that wins R4 / R5 carries the next
  construction items.
* **H1 / H0**: H1 = this engine succeeds on R5 at both budgets and on at least one R4 unit; H0 = 0 on R4 (both maps,
  all budgets): the full genus-3 map from random planes is this engine's frontier too.
* **Why this**: PROTOCOL 8a: an engine is scored on rungs with a known answer before it runs on the target. The
  archive climb (E-261030-10) realized a genus-3 map in 204 of 680 six-minute tasks (median 19 s; every float zero
  passed the exact check), always from a genus-2 parent or a perturbed realization, never from random planes. R5 is
  that setting on one map; R4 is the setting it never had.
* **Method**: harness `../E-261101-26-engine-benchmark-ladder/ladder.py` and its `tasks.json` unchanged, plus the
  option `run --engine genus-ladder`: `genus_ladder.search(links, n, minutes, rng, seed_planes)` with the degeneracy
  floor of `archive_climb` (`use_floor(FLOOR_EDGE, FLOOR_MARGIN)`), half the budget one-plane annealing, half CMA-ES,
  until a float zero (pair energy < 0.5) or the budget. Random-plane seeds: the engine draws its own random starts
  (`seed_planes=None`), rng from the unit tag; parent seeds (R5): the parent planes (seed 0-2 exact parents, 3-9 with
  noise 0.01) as `seed_planes`. The budget key of a recorded unit now includes its minutes, so a task runs at several
  budgets into the same directories; `score` reports `TASK@Mmin` cells. R6k is not addressed: the search takes a
  full map's links, not a k-face sub-instance. Target: S3 (genus-3 maps), S4 (Szilassi). Counter: exact success per
  unit, time to success (monotonic).
* **Judge (exact, the only one)**: as E-261101-26, `ladder_exact.verify(planes, links, require_all_pairs=neighborly)`
  EMBEDDED. A float zero that the judge rejects is a failure of that unit (recorded as `FLOAT-ZERO`, success false).
  Every R4 / R5 success goes through `candidate-check` and `verify_candidate.py --all-pairs` before it is called a
  result.
* **Controls**: positive: the `tasks.json` controls (every reference judged, checked by `ladder.py build`, file
  unchanged, hash in each manifest); R1 must succeed (Szilassi from random planes; a session check gave 2/2 in
  5-8 s). Negative: the judge rejects random planes on every task (`tasks.json` controls).
* **Pilot**: R1 3 seeds x 5 min, R5 seed 3 (parent + noise) x 40 min, R4 seed 0 of each map x 40 min, in parallel, in
  a session; results kept in `pilot/`. It can expose: a float zero the exact judge rejects (floor too loose), an
  engine that never ends by time (hang), a seed handling error (parents not used).
* **Pilot gate** (PROTOCOL §2.4): the long run starts only if every pilot unit ends by a judged float zero or by its
  time budget (>= 95 % used), R1 passes, and at least one prediction below keeps a real chance of failing.
* **Predictions** (written before the pilot results):
  * (P1) R1 at least 18 of 20 at 5 min.
  * (P2) R5 at 6 min at least 5 of 10, and at 40 min at least 4 of 5 (the archive's per-task rate was 30 % over many
    maps at 6 min; one map from its own parents should do better). Fails -> the archive's success came from the
    choice of arms (the bandit picked easy handles), not from the search; the constructive queue does not move to
    this engine.
  * (P3) R4: at most 1 of 10 at 40 min and at most 1 of 4 at 120 min, both maps together (from random planes the
    engine never reached genus 3 in the archive runs). Fails -> this engine beats chirotope-first on R4; the
    constructive queue goes through it.
  * (P4) no HARD-CAP, no CRASH; every failure ends by `TIME-CAP` with >= 95 % of the budget; every float zero passes
    the exact judge.
* **Grid** (PROTOCOL §2.5): the budget per seed matters for this engine (it splits the budget between annealing and
  CMA-ES, so a long unit cannot be truncated): R5 {6 min (the archive's task length), 40 min (E-261101-26's)}, R4 {40
  min (E-261101-26's), 120 min (E-261102-03's)}. Seeds per cell: R1 20, R5 10 at 6 min and seeds 0-4 at 40 min, R4
  seeds 0-4 at 40 min and seeds 0-1 at 120 min, per map.
* **Budget**: at most 20 x 5 + 10 x 6 + 5 x 40 + 10 x 40 + 4 x 120 = 1240 min = 20.7 core-h (less where float zeros
  end units early); laptop night shared with E-261102-03: `overnight/launch.sh start
  experiments/E-261102-04-genus-ladder-engine-score 4` (the 4 cores E-261102-03 leaves; about 5-6 h wall).
* **Power statement**: 10 seeds per R4 cell at 40 min (both maps): 0/10 bounds the per-seed rate below ~26 %
  (95 %, one-sided); 0/4 at 120 min below ~53 %. 5 seeds per R5 cell at 40 min cannot separate rates above ~50 %.
  Nothing about other settings, other maps or the target.
* **Counter calibration**: no float diagnostic enters the verdict. `best_energy` (the pair-energy violation count of
  the best attempt) is reported, not used; the exact judge decides, both its sides reachable on every task
  (`tasks.json` controls).
* **Scenario move**: none on A / B / C (the ladder scores an engine, not the target).
* **Outcomes and their meaning**:
  * an R4 / R5 success: an exact genus-3 realization of that map (S3, `candidate-check` before it is added
    anywhere); a new realization of a known map, not a new map;
  * 0 on a rung with R1 passing: the frontier of this engine at that budget;
  * TIME-CAP / HARD-CAP: a failure of that seed at that budget, no information about the target;
  * a float zero rejected by the judge: a failure of that unit and a defect of the float energy, reported;
  * a near-miss (best energy 1-3): not a result.
* **Stop rule**: all units of the grid.
* **STATUS / ROADMAP changes**: STATUS 3b engine-score table gets a genus-ladder row per cell; ROADMAP E-261102-04
  concluded; if P3 fails, the constructive queue (I-261101-22) is re-ordered around this engine.

## Amendments
* 2026-11-02 pilot (session, commit `c2b1ab6` plus the uncommitted `--engine` option and budget key; `pilot/`; four
  processes in parallel): R1 3/3 exact (FLOAT-ZERO judged EMBEDDED in 2, 5, 6 s). R5 seed 3 (archive parent 26 with noise
  0.01): `TIME-CAP` after 2401 s (100 %), best energy 1. R4 type-15 seed 0: `TIME-CAP`, best
  energy 2; R4 type-0 seed 0: `TIME-CAP`, best energy 1. No float zero was rejected by the judge (none on R4 / R5).
  **Gate passed**: every unit ended by a judged float zero or by its time budget at 100 %; R1 passes; P2 now has a real
  chance to fail (one R5 unit failed at 40 min), P3 looks likely to hold. Projection: the night costs close to the
  1240-min maximum (~20 core-h, ~5.2 h wall on 4 shards). Limitation stated now: the night runs 14 processes
  (E-261102-03 on 10, this run on 4) on 10 performance and 4 efficiency cores; budgets are wall-clock, so the
  compute per unit depends on the core the scheduler gives it (not recorded), in both experiments.
