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

## Owner run conclusion (2026-11-14)
* **Verdict: COMPLETE-UNSAT-SOLVER.** SPEC §4 instance scope; NUMERICAL cost observations.
  No checked proof, geometric negative, target witness or change to H-261101-07 / A/B/C.
* **Prediction vs outcome:** the full queue fits the registered budget. All 753 remaining maps
  returned UNSAT-SOLVER: A 518, B 235; no SAT, TIMEOUT or ERROR. With prep #96/#926/#85/#852,
  all 757 A+B maps have solver answers. No queue entries remain; no duplicate decisions.
* **Runs:** ten shards, two launcher invocations at 18:17:00 and 20:35:15 local time;
  last manifest 21:03:22. Total elapsed span 2 h 46 min; maximum cumulative worker wall
  5574.712 s, below 8 h per shard. Worker CPU totals 14.207803 core-h against 80 core-h;
  worker wall sum 14.249804 h; solver sum 14.202252 h. Outer launcher CPU is not recorded.
  Per-shard counts, timings and both manifests: results/night-summary.json.
* **Timing limits:** maximum solve 392.757 s against 3600 s. First passes ended normally;
  the idle interval before restart is not compute. Endpoint clock gaps <=0.109 s;
  no heartbeat exists, so sleep cannot be excluded from endpoint clocks alone.
* **Controls / verification:** saved invariance, positive and negative PASS summaries reused;
  current Python, dependencies, solver, encoder, queue and runner hashes match recorded provenance.
  Fresh read-only audit PASS: exact queue/shard coverage, unique records, per-map checkpoint equality,
  CNF hash presence and all solver logs reporting UNSATISFIABLE / exit 20; no solver or DRAT replay.
* **Scope:** no SAT model to bridge or candidate to verify. Recovery controls do not measure discovery
  power; neither LOW-YIELD nor a geometric exclusion follows. Stratum C was not rerun.
* **Evidence:** results/night-summary.json binds retained records and local raw logs by SHA-256;
  results/run holds the two sets of manifests, checkpoints and launcher logs.
* **Next:** item 2 done; proceed to week item 5. The lead may propose a proof replay and
  I-261114-03 (11,5) probe. Neither is launched or approved by this conclusion; no second night.
