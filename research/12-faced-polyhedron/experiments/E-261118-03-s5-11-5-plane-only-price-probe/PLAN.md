# E-261118-03: (11, 5) plane-only price probe

Pre-registration, 2026-11-19 (lab session, week item 4 of the owner-approved plan). No solver run before this commit.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3), explore, J 2. Origin I-261117-02, I-261116-04,
  E-261117-02, E-261116-01. New compared with E-261116-01 (plain normalised formulas, all censored at 3600 s):
  plane-only C2 symmetry clauses in a moved chart, which no (11, 5) run has used (E-261116-06 withdrawn unrun).
* **Question**: does the plane-only C2 formula decide an (11, 5) Aut+ = 2 map fast enough to price the 20 such maps
  into one laptop night?
* **Hypotheses moved**: H-261101-07 ((11, 5) part) only by a verified `--target S5` candidate; otherwise planning.
* **H1 / H0**: H1: both maps have a median over four kissat seeds <= 360 s (SAT or UNSAT-SOLVER). H0: at least one
  map stays near the 12-element baseline (E-261116-01 sample median >= 3597 s, censored).
* **Why**: a half-turn halves the free signs; E-261117-02 showed the moved chart makes a fixed-face half-turn
  admissible for uniform formulas (gate passed at seven planes). Eleven faces admit no free C2 or C3, so every
  symmetric (11, 5) object has a fixed-face involution (PROVED-1, `reviews/dialogue-2026-11-16-strategy.md`).
* **Method**: `make_queue.py` recomputes the orientation-preserving automorphisms of the 20 admissible Aut+ = 2 maps
  of the E-261116-01 census from their links (each: exactly one involution, exactly one fixed face; 20 of 20) and
  draws two by `random.Random(2611180301)`: census 3634 (fixes face 8) and 4096 (fixes face 6), both extra pattern
  [1, 1, 1, 1]. Each map x kissat seeds 0-3 = 8 units. Formula: E-261103-03 `tranche.py` imported-map mode,
  `submap_formula` -> `omsat_sym.build_sym` (cyclic group of the involution, det +1, orbit-flip and mirror gauge,
  no `symbreak`), `ALL_OPTS` plus `sym_planes_only` (symmetry clauses on plane quadruples only; INF a generic plane;
  no forced zero on any plane quadruple, checked). About 20 000 variables, 294 000 clauses. kissat, cap 1800 s, no
  proofs; every SAT model through `tranche.bridge` (hinge, two_stage, fp, 120 s each) and `verify_candidate.py
  --target S5`. One code change: `submap_formula(..., planes_only)` reads the record's `sym_planes_only`; without
  it the formula is unchanged (`test_tranche`, 28 OK). Target S5 (11, 5). Counters (SPEC §4): SAT / UNSAT-SOLVER /
  TIMEOUT per unit, solver seconds, the per-map median (TIMEOUT = +inf), bridge status.
* **Controls**: N2 Szilassi chain through the runner (`queue_control.json`, 10 shards, cap 60 s): Szilassi's map
  (coherent links, Aut+ 42, the half-turn G_SZ fixing face 5) plane-only, seeds 0-3, must be SAT with the bridge
  realizing at least one model and `--target S5` PASS ((7, 1) is S5); the standard-chart formula (INF fixed, forced
  zeros), seeds 0-5, must be UNSAT-SOLVER. Shard controls in `queue.json`: convex f11 pinned SAT, its wrong map
  UNSAT-SOLVER. Pinned K4 and gauge reachability are reused from E-261117-02 (`test_n2.py` in `verify_all`).
* **Pilot**: the control chain, then `queue_pilot.json` shards 0 and 4 (both maps, seed 0, cap 120 s): build time,
  runner path, the seed on the kissat command line.
* **Pilot gate**: the control chain passes (else repair: kill rule of the row). Binding limit in the run: the
  1800 s cap. The run starts when the controls pass; an outcome at 120 s is recorded and the full run still runs.
* **Predictions**: (P1, ~75 %) CLOSED: at least one map has a median > 360 s; (P2, ~35 %) at least one of the 8
  units decides within 1800 s; (P3, ~85 %) the control chain passes in the pilot.
* **Grid**: one setting; the seed is the replicate, the cap is fixed by the row.
* **Budget**: <= 4 core-h solver (8 x 1800 s), plus controls and the bridge only on SAT (<= 0.8 core-h); 10 shards
  (shards 8, 9 run controls only: `launch.sh` default), about 40 min wall, laptop on AC, launched by the owner.
  The 36 000 s in `run.sh` is the runner's reservation ceiling, not the plan budget.
* **Power**: two maps x four seeds price the formula on two of 20 maps; they cannot rank the other 18 or bear on
  plain (11, 5) maps. UNSAT-SOLVER: likely no realization of that map whose chirotope is invariant under the
  involution in some generic chart (plane-only is a relaxation of a symmetric solid); nothing for asymmetric
  realizations. TIMEOUT: no information.
* **Proofs**: none (owner, 2026-11-13). **Calibration** (`summary.py --selftest`): medians 359 / 361 s on each side
  of the gate; one TIMEOUT of four still passes, two fail; the cap (1800 s) is above the threshold, so the clamp
  cannot pass the gate. No float geometric diagnostic enters the verdict.
* **Scenario move**: none for S0 (A / B / C unchanged); a verified (11, 5) S5 object moves H-261101-07, not S0.
* **Outcomes**: SAT: bridge; realized with `--target S5` PASS -> CANDIDATE-NEEDS-REVIEW -> `candidate-check`,
  escalate (Opus high / gpt-6-astra high); not realized -> SAT-NOT-REALIZED, a model for the lead, no claim.
  UNSAT-SOLVER: that map's plane-only formula, scope as in Power. TIMEOUT: no information. Near-miss: n/a.
* **Follow-up tree** (`summary.py`): NIGHT (both medians <= 360 s) -> the 20 maps x the same seeds in one owner
  night (<= 80 core-h) by an amendment that only rebuilds the queue; CLOSED -> (11, 5) closes for the laptop, no
  further (11, 5) item; CANDIDATE -> `candidate-check` first, the gate reading waits.
* **Stop rule**: all 8 units recorded, a failed control, a verified candidate (the runner stops), or the cap.
* **STATUS / ROADMAP**: a STATUS 3 section (statuses, medians, reading); ROADMAP row and week item 4 to done; the
  reading goes to the strategy line ((11, 5) one probe, then a night or closed).

## Amendments

### 2026-11-19: amendment 1, pilot (lab session)

* **Control chain** (`prep/control`, `queue_control.json` through `run.sh`, 10 shards, about 10 s each): Szilassi
  plane-only seeds 0-3 SAT (0.04-0.06 s), every model realized by the bridge, `--target S5` PASS, (14, 21, 7, 0)
  (the known Szilassi type, a control object); standard chart seeds 0-5 UNSAT-SOLVER. The seed reaches kissat.
  Shard controls (convex f11 pinned SAT, wrong map UNSAT-SOLVER) pass. Gate met; kill rule not triggered.
* **Pilot** (`prep/pilot`, `queue_pilot.json`, shards 0 and 4, cap 120 s): map 3634 seed 0 UNSAT-SOLVER in 35.9 s,
  map 4096 seed 0 UNSAT-SOLVER in 28.7 s (formula build under 1 s; shards 44 s and 37 s wall). Ended by completion,
  not by the cap.
* **Added control** (fast UNSATs of a new encoding are suspect): `controls_12.py`, for each drawn map 5 random
  integer plane sets symmetric under the half-turn acting as the map's involution, moved by `n2.chart`, brought to
  the `build_sym` gauge and pinned into the map's formula with only GP + symmetry + gauge clauses: must be SAT, and
  the unpinned formula SAT. Result (`prep/controls_12.json`): 10 of 10 pinned SAT, both unpinned SAT. So the
  symmetry and gauge clauses at 12 elements admit genuine symmetric configurations; the UNSATs come from the
  embedding clauses. Not covered: a positive control with a fixed-face involution on a map with doubled pairs
  (no such object is known); the mirror normalisation is inherited from `omsat_sym` (E-261103-02), not re-checked.
  `controls_12.py` reruns in the full run's session before the reading.
* **Projection**: 8 units x about 30-40 s plus controls, about 0.15 core-h, a few minutes wall; the cap does not
  bind. The run is therefore made in this session by the owner's launcher (`overnight/launch.sh 18-03 start`), not
  as an owner night; budget, units, caps and readings unchanged.

### 2026-11-19: amendment 2, the NIGHT follow-up (lab session)

* **Run** (`results/run`, `launch.sh 18-03 start`, 10 shards, controls pass): 8 of 8 units UNSAT-SOLVER, map 3634
  36.6-49.4 s (median 40.2 s), map 4096 40.4-48.4 s (median 41.7 s); 0.094 solver core-h. `summary.py`: NIGHT.
* **Follow-up, as registered**: the other 18 Aut+ = 2 maps x kissat seeds 0-3 (72 units), same formula, caps,
  controls and bridge; only the queue is rebuilt (`make_queue.py` -> `maps/formulas_rest.json`, `queue_rest.json`,
  sha256 a0469036...5734; the probe's queues are unchanged). `run.sh` now defaults to `queue_rest.json`, results in
  `results/rest`. Kissat takes the last `--seed` when the runner accumulates them in a shard (checked).
* **Projection**: 72 x about 45 s, about 0.9 core-h, under 10 min wall on 10 shards, far below the registered
  80 core-h; made in this session by the owner's launcher, as amendment 1 argued.
* **Readings**: per map and seed SAT / UNSAT-SOLVER / TIMEOUT. All 20 maps UNSAT-SOLVER on every seed -> the
  plane-only C2 slice of (11, 5) is UNSAT-SOLVER for planning (no proof, never "no symmetric (11, 5) object");
  any SAT -> bridge, `--target S5`, `candidate-check`; TIMEOUTs are reported per map, no information.
