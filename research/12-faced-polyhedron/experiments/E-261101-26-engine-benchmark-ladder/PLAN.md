# E-261101-26: engine benchmark ladder, first scope - the chirotope-first engine

Pre-registration (2026-11-02, before the night run). Amendments at the end.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (T + D = 3).
* **Question**: on tasks whose answer is known (a realization exists and lies in the engine's search space), how often
  and how fast does the chirotope-first engine, in the configuration E-261102-02 will run on the target, reach an
  exactly verified success from random (or parent) planes within a fixed budget per seed?
* **Scope of this first run (owner's decision 2026-11-02)**: one engine, chirotope-first (E-261101-25,
  `chirotope_first.one_run`), on the rungs its encoder can address with a known answer. Rungs:
  * **R1** Szilassi (n = 7, neighborly, genus 1) from random planes: 20 seeds x 5 min.
  * **R4** a genus-3 12-face map from random planes, two maps: the type-15 archive map (54 archived realizations, all
    on one map; reference archive id 72) and the type-0 extendable witness map
    (`E-261030-03.../type0_genus3_extendable.json`): 10 seeds x 40 min each.
  * **R5** the type-15 genus-3 map seeded from its genus-2 parents (the archived genus-2 realizations whose map is
    the genus-3 map minus one handle, i.e. shares all but 6 of its 32 triangles: archive ids 26, 165, 229): 10 seeds
    x 40 min (seeds 0-2 the three parents unchanged, 3-9 the parents with Gaussian noise 0.01).
  * **R6k** k-face sub-instances of the type-15 genus-3 map, k = 7, 8, 9 (first k faces of its greedy face order),
    from random planes: 10 seeds x 20 min each. This rung replaces the ROADMAP's R6 for scoring: the k-face
    sub-instances of the target types (types 0, 15, 58) have no known answer, and no archived realization agrees with
    its type on more than 2 face polygons (checked on all 247), so none of them yields a known-answer k-face
    sub-instance of a type. R6k is the realizer positive control at the k-face level that E-261101-23 and
    E-261102-01 lacked.
  * **Not addressed, stated explicitly**: R2 and R3 (Roest-Vigh and Mizhaev 8-face objects): their maps have doubled
    adjacencies, and `omsat.Triangulation` requires each pair of faces to share at most one edge (each edge pair in
    exactly two triangles), so the encoder cannot express them. R6 on the target types and R7 (the full type) have no
    known answer and are not scored. The other engines (genus ladders, solid-first, normals-first) are later scopes.
* **Hypotheses moved**: H-261101-17 (chirotope-first reaches models): success on R4 / R6k supports its "some models
  are realizable" part on instances where realizable models exist; 0 successes there with the controls passing
  supports its rival for this engine configuration. H-261101-10 (handles are the wrong move): no move (R5 is a
  handle step on a map known to be realizable, not an in-class handle of the target).
* **H1 / H0**: H1 = the engine succeeds on at least one seed of every rung R1, R4, R5, R6k; H0 = there is a rung with
  0 successes (that rung is then the engine's frontier and the measured reason it should not yet run on the target).
* **Why this**: PROTOCOL 8a: a failure on the target says nothing about an engine, a failure on a rung with a known
  answer does. E-261102-02 (chirotope-first night 2) waits for this score.
* **Method**: `ladder.py build` writes `tasks.json` (7 tasks, 80 units) and checks each task's controls;
  `run.sh SHARD` (10 shards, every 10th unit) runs `ladder.py run`, which calls `chirotope_first.one_run` with the
  E-261102-02 configuration (`--alt 20 --timeout 60 --rounds 40 --readd 1000 --realize-restarts 6 --block 1
  --realizer two-stage --simple 1 --fp 1`, face ladder from k = 7 on the map's greedy face order, `--seed-minutes` =
  the rung budget). Each unit runs in its own process group with a hard cap of budget + 15 min (HARD-CAP).
  `ladder.py score` writes `scores.json`. Target: S3 (genus-3 maps), S4 (Szilassi), and k-face partial objects.
  Counter: exact success per (task, seed); time to success (monotonic).
* **Judge (exact, the only one)**: full map: `ladder_exact.verify(planes, links, require_all_pairs=neighborly)`
  EMBEDDED; k-face task: the realized integer planes are in general position and their normalised chirotope
  satisfies the task's CNF (CaDiCaL under all 715 signs as assumptions). The engine's own labels are recorded, not
  used.
* **Controls (in `tasks.json`, checked by `build`)**: positive: for every task the judge accepts the reference
  realization, and the reference chirotope satisfies the task's CNF (the answer is in the engine's search space; for
  Szilassi a perturbation of the symmetric planes, accepted by the judge, since the encoder assumes general position);
  negative: the judge rejects random planes on every task.
* **Pilot**: R1 3 seeds, R6k k = 7 and R4 type 15 one seed each, 5 min budget, same code path; see Amendments.
* **Budget**: at most 20 x 5 + 30 x 40 + 30 x 20 min = 31.7 core-h plus HARD-CAP margins; 10 shards, about 3.5-4.5 h
  wall; laptop night 7, `overnight/launch.sh`.
* **Power statement**: 10 seeds per task: 0/10 bounds the success rate per seed below ~26 % (95 %, one-sided) at that
  budget and configuration; it says nothing about longer budgets, other configurations or the target.
* **Counter calibration**: the score is an exact pass / fail count and a time, no float diagnostic. Both sides of the
  judge are reachable on every task (reference passes, random planes fail). `realized_wrong_signs` is reported, not
  used for the verdict.
* **Predictions (written before the run)**: (P1) R1 at least 18/20 within 5 min; (P2) R6k: k = 7 at least 3/10,
  falling with k; (P3) R4 at most 2/10 per map (random planes to a genus-3 map in 40 min is the hard rung); (P4) R5 at
  least as many successes as R4 type 15; (P5) no HARD-CAP, no CRASH.
* **Scenario move**: none on A / B / C (the ladder scores an engine, not the target); the ROADMAP order of the
  construction items moves by the score (I-261101-22).
* **Outcomes and their meaning**:
  * success on a rung: the engine reaches that known answer at that budget; R4 / R5 successes are new exact genus-3
    realizations (S3, `candidate-check` before they are added to any witness list);
  * 0 successes on a rung with the controls passing: the frontier of this engine configuration; E-261102-02 is
    re-planned (engine change) before it runs on the target;
  * TIME-CAP / NOT-REALIZED / HARD-CAP: a failure of that seed at that budget;
  * a judge failure on a reference after the run (tasks.json changed): the run is void.
* **Stop rule**: all 80 units (the row: all engines scored, or the first rung where every engine fails; this scope
  is one engine).
* **STATUS / ROADMAP changes**: a new STATUS table "engine scores" (rung x engine: successes / seeds, median time,
  budget); ROADMAP E-261101-26 stays open for the next engines; E-261102-02 goes ahead unchanged if R4 or R6k k = 9
  has a success, otherwise its PLAN gets an amendment first.

## Amendments
* 2026-11-02 pilot (session, before the run; same code path, budget overridden to 5 min, results in the session
  scratchpad, not kept): `ladder.py build`: all 7 tasks pass their controls (reference judged and in the CNF; random
  planes rejected; the Szilassi reference needed perturbation trial 1). R1: 3/3 EMBEDDED in 0.2 s each. R6k k = 7:
  1/1, an exactly verified 7-face realization after 8 alternations in 90 s (models before it had 3 wrong signs and
  FEASIBLE final polynomials). R4 type 15: 0/1, TIME-CAP at 5 min (best model 5 wrong signs, one LP-TIMEOUT).
  Harness checks (session script): a re-run skips the recorded units; a unit that hangs with a forked child is killed
  with its whole process group and recorded as HARD-CAP; `score` counts 3/3, 1/1, 0/1. Change after the pilot: the
  hard-cap margin is the constant `CAP_MARGIN_MIN` (15 min, unchanged) so the check can set it to 0.
  Shard layout: 80 units, shard s takes units s, s + 10, ...: 2 R1, 1 + 1 R4, 1 R5, 3 R6k per shard, at most
  190 min of budgets per shard.
