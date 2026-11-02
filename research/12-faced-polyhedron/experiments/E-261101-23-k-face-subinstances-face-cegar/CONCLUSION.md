# E-261101-23: conclusion (night 6, 2026-11-01/02)

* **Runs**: commit `1bbe052` (branch `experiment/E-261101-25-chirotope-first`, 10 dirty files: untracked results),
  6 laptop shards (types mod 6), started 2026-11-01T17:41Z, all under `caffeinate -dimsu`. Core-hours from
  `results/*/manifest.txt`: 59.75 in total (shard 2: 4.63, finished normally at 2026-11-01T22:18Z; shards 0, 1, 3,
  4, 5: 11.02 each, ended by the owner's `stop` at 2026-11-02T04:42Z; five restart lines of 0.003-0.004 each from a
  15-second restart just before the stop). Productive time (start to the last record of each shard): about 11.9
  core-h; the other ~47.8 core-h were spent inside five hung units.
* **Why the night stopped producing**: five shards hung in one unit each (type 30 k = 9, type 19 k = 8, type 15
  k = 8, type 16 k = 8, type 29 k = 8), from 21:29-22:47 local time (UTC+3) until the stop at 07:42.
  Reproduced on type 19 k = 8 in the morning session with a stack dump: CaDiCaL returns SAT, both realizers finish in
  seconds, and the process then stays at 100 % CPU in `scipy.optimize.linprog` (HiGHS) called from
  `final_polynomial.py` line 75, which had no time limit (the dump at 4 minutes and 100 % CPU at 6 minutes;
  this LP took 3-8 s on the other models). The other four hung units are inferred to be the same (same code path,
  no record, same symptom), not reproduced. Fixed after the night: `final_polynomial(..., time_limit=120)` returns
  `LP-TIMEOUT` (`PLAN.md` Amendments). The restart at 07:41:59 also truncated every `night.log` (the launcher used
  `>`; now `>>`), so the night's logs are lost; the records, manifests and `progress.jsonl` files are intact.
  The CNF / DRAT pairs in shards 0, 1, 3, 4, 5 are partial files of the units in flight at the stop (not UNSATs) and
  are not kept.
* **Controls**: negative control (Lutz #36 C2 rebuilt, CNF SHA-256 equal to the record, UNSAT, drat-trim VERIFIED)
  passed in the pilot through the same code path. Positive control for realization ("the pipeline reports SAT and
  realizes"): not met: the pilot model of type 0 k = 8 did not realize, and no k-face model with a known
  realization exists to test the realizer on (the realizer was validated only on full 12-plane chirotopes of known
  configurations, E-261101-25). So "0 realized" cannot be read as non-realizability: the verdict is underpowered.
* **Outcome** (counter: CaDiCaL status per (type, k), face set = the first k faces of `greedy_face_order`, one set
  per (type, k)):

  | k | timeout | SAT | UNSAT | TIMEOUT | not reached |
  |---|---|---|---|---|---|
  | 8 | 300 s | 27 | 0 | 0 | 32 types (hang) |
  | 9 | 600 s | 15 | 0 | 11 | 33 types |
  | 10 | 1200 s | 0 | 0 | 26 | 33 types |

  Types reached: 0-14, 17, 18, 20, 23, 24, 26, 30, 32, 38, 44, 50, 56 (27). Not reached: 15, 16, 19, 21, 22, 25,
  27-29, 31, 33-37, 39-43, 45-49, 51-55, 57, 58 (32). SAT solve times at k = 8: median 23 s, max 129 s; at k = 9:
  median 237 s, max 479 s. Realization of the 42 SAT models: 0 realized; wrong signs after the two realizers 9-38
  (k = 8), 10-27 (k = 9). Final polynomial on the 42 unrealized models: 2 FEASIBLE (t* > 0, no biquadratic final
  polynomial), 39 NONREALIZABLE-NUMERICAL (t* = 0 within 1e-15, the rounded multipliers fail the exact identity),
  1 NONREALIZABLE-EXACT (type 0 k = 9: the in-run rational check of the Farkas identity passed, 26 brackets).
* **Prediction vs outcome**: P1 (k = 8 SAT for most types within 5 min): true on the 27 types reached (27/27, all
  under 130 s). P2 (at least 10 types with a decided k = 10 instance): false, 0 of 26 tried; every k = 10 run
  timed out at 20 minutes. P3 (an UNSAT at k <= 10, prior 0.3): not observed; 0 UNSAT among 42 decided units.
  P4 (at most a third of the SAT models realize): true, 0/42, but trivially so without a positive control.
* **Exact verification**: no candidate (nothing EMBEDDED, no realized k-face model), so `candidate-check` had nothing
  to run on. No UNSAT, so no CNF / DRAT is evidence. The one exact final polynomial is not reproducible from the
  files: the record keeps the bracket count, not the multipliers.
* **What may be claimed**:
  * NUMERICAL (solver outcome, instance scope): for the 27 types listed, the k = 8 sub-instance on the greedy face
    set is SAT under CaDiCaL 3.0.1; for 15 of them also k = 9 (types 0, 2, 3, 4, 6, 7, 10, 12, 13, 18, 24, 26, 38,
    44, 50). A SAT model is a CANDIDATE-level object (SPEC §4); these are SAT answers about those formulas only.
  * NUMERICAL: the realizers did not realize any of the 42 models; for 39 of them the biquadratic LP has optimum 0.
  * NUMERICAL (an exact computation inside the run, not reproduced by `verify_all.py`): the SAT model of type 0 at
    k = 9 has a biquadratic final polynomial, i.e. that one chirotope is not realizable.
* **What may NOT be claimed**: that any type is excluded or not excluded; anything about other 8- or 9-face sets of
  these types (one face set per (type, k) was run); anything about k = 10 (all timeouts) or the 32 types not
  reached; that the k-face models are non-realizable (39 are numerical zeros, one exact certificate was not
  stored); that the obstruction is global (H-261101-15's rival) - SAT on one face set per k does not say that.
* **Hypotheses**: H-261101-15 stays open (evidence: no UNSAT at k <= 9 on the greedy face set for the 27 types
  reached; the face set choice and k = 10 remain untested). H-261101-02: no move (no UNSAT core to mine).
  H-261101-12: no move (its statement is about full-instance models; one exact final polynomial on a k = 9 model is
  recorded as evidence of the kind it needs).
* **Scenario move**: the pre-registered "all SAT and all unrealized raises C" is met only on the decided 42 units,
  with an unvalidated realizer; by PROTOCOL §3 (a positive control that could not succeed) the run is underpowered,
  so the credences in `ROADMAP.md` stay unchanged.
* **Verdict for the direction**: UNDERPOWERED@59.75 core-h (11.9 productive; 27 of 59 types at k = 8, 26 at k = 9
  and 10; one greedy face set per (type, k); no realizer positive control at k-face level). Not LOW-YIELD.
* **Next step**: ROADMAP row E-261102-01 (the 32 types not reached at k = 8, 9 with the LP time limit; k = 10 only
  with a longer timeout or dropped; final-polynomial certificates stored so an exact one can be re-checked; a
  realizer positive control on k-face sub-instances of known realizations, from E-261101-26).
* **Rows updated**: `STATUS.md` DR8 and the "As of" line, `ROADMAP.md` E-261101-23 State done and row E-261102-01,
  `experiment-log.md` (2026-11-02), `hypotheses/H-261101-15`, `reports/NIGHT_REPORT_2026-11-02.md`.
