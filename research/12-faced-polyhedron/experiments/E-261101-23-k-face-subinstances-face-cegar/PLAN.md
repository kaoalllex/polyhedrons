# E-261101-23: k-face sub-instances with DRAT, and their realized models

Pre-registration (2026-11-01, before the night run). Amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2.
* **Question**: for each of the 59 types and k = 8, 9, 10, is the k-face sub-instance (GP, normalisations, TRIPLE
  inside the set, SIMPLE, REFLEX1, POC for the first k faces of the greedy order) UNSAT, SAT, or undecided within
  5 / 10 / 20 minutes; and do the SAT models realize?
* **Hypotheses moved**: H-261101-15 (an UNSAT at k <= 10 for some type supports it and excludes that type, EXACT after
  drat-trim; all SAT weakens it), H-261101-02 (a recurring UNSAT face pattern across types is the structural
  obstruction), H-261101-12 (SAT models that fail to realize and carry an exact final polynomial support it).
* **H1 / H0**: H1 = at least one type has an UNSAT sub-instance at k <= 10 (then every larger k and the full instance
  are UNSAT for that type: the first exclusion of a type); H0 = every decided sub-instance is SAT.
* **Why this**: the face ladder is monotone (I-261101-18): any realization of the type restricts to a realization of
  every sub-instance, so a sub-instance UNSAT is a theorem about the type, with a formula a human can read. The
  pilots of E-261101-25 showed k = 7 sub-instances decided in seconds; the full instance times out at hours.
* **Method**: `kface_sweep.py` (CaDiCaL 3.0.1 binary with DRAT, drat-trim check, SHA-256 of CNF and proof for every
  UNSAT; SAT models saved and realized with the E-261101-25 realizers; unrealized models tested for a biquadratic
  final polynomial). Target: S0 (exclusions) and k-face partial objects. Counters: status per (type, k), solve
  seconds, proof size, realized wrong signs.
* **Controls**: positive (the pipeline reports SAT and realizes): type 0, k = 8 in the pilot; negative (the pipeline
  reports UNSAT with a VERIFIED proof): the certified symmetric immersion instance Lutz #36 C2 built with
  `run_overnight.sym_build_immersion`, run through the same cadical + drat-trim path (its CNF SHA-256 should equal
  the recorded e9b15e62...). Encoder equality: `build_faces(all, simple=False)` = `omsat.build`.
* **Counter calibration**: the fraction of TIMEOUTs per k is reported; a k at which every type times out carries no
  information (a timeout is never a negative result).
* **Scenario move**: an UNSAT at k <= 10 for one type raises B (per-type decisions are cheaper than feared) and is
  neutral on A for the other types; a realized k = 10 model raises A slightly (partial objects exist deep in the
  ladder); all SAT and all unrealized raises C.
* **Pilot**: type 0, k = 8, 300 s; the negative control.
* **Budget**: 6 shards (types with id mod 6 = shard), per type at most 5 + 10 + 20 = 35 minutes, so about 6 hours per
  shard; one laptop night alongside E-261101-25's 4 shards (10 processes on 11 cores).
* **Power statement**: with these timeouts the sweep decides what CaDiCaL can decide in 5-20 minutes per sub-instance;
  types whose k = 8 instance times out remain undecided at every k; the number of decided (type, k) pairs is itself
  the measurement.
* **Predictions (written before the run)**: (P1) k = 8 is SAT for most types within 5 min; (P2) at least 10 of 59 types
  have a decided k = 10 instance; (P3) at least one UNSAT at k <= 10 (a type exclusion) is possible but not expected
  (prior 0.3); (P4) at most a third of the SAT models realize.
* **Outcomes and their meaning**: UNSAT (VERIFIED): the type is excluded (EXACT; CERTIFIED after a human reads the
  soundness of the clause families), add to `STATUS.md` as a new FD row and run the same face set on every type
  containing that sub-map; SAT realized: a k-face partial object (store planes, label EXACT on the chirotope level,
  not a witness until an exact geometric check of the k faces is written); SAT unrealized with an exact final
  polynomial: evidence for H-261101-12; TIMEOUT: no information.
* **Stop rule**: the night; within a type, stop increasing k after the first UNSAT.
* **STATUS / ROADMAP changes**: per outcome as above; the E-261101-23 State to done with its verdict.

## Amendments

* 2026-11-01 pilot (session): type 0, k = 8 (faces [0, 1, 2, 3, 11, 7, 8, 4] of the greedy order, with SIMPLE
  clauses): SAT in 20 s with the CaDiCaL binary; the model did not realize (two-stage realizer: offsets LP infeasible
  for every normal realization; hinge realizer: 9 wrong signs with the same loss 0.128 from six random starts, which
  points at a structural obstruction rather than a bad start); no biquadratic final polynomial (FEASIBLE), so the
  model's non-realizability is neither proved nor excluded. Encoder equality with `omsat.build` re-checked after the
  SIMPLE option (identical with simple=False).
  Negative control passed: the certified symmetric immersion instance Lutz #36 C2 rebuilt with
  `run_overnight.sym_build_immersion` has the recorded CNF SHA-256 (e9b15e62c33b43d3...), CaDiCaL 3.0.1 returns UNSAT
  in 51 s and drat-trim VERIFIES the proof in 25 s through the same code path as `kface_sweep.py`. Pipeline ready for
  night 6 (shards 0-5).
