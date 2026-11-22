# E-261119-03: face-transitive cubic nine-face maps at genus 7, plain formula on admissible classes

Pre-registration, 2026-11-22. Week item 5, optional (`ROADMAP.md`; `reviews/strategy-review-2026-11-19.md` §1, §5 Q1;
the owner's idea, I-261119-03).

* **ROADMAP row / scores**: T 1 D 1 F 2 G 1 R 2 (T + D = 2 < 3). **Owner exception, 2026-11-22**: asked about the
  failed gate, the owner answered "для пункта 5 - исключение. выполняй" (an exception for item 5, run it). Explore, jump 2.
* **Question**: which cubic (9, 7) maps with every face pair adjacent have Aut+ transitive on the faces, and is the
  plain formula (10 elements) of any admissible one SAT?
* **Hypotheses moved**: H-261101-07. A verified nine-face S1 object of genus 7 is outside its genus 2-5 range but
  would be a new nine-face object (escalate). UNSAT-SOLVER, TIMEOUT or an empty list leave it unchanged.
* **H1**: an admissible face-transitive (9, 7) class exists and its plain formula is SAT. **H0**: none exists, or every
  plain formula is UNSAT-SOLVER.
* **Why**: face degree 2E / 9 = (42 + 12 g) / 9 is an integer only for g = 1 mod 3; genus 4 is empty (E-261117-01,
  STATUS 3au), genus 7 (valency 14, E = 63) is the next and is not enumerated. Coverage (PROVED-1 sketch, as A3 of
  E-261117-01): a face stabiliser of Aut+ acts freely on the 14 darts at that dual vertex, so its order divides 14;
  |Aut+| = 9 |stab| and a Sylow 3-subgroup of order 9 meets every stabiliser trivially, hence acts regularly on the
  faces. The maps are Cayley maps of Z9 or Z3 x Z3, every one found by the slot / involution / rotation enumeration.
* **Method**: `cayley7.py` reuses E-261117-01 `cayley.py` (labellings: 272 per group at k = 14; `by_phi`; `trimap`;
  census `check` (K9, genus 7, connected), `admissible` (no repeated vertex triple), canonical code, mirror
  identified). Second enumeration: `brute` needs 13! = 6.2e9 rotations per labelling (out of reach), so it is
  replaced by `rho_dfs`: the same cyclic orders rho from slot 0, depth first, pruned by necessary conditions on the
  partial phi = rho o iota; independent of `by_phi` (rho first, not phi first). Stage A: `bash run.sh stage_a`. Stage
  B: `bash run.sh stage_b`, on each admissible class the plain formula (`formulas.formula(links, None)`: pilot
  `build`, ALL_OPTS), kissat, cap 120 s. Target S1 at nine faces, genus 7 reported (never S5 or S0). Counters: raw,
  valid, admissible, distinct classes per group; per formula SAT / UNSAT-SOLVER / TIMEOUT.
* **Controls** (any failure stops the run):
  * `test_cayley7.py` (before stage A, in the pre-registration commit): `rho_dfs` gives exactly the `brute` set per
    labelling on Z7 (all labellings) and order 8 (four per group), nothing on Z9 at (9, 4); K7 and the one
    vertex-regular K12 census class come out of `rho_dfs` (positive), the other 58 K12 classes do not (negative);
  * stage A rung: `rho_dfs` reproduces the saved `brute` raw counts per group and the saved class lists of
    E-261117-01 at (8, 3) (Roest-Vigh's map inside) and (9, 4); at (9, 7) `by_phi` and `rho_dfs` give equal raw
    counts per group and equal class lists; every class has 9 | Aut+;
  * stage B, per map: random uniform nine planes pinned on the GP subformula of that map's CNF must be SAT (the
    builder is not trivially UNSAT on these large maps). The formula-side controls of E-261117-01 (Roest-Vigh pinned
    SAT, its planes on Mizhaev's map UNSAT-SOLVER; `formula_controls.json`, PASS) are reused: `pilot.py` is
    unchanged since; `formulas.py` changed only in a summary `print` (f72a46ec).
* **Pilot**: stage A is the pilot (minutes, 10 workers); it exposes enumeration bugs through the rung.
* **Pilot gate**: stage B runs in this session only if there are at most 10 admissible classes (<= 10 x 2 x 120 s);
  more -> price, matrix of 10 shards, owner launch through a dated amendment.
* **Predictions**: (P1) no admissible class (~65 %; at genus 4 every valid class repeated a vertex triple, and 27
  extra edges on 36 pairs make repeated triples likelier); decision: the slice closed at genus 4 and 7. (P2) if any
  exists, every plain formula is UNSAT-SOLVER or TIMEOUT (~90 %).
* **Grid**: one cap; the result depends on it only through TIMEOUTs, which decide nothing.
* **Budget**: <= 1 session; stage A <= 0.2 core-h, stage B <= 0.7 core-h; laptop, in the session (minutes).
* **Power statement**: the enumeration is exhaustive for face-transitive cubic (9, 7) maps (coverage PROVED-1). The
  formulas detect only what kissat finishes in 120 s; genus 10 and beyond are not enumerated.
* **Proofs**: none; every UNSAT is UNSAT-SOLVER (no named negative claim).
* **Counter calibration**: no float diagnostic enters the verdict (exact codes, exact signs, solver status).
* **Scenario move**: the S0 and S5 tables do not move (S1 at nine faces); UNSAT-SOLVER moves no credence.
* **Outcomes and their meaning**:
  * no admissible class: no face-transitive cubic (9, 7) map is the map of a polyhedron with nine mutually adjacent
    faces (EXACT computation, coverage PROVED-1); with E-261117-01 the slice is closed at genus 4 and 7;
  * SAT: a clause-checked OM model of that formula only, not a polyhedron; follow-up below;
  * UNSAT-SOLVER: that formula only; may skip the class in planning, never "no nine-face object";
  * TIMEOUT: no information, listed with its time; near-miss: not applicable.
* **Follow-up tree**: SAT -> the bridge (pilot `hinge` / `two_stage` realizers, as E-261103-03),
  `verify_candidate.py FILE --all-pairs` with nine faces, `candidate-check`, escalate (Opus high). All UNSAT-SOLVER
  or TIMEOUT -> recorded, slice closed for planning at this cap.
* **Stop rule**: a failed control or kill; the pilot gate; the 1-session budget.
* **STATUS.md / ROADMAP.md**: class counts and formula statuses in a new STATUS 3 entry (nine-face S1 section);
  ROADMAP State done; I-261119-03 status; a SAT goes to "For the lead".

## Amendments
