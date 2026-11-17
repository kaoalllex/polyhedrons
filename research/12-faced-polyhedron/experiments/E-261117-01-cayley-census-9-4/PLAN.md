# E-261117-01: Cayley census of face-transitive cubic (9, 4) maps, each decided

Pre-registration, 2026-11-17. Week item 1 (`ROADMAP.md`; dialogue 2026-11-16-strategy §2 row 1, Appendix A3).

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2 (T + D = 4). Exploit, jump 2.
* **Question**: which cubic nine-face genus-4 maps with every face pair adjacent have Aut+ transitive on the faces,
  and is the plain formula (10 elements) or a uniform free-C3 formula of any of them SAT?
* **Hypotheses moved**: H-261101-07 (genus 2-5 objects with few doubled pairs). A verified nine-face S1 object of
  genus 4 supports it at (9, 4); UNSAT-SOLVER or TIMEOUT on every formula leaves it unchanged (no negative result).
* **H1**: some face-transitive (9, 4) map has a SAT formula. **H0**: none has (or none exists).
* **Why**: face transitivity forces a Sylow 3-subgroup of order 9 acting regularly (PROVED-1 sketch, A3), so the
  maps are Cayley maps of Z9 or Z3 x Z3: a complete list of one natural S1 slice without the full (9, 4) census.
* **Method**: `cayley.py` (dual map = vertex-regular triangulation; slots = the eight non-identity elements plus one
  inverse pair repeated, valency 10; every slot involution; every rotation). Two independent enumerations: `brute`
  over all 9! cyclic orders per labelling (the raw count) and `by_phi` from the face permutation phi = rho o iota
  (3-cycles with product e, fixed points of order 3). Each raw rotation -> `TriMap`, the census `check` (K9, loopless,
  genus 4, connected) and `admissible` (no repeated triple); classes by the census canonical code (mirror identified).
  Rung below: the five groups of order 8, valency 9, (8, 3). Then `formulas.py` (stage B) on each admissible (9, 4)
  class: one uniform free-C3 formula per Aut+-conjugacy class of free C3 subgroups (`build_sym`, as E-261103-03),
  then the plain formula (`build`, ALL_OPTS); kissat, no proofs. Target S1 at nine faces (genus 4 reported, never S5
  or S0). Counters: SAT / UNSAT-SOLVER / TIMEOUT / NOT-RUN per formula; raw, valid, admissible, distinct per stage.
* **Controls** (all before targets; any failure stops the run):
  * enumerator, positive and negative, against the independent census E-261103-01 (`test_cayley.py`): Z7 gives
    exactly the one K7 class; the five groups of order 12 give exactly the K12 census classes whose Aut+ (order 12)
    acts freely on vertices (done in development: one class, from A4; the other 58 must not appear);
  * kill: Roest-Vigh's map (Aut+ = 8, free on faces: session check) appears at (8, 3); both enumerations give equal
    raw counts per group and equal class sets at (8, 3) and (9, 4); every class has 9 | Aut+ (resp. 8);
  * formulas (`formulas.py --controls`): Roest-Vigh pinned SAT; Roest-Vigh's planes pinned on Mizhaev's map
    UNSAT-SOLVER (must fail); random uniform nine planes GP SAT; uniform C3-symmetric planes pinned on the first
    C3 unit's group SAT; helper test: link automorphisms equal Aut+ and exactly 8 free-C3 maps on the (9, 3) census.
* **Pilot**: stage A in the session (both enumerations, kills, formula controls; bounded at 15 min wall, 10 workers),
  then shard 0 of stage B with a 120 s budget into `results/pilot/`. It exposes enumeration bugs (the K7/K12/RV
  checks), wrong C3 groups (aut count assertion) and the unit cost.
* **Pilot gate**: the binding limit of stage B is the per-shard budget or the formula cap; the pilot reports per
  unit the status, seconds and budget fraction and projects how many formulas 10 x 280 s decide.
* **Predictions**: (P1) at least one admissible (9, 4) class exists (~60 %); decision: none -> slice closed for
  planning. (P2) every stage-B formula is decided within 10 x 280 s (~50 %); fail -> the undecided formulas go to
  the lead with their measured times, no extra compute here. (P3) every decided formula is UNSAT-SOLVER (~85 %).
* **Grid**: one formula cap (120 s); the outcome depends on it only through TIMEOUTs, which decide nothing. A longer
  cap is a new budget line through the lead.
* **Budget**: <= 1 core-h joint cap: stage A <= 0.2 core-h (10 workers), pilot <= 0.05, stage B 10 shards x 280 s
  (0.78 core-h), laptop, owner launch on AC under caffeinate. `matrix.json`: 10 shards.
* **Power statement**: the enumeration is exhaustive for face-transitive cubic (9, 4) maps (coverage PROVED-1: the
  Sylow argument and the slot/involution/rotation parametrisation; not CERTIFIED). Genus 7 (g = 1 mod 3) is not
  enumerated. Formulas: only what finishes inside 120 s; maps without a free C3 cannot occur here (Z9 and Z3 x Z3
  have one), so every class gets at least one C3 formula and its plain formula.
* **Proofs**: none; every UNSAT is UNSAT-SOLVER (no named negative claim).
* **Counter calibration**: no float diagnostic enters the verdict (exact codes, exact signs, solver status only).
* **Scenario move**: the S0 and S5 tables do not move (this is S1 at nine faces). A verified S1 nine-face object is
  a new result for the focus target; UNSAT-SOLVER moves no credence.
* **Outcomes and their meaning**:
  * SAT: a clause-checked OM model of that formula only, not a polyhedron. Follow-up below.
  * UNSAT-SOLVER: that formula only (the plain formula at 10 elements, or the uniform free-C3 ansatz); may skip the
    map in planning, never "no nine-face object".
  * TIMEOUT / NOT-RUN: no information; listed with the time spent.
  * no admissible class: no face-transitive cubic (9, 4) map (EXACT computation, coverage PROVED-1).
  * near-miss: not applicable (no geometry here).
* **Follow-up tree**: SAT -> the bridge (pilot.py `hinge` / `two_stage` realizers and the final polynomial, as
  E-261103-03), `verify_candidate.py FILE --all-pairs` with nine faces, `candidate-check`, escalate to the lead.
  Empty list or all UNSAT-SOLVER -> this slice closed for planning. Classes with a one-face involution in Aut+ ->
  item 2's route (E-261117-02), listed only.
* **Stop rule**: a failed control or kill; the first SAT stops nothing (others still decided) but its model is
  processed first in the follow-up; stage-B budget; the 1 core-h joint cap.
* **STATUS.md / ROADMAP.md**: the class counts at (8, 3) and (9, 4) and the formula statuses in STATUS (nine-face
  S1 section); ROADMAP State concluded; a SAT goes to "For the lead".

## Amendments

### 2026-11-17: stage A result (pilot), no stage B

Stage A ran once (`results/census/`, 5.9 s wall, 10 workers); every control passed. (9, 4): two valid classes,
both inadmissible (repeated vertex triples), zero admissible, so stage B has no unit and no owner launch is needed;
the outcome "no admissible class" applies as written. The summary `print` of `formulas.py --controls` crashed after
the report was saved; fixed, not rerun. Concluded in `CONCLUSION.md`.
