# E-261110-05: conclusion

2026-11-13. Stage 1 ((8, 2), 2 shards) ran in the prep session (PLAN amendment 1, `results/prep-8-2/`); stage 2 ((9, 3))
is one owner launch (`launch.sh 13-02 10-05 start`, after E-261113-02), 10 shards, `results/`, commit `c242b0df`, kissat
4.0.4, `NO_PROOF=1`, cap 900 s.

* **Runs**: stage 1 0.085 core-h; stage 2 started 15:29:42 UTC, every shard `exit_status 0`, **0.355 core-h** (sum of
  the ten `manifest.txt`; shard 1 carried the 900 s timeout); total 0.44 core-h of the 3 core-h budget. No restart.
* **Controls**: c1-c4 `CONTROLS-PASS` in all 12 shard runs: the eight plain CNF SHA-256 equal the E-261103-03 records;
  V2 drops only SEGMENT_DISJOINT and equals plain on the convex f9 map; Roest-Vigh and Mizhaev pinned SAT under V1
  and V2; convex f9 swapped negative UNSAT-SOLVER under V2 (and V1).
* **Results** (`summary.py`; all UNSAT are UNSAT-SOLVER, no proofs):

  | map | V2 (no SEGMENT_DISJOINT) | V1 (immersion-only) |
  |---|---|---|
  | (8, 2) #0, #1 | UNSAT-SOLVER 6.4 s, 13.0 s | UNSAT-SOLVER 150 s, 134 s |
  | (9, 3) #40, 43, 10, 30, 48 | UNSAT-SOLVER 40-90 s | SAT 3-10 s |
  | (9, 3) #5 | UNSAT-SOLVER 27 s | TIMEOUT 900 s |

* **Prediction vs outcome**: P1 (V2 SAT on an (8, 2) map, ~50 %) failed; P2 (V1 SAT on both (8, 2) maps, ~60 %)
  failed; P3 (>= 10 of 12 (9, 3) units decided, ~40 %) held (11/12).
* **Readings** (registered tree): V2 UNSAT on all eight maps -> H-261110-01 weakened in its stated form (the segment
  clauses are not needed for the refutation); **TRIPLES-CARRY** on (9, 3) #10, 30, 40, 43, 48 (V1 SAT, V2 UNSAT): the
  global forbidden triples carry it there; **LOCAL** on (8, 2) #0, #1 (V1 UNSAT): one session of core mining on the
  (8, 2) formulas is the registered next step.
* **What may be claimed**: instance scope, per formula: kissat returns UNSAT without a checked proof on the eight V2
  and two (8, 2) V1 formulas, SAT (model checked) on five (9, 3) V1 formulas. A V1 SAT is an OM model of the
  immersion-only formula, not a geometric immersion.
* **What may NOT be claimed**: any negative result (UNSAT-SOLVER, `SPEC.md` §4); that the (8, 2) or (9, 3) obstruction
  is local or global as a theorem; anything about S0. Not run: proofs, a second solver, maps beyond these eight,
  the V1 decision on (9, 3) #5.
* **Verdict**: **DONE@0.44 core-h**: H-261110-01 weakened (planning evidence: the segment clauses are not what
  refutes these formulas); at (9, 3) the triples carry the refutation, at (8, 2) even the immersion-only formula is
  refuted. No scenario move.
* **Next**: one core-mining session on the (8, 2) V1 formulas (follow-up tree; not in this week's plan, so the lead
  schedules it); week item 4.
