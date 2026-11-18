# E-261116-02: S6 lookahead cube pilot

## Owner run conclusion (2026-11-16)

* **Verdict: BOTH-DECIDED-UNSAT-SOLVER@3.4313 worker-h recorded.** NUMERICAL,
  SPEC §4 instance scope: the two normalised uniform S6 embedding formulas only.
* **Prediction vs outcome:** the prediction passes. Lutz #1 and #2 each have all
  128 covered cubes UNSAT-SOLVER; both monolithic arms also UNSAT-SOLVER.
  All 258 scheduled units recorded exactly once; no SAT, TIMEOUT or ERROR.
* **Runs:** commit `b5dbef78`, ten shards, longest worker 3039.76 s; summed worker wall
  against the 8 h cap is above. Prep records 4.053 worker-s and the SAT-option control
  0.400 solver-s separately. All ten production JSON manifests present; no manifest.txt
  or CPU accounting. Outer launcher logs include failed starts (`nice: setpriority:
  Operation not permitted`); their overhead is unmeasured. No continuous sleep audit.
* **Methods:** monolithic `kissat --sat` takes 2175.816 / 2525.559 solver-s;
  cube totals 3671.658 / 3926.471 solver-s, respectively. Select monolithic `--sat`
  for the registered follow-up because it costs less on both pilot maps.
  This is not a speedup estimate against the older, censored baseline.
* **Controls / checks:** prep cover and known-SAT gates reused; saved positive
  assignments rechecked, including the SAT-oriented arm. Fresh audit rebuilds all
  target and prep source/cover CNF hashes and checks checkpoint coverage, unit copies,
  solver logs, source/Python/solver identity and budget reconciliation: PASS
  (`results/run-audit.json`); no solves or proof replay, earlier quick PASS reused.
* **Scope / next:** H-261110-03 remains open and S0 A/B/C unchanged. Follow-up gate
  passes: prepare one owner night covering all twenty maps with the winning method,
  <=80 core-h, reusing these two decisions; no rerun of decided maps. The follow-up
  still needs its committed PLAN and checked launcher before an owner launch.
