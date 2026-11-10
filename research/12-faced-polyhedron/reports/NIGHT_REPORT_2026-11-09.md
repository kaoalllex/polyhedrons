# E-261109-06 (10, 4) stratum C sweep night report (2026-11-09/10)

One owner laptop launch (`launch.sh 09-06 start`), 10 shards, started 23:02:44 local, no restart.

* Wall vs budget: last shard ended 05:54:44 local, 6.87 h of the 10 h limit; 63.84 core-h (attempt manifests) against the
  80 core-h cap. No sleep gap: per shard, wall time minus summed unit seconds is 22-24 s.
* Job (one root, kissat rel-4.0.4, no DRAT, cap 3600 s): 358 maps, 35-36 per shard, all UNSAT-SOLVER (148-2041 s), 0 SAT,
  0 TIMEOUT; controls pass in all 10 shards (positive SAT with a checked model, negative UNSAT-SOLVER).
* Exact checks: none needed (no SAT, no UNSAT used as evidence).

Verdict: stratum C 360/360 UNSAT-SOLVER (845 and 146 reused), 0 SAT, f = 7.16, A + B priced at 6.06 laptop nights ->
Actions route after week item 2 (CONCLUSION, STATUS 3ad).
