# E-261103-07 (10, 4) cost probe report (2026-11-08)

One laptop run, 10 shards, one `launch.sh 03-07 start`, started 15:18:17 UTC, no restart.

* Wall vs budget: longest shard 1810 s (0.50 h) of the 2 h deadline; 2.53 core-h (sum of shard wall times; manifests hold no core-hours)
  against the 6.5 core-h cap bound. No sleep gap seen (wall equals cap plus 9-10 s per shard); OS sleep telemetry not collected.
* Jobs: 20 control units (10 SAT with checked model, 10 UNSAT-VERIFIED), all passed; 10 (10, 4) plain maps: 0 SAT, 0 UNSAT, 10 TIMEOUT
  (6 fast at 300 s, 4 slow at 1800 s). Exact checks: drat-trim `s VERIFIED` for the negative controls (recorded, not replayed).
* No SAT: no candidate verification.

Verdict: "needs a speed-up first" by the pre-registered rule; no claim about (10, 4) existence (CONCLUSION).
