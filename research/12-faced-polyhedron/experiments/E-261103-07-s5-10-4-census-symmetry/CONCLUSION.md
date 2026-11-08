# E-261103-07: (10, 4) cost probe conclusion

2026-11-08. One laptop run, 10 shards, one map per shard, started 15:18:17 UTC; commit `78b25aa` (pre-registration `bf1a756`).

* **Runs**: shards 0-5 (fast patterns, solver cap 300 s) ended at 308.8 s wall, shards 6-9 (slow patterns, cap 1800 s) at 1809.9 s;
  longest shard 0.50 h of the 2 h deadline. Sum of the shard wall times (`SHARD-COMPLETE` in `night.log`): 9093 s = 2.53 core-h
  (reservation 58,200 s, cap bound about 6.5 core-h). The manifests carry only start time and exit status (all 0), no core-hours;
  the figure is the sum of the logged shard wall times, not a manifest value. No Actions run.
* **Controls**: all 20 pass (10 positive `control-f10-sK` SAT with a checked model, 10 negative `control-f10-neg-sK` UNSAT-VERIFIED,
  each below 0.14 s). They test the n = 10 encoder-solver-checker path, not solve times: the planes are pinned, so a 300 s cap
  has no power statement from them.
* **Result**: 0 SAT, 0 UNSAT-VERIFIED, **10 of 10 maps TIMEOUT** (solver stopped by the cap): maps 690, 1104, 78, 845, 146, 57 at 300 s
  and 96, 926 (`(1^4,2)`), 85, 852 (`1^6`) at 1800 s. Each formula has about 12,950 variables and 157,400 clauses (the pre-registered
  size).
* **Prediction vs outcome**: (1) >= 5/6 fast maps decided at 300 s: **failed**, 0/6. (2) F between 2 and 10: **not measurable**, every
  F_p is a lower bound; per map (cap / (9,3) reference): 690 > 3.3, 1104 > 3.3, 78 > 5.2, 845 > 8.3, 146 > 11.1, 57 none (no reference),
  96 > 8.5, 926 > 8.5, 85 > 3.6, 852 > 3.6, so F exceeds 3.3 at least and for the pattern `(2,2,2)/(2,2,2)` already exceeds the H1 bound
  of 10. (3) >= 2/4 slow maps within 1800 s: **failed**, 0/4. (4) 0 SAT: holds. (5) controls pass in every shard: holds.
* **Exact verification**: no SAT and no UNSAT used as evidence (the 10 negative-control UNSATs carry their CNF/proof hashes and
  `s VERIFIED` in `results/probe/*/results.jsonl`; cached acceptance, no replay). No candidate, so no `candidate-check`.
* **Verdict rule (pre-registered)**: >= 3 of 6 fast maps TIMEOUT (here 6) and all 4 slow maps TIMEOUT -> **"needs a speed-up first"**
  (an item 5b-type benchmark before any full (10, 4) run). The projection P is not computed (F undetermined).
* **What may be claimed**: NUMERICAL, instance scope: for these 10 (10, 4) maps, the plain uniform S5 formula (E-261103-03 encoder,
  CaDiCaL, default options, 10 simultaneous shards on the laptop) is not decided within 300 s (fast patterns) or 1800 s (slow
  patterns); controls at n = 10 pass. Pattern coverage: one map per fast pattern, two per slow pattern.
* **What may NOT be claimed**: nothing about the existence of a (10, 4) polyhedron (no SAT, no UNSAT); not "the route is infeasible"
  (a timeout is not a result, caps were chosen from (9,3) medians; other seeds, caps, solver options or cube-and-conquer were not run);
  no per-pattern distribution; no growth factor value; the cost of all 1117 maps.
* **Verdict for the direction**: (10, 4) exact plain route: NEEDS-SPEED-UP@2.53 core-h, 10 maps, caps 300/1800 s (not LOW-YIELD:
  the budget is a probe, the cap is below the (9,3) 90th percentile for some patterns). No hypothesis changes: H-261101-07 stays open.
* **Next step**: lead review decides (review 2026-11-08c §4, option 2): a speed-up benchmark on (10, 4) maps (CaDiCaL options,
  kissat, cube-and-conquer, symmetry breaking by Aut+; must say in its `PLAN.md` what differs from the parked plain run), or
  longer caps on the same 10 maps. No new ROADMAP row here.
* **Rows updated**: `STATUS.md` 3w and "As of", `ROADMAP.md` E-261103-07 `done`, `experiment-log.md` (2026-11-08), README, night report.
