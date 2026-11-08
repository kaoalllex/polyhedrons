# E-261103-03 item 5a run report (2026-11-08)

One laptop run (a day run, 15:00-17:22 local), 10 shards, one `launch.sh 03-03 start`, no restart. Counts, costs and scope:
STATUS section 3d and the experiment CONCLUSION (section "Item 5a").

* Wall vs budget: longest shard 2.36 h of the 8 h deadline; 18.51 core-h of the 80 core-h ceiling. Wall minus solver and
  checker time is 16-17 s per shard, so no sleep gap; OS sleep telemetry was not collected.
* Job: 20 control units (positive SAT and negative UNSAT-VERIFIED in every shard, all passed) and 158 (9,3) plain maps:
  158 UNSAT-VERIFIED, 0 TIMEOUT, 0 SAT. Exact checks: drat-trim `s VERIFIED` for every UNSAT in the run; at conclusion
  all 158 CNFs rebuilt from the committed encoder match their recorded hashes; no DRAT replay.
* No SAT, so no first-SAT processing and no candidate verification.

Verdict: DECIDED. Every admissible (9,3) plain formula (203/203) is UNSAT-VERIFIED (EXACT, formula scope); the geometric
reading is conditional PROVED-1. Focus compute stops; the lead review is next.
