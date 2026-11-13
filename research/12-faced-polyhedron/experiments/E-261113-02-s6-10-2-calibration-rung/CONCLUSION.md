# E-261113-02: conclusion

2026-11-13. One owner launch (`launch.sh 13-02 10-05 start`, queued before E-261110-05), 10 shards, root `results/run/`,
commit `c242b0df` in every attempt manifest, `queue.json` sha256 `2568a267...cd2e`, `no_proof: true`, kissat 4.0.4.

* **Runs**: started 15:28 UTC, every shard `SHARD-COMPLETE` with one attempt, all ended by 15:29:42 UTC: wall about
  1.5 min of the ~0.3 core-h plan; **0.239 core-h** (sum of the ten attempt manifests; pilot 0.014 core-h) against
  the 3 core-h budget and the 10 core-h runner ceiling. No sleep gap, no restart.
* **Controls**: encoder controls `CONTROLS-PASS` in all shards; convex f10 positive SAT, negative UNSAT-SOLVER (20/20);
  importer checks passed at the freeze; the witness map #739 SAT on all three seeds.
* **Results** (`summary.py`): 153/153 units SAT (150 drawn, 3 witness); 0 UNSAT-SOLVER, 0 TIMEOUT; median SAT time
  **0.83 s**, maximum **5.2 s**; no seed spread, no mixed map. Bridge: **16 of 153** SAT models realized (10.5 %),
  on 13 of the 50 drawn maps (#148, 309, 364 x2, 427, 443, 494 x2, 521, 574, 603, 608, 667, 704, 735 x2), none of
  the three witness models; two_stage 9, hinge 7; every realized file `--target S6` PASS in the run (rc 0).
  Drawn units used 0.188 core-h of solver and bridge time.
* **Prediction vs outcome**: P1 (median < 60 s, ~60 %) held; P2 (no timeout, ~50 %) held; P3 (bridge >= 50 %,
  ~60 %) failed (10.5 %); P4 (drawn units < 0.3 core-h, ~70 %) held.
* **Readings** (registered tree): **LIGHT** -> the (10, 3) timeouts of E-261110-02 read "probably UNSAT" for
  planning only, route = week item 4; **BRIDGE < 50 %** -> a SAT in the E-261113-01 line takes more models per SAT
  (no SAT occurred there); **CHEAP** -> the full 865 x 3 seeds in the same budget, one owner launch.
* **What may be claimed**: instance scope: on these 50 maps every `submap=True` (10, 2) formula is SAT within 6 s on
  every seed (NUMERICAL timing, EXACT model check); the frozen bridge realizes about one model in ten. The 16
  realized files are S6 (10, 2) control objects on 13 maps other than the witness's, checked by `verify_candidate.py
  --target S6` in the run only (no `candidate-check`, no independent `verify_s6_10_2.py` replay); not a headline,
  never S0 or S5 objects.
* **What may NOT be claimed**: anything about (10, 3) existence; that the (10, 3) formulas are UNSAT (the gap between
  6 s and 3600 s is a planning reading only); a bridge rate beyond these maps and settings.
* **Verdict**: **DONE (calibration)@0.239 core-h**: SAT at (10, 2) is fast and light-tailed, realization is the
  bottleneck. No scenario move; H-261110-03 unchanged.
* **Next**: the full 865 (follow-up branch, owner launch after `make_queue.py` gains the full list); week item 4.
  For the lead: the bridge realizes ~10 % of models even where objects exist; the SAT-to-coordinates step, not the
  solver, limits any (10, 3) SAT.
