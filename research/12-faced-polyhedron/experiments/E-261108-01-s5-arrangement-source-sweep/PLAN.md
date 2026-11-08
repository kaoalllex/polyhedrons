# E-261108-01: arrangement-source sweep for solid-first

Pre-registration, 2026-11-08, branch `lab/2026-11-07`. Week plan item 4 (`ROADMAP.md`; origin I-261103-04 with the
36-pair trigger fixed). Explore run at the focus target S5 (F = 9, g = 3), `STRATEGY.md`. A solid found here is an S5
candidate only after `verify_candidate.py --target S5` PASS and `candidate-check`; nothing is claimed before.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2 (T + D = 4). D: E-261107-01 sampled 30 purposive arrangements of
  three generic families; this run changes the source of the planes (the two known (8, 3) arrangements plus a ninth
  plane; random C2-invariant arrangements) and is 10x larger. Not a re-run.
* **Question**: does any of 300 nine-plane arrangements from "near-known" or symmetric sources admit a 36-pair
  embedded solid?
* **Hypotheses moved**: H-261103-02 (free-C3 (9,3) existence) and H-261101-07 (maximal genus-3 existence). A SOLID
  raises both; no SOLID moves neither (a sample of sources, not a family).
* **H1**: at least one of the 300 arrangements admits a 36-pair embedded solid found within the cap. **H0**: none
  does. Prior low.
* **Engine**: E-261107-01 `nine.py` Phase A (`run_unit`, `worker`, `verdict`, `planes('c3', 0)`) imported **unchanged**
  with E-261103-05 `pilot.py`, `solid_fast.Tables`, `solid_cpsat.best_solid`: hard decision, `target_edges = 39`,
  `max_runs = 3`, one CP worker. No Phase B (the pair-count diagnostic): at 30-80 s per unit it would cost about 2x
  the budget, and the only use of its output was the "best >= 34 pairs" follow-up below, which is dropped (amended in
  the ROADMAP item 4 text, same commit). New code: `sweep.py` (draws, shard loop, controls, budget) only.
* **Sources** (100 units each, ids `rv9_sNNN`, `mz9_sNNN`, `inv9_sNNN`; seeds in `sweep.py`, draws deterministic,
  exact uniform arrangement, degenerate draws rejected and counted in `rejected`):
  * `rv9`: the 8 Roest-Vigh planes (`control_rost_vigh.build`) plus one random plane (integer normal in -8..8, offset
    0.3-1.0 of the median plane distance of the 8 planes from the origin);
  * `mz9`: the 8 Mizhaev planes (`literature/mizhaev2026-planes.json`) plus one random plane, same rule;
  * `inv9`: random integer planes invariant under the involution C2 about z, (x, y, z) -> (-x, -y, z): 4 swapped
    pairs plus 1 fixed plane through the axis (the arrangement, not the solid, is C2-invariant). A mirror involution
    was tried and is impossible: its pairs force 4 concurrent planes (checked: 200 rejections), and a fixed plane
    with a z-normal has dependent normals.
* **Cap and sharding**: 60 s per unit (hard budget cap + 30 s), 10 shards (owner rule 2026-11-08), unit i goes to
  shard i mod 10 of the family-interleaved list, so every shard gets 10 + 10 + 10 units. Resumable.
* **Controls** (run by every shard at every start, before any unit; any miss = `CONTROL-FAILED`, the shard stops and
  nothing is inferred): positive (must succeed): Roest-Vigh and Mizhaev own planes, E = 36, exact EMBEDDED with the
  known map. Negative (must fail): tetrahedron with E = 7 and the `c3` seed-0 nine planes with E = 33, both
  INFEASIBLE. Same controls as E-261107-01 minus its Phase B 28-pair check.
* **Counter calibration**: the verdict has no float diagnostic: the status is the exact CP status, SOLID goes through
  the exact `ladder_exact.verify(require_all_pairs=True)`. The positive control calibrates SOLID, the negatives
  INFEASIBLE. `ended_by` (solver_timeout / solved) is recorded per unit.
* **Budget / stop**: <= 2 core-h = 720 core-s per shard (controls included, checked before each unit); expected about
  1.2-1.5 core-h (E-261107-01 Phase A: 5.9-21 s, mean 13.5 s). A shard that hits the budget stops (`BUDGET-STOP`,
  exit 4); the units not run are reported as not run, and the bound below uses the number of decided units N.
* **Power statement**: 0 SOLID in N decided units bounds the density of 36-pair solids among arrangements from
  these sources below 3/N (95 %, rule of three; 1 % at N = 300, sources treated as i.i.d. draws). It says nothing
  about other planes, other symmetries, solids that need another source, or a longer cap; INFEASIBLE holds only for
  that exact CP model at those planes (re-solved, not DRAT). Timeout is not a result: timeouts are not counted in N.
* **Predictions**: (1) controls pass on all 10 shards (~95 %). (2) >= 90 % of the units are decided in 60 s (~70 %;
  the pilot's largest was 21 s, `rv9`/`mz9` may be harder as they sit near a feasible region). (3) No SOLID (~90 %).
* **Outcomes**: SOLID -> `verify_candidate.py --target S5`, `candidate-check`, owner informed at once.
  INFEASIBLE units -> UNSAT of the saved model at those planes, no family exclusion. UNKNOWN / HARD-TIMEOUT -> no
  information. If > 30 % of the units are undecided: verdict UNDERPOWERED, a longer cap needs the lead.
* **Kill / follow-up tree**: no 36-pair solid -> park arrangement-first for (9, 3) with the bound 3/N. A SOLID ->
  as above. The "best Phase B >= 34 pairs -> 1000 more arrangements" branch is dropped with Phase B; a decided
  fraction < 70 % escalates instead.
* **Where**: laptop, AC power, `bash research/12-faced-polyhedron/overnight/launch.sh 261108-01 start|status|stop`,
  10 shards, results in `results/<shard>/` (`results.jsonl`, `controls.jsonl`, per-unit input/output/log, models
  gzipped with SHA-256 in the records). Runs after item 1 finishes or on <= 2 cores beside it.
* **STATUS / ROADMAP changes**: ROADMAP row (running, then done); one STATUS section after the conclusion.

## Amendments

### 2026-11-08 (before any run): startup check on 10 shards
`run.sh` with SHARDS=10, scratch output, cap 10 s, budget 45 s: all 10 shards ran 4 controls with the expected
outcomes (tetrahedron and E = 33 INFEASIBLE, Roest-Vigh and Mizhaev SOLID with the known map; the E = 33 control took
13.8 s under 10-way load) and 3-4 units each; all units UNKNOWN by `solver_timeout` at 10 s, as expected for a
startup check (not data). Every shard ended `BUDGET-STOP` (exit 4), the stop path works. No stop file left.
