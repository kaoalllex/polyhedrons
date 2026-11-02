# E-261102-01: conclusion (laptop, daytime, 2026-11-02)

* **Runs**: commit `207be71` (branch `experiment/E-261101-25-chirotope-first`, 1 dirty file: the untracked
  `results/`), 8 laptop shards started together at 2026-11-02T08:42:53Z through `overnight/launch.sh`, all
  `exit_status: 0`, last shard finished at 09:23:01Z (40 min wall against the ~1.5 h budget). Core-hours from
  `results/*/manifest.txt`: 4.22 in total (0.39-0.67 per shard); CaDiCaL solve time 3.89 h of it.
* **Controls**: negative (UNSAT with a VERIFIED proof through the same code path): Lutz #36 C2 in the E-261101-23
  pilot, SAT / DRAT path unchanged since. Positive for the SAT path and the exact final polynomial: type 0 k = 9 in
  this experiment's pilot (`PLAN.md` Amendments). Positive control for realization at the k-face level: none exists
  (planned in E-261101-26), so "0 realized" is not read as non-realizability (as pre-registered).
* **Outcome** (counter: CaDiCaL status per (type, k), face set = the first k faces of `greedy_face_order`, one set
  per (type, k)):

  | k | timeout | SAT | UNSAT | TIMEOUT |
  |---|---|---|---|---|
  | 8 | 300 s | 32 | 0 | 0 |
  | 9 | 600 s | 18 | 0 | 14 |

  k = 9 SAT: types 15, 27, 29, 31, 34, 35, 39, 40, 42, 45, 46, 48, 49, 51, 53, 54, 55, 58; k = 9 TIMEOUT: 16, 19,
  21, 22, 25, 28, 33, 36, 37, 41, 43, 47, 52, 57. SAT solve times at k = 8: median 23 s, max 93 s; at k = 9: median
  240 s, max 597 s. Every one of the 64 units logged a start line and wrote a record (no hang). Realization of the 50
  SAT models: 0 realized; wrong signs after both realizers 8-32 (k = 8), 11-27 (k = 9). Final polynomial on the 50
  unrealized models: 40 NONREALIZABLE-NUMERICAL (t* = 0, the rounded multipliers fail the exact identity),
  6 LP-TIMEOUT (120 s), 2 FEASIBLE (t* > 0: type 25 k = 8, t* = 0.0017; type 45 k = 9, t* = 0.00076),
  2 NONREALIZABLE-EXACT (type 57 k = 8, 39 brackets, 20 rows; type 53 k = 9, 22 brackets, 11 rows; certificates in
  the records, CNF SHA-256 `db9c6a0f...` and `cf30a90a...`).
* **Together with night 6** (E-261101-23): k = 8 is SAT on the greedy face set for all 59 types; k = 9 is SAT for 33
  types, TIMEOUT for 25, and undecided for type 30 (hung in night 6, not re-run). Three exact final polynomials now
  exist (type 0 k = 9 from night 6 and this pilot, type 53 k = 9, type 57 k = 8); none has been checked by an
  independent script.
* **Prediction vs outcome**: P1 (k = 8 SAT for >= 28 of 32): true, 32/32. P2 (12-20 of 32 decided at k = 9): true, 18.
  P3 (an UNSAT at k <= 9, prior 0.15): not observed. P4 (no model realizes): true, but without a realizer positive
  control this carries no information. P5 (no hang; LP-TIMEOUT in at most 20 % of final-polynomial calls): true,
  64/64 records, 6/50 = 12 %.
* **Exact verification**: no candidate (no realized k-face model, nothing EMBEDDED), so `candidate-check` had nothing
  to run on. No UNSAT, so no CNF / DRAT is evidence; the CNF hashes of all units are in the records.
* **What may be claimed**:
  * NUMERICAL (solver outcome, instance scope): for the 32 types listed in `run.sh`, the k = 8 sub-instance on the
    greedy face set is SAT under CaDiCaL 3.0.1; for the 18 types above also k = 9. A SAT model is a CANDIDATE-level
    object (SPEC §4) about that formula only.
  * NUMERICAL: the realizers did not realize any of the 50 models; for 40 the biquadratic LP has optimum 0.
  * NUMERICAL (an exact rational check inside the run, not reproduced by `verify_all.py` or an independent
    checker): the SAT models of type 57 at k = 8 and type 53 at k = 9 each have a biquadratic final polynomial, i.e.
    those two chirotopes are not realizable.
* **What may NOT be claimed**: that any type is excluded or not excluded; anything about other 8- or 9-face sets
  (one face set per (type, k); the README's "second face set when k = 9 is SAT" was not pre-registered and not run);
  anything about k >= 10 (dropped) or about the 14 k = 9 timeouts; that the models are non-realizable (40 numerical
  zeros, 2 exact certificates not independently checked, 2 FEASIBLE, 6 LP-TIMEOUT); that the obstruction is global.
* **Hypotheses**: H-261101-15 stays open (no UNSAT at k = 8 on the greedy face set for any of the 59 types, none at
  k = 9 for 33; other face sets untested). H-261101-02: no move (no UNSAT core). H-261101-12: no move (its statement
  is about full-instance models).
* **Scenario move**: "all SAT and unrealized: no move" (pre-registered); credences in `ROADMAP.md` unchanged.
* **Verdict**: for exclusion by k-face sub-instances on the greedy face set, LOW-YIELD@4.2 core-h (k <= 9, 5 / 10
  min per unit, one face set per (type, k), with night 6: 59 types at k = 8, 59 at k = 9 of which 25 timeouts and
  1 undecided); not REFUTED (no proof). For the realization of k-face models, UNDERPOWERED (no realizer positive
  control).
* **Next step**: E-261101-26 (benchmark ladder) supplies the realizer positive control on k-face sub-instances of
  known realizations; the two FEASIBLE models (type 25 k = 8, type 45 k = 9) are natural hard cases for that rung. An
  independent checker for the three stored final-polynomial certificates (hand-over item). Other face sets per type
  only in a new pre-registered row.
* **Rows updated**: `STATUS.md` DR8 and the "As of" line, `ROADMAP.md` E-261102-01 State done, `experiment-log.md`
  (2026-11-02), `hypotheses/H-261101-15`. Daytime run, so no night report.
