# E-261113-02: (10, 2) calibration rung - time to SAT over seeds and bridge realization rate

Pre-registration, 2026-11-13 (lab session, week item 2 of the owner-approved plan). No solver run before this commit.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (T + D = 3), explore, calibration. Origin I-261113-02.
* **Question**: on the rung where S6 SAT is known to occur, how fast does kissat find a model across maps and seeds,
  and how often does the SAT-to-coordinates bridge realize a model?
* **Hypotheses moved**: H-261110-03 only through planning: the readings below price the (10, 3) timeouts of
  E-261110-02 and the SAT handling of E-261113-01. No existence statement at (10, 3) follows from any outcome.
* **H1 / H0**: H1 (light): the median SAT time is below 60 s and no unit times out at 300 s. H0: a heavy tail.
* **Why**: 20/20 (10, 3) formulas timed out at 3600 s (STATUS 3af); without a time-to-SAT distribution at a
  comparable element count a timeout cannot be ranked; the bridge left 3 of 6 foreign (10, 2) models unrealized in
  the E-261110-02 prep.
* **Method**: Lutz's list `manifolds_lex_d2_n10_o1_g2.txt` (865 entries, untrusted data, downloaded 2026-11-13 from
  the archived Manifold Page, sha256 66012aea...67f1) parsed by `code/lutz_import.py` (only parsed). `make_queue.py`:
  50 maps by `random.Random(2611130201)`, plus the S6 (10, 2) witness map (Lutz #739, an end-to-end control), each
  with kissat seeds 0, 1, 2 (`--seed`, one formula record per seed; the CNF is the same) -> 153 units. Formula and
  SAT handling as E-261110-02: E-261103-03 `tranche.py` imported-map mode, `submap_formula` (`submap=True`,
  `ALL_OPTS`), kissat rel-4.0.4, no proofs, solver cap 300 s; every SAT model through `tranche.bridge` (hinge,
  two_stage, fp, restarts 6, 120 s each, frozen settings) and `verify_candidate.py --target S6`. One code change:
  `tranche.unit` passes the record's `seed` to kissat. Counters (SPEC §4): SAT / UNSAT-SOLVER / TIMEOUT per unit,
  solver and bridge seconds; realized = EMBEDDED and `--target S6` PASS.
* **Controls**: importer: closed, orientable, simplicial, (10, 36, 24), 865 pairwise non-isomorphic (passed while
  freezing the input; this run is the first import of this list); the witness map is found in the list (#739).
  Positive: the three #739 units SAT; the witness itself passes `--target S6` (`verify_all.py`). Shard controls:
  convex f10 pinned positive SAT, its swapped-map negative UNSAT-SOLVER. Code change: with no `seed` the formula and
  options are unchanged (`test_tranche`), and the seed reaches the solver command line (pilot solver logs).
* **Pilot**: `queue_pilot.json`, 2 shards: shard controls, #739 and #17 (the first drawn map), three seeds each, cap
  300 s. Reports per unit the limit that ended it, and whether the seeds change the model (diversity check).
* **Pilot gate**: binding limit = the 300 s cap or completion. The run starts if every control passes and the
  projection from the pilot is <= 3 core-h. If the three seeds give identical models and times on both maps, the
  seed does not diversify kissat: an amendment replaces it by a seeded clause/variable shuffle before the run.
* **Predictions**: (P1, ~60 %) the median SAT time is below 60 s; (P2, ~50 %) no unit times out (LIGHT needs both);
  (P3, ~60 %) the bridge realizes >= 50 % of SAT models; (P4, ~70 %) the drawn units take under 0.3 core-h.
* **Grid**: one setting; the seed is the replicate, the cap is fixed by the reading (300 s).
* **Budget**: 1 prep session + <= 3 core-h, 10 shards, laptop, launched by the owner (with E-261110-05 in one
  queue). The runner reserves 10 core-h as a hard ceiling (per-unit margins of 300 s + 360 s bridge); a pilot
  projection above 3 core-h cuts the queue by amendment before launch.
* **Power**: 50 maps x 3 seeds estimate the median within about +-15 % and detect a tail fraction of ~5 % of units;
  an UNSAT-SOLVER unit says only that its formula is likely UNSAT; nothing here bears on (10, 3) existence.
* **Proofs**: none (owner, 2026-11-13). **Calibration** (`summary.py --selftest`): median 59 s LIGHT / 61 s not;
  seed spread (max >= 60 s and >= 10 x min) on 5 of 50 maps HEAVY-TAIL / 4 not; one SAT + TIMEOUT map HEAVY-TAIL;
  bridge 50 % no escalation / 48 % escalation; 0.25 / 0.33 core-h on each side of the 0.3 core-h rule.
* **Scenario move**: none ("(10, 3) exists" 0.25 unchanged; the run prices methods, not existence).
* **Outcomes**: SAT units: timing data; a realized model is a control object (`--target S6` PASS), not a headline,
  and never an S0 or S5 object. UNSAT-SOLVER: a map with likely no S6 sub-map formula model, counted, no claim.
  TIMEOUT: the tail. Near-miss: not applicable.
* **Follow-up tree** (`summary.py` readings): HEAVY-TAIL (checked first) -> propose a seed-portfolio day run on
  (10, 3) to the owner; LIGHT -> the (10, 3) timeouts read "probably UNSAT" for planning, never a claim; route =
  week item 4; neither -> record. Bridge < 50 % -> E-261113-01's SAT follow-up takes more models per SAT. Drawn
  units under 0.3 core-h -> the full 865 x 3 seeds in the same budget, one owner launch (queue rebuilt by
  `make_queue.py`, no new amendment). A failed control stops the shard; escalate.
* **Stop rule**: all 153 units recorded, a failed control (importer or shard), or the cap.
* **STATUS / ROADMAP**: a STATUS 3 section (distribution, bridge rate, readings); ROADMAP row to done; the reading
  goes to "For the lead" when it changes a route.

## Amendments

### 2026-11-13: amendment 1, pilot (prep session)

`prep/pilot` (2 shards, `run.sh` with `QUEUE=queue_pilot.json`, 48.8 core-s): shard controls SAT / UNSAT-SOLVER; all 6
units SAT, solver 0.2-3.6 s (ended by completion); the seed reaches kissat (`seed=1`, `seed=2` in the solver logs) and
the six models are pairwise distinct, so the seed diversifies (no shuffle amendment). Bridge: 0 of 6 realized, the
three #739 models included (`SAT-NOT-REALIZED`; fp FEASIBLE on 5, NONREALIZABLE-NUMERICAL on 1); about 3 s per model.
The hinge stage returns the same loss from all 6 random starts on each model (one attractor), so its restarts add
nothing here; two_stage restarts vary (64-121 of 715 signs wrong). The G3 realization of E-261110-02 came from one
two_stage restart. Projection: 153 units x ~6 s plus controls ~0.3 core-h, far below 3 core-h; the cap does not bind.
Gate met (controls pass; P3 is at risk). Startup: the pilot ran the owner's `run.sh`; the `launch.sh` path is the one
E-261113-01 used, not re-exercised. Launch: owner, together with E-261110-05.
