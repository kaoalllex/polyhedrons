# E-261101-25: chirotope-first realization (algorithm v2)

Pre-registration. Written before the night run; the session pilot (controls and a few seeds) is recorded under
Amendments.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2.
* **Question**: does a SAT solver, given the rank-3 signs of a Gauss-admissible plane set as assumptions, reach a
  model of the full 12-face embedding instance after few core-guided releases, and do such models realize?
* **Hypotheses moved**: H-261101-17 (supported by fast decisions, small cores, a model within the round budget;
  weakened by timeouts or cores of hundreds of literals), H-261101-12 (a model that fails realization from many
  starts is weak evidence for non-realizable OMs; a final polynomial would make it exact), H-261101-01 (a realized
  model is an S0 candidate).
* **H1 / H0**: H1 = models are reached within 40 rounds for most seeds and some realize; H0 = every seed ends in a
  timeout or in 'ROUNDS' with nothing realized.
* **Why this**: FD2 makes embedding a logical constraint, FD8 makes the problem easy once the normals' combinatorics
  is fixed, and the project's exact seeds (class seeds, witnesses) are the natural assumptions; nothing has searched
  the OM side for models before (OM-SAT was used only for UNSAT).
* **Method**: `chirotope_first.py run --type T --seeds <class seeds, witnesses> --random-seeds R --timeout 120
  --rounds 40`; target S0; counters: `EMBEDDED` (exact), core sizes, solve seconds, releases, realized wrong signs.
  Optional face ladder `--ladder 7`.
* **Controls**: positive: `control-szilassi` (n = 7, random seeds -> EMBEDDED) and `control-realizer` (exact
  chirotopes of the type-0 witness and of a class seed recovered from random starts, 0 wrong signs); negative: the
  instance with all assumptions released is the known hard asymmetric instance (a timeout there is expected and
  carries no information); `count-clauses` shows the restricted encoder equals `omsat.build` on the full face set.
* **Counter calibration**: core size is reported per round and must vary (not constant); 'realized wrong signs'
  must be 0 on the controls and positive on a random sign vector (a random chirotope is not realizable).
* **Scenario move**: a realized 12-face model raises A to near 1; models that never realize raise C; fast UNSAT
  with empty core (unassumed instance UNSAT) would raise B but is not expected within the time limits.
* **Pilot**: controls plus 2 class seeds of type 0 at 120 s per solve (minutes).
* **Budget**: night: 11 workers x 8 h on the laptop, seeds = all 149 class seeds (their types) + 7 type-0 witnesses
  + 50 random Gauss-admissible seeds; shard = seed list slice.
* **Power statement**: 200 seeds x 40 rounds x 120 s bounds the night; a seed that times out at round 0 tells
  nothing about existence; only the fraction of seeds that reach a model, and the realization rate, are measured.
* **Outcomes**: realized model -> `candidate-check`, stop everything; models but no realization -> E-261101-15
  needs a realizability stage (final polynomials), H-261101-12 up; timeouts at every round -> H-261101-17 down,
  try the face ladder (`--ladder 7`) before giving up; UNSAT with an empty core -> the type is excluded (keep the
  DRAT: not produced by this script yet, re-run with proofs).
* **Stop rule**: as in README.
* **STATUS / ROADMAP changes**: DR8 verdict line per outcome; new FD or witness only after `candidate-check`.

## Amendments

* 2026-11-01 pilot, session (commit of the engine follows this entry). Encoder check: `build_faces(all)` produces
  exactly `omsat.build`'s formula for type 0 (19,635 vars, 481,742 clauses, identical clause lists).
  Controls: `control-szilassi`, 3 random seeds -> core-guided SAT in 2-3 rounds (cores 14-16 of 35), realized in one
  restart, exact EMBEDDED 3/3; with all 70 signs as assumptions: 5 rounds, re-add keeps 15, EMBEDDED. Realizer
  control: the exact chirotopes of the type-0 witness and of a class seed (715 signs) recovered from a random start in
  0.3 s each, 0 wrong signs.
  Pilots A-B (type 0, full instance, rank-3 assumptions from a class seed and from the witness, 60 s per solve):
  round 0 UNSAT in 0.3 s with cores 78 and 75; round 1 UNSAT in 3-8 s with cores 99 and 106; round 2 with ~40
  assumptions left: TIMEOUT. Releasing whole cores reaches the unassumed hard instance in two rounds.
  Pilots C-D (face ladder, k = 7, rank-3 assumptions): SAT after one release (core 77) in 2-6 s, but the models did not
  realize (14 and 31 wrong signs after 4 restarts).
  Pilots E-F (k = 7, all 715 signs as assumptions, re-add 15): SAT after 7-8 rounds releasing 623-635 signs, re-add
  recovers 13-14, models not realized (13-14 wrong signs).
  Pilot G (k = 7, alternating projections, 6 iterations): wrong signs 15 -> 12 -> 8 -> 9 -> 15 -> 15: the solves are
  instant (<= 5 s), the bottleneck is the realizability of the models, and releasing whole cores overshoots.
  Change made after G: the projection step is now an exact MaxSAT (RC2: hard = instance, soft = the seed's signs), i.e.
  the embedding model with the minimum number of flipped signs; pilot H below.
  Pilot H (k = 7, exact RC2 MaxSAT, 180 s): n = 7 control fine (17 flips, EMBEDDED); at n = 12 TIMEOUT: exact MaxSAT
  on 440k hard clauses and 715 soft units is too slow here. Pilot J (anytime LSU MaxSAT, 120 s): the CaDiCaL oracle in
  pysat ignored the interrupt, no model returned; mode kept as experimental, default is `core`.
  Pilot I (k = 7, core-guided with a full greedy re-add pass = a minimal correction set, 6 alternations): the release
  shrinks to 8-9 signs (re-add keeps 419-514 of ~630 released; 60-150 s per projection), and the alternation reaches
  a fixed point: the 7-face model is 8 sign flips away from the realized configuration, and that model does not
  realize (8 wrong signs after 5 restarts, three identical iterations). Reading: the SAT instance has no realizability
  constraints, so the nearest embedding model is a non-realizable chirotope; alternating projections between the
  two non-convex sets stall there. Change: heuristic no-good blocking of the exact flipped-sign set of a model that
  failed to realize (`--block 1`), so the next projection returns a different near model; pilot K.
  Pilot K (k = 7, blocking on, 8 alternations, ~1-4 min each, re-add dominating): wrong signs after realization
  15, 32, 16, 15, 10, 5, 9, 16; the flipped-sign sets of the blocked models had sizes 122, 238, 19, 21, 13, 10, 17,
  216. Blocking diversifies the near models (best 5 wrong signs, from 8 before) but no k = 7 model realized within
  8 alternations. Two-stage realizer added after K (normals by hinge on the 220 rank-3 signs, offsets by an exact LP,
  FD8): exact on n = 7 (LP margin 0.02); on the n = 12 realizer control from random normal starts the offsets LP is
  infeasible (190-339 wrong signs) because the fixed-normal fibre is empty for most normals with the right rank-3
  combinatorics (the thinness of H-261101-09 seen directly); used in the loop with the seed's normals as warm start
  and the hinge realizer as fallback. Night settings in `run.sh`: `--ladder 7 --alt 20 --timeout 60 --rounds 12
  --readd 1000 --realize-restarts 6 --block 1 --realizer two-stage`. Open weaknesses for the next version: no
  realizability constraints in the SAT instance (final polynomials would be exact cuts); re-add is the time sink
  (a binary-search MCS would cut it 10x); the LSU/RC2 projections are unusable at n = 12 in pysat.
  Follow-up (same session): `final_polynomial.py` added: biquadratic final polynomials over all 25,740 three-term
  Grassmann-Pluecker relations of the 13-element rank-4 chirotope, LP in 715 log-variables, Farkas multipliers
  rounded to rationals and the identity re-checked exactly (an EXACT certificate is a proof of non-realizability; a
  feasible LP proves nothing). Control: the chirotopes of the type-0 witness and of a class seed are FEASIBLE
  (t* = 0.0065 and 0.0071, 6-8 s each). Single-sign flips of a realizable chirotope that remain chirotopes were not
  certified (5 tried), as expected for mutations. In the loop: every model that fails to realize is tested; an exact
  final polynomial becomes a SOUND cut (at least one bracket of its support must change sign), otherwise the
  heuristic block is used. Re-add replaced by the CLD algorithm for minimal correction sets (one disjunction of all
  released literals under a selector per call; all literals true in the model are added back at once).

## Night run 1 (pre-registered 2026-11-01, before launch)

* **Command**: `caffeinate -dimsu bash experiments/E-261101-25-chirotope-first/run.sh <shard>` for shards 0-9 (each a
  tenth of the 149 class seeds, type taken from the seed), one process per shard, laptop on AC power.
* **Engine settings** (fixed in `run.sh`): face ladder from k = 7, 20 alternations per k, 60 s per SAT call, 12
  core-guided rounds, CLD re-add (60 calls max), 6 realizer restarts, two-stage realizer with hinge fallback, final
  polynomials on every unrealized model (exact ones become sound cuts), heuristic blocks otherwise.
* **Predictions, written before the run**: (P1) every seed's k = 7 step produces SAT models within the round budget
  (solves took <= 6 s in the pilots); (P2) at least 30 % of the unrealized k = 7 models receive an EXACT final
  polynomial (if far fewer, non-realizability is not the main reason the realizer fails and the realizer is the
  weak link); (P3) at least one seed realizes a k = 7 model (a 7-face partial object of its type in the right
  class, the first of its kind in the project); (P4) no seed reaches k = 12 (if one does, `candidate-check` at once).
* **What each outcome changes**: P2 false -> invest in the realizer (more restarts, staged flips), not in cuts; P3
  false -> the alternation needs the Farkas-type guidance of E-261101-24 or the MaxSAT projection made tractable;
  P3 true -> run the same seeds to k = 8, 9 (E-261101-23 owns the UNSAT side); P4 false -> stop everything and verify.
* **Collection**: `results/<shard>/results.jsonl` and `manifest.txt` (core-hours), analysed by `experiment-conclude`.
  Pilot L (k = 7, CLD re-add, final polynomials, SIMPLE clauses, 6 alternations) was still running when night 6 was
  handed over; its record will appear in `results/pilot_type0_fp.jsonl` and is to be read with the night's results.
  Night settings now also include `--simple 1` (explicit face-simplicity clauses, as in the certified immersion
  instances) and `--fp 1`.
