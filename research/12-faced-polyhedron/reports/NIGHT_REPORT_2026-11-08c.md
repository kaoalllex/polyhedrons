# E-261108-03 (10, 4) speed-up benchmark report (2026-11-08/09)

One laptop launch, 10 shards, started 22:21:09 local, no restart.

* Wall vs budget: longest shard 8,562 s of tasks (shard 5 ended 00:44:04, 2.38 h) of the 5.1 h limit; 8.59 core-h (sum of
  shard wall times; manifests hold no core-hours) against the 47 core-h cap. No sleep gap seen (each job starts when the
  previous one ends); OS sleep telemetry not collected.
* Jobs (five roots, no DRAT): controls passed in all 50 shard-root jobs (positive SAT with a checked model, negative
  UNSAT-SOLVER). kissat-A 6/6 decided; unsat-A 5/6 decided, map 7 TIMEOUT at 1800 s; kissat-B, unsat-B 4/4 decided;
  default-B 2/2 decided (96 in 1970 s, 85 in 6454 s). 0 SAT; all UNSAT-SOLVER; Phase A agrees with the recorded UNSAT-VERIFIED records.
* Exact checks: none needed (no SAT, no UNSAT used as evidence).

Verdict: kissat wins, best measured speed-up 2.35x (no 10x), P(4) = P(16) = 475 core-h without DRAT; next, Actions
calibration (CONCLUSION, STATUS 3x).
