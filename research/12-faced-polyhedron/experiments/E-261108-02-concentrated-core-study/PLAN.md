# E-261108-02: concentrated-multiplicity core study

Pre-registration, 2026-11-08. Focus S5 (9,3); label ceiling EXACT per formula, PROVED-1 for any lemma (AI-written).

* **ROADMAP row / scores**: week item 3, explore; T 2 D 2 F 1 G 2 R 2 (T + D = 4; not a parked method: a new measurement on
  decided formulas, no new decision).
* **Question**: for the maps whose extra segments meet at one face, is the UNSAT of the plain formula already forced by
  the clauses on few faces?
* **Hypotheses moved**: H-261103-03 (OM-UNSAT of (9,3) maps: a local core gives a map-independent lemma),
  H-261101-07 (a lemma excluding many (10,4) maps). Core on <= 6 faces in >= 3 maps: +; none: the UNSAT is global, no move.
* **H1 / H0**: H1: for >= 3 of the 24 maps some face set F, |F| <= 6, has an UNSAT sub-formula. H0: no such F.
* **Method** (`cores.py`; the answer to "how to get cores" is a choice, not CaDiCaL cores):
  1. Rebuild the plain formula (`pilot.build`, `ALL_OPTS`, `from_links`, as `tranche.unit`); check the census map hash and,
     where a local `results/*/map<i>/result.json` exists, `formula_sha256`.
  2. Support of a variable: chirotope variable q_S -> S minus INF (elements 0..8 are the faces; INF is free); Tseitin
     variables from `_xor`/`_and` (union of the inputs' supports). Support of a clause = union over its variables.
  3. `sub(F)` = clauses with support inside F. It is a clause subset, so `sub(F)` UNSAT => the plain formula UNSAT
     (sound by construction; no solver core is used, nothing depends on a core minimiser).
  4. Per map, F by increasing size k = 3, 4, 5, 6 (monotone: `sub(F)` UNSAT => every superset UNSAT), stop at the first
     level with an UNSAT; k_min = that size (exact minimum over face sets, not a locally minimal core). All UNSAT-VERIFIED
     by `pilot.solve` (CaDiCaL + drat-trim, hashes kept). Solver cap 20 s per sub-formula; a TIMEOUT is UNKNOWN.
  5. For each k_min set: re-test with the unit clauses on q (symmetry normalisation) removed (arm N: does the core need the
     labelling?). Counts of UNSAT sets at k = 6 and which faces occur are recorded.
  6. Independent cross-check on 3 maps with k_min <= 6 (and on control C1): clauses grouped by support, one selector per
     group, pysat Cadical153 with assumptions, `get_core`; the union U of the core groups' supports must give an UNSAT
     `sub(U)` and |U| >= k_min. Disagreement stops the run.
* **Maps**: the 24 admissible 11-gon maps (1,2,3): 40 43 58 59 60 66 67 90 111 123; (1,1,1,3): 48 74 75 94 100 102 171 174
  176 177 181 184 199 200. Comparators (not in the verdict): (2,2,2) 5 6 20, (1^6) 0 1 2. (The prompt's "3 maps of (2,2,2)" have 10-gons.)
* **Controls**: C1 positive (planted core): convex 9-face control formula (`control_f9.py`, planes not pinned, SAT) plus two
  unit clauses q_S and -q_S, S = {a,b,c,INF}: must give k_min = 3 and exactly the 20 UNSAT 6-sets that contain {a,b,c}.
  C0 negative: the same formula unplanted must give no UNSAT F at k <= 6, and the full formula must be SAT (cadical).
* **Pilot** (shard 0, minutes): C0, C1, map 40 and map 0 with levels 3-6; per-solve times. It could expose a measurer that
  returns constant sizes, or sub-formulas that time out at the cap.
* **Pilot gate**: median sub-solve < 1 s and < 5 % TIMEOUT, projected total <= 1 core-h; else cut to k <= 5 and 6 only
  for maps with a smaller hit, or escalate.
* **Predictions**: (P1) >= 3 of 24 maps have k_min <= 6 (~40 %). (P2) if so, k_min >= 5 (a GP relation needs 6 elements)
  (~70 %). (P3) comparators (1^6) have no UNSAT F at k <= 6 (~75 %).
* **Grid**: k = 3..6 (the kill threshold is 6); one solver, one cap; the cap is the only free parameter (a TIMEOUT-bound
  verdict is reported as such, not as a result).
* **Budget**: <= 1 core-h, one session, 10 shards (maps round-robin, `SHARDS=10`), laptop, short enough to run from the
  session (minutes). Worst case 30 maps x 420 solves x 20 s is not reached; the gate above bounds it.
* **Power statement**: decides, per map, whether a <= 6-face core exists among clause subsets by support; says nothing
  about cores that need clauses outside the support closure of F, nothing about other maps, and a map with TIMEOUT sets at
  k <= 6 and no UNSAT is "not decided".
* **Counter calibration**: no float diagnostic; the discrete measurer (k_min) is calibrated by C0 (none) and C1 (3, with the
  exact 20-set family). A k_min equal for all maps is not a phenomenon until the comparators and C0/C1 show the measurer moves.
* **Scenario move**: none of A/B/C by itself (OM-UNSAT of these maps is already decided); a lemma only shrinks the search.
* **Outcomes**:
  * k_min <= 6 in >= 3 of 24: pass -> follow-up below.
  * otherwise (including undecided maps): park, with scope "face-support sub-formulas, cap 20 s, these 24 maps".
  * a SAT sub-formula never matters; a SAT full formula (cannot happen, all 24 UNSAT-VERIFIED) stops the run.
* **Follow-up tree**: pass -> a PROVED-1 lemma draft in `CONCLUSION.md` (<= 1 session) and the exact count of the (10,4)
  census maps (E-261103-01 `maps_10_4.json`) it excludes (minutes, no solver; the exclusion must be checked as a
  sub-structure of the map, not by pattern name).
* **Stop rule**: 1 session, 1 core-h, then conclude.
* **STATUS / ROADMAP for each outcome**: pass -> STATUS 3d line + item 3 DONE; park -> item 3 DONE-PARKED, one line.

## Amendments
