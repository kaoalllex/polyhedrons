# E-261107-01: nine-plane solid-first target pilot

Pre-registration, 2026-11-07, branch `lab/2026-11-07`. Week plan item 1 (`ROADMAP.md`). Explore run at the focus
target S5 (F = 9, g = 3), `STRATEGY.md`. A solid found here is an S5 candidate only after `verify_candidate.py
--target S5` PASS and `candidate-check`; nothing is claimed before.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2 (T + D = 4), as the parent E-261103-05.
* **Question**: does the disk-aware CP-SAT hard-decision engine find an embedded 9-face solid with all 36 pairs
  adjacent from uniform arrangements of 9 planes?
* **Hypotheses moved**: H-261103-02 (free-C3 (9,3) existence) and H-261101-07 (maximal genus-3 existence). A SOLID
  raises both; a miss moves neither (the pilot samples a few arrangements, not a family).
* **H1**: at least one sampled arrangement of 9 planes admits a 36-pair embedded solid, found in the cap. **H0**:
  none does, at this cap and sample. Prior is low; the pilot buys the per-seed solve time and the pair-count profile.
* **Why this configuration**: the engine recovered both known (8,3) objects and one random D2 (8,3) solid in about 1 s
  per solve (E-261103-05). Different from that run: nine planes, E = 39 (V = 26, chi = -4), 36 pairs, the three
  families below, never the 8-plane catalogue. Parked methods are not rerun.
* **Method**: `nine.py` (imports the committed E-261103-05 `pilot.py` helpers and `solid_cpsat.best_solid` /
  `solid_fast.Tables`, unchanged). Phase A per unit: hard decision, `target_edges=39`, `max_runs=3` (three disjoint
  shared segments per pair suffice at F = 9, parent CONCLUSION), one CP worker, cap 180 s. Phase B only if A is
  INFEASIBLE or times out: `best_solid(max_runs=3)` maximising adjacent pairs, 60 s, **diagnostic only** (raw
  solver count, not exact-verified). Exact check of any SOLID: `ladder_exact.verify(require_all_pairs=True)`.
* **Families** (uniform integer planes, exact arrangement; draws rejected by `arrangement` if degenerate, count
  recorded): `c3` three orbits of the cyclic coordinate shift (C3 of the arrangement, not of the solid); `d2p1` two
  D2 orbits of 4 plus one generic plane (a pure D2 orbit set cannot have 9 planes; no symmetry of the solid is
  assumed); `rand` nine random planes. Seeds 0..9 per family: 30 units. Fixed-face C2/D3 families are outside the
  uniform builder and are not run.
* **Controls**: positive (must succeed): Roest-Vigh and Mizhaev own planes, E = 36, 60 s, exact EMBEDDED with the
  known map, then Phase B on the same planes reports 28 pairs. Negative (must fail): tetrahedron with E = 7 and the
  seed-0 `c3` nine planes with E = 33, both INFEASIBLE (36 pairs need 36 edges). Any control miss stops the run
  (`CONTROL-FAILED`) and escalates; nothing is inferred about nine planes.
* **Counter calibration**: the only float-free diagnostic in the verdict is the Phase B pair count. It is checked
  at one saturation point only: 28 (Roest-Vigh and Mizhaev, expected). A pair count below the maximum has no
  calibration control; it is reported, never used as a verdict,
  and trusted only after an exact check of its solid (follow-up tree).
* **Pilot / gate**: the first measured quantity is the Phase A time on nine planes. Per unit the log records the
  ending status, `ended_by` and wall fraction of the cap. If most units end `solver_timeout` at 180 s, the verdict
  `NO-36-PAIR-SOLID` is UNDERPOWERED (a timeout is not a result), and a longer cap needs the lead.
* **Predictions**: (1) all four controls behave as stated (~90 %). (2) At 9 planes most INFEASIBLE units finish
  inside the cap (~50 %; the 8-plane ones took about 1 s but the cell count grows fast). (3) No SOLID in 30 units
  (~85 %).
* **Grid**: family x seed is the sampled parameter; the cap is fixed at 180 s because the question is the per-seed
  solve time. No cap grid in this pilot.
* **Budget**: <= 2 core-hours, one shard, laptop, `WORKERS` <= 10 (about 15 min wall on 10 cores). Worst case:
  controls 4 x 2 min plus 30 x (180 + 60) s = 2.1 core-h upper bound, expected well below. Not a night.
* **Power statement**: detects a 36-pair solid only on these 30 arrangements. It cannot detect a solid that needs
  another symmetry, a fixed-face C2/D3 family, a longer cap or a different arrangement; INFEASIBLE holds only for
  that exact CP model at those planes (parent scope: re-solved, not DRAT).
* **Scenario move**: SOLID (after S5 PASS): A (exists) up sharply, owner informed at once. No SOLID with
  completed INFEASIBLE units: no change (sample, not a family). Timeouts: no change.
* **Outcomes**: SOLID -> exact verify, `--target S5`, `candidate-check`. INFEASIBLE units -> UNSAT of the saved model
  at those planes, no geometric family exclusion. timeout/UNKNOWN -> no information. near-miss (Phase B pairs) ->
  diagnostic only.
* **Follow-up tree** (allowed without a new amendment): any embedded output -> `verify_candidate.py --target S5` +
  `candidate-check`; >= 1 output with >= 33 pairs (exactly checked) -> one seed grid on that symmetry as an owner
  night (10 cores, <= 8 h, skill `overnight-run-script`); engine failure on its own 8-plane controls -> stop and
  escalate (line under "For the lead").
* **Stop rule / kill**: all 30 units decided or timed out, or 2 core-h. No 36-pair solid in budget -> park this
  configuration; keep the best pair count per seed as a diagnostic only.
* **STATUS / ROADMAP changes**: a new ROADMAP row (state running, then done); one STATUS section after the
  conclusion; E-261103-05 row unchanged.

## Amendments
