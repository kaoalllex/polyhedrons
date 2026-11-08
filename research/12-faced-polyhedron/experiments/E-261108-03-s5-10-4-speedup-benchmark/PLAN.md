# E-261108-03: (10,4) speed-up benchmark, kissat and CaDiCaL --unsat

Pre-registration (`PROTOCOL.md` §2) of `ROADMAP.md` week item 2, cut down by the owner on 2026-11-08 21:30.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (lead review 2026-11-08d §7; follow-up of E-261103-07).
* **Owner decision 2026-11-08 21:30 (deviations from item 2)**: one launch tonight, <= 2 h prep, <= 10 core-h, 10 shards.
  V2 = CaDiCaL `--unsat` (the item's fallback) instead of cube-and-conquer, which is a later, separately approved launch.
  Phase A <= 1 core-h in total; Phase B as in the item; the holdout (926, 852, 78, 1104) is not run tonight but is a
  separate short launch after the analysis. Consequence of the 1 core-h cap: Phase A caps are 120/90 s, so the named slow
  maps 7, 87, 130 (default 1240/842/636 s solver) are expected to time out unless a variant is >= 5-10x faster.
* **Question**: does kissat or CaDiCaL `--unsat` make the (10,4) plain formulas >= 10x cheaper, measured on (10,4) maps?
* **Hypotheses moved**: H-261101-07 only by a realized SAT model at (10,4); otherwise a cost measurement that decides the
  compute route (item 2 follow-up tree), not (10,4).
* **H1**: a variant decides >= 1 of the slow maps 96 / 85 within the 2400 s solver cap (their default-CaDiCaL runs
  are censored at 1800 s) and has P(4) <= 1,000 core-h. **H0**: no variant decides a
  slow (10,4) map; the route needs cubing or Actions-scale compute.
* **Why**: E-261103-07 timed out on 10/10 (10,4) maps with default CaDiCaL (STATUS 3w); kissat and `--unsat` are the
  cheapest changes that keep the encoder, the DRAT check and the runner.
* **Method**: the E-261103-03 runner (`tranche.py` through `run_overnight.py s5 --s5-queue`), unchanged except a solver
  choice: `SAT_SOLVER` (binary; default `CADICAL`, i.e. `~/bin/cadical`) and `SOLVER_OPTS` (extra arguments before the
  CNF), recorded in the identity. Binaries (SHA-256): V1 kissat tag `rel-4.0.4`, commit
  8af8e56f174b778aef3aa45af9f739b2a5f492c2, built locally (`./configure && make`), `~/bin/kissat`
  4bc069939394b3b56f8dfa9518094f3a716246d65701635f9c722c2c7af4ceb7, proof format as accepted in the smoke test (binary DRAT,
  else `--no-binary`, recorded as an amendment); V2 `~/bin/cadical` 3.0.1
  4404d246936d892e6ee8433ebba581fc2a19ce5a8f33bb6a8d68e3aa20cf435e with `--unsat`; checker `~/bin/drat-trim`
  8ae847701b5d9537322a3cbdca840ca49f2dd77c6ab7d83539e33bc4eb8c8b09. Target S5, plain uniform formula (`ALL_OPTS`), counters
  `SAT / UNSAT-VERIFIED / TIMEOUT` (SPEC §4); CNF and proofs deleted after the check, hashes and transcripts kept.
* **Units**: Phase A, per variant, (9,3) maps of `maps_9_3.json` 7 and 165 `1^6`, 87 and 130 `(1^4,2)`, 29
  `(1,1,2,2)/(2,2,2)`, 184 `(1,1,1,3)` (165, 29, 184: fastest decided records of their pattern; default solver/checker
  81/49, 29/20, 35/20 s), solver/checker 120/90 s. Phase B, per variant, (10,4) maps of `maps_10_4.json` (SHA-256
  e563f7cd37118742a48446856b571fde87a21bf12d72931b309b58eebb922328) 96 `(1^4,2)`, 85 `1^6`, 146 `(2,2,2)/(2,2,2)`, 845
  `(1,2,3)`, solver/checker 2400/1140 s (+60 s unit slack = 3600 s end-to-end). Queues from `make_queue.py`; four
  roots `results/run/{kissat,unsat}-{A,B}`, each map on its own shard (V1-B shards 0-3, V2-B shards 4-7).
* **Controls**: in every root and shard `pilot.py --controls-only`, a positive pinned-plane control (`control_f9.json` in
  A, `control_f10.json` in B) that must be SAT with a checked model, and its negative (other map, same planes) that must
  be UNSAT-VERIFIED, caps 60/120 s. A wrong model, a failed control or a proof rejected by drat-trim (`s NOT VERIFIED`
  before the cap) rejects that variant; a solver or checker timeout is censored, not a failure.
* **Smoke test (before the launch)**: both variants on the f9 and f10 controls and one fast (9,3) map at short caps through
  this runner, with proof check; results discarded. Not green for both variants by 23:00 -> no launch.
* **Pilot gate**: binding limit = the per-unit solver cap; the launch starts only after the green smoke test.
* **Predictions**: (P1, ~50 %) kissat decides at least one of 146 / 845; (P2, ~70 %) neither variant decides 85; (P3, ~60 %)
  both variants decide 165, 29 and 184 in Phase A; (P4, ~60 %) no winner by the rule below.
* **Projection** (item 2, unchanged): strata A = `(1^4,2)` (N 520, map 96), B = `1^6` (N 237, map 85), C = others (N 360,
  maps 146, 845, pooled). Per variant and stratum n, k checked decisions, p = k/n, mu = mean end-to-end seconds of the
  decided units (0 if k = 0), tau = 3600 s; B_h = N_h [p_h mu_h + (1 - p_h) tau] / 3600,
  R_h(lambda) = N_h (1 - p_h)(lambda - 1) tau / 3600, P(lambda) = 1.25 sum_h [B_h + R_h(lambda)], lambda in {4, 16}. Report
  n, k, p, mu, every censored cap and sum B. Baseline (no new jobs): default CaDiCaL 96, 85 TIMEOUT at 1800 s, 146, 845
  TIMEOUT at 300 s (E-261103-07), censored.
* **Winner**: at least as many checked decisions as the other variant in each slow stratum (A, B), smaller P(4), and >= 2x
  lower sum B; otherwise no winner.
* **Grid**: one setting per variant; the cap is the parameter, fixed by the owner.
* **Budget**: laptop, 10 shards (`matrix.json`), worst case 8 x 3600 + 12 x 270 s + controls (~0.2 s each, measured in
  E-261103-07) + 40 startup checks (~10 s) ~= 9.2 core-h; wall per shard <= 1 h 15 min (one B unit + one or two A units).
* **Power statement**: n = 1-2 per stratum; it can show a variant that decides slow maps at all, not a reliable per-stratum
  rate. A k = 0 stratum gives the full censored term; P is a risk-allocating scenario, not a bound.
* **Counter calibration**: P(lambda) and sum B are formulas over counts, checked by `projection.py --selftest` on both sides
  of the 160 and 1,000 core-h thresholds (all censored -> P(4) = 5,585; all decided at 60 s -> P(4) = 23.3). Speed-up ratios
  are reported only against uncensored baselines (165, 29, 184); against censored ones only as lower bounds.
* **Scenario move**: A exists / B all OM-UNSAT / C OM-SAT but non-realizable: no move from any timing outcome; a realized
  (10,4) SAT moves A (after `candidate-check`); single-map UNSATs move nothing at this n.
* **Outcomes**: SAT -> first-SAT stop, exact model check, realizers, `verify_candidate.py --target S5`, `candidate-check`;
  UNSAT-VERIFIED -> that plain formula only, and every (10,4) UNSAT carries the item 1 caveat (multiplicity >= 3 control)
  until item 1 passes; TIMEOUT -> censored at its cap; near-miss -> not applicable.
* **Follow-up tree** (item 2; nothing starts without the owner): a control fails -> reject that variant; no Phase B
  decision -> park these variants, not the exact route; no winner -> no campaign; winner with P(4), P(16) <= 160 core-h ->
  the holdout launch (all four checked) before a capped two-night proposal; otherwise P(4) <= 1,000 -> Actions calibration
  (I-261108-07); P(4) > 1,000 -> park the route at this budget, escalate; cube-and-conquer remains the open V2 of item 2.
* **Stop rule**: all 8 Phase B units and 12 Phase A units ended, or `launch.sh stop`, or a first SAT.
* **STATUS / ROADMAP**: a new STATUS 3 entry with the table and P; ROADMAP item 2 and the row get the verdict.

## Launch

`bash research/12-faced-polyhedron/overnight/launch.sh 08-03 start` (then `status`, `stop`), on AC power.

## Amendments
