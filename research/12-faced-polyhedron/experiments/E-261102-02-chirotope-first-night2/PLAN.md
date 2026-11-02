# E-261102-02: chirotope-first engine, night run 2

Pre-registration (2026-11-02, before the run). Amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2.
* **Question**: with the round budget no longer binding and every solver call capped, what fraction of the 149 class
  seeds reaches a k = 7 model, how close do those models come to realizing, and how many unrealized models carry an
  exact final polynomial?
* **Hypotheses moved**: H-261101-17 (supported if most seeds reach models with small corrections; weakened if they
  still end ROUNDS at 40 rounds or TIME-CAP without a model), H-261101-12 (exact final polynomials on unrealized
  models; k = 7 scope only), H-261101-01 (a realized model is an S0 candidate only at k = 12, not expected).
* **H1 / H0**: H1 = at least half of the seeds reach a k = 7 model and some model realizes; H0 = no model realizes.
* **What is different from night run 1** (`../E-261101-25-chirotope-first/CONCLUSION.md`): `--rounds 40` instead of
  12 (21 of 27 seeds ended at the round budget); the final-polynomial and offsets LPs have time limits; the seed cap
  also bounds each step (no new round, no re-add and an LP limit past the deadline); `--seed-minutes 40` instead of
  75, so that 15 seeds per shard fit a 10-hour night; all 10 seed slices; exact final polynomials store their
  certificates.
* **PROTOCOL 8a gate**: the engine has not been scored on the benchmark ladder E-261101-26 (not built yet). The owner
  asked on 2026-11-02 to run night 2 first. Consequence, fixed now: a failure on the target is not evidence about the
  engine; only the fractions measured below are reported, and no LOW-YIELD verdict can come from this run.
* **Method**: `run.sh SHARD` (10 shards, shard s = class seeds with index % 10 == s) calls
  `../E-261101-25-chirotope-first/chirotope_first.py run` with `--ladder 7 --alt 20 --timeout 60 --rounds 40
  --readd 1000 --realize-restarts 6 --block 1 --realizer two-stage --simple 1 --fp 1 --seed-minutes 40`. Target S0.
  Counters: core-guided status, released signs (minimal correction set), realized wrong signs, final-polynomial
  status, `EMBEDDED` (exact) if ever reached.
* **Controls**: positive: `control-szilassi` (n = 7, random planes -> EMBEDDED) and `control-realizer` (known 12-plane
  chirotopes recovered), both passed in the E-261101-25 pilot with the same engine; negative: a random sign vector is
  not realized (wrong signs > 0). Smoke run of the changed engine: see Amendments.
* **Counter calibration**: realized wrong signs: 0 on the realizer control, > 0 on random sign vectors; `t_star`:
  > 0 on the type-0 witness and a class seed, 0 with an exact certificate on seed type39-kd_4aecd06992 step 3.
* **Budget**: 10 shards x ~10 h = ~100 core-h, laptop night, 10 performance cores, on AC power.
* **Power statement**: 149 seeds, k = 7 only, 40 minutes per seed; a seed that ends TIME-CAP or ROUNDS says nothing
  about existence; nothing about k >= 8 unless a k = 7 model realizes.
* **Predictions (written before the run)**: (P1) at least half of the seeds that finish reach a k = 7 model (night 1:
  6 of 27 with 12 rounds); (P2) at most 20 % of the unrealized models get an exact final polynomial (night 1: 1 of 19);
  (P3) no k = 7 model realizes (night 1: 0 of 42, best 3 wrong signs); (P4) no shard hangs: every shard keeps writing
  `progress.jsonl` or `night.log` at least once an hour.
* **Scenario move**: a realized k = 7 model raises A slightly and sends the same seeds to k = 8, 9; models that never
  realize, with exact certificates on a sizeable fraction, raise C slightly; otherwise no move.
* **Outcomes and their meaning**: realized k = 7 model: `candidate-check` on its planes (a 7-face partial object,
  not a witness); EMBEDDED at k = 12: `candidate-check`, stop everything; exact final polynomial: a proof about one
  chirotope once an independent checker accepts the certificate; TIME-CAP / ROUNDS / TIMEOUT / LP-TIMEOUT: no
  information.
* **Stop rule**: the night; or the first realized 12-face model (`candidate-check`); or 20 seeds ending ROUNDS at 40
  rounds.
* **STATUS / ROADMAP changes**: STATUS DR8 per outcome; E-261102-02 State done with its verdict.

## Amendments

* 2026-11-02 smoke run (session, before the run): seed type39-kd_4aecd06992 with the night settings and
  `--seed-minutes 1`: 5 alternation steps, final polynomials NUMERICAL, FEASIBLE, FEASIBLE, EXACT (step 3, 98 rows,
  135 brackets, as in night run 1; certificate with 222 bracket signs stored), result TIME-CAP after 62 s.
* 2026-11-02 (owner, before any launch): the request to run before the benchmark ladder is withdrawn. The run is
  launched only after E-261101-26 has scored the chirotope-first engine on the rungs it can address (PROTOCOL 8a);
  the "PROTOCOL 8a gate" paragraph above no longer applies. If the ladder score changes the engine or its settings,
  that change is recorded here as an amendment before the launch.
* 2026-11-02 (infrastructure, before any launch; no change to the engine or its settings): `run.sh` splits the 149
  seeds by `SHARDS` (set by `overnight/launch.sh start DIR CORES`, default 10) and skips a seed recorded by any shard,
  so the owner can run fewer cores by day and all at night without losing or repeating seeds.
