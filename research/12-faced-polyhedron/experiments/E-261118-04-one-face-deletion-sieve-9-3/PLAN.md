# E-261118-04: (9, 3) one-face deletion sieve

Pre-registration (2026-11-18), at most 80 lines. Amendments at the end.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3); week item 1, explore, J 0.
* **Formula (owner's choice, 2026-11-18, option (a))**: the README asks for "every condition on S's plane removed".
  Two readings were put to the owner. Removing plane S (8 planes + infinity) drops almost everything but GP at
  (9, 3): S is adjacent to all eight faces and IN / REFLEX / RTURN of every face read its edges e_XS. A true curved
  face (free vertices on the lines L_XY, a non-uniform chirotope) needs a new encoder; it goes to the lead. This run
  is the k-face mechanism of E-261101-23 on the S5 encoder: **plane S stays an element; the own conditions of the
  polygon F_S are dropped** (TRIPLE on non-triangles containing S, INCONS with S as the in-face, RFCONS and POC of S,
  REFLEX1 on triangles containing S). Kept: GP, SEGMENT_DISJOINT, and every condition of the other eight faces,
  whose edges with S stay on the lines L_XS. A model is a **planar but possibly defective face S** (self-crossing,
  pierced, bad corners) on eight correct faces, not a curved face.
* **Question**: for which admissible (9, 3) maps and faces S is the deleted formula SAT, i.e. does the (9, 3)
  obstruction (STATUS 3d) need the conditions of one particular face?
* **Hypotheses moved**: H-261101-07. All UNSAT-SOLVER: the obstruction is robust, it does not sit in one face's
  polygon (planning only). SAT: the obstruction of that map needs the conditions of F_S.
* **H1 / H0**: H1 = some (map, S) is SAT; H0 = all 1827 UNSAT-SOLVER.
* **Method**: `sieve.py` (`build_deleted`, a family-by-family mirror of `omsat.build` with ALL_OPTS split into a kept
  and an own phase), `pilot.solve` of E-261103-03 with kissat 4.0.4 (`$HOME/bin/kissat`, SHA-256 in each manifest),
  NO_PROOF=1, cap 300 s. Units: the 203 admissible maps of `maps_9_3.json` x 9 faces, map-major, unit k on shard
  k mod 10. Target S5 (9, 3), relaxed; counters (SPEC §4): status per unit, solver seconds, budget fraction.
* **Encoder checks (`test_sieve.py`, run in this commit)**: S = None gives `omsat.build`'s CNF exactly (a (9, 3) map
  and Roest-Vigh); for every S the deleted CNF is a prefix of the two-phase full CNF, whose variable count, clause
  count and family counts equal `omsat.build`'s (monotonicity by construction); TRIPLE and POC survive deletion.
* **Controls** (`sieve.py --controls`, cap 300 s): positive, Roest-Vigh's (8, 3) planes pinned on each of its 8
  deleted formulas: SAT; negative, the same with plane 0 shifted (rhs + 259 on the x100 planes, uniform): UNSAT for
  all 8; negative, the full formulas of maps 29, 66, 20 (UNSAT-VERIFIED in E-261103-03, 29-31 s with CaDiCaL): UNSAT.
* **Counter calibration**: the only diagnostic is the Eval violation count of `build_deleted`: 0 on Roest-Vigh's
  planes for every S, > 0 on the shifted planes for every S (both sides in `test_sieve.py`). Solver statuses are exact.
* **Pilot** (minutes): the controls, then shard 0 with `--limit 9` (map 0, all faces). Exposes: deleted formulas
  much slower than the full ones, an encoder slip the unit tests miss, kissat interface faults.
* **Pilot gate**: per unit the ending limit (decided / cap) and the budget fraction; the projected core-hours of the
  1827 units from the pilot's median and timeout share. Start the long run only if the projection is <= 1 core-h,
  or the owner approves the stated price; otherwise amend (face orbits under Aut, fewer maps) before any run.
* **Predictions**: (P1) the controls pass (0.95); (P2) median deleted solve time above the full formula's (0.6),
  so 1 core-h covers only part of the 1827; (P3) at least one SAT among the decided units (0.4).
* **Grid**: one cap (300 s, the row's); the sieve's question does not depend on a parameter beyond the face S.
* **Budget**: <= 1 core-h, 10 shards x 360 solver-s each (`BUDGET`), laptop, one launch of minutes to an hour.
* **Power**: decides what kissat decides in 300 s per formula; units cut by the cap or the budget carry no
  information; the recorded coverage is part of the result.
* **Proofs**: none. Every UNSAT is UNSAT-SOLVER (ranking only); no negative claim is made from this run.
* **Scenario move**: all UNSAT-SOLVER: B +0.01 at most (the (9, 3) obstruction is not local to one face); SAT: neutral
  on A, B, C until the lead prices a follow-up; mostly timeouts: none.
* **Outcomes**:
  * SAT: model saved (`map<i>_del<S>.model.json`), checked against the clauses. The planar-but-defective S is a
    relaxation object, never an S5 candidate. Record the map / face pattern; in the session, the bridge of
    E-261103-03 on one model (9 planes realized, the eight other faces checked); then the lead.
  * UNSAT-SOLVER: the deleted formula's scope only; ranking information, no exclusion.
  * TIMEOUT / budget cut: no information.
  * near-miss: not applicable (no float search).
* **Follow-up tree**: a SAT: the bridge on at most 3 models (session, minutes); nothing else without the lead.
  All UNSAT-SOLVER or timeouts: conclude, go to week item 2. The curved-face encoder: "For the lead" (owner, 2026-11-18).
* **Stop rule**: all 1827 units recorded, or each shard's 360 s budget spent.
* **STATUS / ROADMAP**: E-261118-04 row to done with its verdict and coverage; STATUS 3d one line (scope: deleted
  formulas, UNSAT-SOLVER); I-261118-04 keeps open status (the curved face is untested).

## Amendments

* 2026-11-18 pilot (session, kissat 4.0.4, NO_PROOF, cap 300 s; `results/pilot-controls`, `results/pilot`,
  `results/pilot29`). Controls pass: Roest-Vigh pinned SAT for all 8 deleted faces, shifted planes UNSAT-SOLVER for
  all 8, full formulas of maps 29, 66, 20 UNSAT-SOLVER in 28 / 31 / 20 s. Map 0 (its full formula timed out at 60 s in
  E-261103-03): all 9 deleted formulas TIMEOUT at 300 s. Map 29 (full 28 s): faces 5 and 8 SAT (2.9 s, 0.4 s), faces
  0-4, 6, 7 UNSAT-SOLVER in 53-174 s. Bridge (two-stage, then hinge, 120 s, 6 restarts): neither model realized
  (best 1 and 4 wrong signs, `map29_del{8,5}.bridge.json`). P1 held; P2 held (deleted formulas slower than full);
  P3 held (SAT on the second map tried). **Pilot gate failed**: map 0 spends 2700 s and map 29 770 s, so the 1827
  units project to 40-150 core-h, against <= 1 core-h. No long run without the owner's decision on the price.
