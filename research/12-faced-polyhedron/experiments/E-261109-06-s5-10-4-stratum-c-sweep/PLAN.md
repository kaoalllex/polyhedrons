# E-261109-06: (10,4) first-witness sweep, stratum C (kissat, no DRAT)

Pre-registration, 2026-11-09. Week plan item 1 (lead review 2026-11-09, owner-approved). Focus S5 at (10, 4).

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2 (T + D = 4). Follow-up of E-261108-03 (STATUS 3x).
* **Question**: does any of the 360 admissible (10,4) maps outside the patterns `(1^4,2)` and `1^6` have a SAT plain S5
  formula, and what does each pattern cost with kissat?
* **Hypotheses moved**: H-261101-07. A SAT model starts the realization stage (only a realized, verified object moves
  "exists"); 0 SAT moves nothing by itself (UNSAT-SOLVER is never a negative result) but prices strata A and B.
* **H1 / H0**: H1 (scenario): all 360 decided within 80 core-h, total near 51 core-h. H0: the cost model is wrong by
  > 1.5x (cap reached with < 300 decided, or > 10 % censored at 3600 s).
* **Why this stratum**: the six fastest patterns (32 % of the maps, about 12 % of the priced cost, review 2026-11-09
  §3.2); it fits one laptop night and calibrates the per-pattern factor used to price A and B.
* **Method**: target S5 at (F, g) = (10, 4), V, E, F = 32, 48, 10. Census `maps_10_4.json` (SHA-256
  e563f7cd37118742a48446856b571fde87a21bf12d72931b309b58eebb922328, coverage PROVED-1). Formula: E-261103-02 encoder via
  the E-261103-03 runner (`pilot.build`, `ALL_OPTS`, `from_links`, `submap=False`), unchanged. Solver: kissat rel-4.0.4,
  `~/bin/kissat` SHA-256 4bc069939394b3b56f8dfa9518094f3a716246d65701635f9c722c2c7af4ceb7 (E-261108-03), `NO_PROOF=1`,
  solver cap 3600 s per map. Queue `queue.json` (`make_queue.py`, SHA-256
  85d8faf214a0888ba550ed4b722b0dcb7f0311c0b91849876e13d571f934f1ab): 358 maps in pattern order `(1,2,3)/(2,3)` 37,
  `(1,1,1,3)` 58, `(1,1,2,2)/(2,3)` 70, `(1,1,2,2)/(2,2,2)` 186, `(2,2,2)/(2,2,2)` 6, `(3,3)/(4)` 1 (census index order
  within a pattern); maps 845 (188.4 s) and 146 (692.6 s) enter with their E-261108-03 kissat UNSAT-SOLVER records.
  10 shards, shard s runs entries s, s + 10, ... (36 or 35 maps each, every pattern spread over all shards).
  Counters (SPEC §4): SAT / UNSAT-SOLVER / TIMEOUT per map; solver seconds; core-h from `budget.json`.
* **Controls** (every shard, first in its queue, plus the runner's `pilot.py --controls-only` per attempt): positive
  `control-f10-sK` (convex 10-face map, planes pinned) must be SAT with a checked model; negative `control-f10-neg-sK`
  (another map, same pinned planes) must be UNSAT-SOLVER. A control failure stops the root (`stop.json`).
* **Pilot** (2026-11-09, before this commit, scratch results, not counted): shard 0 with the two controls and map 108
  (`(1,2,3)/(2,3)`) at a 120 s cap: controls SAT / UNSAT-SOLVER, map 108 TIMEOUT at 120 s, SHARD-COMPLETE in 129 s; identity
  kissat hash and `no_proof` as above; `progress.sh` and `summary.py` read the records. It checks the plumbing, not times.
* **Pilot gate**: binding limit = the per-shard budget share 28800 s (a shard stops dispatching when a 3600 s unit no
  longer fits). The night starts on the pilot above; E-261108-03 gave the per-map times (188-2749 s at (10,4)).
* **Predictions**: (P1, ~60 %) all 360 decided, total <= 51 x 1.5 = 76.5 core-h; (P2, ~85 %) 0 SAT; (P3, ~40 %) the
  measured factor f puts A + B above 4 laptop nights (-> Actions route); (P4, ~70 %) no pattern has > 10 % censored.
* **Grid**: one setting; the solver and cap were chosen by E-261108-03, the cap by the week plan.
* **Budget**: <= 80 core-h, <= 10 h wall, 10 shards, one owner laptop night (`launch.sh 09-06 start`), no Actions.
* **Power statement**: detects any SAT plain formula of stratum C that kissat finds within 3600 s; a censored map says
  nothing; an UNSAT-SOLVER says nothing about realizability elsewhere and is not a negative result. Strata A, B untouched.
* **Counter calibration** (`summary.py --selftest`, passed): censored fraction 37/360 escalates, 36/360 does not; f = 5.5
  gives A + B = 4.66 nights (Actions), f = 4 gives 3.39 nights (stratum A); spent 76.6 core-h is over 1.5x the scenario,
  76.4 is not; < 300 decided escalates only with a DEADLINE-STOP. f = sum of min(t, 3600) over measured maps / sum of
  the (9,3) default-CaDiCaL pattern means (37, 80, 96, 103, 30 s; `(3,3)/(4)` excluded); A, B priced as N x mean x f.
* **Scenario move** ((10,4) exists / does not / cannot tell = 0.15 / 0.50 / 0.35): realized SAT -> exists 1; 0 SAT, all
  decided -> no move (UNSAT-SOLVER); > 1.5x scenario -> cannot tell back to 0.45 (review 2026-11-09 §8).
* **Outcomes**:
  * SAT: first-SAT stop of all shards (`first_sat.json`); the runner checks the model against the clauses and runs its
    hinge / two-stage / final-polynomial stages; then the follow-up tree. An OM model alone is not a result.
  * UNSAT-SOLVER: skips the map for this sweep; no negative claim (needs a DRAT replay).
  * TIMEOUT: no information; counted as censored.
  * near-miss: not applicable (exact formulas).
* **Follow-up tree** (week plan item 1; nothing starts without the owner): SAT -> exact model check, realization with
  the E-261103-04 saved-OM tools; realized -> `verify_candidate.py --target S5`, `candidate-check`; not realized in one
  session -> final polynomials and escalate. All decided, 0 SAT -> per-pattern table, price A and B with f; A + B <= 4
  nights -> propose stratum A nights (fastest maps first, same design), else Actions after item 2 if allowed. > 10 %
  censored -> no A/B proposal, escalate (LOW-YIELD at this cap for those patterns, not refuted).
* **Stop rule**: all 358 units recorded, the first SAT, a control failure (stop that root, escalate), or the 80 core-h
  cap; cap reached with < 300 decided -> stop, record, escalate.
* **STATUS / ROADMAP**: a new STATUS 3 entry with the per-pattern table and the verdict; the ROADMAP row to done; a SAT
  goes to `candidate-check` before any wording.

## Amendments
