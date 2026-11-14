# E-261114-01: normalised S6 (10, 3)

Pre-registration, 2026-11-14. No target formula before the soundness and positive-control gates.

* **ROADMAP / scores**: week item 1, T 2 D 2 F 2 G 2 R 2; exploit, jump 2.
* **Question / H1 / H0**: do reorientation and mirror units decide the twenty S6 (10,3) formulas
  within 3600 s (H1), or does a substantial timeout tail remain (H0)?
* **Hypothesis moved**: H-261110-03, planning evidence only unless an exact target witness passes.
* **Why**: the previous plain formulas all timed out; the review's known-answer timings suggest
  normalisation may remove redundant search. This run changes the formula options, not the target.
* **Method / counters**: existing omsat.build with ALL_OPTS plus symbreak=True, mirror=True,
  submap=True for S6; kissat, no proofs. SPEC §4 statuses, solver seconds, EMBEDDED,
  nonsimple_faces, bad_pairs, adjacent_pairs. An S6 result requires F=10, g=3 and --target S6 PASS.
* **Prep (a)**: ten shards, each with a deterministic random seed, ten uniform integer-plane
  chirotopes per map kind (Szilassi, Roest-Vigh, a (10,2) submap). Compare every ALL_OPTS
  clause family under every single face reorientation and global chirotope sign reversal;
  compare equality clauses as equalities, not the order of their two CNF implications.
  Check gauge-unit attainability and record a PROVED-1 argument. Stop on any mismatch.
* **Prep (b)**: re-gauged pinned SAT controls: Szilassi, Roest-Vigh, Mizhaev, convex f9/f10,
  grooved box, all sixteen realized (10,2) objects; the fifty sampled (10,2) maps unpinned SAT.
  A failed positive -> one retry with reorientation only; persistent failure -> escalate.
* **Prep (c)**: two (8,2) and 203 (9,3) admissible formulas must be UNSAT-SOLVER;
  measure normalized/plain ratios on (10,4) maps 845,96,85 using hash-matched saved baselines.
* **Prep (d) / pilot**: Lutz #1,#2 at 1200 s, after (a)-(c) pass; record binding cap and fraction
  consumed. Both TIMEOUT -> no day run, item 4 first. A control failure blocks the target.
* **Controls**: positive as (b); negative as (c); invariance harness must detect a deliberate
  chirotope-bit mutation on a GP relation. No target exclusion from these checks.
* **Prediction**: at least one pilot map finishes before 1200 s; failure kills the day launch.
* **Grid**: 1200 s pilot then 3600 s day cap; all twenty maps, ten shards, fixed solver seed 0.
* **Budget**: one prep session, then owner day run <=20 core-h, laptop only under caffeinate
  on AC. Never start the day run from this session. Prep timing units capped at 1200 s.
* **Power**: complete map coverage only if all twenty finish; timeout gives no information.
  SAT models need not be realizable and bridge failures cannot exclude a model or map.
* **Proofs**: none; every unchecked UNSAT is UNSAT-SOLVER, instance scope only.
* **Counter calibration**: no float geometric diagnostic decides success. Timings measure runtime;
  bridge diagnostic objectives never replace exact verification.
* **Scenario move**: exact target witness establishes A; all UNSAT-SOLVER prioritizes B for a
  proposed proof replay without changing credences; SAT without a witness leaves A/C unresolved.
  Timeouts and failed controls leave all credences unchanged.
* **Follow-up**: SAT -> at least 30 solver-seed models, bridge each, candidate-check and escalate;
  all UNSAT-SOLVER -> lead proposes proof replay; >20% TIMEOUT -> item 4 on remaining maps.
  Chain item 3 (E-261114-02) after separate pre-registration; frozen-bridge recovery controls.
* **Stop**: failed control, all units recorded, first verified candidate, or budget exhausted.
* **Ledger**: prep failure -> blocked/escalated with exact scope; successful prep -> ready for
  owner launch; day outcome -> concluded with the registered follow-up. No family negative.

## Amendments
