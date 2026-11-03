# E-261102-01: completion of the k-face sweep (the 32 types night 6 did not reach, k = 8, 9)

Pre-registration (2026-11-02, before the run). Amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2.
* **Question**: for each of the 32 types E-261101-23 did not reach (list in `run.sh`), is the k-face sub-instance on
  the greedy face set (the first k faces of `greedy_face_order`) UNSAT, SAT or undecided within 5 min (k = 8) and
  10 min (k = 9); do the SAT models realize; do the unrealized ones carry an exact final polynomial?
* **Hypotheses moved**: H-261101-15 (an UNSAT at k <= 9 supports it and excludes that type, EXACT after drat-trim;
  all SAT leaves it open, since only one face set per (type, k) is run), H-261101-02 (a recurring UNSAT face set
  across types), H-261101-12 (exact final polynomials on unrealized models are the kind of evidence it needs; the
  statement is about full-instance models, so this moves it only through a later full-instance run).
* **H1 / H0**: H1 = at least one of the 32 types has an UNSAT sub-instance at k <= 9; H0 = every decided unit is SAT.
* **Why this**: night 6 decided k = 8 for 27 types and k = 9 for 15 before five shards hung in the final-polynomial
  LP; the missing 32 types are the cheapest part of the face ladder not yet seen (`CONCLUSION.md` of E-261101-23).
* **What is different from E-261101-23**: (1) the final-polynomial LP and the offsets LP have time limits
  (`LP-TIMEOUT` is its own status), (2) exact final polynomials store their certificate (relations, multipliers,
  bracket signs) in the record, (3) every unit logs a start line, so `overnight/launch.sh status` can flag a hang,
  (4) k = 10 is dropped (26 of 26 timeouts at 20 min in night 6), (5) 8 shards of 4 types, (6) a drat-trim check
  that exceeds its time limit is recorded as `CHECK-TIMEOUT` (CNF and proof kept) instead of crashing the shard.
* **Method**: `run.sh SHARD` (8 shards) calls `../E-261101-23-k-face-subinstances-face-cegar/kface_sweep.py
  --types <4 types> --ks 8 9 --timeouts 300 600` (CaDiCaL 3.0.1 binary with DRAT, drat-trim, SHA-256 of CNF and
  proof for every UNSAT; realizers of E-261101-25; biquadratic final polynomial on unrealized models). Target S0
  (exclusions) and k-face partial objects. Counters: CaDiCaL status per (type, k), solve seconds, realized wrong
  signs, final-polynomial status.
* **Controls**: negative (UNSAT with a VERIFIED proof through the same code path): Lutz #36 C2, passed in the
  E-261101-23 pilot with the unchanged SAT / DRAT path. Positive for the SAT path: type 0 k = 9 re-run in the pilot
  below (SAT, model, exact final polynomial reproduced). Positive control for realization at the k-face level: none
  exists (it comes with E-261101-26), so "0 realized" will not be read as non-realizability.
* **Counter calibration**: `t_star` of the final-polynomial LP: a realizable chirotope gives t* > 0 (type-0 witness
  and a class seed, E-261101-25 pilot, t* = 0.0065 / 0.0071); a certified non-realizable model gives t* = 0 with an
  exact certificate (type 0 k = 9, pilot below). Both sides are reachable.
* **Pilot**: type 19 k = 8 (the unit that hung in night 6) with a 60 s LP limit, and type 0 k = 9 with the new code;
  see Amendments.
* **Budget**: 8 shards, at most 4 x (5 + 10 + 4) minutes plus drat-trim per shard, about 1.5 h wall, at most
  ~12 core-h; laptop, daytime, 8 of 10 performance cores.
* **Power statement**: decides what CaDiCaL decides in 5 / 10 minutes on one face set per (type, k); an undecided
  k = 9 says nothing; no other face sets, no k >= 10.
* **Predictions (written before the run)**: (P1) k = 8 SAT for at least 28 of 32 types within 5 min (night 6:
  27/27); (P2) 12-20 of 32 types decided at k = 9 (night 6: 15/26); (P3) an UNSAT at k <= 9: not expected
  (prior 0.15); (P4) no model realizes; (P5) no unit hangs: every started unit writes a record, and `LP-TIMEOUT`
  ends at most 20 % of the final-polynomial calls (night 6: 5 hangs among 47 calls).
* **Scenario move**: an UNSAT (VERIFIED) raises B (per-type decisions are cheaper than feared) and is neutral on A for
  the other types; all SAT and unrealized: no move (no realizer positive control); a realized k-face model raises A
  slightly.
* **Outcomes and their meaning**: UNSAT VERIFIED: the type is excluded (EXACT; CERTIFIED after a human reads the
  soundness of the clause families), new FD row, same face set on every type containing that sub-map; SAT realized:
  a k-face partial object (`candidate-check`); SAT unrealized with an exact certificate: evidence for H-261101-12
  once an independent checker accepts the certificate; TIMEOUT / LP-TIMEOUT: no information.
* **Stop rule**: all 32 types at k = 8, 9; within a type, stop increasing k after the first UNSAT.
* **STATUS / ROADMAP changes**: STATUS DR8 per outcome; E-261102-01 State done with its verdict.

## Amendments

* 2026-11-02 pilot (session, before the run): type 19 k = 8 with `final_polynomial(..., time_limit=60)`: SAT in
  16 s, 11 wrong signs after both realizers, `LP-TIMEOUT`, record written (in night 6 this unit hung for 9 h; without
  the limit it was still in the LP after 20 minutes). Type 0 k = 9 with the new code: SAT in 184 s, 19 wrong signs,
  NONREALIZABLE-EXACT with 26 brackets (the night-6 result reproduced), certificate stored in the record, start line
  logged (that run had the first certificate layout; the final layout with the three bracket pairs and the signs was
  checked on the E-261101-25 engine, seed type39-kd_4aecd06992: 98 rows, 222 signs). Launcher `overnight/launch.sh` tested on a dummy experiment (start, refused second start, status with the
  silence flag, stop of the whole process tree, usage on a wrong command).
