# E-261110-06: preparation (2026-11-14)
* **Verdict: READY FOR ONE OWNER NIGHT.** NUMERICAL cost estimate; SPEC §4 instance scope.
  No target witness and no geometric negative; H-261101-07 and A/B/C unchanged.
* **Prediction vs outcome:** all ten probe maps UNSAT-SOLVER, no SAT / TIMEOUT / ERROR.
  Three existing normalized timings reused; seven new decisions, ten shards, no proofs.
* **Cost:** A samples #96/#926: 23.981/31.806 s; B #85/#852: 203.839/70.678 s.
  P = 13.065 solver core-h; partial total-time projection 13.085 core-h (reused samples
  lack per-unit build time). Two samples per pattern do not bound the slow tail.
* **Runs:** new worker CPU deltas 0.077615 core-h; maximum worker wall 129.353 s,
  versus 1800 s solver caps and 6 core-h prep ceiling. Parent CPU not recorded.
  AC checked, caffeinate attached; endpoint clock difference <= 0.150 s, no heartbeat.
* **Reuse:** encoder, solver, Python and dependencies match E-261114-01 environment;
  invariance / positive / negative summaries PASS. No solver, geometry or DRAT replay.
* **Queue:** both strata, 753 remaining maps; four already decided A/B samples excluded.
  Bound sources and census in queue.json. Cap 3600 s, ten shards, <=80 core-h / 8 h.
* **SAT path:** thirty solver seeds, bridge with submap=False and exact --target S5;
  fewer than thirty SAT models explicitly incomplete. No first-SAT stop.
* **Verification:** two focused tests PASS; compile / bash syntax PASS; integrated quick
  ALL PASS, archive SKIP. Corrected actual launcher start/status/stop/start test PASS:
  ten 0.01 s TIMEOUT records, restart adds none. No production night started.
* **Startup failures:** first detached attempt signal 9 (cause unknown); next fixture lost
  QUEUE to launcher's array and dispatched no maps. S5AB_QUEUE fixes the fixture override.
* **Evidence:** results/validation.json, results/prep/summary.json, results/startup.json.
* **Next:** owner launch via overnight/launch.sh 10-06 start on AC; conclude the night
  before item 5. Stop on first verified candidate or failed control; no second night by default.
