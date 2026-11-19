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
