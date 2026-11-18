# E-261118-01: N1b, the five unrealized face-transitive (8, 3) classes

Pre-registration (2026-11-18), at most 80 lines. Amendments at the end.

* **ROADMAP row / scores**: T 2 D 1 F 2 G 1 R 2 (T + D = 3); week item 2, exploit, J 0.
* **Question**: is any of the five face-transitive (8, 3) classes of E-261117-01 other than Roest-Vigh's (class 0)
  SAT at formula level, and does the bridge realize a model as eight mutually adjacent faces?
* **Hypotheses moved**: H-261101-07. A realized, `--all-pairs` PASS class: a third eight-face S1 object (supports
  the symmetric route; rung control for E-261118-02). All UNSAT-SOLVER: none (formula scope, planning only).
* **H1 / H0**: H1 = some class 1-5 has a SAT formula; H0 = all its formulas UNSAT-SOLVER.
* **Why**: the census (E-261117-01, STATUS 3au) gives exactly six face-transitive (8, 3) classes (Aut+ 8, 24, 8, 8,
  8, 8; classes 4, 5 reflexible); only class 0 is known realized. At 9 elements the formulas take seconds to minutes.
* **Method**: `n1b.py`, `pilot.build` / `pilot.solve` of E-261103-03, kissat 4.0.4 (`$HOME/bin/kissat`, SHA-256 in
  each manifest), NO_PROOF=1, cap 600 s. Formulas: plain (`ALL_OPTS`) and normalised (`ALL_OPTS` + `symbreak` +
  `mirror`, soundness E-261114-01 `SOUNDNESS.md`, PROVED-1). **Deviation from the row (ten formulas)**: the census
  classes are up to reflection (`canon` minimizes over both orientations) and the encoder's invariance under
  reversing every link is not proved (the CNFs differ syntactically; Roest-Vigh's mirrored planes satisfy the plain
  formula of the reversed links, a single instance). So the mirror map of each chiral class (0-3) runs too: 20
  units, class-major, unit k on shard k mod SHARDS. Target S1 at eight faces (genus 3 reported; (8, 3) is below the
  S5 maximum F = 9 at g = 3, so never S5 or S0). Counters (SPEC §4): status per unit, solver seconds, budget fraction.
* **Bridge** (every SAT, in the shard): the checked model through E-261103-03 `hinge` then `two_stage` (6 restarts,
  120 s each, `submap=False`, so the geometry check requires all pairs adjacent); EMBEDDED -> the saved planes through
  `verify_candidate.py FILE --all-pairs`. One model per SAT formula.
* **Unit tests (`test_n1b.py`, run in this commit, 5 OK)**: 20 distinct units, class 0 first, reflexible flags as
  recorded; mirror links parse as a map; Roest-Vigh's planes give 0 violations on his plain formula, and his mirrored
  planes 0 on the reversed links; exactly one gauge representative of his planes (reorientations x z-reflection)
  meets the normalised units, with 0 violations; his planes violate the plain formula of each class 1-5.
* **Controls** (`n1b.py --controls`, cap 600 s): positive, Roest-Vigh's planes pinned on his own map (plain) and their
  gauge representative pinned on the normalised formula: SAT; negative, his planes pinned on the plain formulas of
  classes 1-5: UNSAT-SOLVER. In-run positive: class 0 (both orientations, both formulas) unpinned SAT.
* **Counter calibration**: the Eval violation count (0 on Roest-Vigh's planes and gauge, > 0 on the other classes,
  both sides in the tests). The bridge's `wrong_signs` is an integer; a failed bridge decides nothing, and class 0's
  bridge outcome is recorded as its calibration (the known OM is one of many models).
* **Pilot** (minutes): the controls, then shard 0 (units 0 and 10: class 0 map plain, class 2 mirror plain) at the
  full cap. Exposes: kissat or multi-adjacency faults, a class 0 that is not SAT, a bridge crash.
* **Pilot gate**: per unit the ending limit and budget fraction; the projected cost of the 18 other units. Hand the
  remaining shards to the owner only if the controls pass, class 0 is SAT and the projection is <= 0.2 core-h;
  otherwise amend or ask the owner for the price.
* **Predictions**: (P1) controls pass and class 0 SAT in both formulas (0.95); (P2) every unit decided within the cap
  (0.8); (P3) every class 1-5 formula UNSAT-SOLVER (0.7); (P4) class 0's single model realized by the bridge (0.4).
* **Grid**: one cap (the row's 600 s); the question depends only on the class and orientation.
* **Budget**: expected <= 0.2 core-h (row); hard limit `BUDGET` 1200 solver-s per shard x 10 shards, plus <= 240 s
  bridge per SAT unit; laptop, owner launch (minutes).
* **Power**: decides what kissat decides in 600 s per formula; TIMEOUTs carry no information and are listed.
  One bridge model per SAT formula: a failed bridge is not a non-realizability statement.
* **Proofs**: none. Every UNSAT is UNSAT-SOLVER; no negative claim is made from this run.
* **Scenario move**: a realized class: A +0.01 (the symmetric eight-face route has a second member); all UNSAT-SOLVER
  or timeouts: none.
* **Outcomes**:
  * SAT: model saved and clause-checked; an OM model of that formula, not a polyhedron. Bridge as above; EMBEDDED and
    `--all-pairs` PASS -> `candidate-check` before any claim, then escalate (Opus high). Not realized: listed with
    `best_wrong_signs`; to the lead.
  * UNSAT-SOLVER: that formula only (plain or normalised, that orientation); ranking information, no exclusion.
  * TIMEOUT / budget cut: no information.
  * near-miss: not applicable (exact statuses only).
* **Kill**: a failed control or class 0 not SAT -> stop and repair (encoder or input).
* **Follow-up tree**: a realized class 1-5 with `--all-pairs` PASS: `candidate-check`, then the lead (rung control for
  E-261118-02). SAT unrealized: at most 3 more models per formula through the bridge in the session (minutes); nothing
  else without the lead. All UNSAT-SOLVER: conclude, go to week item 3.
* **Stop rule**: all 20 units recorded, or each shard's budget spent.
* **STATUS / ROADMAP**: row to done with the verdict and coverage; one STATUS line (formula scope); B7 of the paper
  outline gets the six-class formula statuses.

## Amendments
