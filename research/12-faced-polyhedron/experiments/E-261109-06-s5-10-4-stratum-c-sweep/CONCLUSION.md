# E-261109-06: conclusion

2026-11-10. One owner laptop launch (`launch.sh 09-06 start`), 10 shards, root `results/run`, started 2026-11-09 23:02:44
local (20:02:44 UTC), commit `5960a9c` (pre-registration `dc4666b`), one attempt per shard, no restart, no Actions run.

* **Runs**: 10 shards, every one `SHARD-COMPLETE`, `exit_status: 0`. Core-hours from the attempt manifests
  (`*/attempt_*/manifest.json`, equal to `budget.json`): **63.84 core-h** (cap 80); shards 5.99-6.87 core-h; last shard
  (7) ended 02:54:44 UTC, wall **6.87 h** of the 10 h limit. No sleep gap: in every shard wall time minus summed unit
  seconds is 22-24 s. Identity (`identity.json`): queue SHA-256 `85d8faf2...` as in the PLAN, kissat SHA-256
  `4bc06993...` as in the PLAN, `no_proof: true`; every map solver log reports `c Version 4.0.4 8af8e56f`.
* **Controls**: in all 10 shards the positive control `control-f10-sK` is SAT with `model_checked: true` and the negative
  `control-f10-neg-sK` is UNSAT-SOLVER, each < 0.1 s; no `stop.json`, no `first_sat.json`. The controls test the pipeline
  with pinned planes, not the power of a 3600 s cap on free formulas.
* **Results**: 378 units recorded (358 maps, 20 controls), all `ended_by: completed`. The 358 maps of `queue.json` are all
  **UNSAT-SOLVER** (each solver log ends in `s UNSATISFIABLE`; no log reports SATISFIABLE), 0 SAT, 0 TIMEOUT; every unit
  keeps its CNF SHA-256 in `results.jsonl` (358 distinct). With the E-261108-03 records of 845 and 146
  (`summary.py`, kissat solver seconds, 10 simultaneous shards):

  | pattern | n | decided | censored | median s | max s | core-h | f_p = mean / (9,3) mean |
  |---|---:|---:|---:|---:|---:|---:|---:|
  | `(1,2,3)/(2,3)` | 38 | 38 | 0 | 283.3 | 497.6 | 3.15 | 8.07 |
  | `(1,1,1,3)` | 58 | 58 | 0 | 523.5 | 1380.6 | 9.71 | 7.54 |
  | `(1,1,2,2)/(2,3)` | 70 | 70 | 0 | 682.0 | 1703.2 | 14.37 | 7.70 |
  | `(1,1,2,2)/(2,2,2)` | 186 | 186 | 0 | 636.8 | 2041.3 | 35.88 | 6.74 |
  | `(2,2,2)/(2,2,2)` | 7 | 7 | 0 | 414.2 | 692.6 | 0.80 | 13.66 |
  | `(3,3)/(4)` | 1 | 1 | 0 | 389.2 | 389.2 | 0.11 | - |

  Registered output: 360/360 decided, 0 censored, **f = 7.16**, price A = 250.3, B = 234.8 core-h, A + B = **6.06 laptop
  nights**; verdict `ALL-DECIDED-0-SAT: A/B > 4 nights; Actions after item 2 if allowed`; not over 1.5x the scenario.
* **Prediction vs outcome**: P1 (all 360 decided, <= 76.5 core-h): **holds** (63.84). P2 (0 SAT): **holds**. P3 (f puts
  A + B above 4 nights): **holds** (6.06). P4 (no pattern > 10 % censored): **holds** (0 censored). H1 (all decided within
  80 core-h, near 51): holds, at 1.25x the scenario; H0 (> 1.5x, < 300 decided or > 10 % censored): rejected.
* **Pricing caveat** (not registered; it does not change the verdict): f is measured on stratum C only. Within C, f_p falls
  slightly as the (9,3) pattern mean grows (8.07 at 37 s to 6.74 at 103 s, the 7-map `(2,2,2)/(2,2,2)` aside); the only
  A and B maps measured, 96 and 85 (E-261108-03), have ratios 4.4 and 5.5. With those ratios A + B = 154 + 180 = 334 core-h
  = 4.18 nights, still above 4. Both prices are scenarios (n = 1 in A and in B), not bounds.
* **Exact verification**: no SAT, so no model check beyond the controls, no realization stage, no `verify_candidate.py` and
  no `candidate-check`. No UNSAT is used as evidence: every UNSAT here is UNSAT-SOLVER (`NO_PROOF=1`, no proof, no checker
  transcript).
* **What may be claimed**: NUMERICAL, instance scope (SPEC §4 counter UNSAT-SOLVER). kissat rel-4.0.4 reports UNSAT on
  the plain uniform S5 formula of the E-261103-02 encoder for each of the 360 admissible (10,4) maps of the six patterns
  outside `(1^4,2)` and `1^6`, in 148-2041 s per map (845 and 146 from E-261108-03: 188, 693 s) on the laptop with 10 shards, 63.84 core-h for the 358 run here.
  Stratum C holds no SAT plain formula that kissat finds within these times; the C cost is 1.25x the review's scenario.
* **What may NOT be claimed**: that any stratum C map has no realization, or that stratum C is excluded (UNSAT-SOLVER is
  never a negative result; a negative claim needs a replay with checked proofs, PROTOCOL §5); anything about strata A
  (520 maps) and B (237), which were not run; that the A and B prices are measured (f is extrapolated from C); anything
  about non-cubic (10,4) objects (STATUS §4 scope); a second encoder, another solver or DRAT on these maps (not run).
* **Verdict for the direction**: (10,4) plain exact route with kissat: **OPEN@63.84 core-h, stratum C 360/360
  UNSAT-SOLVER, 0 SAT** (the route works at the predicted cost; no witness in C). H-261101-07 stays open; no scenario
  move (0 SAT, all decided, below 1.5x).
* **Next step** (follow-up tree, nothing starts without the owner): A + B = 6.06 > 4 nights -> no stratum A night
  proposal; strata A and B go to Actions after week item 2 (Actions calibration), if GitHub's terms allow it; week item 3
  (cube-and-conquer on 96, 85) may lower the A/B price. Laptop nights for A remain the owner's alternative (about 3.1
  nights for A at f = 7.16).
* **Rows updated**: `STATUS.md` 3ad and "As of", `ROADMAP.md` E-261109-06 row `done`, `experiment-log.md` (2026-11-10),
  `hypotheses/H-261101-07`, README, `reports/NIGHT_REPORT_2026-11-09.md`.
