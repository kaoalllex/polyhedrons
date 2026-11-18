# E-261116-07: P3 v2 - one census-free formula per (F, E); unit tests, ladder L0-L3, bridge gate at eight faces

Pre-registration, 2026-11-17. Week item 3, the main investment (`ROADMAP.md`; dialogue 2026-11-16-strategy §2 row 3
and its decision tree, Appendix A1). Supersedes the 16b ladder (not run).

* **ROADMAP row / scores**: T 2 D 2 F 1 G 2 R 2 (T + D = 4). Explore, jump 2 via its tree.
* **Question**: does one CP-SAT formula without a given map decide the known S1 rungs correctly, and does one of its
  unpinned (8, E = 36) models realize to exact coordinates passing `--all-pairs`?
* **Hypotheses moved**: H-261101-07 only through the tree: a realized model is a method result at eight faces (a known
  genus); the nine-face run that could move H-261101-07 needs a new budget line from the lead.
* **H1**: L0-L2 agree with the archive and the ledger, and L3 yields a model realized and passing `--all-pairs`.
  **H0**: a control fails, or L3 yields no realized model within the cap.
* **Why**: a map census is out of reach at (8, 3) and (9, 4); the formula quantifies over maps and chirotopes at
  once (I-261103-02), the SAT form of Roest-Vigh's plane-only construction.
* **Method**: `p3.py` (new; blocks as A1, docstring). Host CP-SAT 9.15 (A1's risk note; the frozen engine is CP-SAT;
  cardinalities and levels are native), one worker per unit, no lazy cuts. Elements: faces 0..F-1, INF = F (omsat
  convention). Changes from A1, stated now: (a) the gauge indices are 0-based (sigma_m(0,1,2) = + for m >= 3,
  sigma_m(3,4,5) = + for m <= 2); (b) stage B also fixes chi(0,3,6,INF) = + (a reflection negates every sign and
  keeps the gauge; PROVED-1), so L3 counts chirotopes up to mirror; (c) stage B splits each rung into 16 cubes on
  chi(1,4,6,INF), chi(2,5,7,INF), chi(0,4,7,INF), chi(1,5,7,INF), each with 1/16 of the rung budget, so a budget stop
  is per cube; (d) L1's model also goes through the bridge (diagnostic, not a pass condition).
  Every model is read back by `decode` (pure Python: octant patterns, ends, runs ordered by chi, face cycles) and
  its chi by an independent GP check. Bridge: E-261103-03's frozen stages (hinge, two_stage, fp; six restarts, seed
  26110303), then `verify_candidate.py --all-pairs` on the saved file. Target S1 at F = 7, 8, 9; counters SPEC §4:
  CP-SAT status, UNSAT-SOLVER, `EMBEDDED`, `adjacent_pairs`.
* **Unit tests** (`test_p3.py`, run in development before this commit, all pass): pinch pattern {0,1,3,7} in ALLOWED
  and rejected; every admitted vertex pattern has 0 or 3 ends; pinned annulus (Euler 0, disk INFEASIBLE); pinned
  disk + annulus (Euler 1 passes, connectivity INFEASIBLE, a single rectangle connected); face cycles of the frozen
  engine's Roest-Vigh solid equal `decode`'s; an annulus is rejected by `decode`.
* **Stage A** (`run.sh stage_a`, session, eight processes):
  * L0 regression (not soundness): the 240 K13 arrangements (archive SHA-256 checked, not re-solved), chi pinned, E = 36,
    cap 60 s: OPTIMAL exactly on the 17 SOLID seeds, each `decode`d and `EMBEDDED` (24, 36, 8, -4) on its planes;
    Roest-Vigh, Mizhaev (E = 36) and the saved uniform perturbation of Szilassi (E = 21) OPTIMAL and `EMBEDDED`;
  * gauge reachability: Roest-Vigh and Mizhaev reoriented and mirror-normalised satisfy the stage-B formula of their cube;
  * L1: (7, 21) unpinned with the gauge, cap 1200 s: OPTIMAL, GP-valid, `decode`d to the K7 torus map.
* **Controls**: positive as above. Negative (must fail): raw Szilassi rejected as out of domain (zero signs); a
  tetrahedron at E = 7 INFEASIBLE; Roest-Vigh's chirotope with one GP-breaking sign flipped INFEASIBLE.
* **Stage B** (`launch.sh 16-07 start`, 10 shards, 48 units round-robin): L2 (8, 30) 16 cubes x 225 s and (9, 39) 16
  cubes x 450 s, one model each; L3 (8, 36) 16 cubes x 560 s (solve + bridge), enumerating with chirotope blocking
  clauses, at most 2 models per cube for 14 cubes and 1 for two (<= 30 distinct chirotopes).
* **Pilot**: stage B shard 0 with caps cut to 60 s per unit into `results/pilot/`: build and solve time per rung,
  the limit that ended each unit, model count and bridge time per L3 model.
* **Pilot gate**: the binding limit must be the per-unit cap or a decision, not the build; if an L3 pilot unit
  spends more than half its cap in the bridge, amend the bridge caps before stage B.
* **Predictions**: (P1) L1 OPTIMAL within its cap (~70 %); decision: L1 timeout is a budget stop, the tree's "repair or
  park". (P2) all 16 (8, 30) cubes INFEASIBLE in their caps (~50 %). (P3) all 16 (9, 39) cubes INFEASIBLE (~30 %).
  (P4) L3 yields >= 10 models (~50 %). (P5) >= 1 L3 model passes `--all-pairs` (~30 %); decision: the gate.
* **Grid**: one cap per rung; the outcome depends on the cap and is reported per cube with its time.
* **Budget**: <= 6 core-h: stage A <= 0.5 (L0, gauge, L1), pilot <= 0.1, stage B 16 x (225 + 450 + 560) s = 5.5
  core-h, 10 shards, about 35 min wall; laptop on AC under caffeinate, no night. Two sessions.
* **Power statement**: with 30 L3 chirotopes, a realizable-and-bridged share of 0.1 is detected with probability
  0.96; a smaller one is not. A miss proves nothing about realizability or the (8, 3) maps; L3 is a method test
  with two known objects inside the formula (gauge reachability).
* **Proofs**: none; every INFEASIBLE is UNSAT-SOLVER (no named negative claim; L2 repeats STATUS 3d's decisions).
* **Counter calibration**: no float diagnostic enters the verdict (CP-SAT status, exact signs, exact `verify`); the
  bridge's float losses never decide.
* **Scenario move**: none at nine faces from this run. Gate passed: the method can supply realizable models
  without a census (supports a nine-face run for A); a miss leaves A/B/C unchanged.
* **Outcomes and their meaning**:
  * L0 mismatch, failed unit test, gauge or negative control: encoder bug; repair once, then park with the cause.
  * L1 OPTIMAL with the K7 map: rung passed. INFEASIBLE: bug (Szilassi is in the domain). Timeout: budget stop.
  * L2 INFEASIBLE: UNSAT-SOLVER for this formula only (scope: uniform, cubic, one disk face per plane, the
    finite-vertex coverage lemma open). (8, 30) OPTIMAL: stop, decode, bridge, `candidate-check`, escalate (contradicts
    B2). (9, 39) undecided in its caps: budget stop, no forecast.
  * L3 all cubes INFEASIBLE: control failure (the gauge check put Roest-Vigh in one). Models, no bridge: "models without
    coordinates", with distinct maps as a diagnostic. A realized model: compared with Roest-Vigh and Mizhaev
    (`links_isomorphic` of K13, a weak necessary test); new or known, it is an (8, 3) S1 object, never S0 or S5.
* **Follow-up tree** (review §2): gate passed -> the nine-face run (E = 45, 51, 57: plain, C3, N2 cube, N3) goes to the
  lead for a budget line; models but no bridge -> after item 4, one capped coupled P3 + P4 recovery test at eight
  faces; no model -> park, cause recorded. Proof obligations stay with E-261116-09.
* **Stop rule**: a failed control twice; the stage-B caps; 6 core-h in total.
* **What changes in `STATUS.md` / `ROADMAP.md`**: a new STATUS section with the rung verdicts and the gate; ROADMAP
  row done (or parked with the cause) and the tree's next step.

## Amendments

### 2026-11-17: stage A passed, pilot recorded; no change

* Stage A (`results/controls/`, 39 s wall on eight processes): all PASS. L0 240/240 K13 verdicts matched (17 OPTIMAL
  and `EMBEDDED`); Roest-Vigh, Mizhaev, perturbed Szilassi OPTIMAL and `EMBEDDED`; raw Szilassi OUT-OF-DOMAIN; both
  negatives INFEASIBLE; gauge reachability: Roest-Vigh and Mizhaev both land in cube 5, OPTIMAL. L1 (7, 21) OPTIMAL
  in 8 s, GP-valid, K7 map; its bridge (hinge, 0.8 s) realized it and `--all-pairs` passed (a recovery, not new).
* Pilot (`results/pilot/0/`, shard 0 at 60 s per unit, 0.08 core-h): five units ((8, 30) c00, c10; (9, 39) c04,
  c14; L3 c08), build 0.3-0.9 s, every unit UNKNOWN at its 60 s cap; no model, so no bridge time.
* Gate: the binding limit is the per-unit cap, as intended; P2-P5 all keep a real chance of failing; every outcome
  is tied to a decision. Stage B runs as registered (caps 225 / 450 / 560 s); units ending at the cap are budget
  stops, not results.
