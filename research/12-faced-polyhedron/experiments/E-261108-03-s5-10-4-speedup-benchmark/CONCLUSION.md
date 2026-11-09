# E-261108-03: conclusion

2026-11-09. One laptop launch (`launch.sh 08-03 start`), 10 shards, five roots `results/run/{kissat,unsat}-{A,B}` and
`default-B`, started 2026-11-08 22:21:09 local (19:21:09 UTC), commit `3f24a5c` (pre-registration `8f0e508`, amendment 2).
No restart, no Actions run.

* **Runs**: 50 shard-root jobs. Sum of the `SHARD-COMPLETE` wall times in `results/run/*/night.log`: 30,930.5 s = **8.59
  core-h** (cap 47 core-h); longest shard 5 (default-B ended 00:44:04), wall 2.38 h of the 5.1 h limit. The manifests hold
  only the start time and `exit_status: 0`, no core-hours; the figure is the logged sum, not a manifest value. No sleep
  gap: each job's start equals the previous start plus its logged wall time. `~/bin/kissat` and `~/bin/cadical`
  SHA-256 equal the values in the PLAN and in `identity.json`; `no_proof: true` in every root.
* **Controls**: in every root and shard the positive control (`control-f9-sK` / `control-f10-sK`) is SAT with a checked
  model and the negative is UNSAT-SOLVER, each <= 0.1 s, for both variants and the default baseline; shards without a
  unit carry an extra positive control. No variant is rejected. The controls test the pipeline with pinned planes, not
  solve times. Without DRAT a negative control is UNSAT-SOLVER, not UNSAT-VERIFIED (amendment 2).
* **Results** (solver seconds, 10 simultaneous shards; no SAT anywhere; UNSAT-SOLVER = no checked proof):

  | map | kissat | `--unsat` | default CaDiCaL |
  |---|---|---|---|
  | (10,4) 96 `(1^4,2)` | 1073.5 | 3118.6 | 1969.6 |
  | (10,4) 85 `1^6` | 2748.9 | 8419.5 | 6453.8 |
  | (10,4) 146 `(2,2,2)/(2,2,2)` | 692.6 | 1415.2 | not run (300 s TIMEOUT, E-261103-07) |
  | (10,4) 845 `(1,2,3)` | 188.4 | 366.7 | not run (300 s TIMEOUT, E-261103-07) |
  | (9,3) 7 | 894.4 | TIMEOUT 1800 | - |
  | (9,3) 87 / 130 | 139.9 / 138.6 | 270.1 / 330.6 | - |
  | (9,3) 165 / 29 / 184 | 107.2 / 35.9 / 47.4 | 179.5 / 35.0 / 50.7 | - |

  All 12 Phase A answers agree with the recorded UNSAT-VERIFIED records (no SAT, no failed control); `--unsat` on map 7
  is censored at 1800 s. All (10,4) answers of the three solvers agree (UNSAT-SOLVER on maps 96, 85, 146, 845).
* **Speed-up** (same machine, same load, same formula): kissat / default on (10,4): 96 1.83x, 85 2.35x (both defaults
  decided, so these are ratios, not bounds); `--unsat` / default: 0.63x, 0.77x (slower). Against the recorded
  (9,3) default solver times of the PLAN (earlier runs, indicative only): kissat 7 1.4x, 87 6.0x, 130 4.6x faster,
  165 (81 s), 29 (29 s), 184 (35 s) 0.76x, 0.81x, 0.74x (slower on the fast maps); `--unsat` 7 > 0.69x, 87 3.1x, 130
  1.9x, 165 0.45x, 29 0.83x, 184 0.69x. **No variant reaches 10x; the best measured (10,4) ratio is 2.35x.**
* **Projection** (`projection.py`, selftest OK: all censored P(4) = 5,585, all decided at 60 s P(4) = 23.3; strata A 96,
  B 85, C 146 + 845; n = 1, 1, 2). Registered (tau = 3600 s, a unit above 3600 s is censored):

  | variant | n/k A | n/k B | n/k C | mu A, B, C (s) | censored | sum B (core-h) | P(4) | P(16) |
  |---|---|---|---|---|---|---|---|---|
  | kissat | 1/1 | 1/1 | 2/2 | 1073, 2749, 441 | none | 380 | **475** | 475 |
  | `--unsat` | 1/1 | 1/0 | 2/2 | 3119, -, 891 | 85 at 3600 s (decided at 8419 s) | 777 | 1,859 | 5,414 |
  | default (96, 85 only) | 1/1 | 1/0 | - | 1970, - | 85 at 3600 s (decided at 6454 s) | stratum C empty | infinity | infinity |

  Second report with the measured times (every unit decided): kissat unchanged; `--unsat` sum B 1,094, P(4) = P(16) =
  1,367. Without DRAT: a campaign with proofs adds the checker (0.6-0.9x of the solver time, PLAN amendment 2).
* **Prediction vs outcome**: P1 (kissat decides >= 1 of 146 / 845): **holds**, both. P2 (neither variant decides 85
  within the cap): **failed** (kissat 2749 s, `--unsat` 8419 s at the amended cap; within 3600 s only kissat). P3 (both
  decide 165, 29, 184): **holds**. P4 (no winner): **failed**, kissat wins. H1 as written (a variant decides 96 or 85
  within 2400 s with P(4) <= 1000): **holds for kissat** (96 in 1073 s, P(4) = 475). The goal "at least 10x cheaper" is
  **not met** (<= 2.35x). H0 (no variant decides a slow (10,4) map): rejected at this n and cap.
* **Winner rule**: kissat decides at least as many as `--unsat` in A and B (1/1 and 1/1 against 1/1 and 1/0), smaller
  P(4) (475 against 1,859), and sum B 380 against 777 = 2.04x >= 2 (measured times 2.9x). Winner = kissat, narrowly on
  the sum B criterion; the registered rule does not ask for more.
* **Exact verification**: no SAT, so no `verify_candidate.py` and no `candidate-check`. No UNSAT is used as evidence: every
  UNSAT here is UNSAT-SOLVER (no proof, `NO_PROOF=1`), and the (9,3) agreement is with already UNSAT-VERIFIED records.
* **What may be claimed**: NUMERICAL, instance scope. On these four (10,4) maps the plain uniform S5 formula of the
  E-261103-02 encoder is decided (UNSAT-SOLVER, three solvers agreeing) by kissat rel-4.0.4 in 189-2749 s, by CaDiCaL
  `--unsat` in 367-8420 s, by default CaDiCaL in 1970 s (96) and 6454 s (85) on the laptop with 10 shards. A censored
  projection with n = 1-2 per stratum gives P(4) = 475 core-h for kissat without DRAT (a risk-allocating scenario, not a
  bound). The previous 1800 s TIMEOUTs of default CaDiCaL on 96 and 85 were caps, not hardness: both end in UNSAT-SOLVER
  at about 1.1x and 3.6x the cap.
* **What may NOT be claimed**: that any (10,4) map has no realization (UNSAT-SOLVER is not a negative result, `SPEC.md` §4; a
  negative claim needs a checked proof, and every (10,4) UNSAT also carries the item 1 multiplicity >= 3 control caveat); that
  kissat is faster in general (slower than default on the three fast (9,3) maps, using indicative earlier times); the
  per-stratum distribution or the cost of all 1,117 maps (n = 1-2, one sample for A and B); that P(4) = 475 includes the
  checker, proof size or RAM (DRAT-checked solves beyond 1-1.5 h do not fit 48 GB, amendment 2); that cube-and-conquer, other
  kissat options, seeds or the holdout (926, 852, 78, 1104) were run; anything about the 10x goal being reachable.
* **Verdict for the direction**: (10,4) plain exact route with kissat: **OPEN@8.59 core-h, 4 maps, 3 solvers** (a
  decision is within reach; the 10x speed-up goal is not met; P(4) = 475 is between the 160 and 1,000 thresholds). No
  hypothesis changes: H-261101-07 stays open (no SAT).
* **Next step** (follow-up tree, nothing starts without the owner): P(4) in (160, 1000] -> Actions calibration
  ([I-261108-07](../../ideas/I-261108-07-actions-calibration-wave.md)) on known (9,3) maps with proofs checked inside the job, to
  measure runner speed and proof handling; the holdout (all four checked) is conditional on P(4), P(16) <= 160, so it does
  not run. A (10,4) campaign needs the measured runner cost, a proof-checking route that fits memory, and the owner's
  approval. Open V2 of item 2: cube-and-conquer. The lead review decides which.
* **Rows updated**: `STATUS.md` 3x and "As of", `ROADMAP.md` item 2 and the E-261108-03 row `done`, `experiment-log.md`
  (2026-11-09), README, `projection.py` (new), `reports/NIGHT_REPORT_2026-11-08c.md`.
