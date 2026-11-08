# Strategy review, 2026-11-08 (d): weekly lead review after item 5a and the (10,4) cost probe

Lead review of the week plan of `reviews/strategy-review-2026-11-08.md` (items 1-5 done) and of the E-261103-07 cost
probe. Evidence cut: `78b25aa` on `lab/2026-11-07` plus the uncommitted E-261103-07 conclusion in the working tree
(`CONCLUSION.md`, STATUS 3w, `results/probe/`). This report advises and changes no ledger file. Labels are `SPEC.md` §5;
**Recommendation** and **Untested** mark judgments and proposals. Checks run (seconds each): pattern counts of the 203
admissible (9,3) maps with `pattern_census.py`, the (8,2) plain solve times in `E-261103-03/results/pilot/summary.json`,
repository visibility and the `experiment` workflow history (`gh`).

## 1. Verdict in ten lines

1. **The focus question has an answer.** EXACT (formula scope): all 203 admissible (9,3) plain formulas and both (8,2)
   plain formulas are UNSAT-VERIFIED. Geometric reading "no S5 polyhedron at (8,2) or (9,3)": PROVED-1, conditional
   on census coverage, encoder soundness and the uniformity reduction; one encoder, one enumerator, no human review.
2. **`STRATEGY.md` §1 is stale; the owner should change it.** The pre-registered S5 rule (`ROADMAP.md:235`) says: both
   cases empty -> write the note, focus moves to (10,4). **Recommendation:** follow it, with a gate on each branch.
3. **The claim has three single points of failure, and one has never been tested.** No positive control contains a
   pair with three or more shared segments (Roest-Vigh and Mizhaev have only doubled pairs), yet 18 of 203 (9,3) maps,
   one of the two (8,2) maps and 109 of 1117 (10,4) maps have such a pair (EXACT counts). The census has one
   enumerator for the full list. The encoder is single.
4. **First item:** a positive control with a tripled and a quadrupled pair (one session, almost no compute). It
   protects the (8,2)/(9,3) claim and gates every (10,4) run.
5. **(10,4) cost probe (NUMERICAL):** 10/10 TIMEOUT at 300/1800 s, per-map growth F > 3.3 (> 11 for one pattern).
   Untested estimate from the (8,2) -> (9,3) step (5-12 s -> medians 27-497 s): F is 10-40, so the plain route at
   default settings costs about 1,200-4,900 core-h, i.e. 15-60 laptop nights. Not a laptop week without a >= 10x speed-up.
6. **Answer to the lab:** option 1, the speed-up benchmark, calibrated first on (9,3) maps with known answers. Not
   option 2: longer caps alone fail the follow-up rule (`STRATEGY.md` §2). Drop Aut+ symmetry breaking: 1021 of 1117
   (10,4) maps have trivial Aut+ (91 %, EXACT), and lex-leader clauses break plain DRAT.
7. **Compute lever not used:** the repository is public, so GitHub Actions minutes are free on standard runners
   (CLAIMED, GitHub's terms, not checked here); the `experiment` workflow has never run an experiment (its last five
   runs were skipped). A (10,4) campaign is plausible only with Actions or a large speed-up.
8. **Credences:** (10,4) 0.30 / 0.30 / 0.40 -> **0.15 / 0.40 / 0.45** (exists / does not / cannot tell); (9,3)
   0 / 1 / 0 -> 0.05 / 0.95 / 0 (a planning weight of 1 overstates a PROVED-1, single-encoder result). S0 unchanged.
9. **Note:** worth doing as a side track (nothing in print, item 2), but it needs the control, a second census, a
   second encoder, regenerated archived proofs and a human reader. The owner decides whether a note is a goal.
10. **S0 transfer stays parked:** 13 elements, F > 3.3 per element; revisit only if the benchmark finds >= 10x.

## 2. Week plan (ready to paste into `ROADMAP.md`, replacing the week plan block)

```
## Week plan (lead review 2026-11-08d, `reviews/strategy-review-2026-11-08d.md`; replaced by the next lead review)

Lab sessions take these in order (PROTOCOL.md §8b). Anything outside a follow-up tree goes to "For the lead".
Laptop: at most 10 cores in total; every splittable run uses 8-10 shards (owner, 2026-11-08). Items 1, 3 and 4 need
no night; item 2 is one owner launch of at most 2 h wall.

1. **Multiplicity >= 3 positive control** (audit, exploit; new idea N1 of the review). Question: does the
   E-261103-02 encoder accept a real embedded polyhedron in which one face pair shares three (and four) collinear
   segments? Object: a box with two (three) V-grooves cut from one edge, groove walls tilted to general position,
   exact rational planes, checked by `ladder_exact` / `verify_solid`. Test: its own map through the `submap=True`
   path, planes pinned: SAT required; the same planes on a map with one segment pairing swapped: UNSAT-VERIFIED
   required; also the unpinned formula if it has <= 13 elements (SAT required). At most 1 session, < 0.1 core-h.
   * Kill: none (a control). Follow-up tree:
     * all pass -> record the control (EXACT) in E-261103-02 and STATUS; items 2-4 proceed;
     * a pinned SAT fails -> stop all S5 compute; the 18 tripled-pair (9,3) UNSATs and the tripled (8,2) UNSAT are
       suspended; escalate (encoder bug hunt, at most 1 session, then the lead).
2. **(10,4) speed-up benchmark** (exploit; new row, follow-up of E-261103-07; what differs from the parked plain run:
   solver, options and cubing). Question: is there a variant that makes the (10,4) plain formulas >= 10x cheaper?
   * Phase A (calibration, known answers): six (9,3) maps already UNSAT-VERIFIED: map 7 and one more `1^6`, maps 87 and
     130 `(1^4,2)`, one `(1,1,2,2)/(2,2,2)`, one `(1,1,1,3)`. Variants: CaDiCaL default (baseline, re-run under the
     same 10-shard load), CaDiCaL `--unsat`, kissat (pinned build), cube-and-conquer (cubes on the segment-order
     variables of the multiple pairs, or march_cu; each cube solved by CaDiCaL; core-seconds summed over cubes). Cap per
     unit 2x the recorded baseline. Metric: core-seconds to UNSAT; times only, no evidence claim.
   * Phase B (only for variants >= 3x faster on >= 3 of the 4 slow Phase A maps; at most 2 variants): the probe maps
     146, 845, 78, 1104 at 1 core-h per map and variant. An UNSAT counts as evidence only with a checked proof (for
     cube-and-conquer: one DRAT per cube plus a checked cube-cover formula; the PLAN fixes the format).
   * Budget: 1 prep session; one owner launch, 10 shards, <= 2 h wall, <= 12 core-h worst case, expected about 6.
   * Kill: no variant >= 3x on Phase A -> no Phase B; (10,4) plain route LOW-YIELD on the laptop; escalate.
   * Follow-up tree, from the projection P_best = sum over patterns of count x (9,3) median x F_best x 1.71 / 3600:
     * P_best <= 160 core-h -> (10,4) completion over two laptop nights (PLAN amendment: fast patterns first,
       first-SAT stop, controls in every shard, the item 1 control included);
     * 160 < P_best <= 1,000 -> Actions calibration wave (queue item 6), then a campaign PLAN; owner decides;
     * P_best > 1,000, or Phase B decides 0 of 4 maps -> escalate: the (10,4) exact route is beyond our compute
       without a new idea;
     * any SAT -> first-SAT stop; exact model check, realizers, `verify_candidate.py --target S5`, `candidate-check`.
3. **Independent census of (8,2) and (9,3)** (audit; new idea N5). Question: does an independently written enumerator
   reproduce 2 classes at (8,2) and 240 classes / 203 admissible at (9,3), with the same canonical hashes? Method not
   shared with E-261103-01 (e.g. genus-g rotation systems of K_F plus the extra edges, by CP-SAT with canonical-form
   deduplication, or lexicographic surface enumeration). At most 2 sessions, minutes of CPU.
   * Kill: two sessions without a complete run -> record, escalate. Follow-up tree: agreement -> coverage evidence
     becomes two-algorithm EXACT (arguments still PROVED-1); any missing map -> its plain formula on one day run,
     10 shards; extra maps in the new enumerator -> bug hunt in one of the two, at most 1 session.
4. **Second encoder on six (9,3) maps** (audit; review 2026-11-08c §7 idea 1, now scheduled). An encoder written
   from `theory/mathematical-model.md` Lemma 5.1 and the S5 definition, not from `pilot.build`; maps 40 (62 s), one
   of each of `(1,2,3)/(2,3)` and `(1,1,2,2)/(2,3)` (tripled pairs), one `(1^4,2)`, one `(1,1,1,3)`, one
   `(2,2,2)/(2,2,2)`; plus the pinned Roest-Vigh, Mizhaev and item 1 controls. At most 2 sessions + 1 core-h, 8 shards (owner rule 2026-11-08).
   * Kill: a disagreement on any instance -> stop, the (9,3) claim is suspended, escalate. Follow-up tree: agreement
     on all -> the claim's encoder caveat reads "two encoders agree on six maps and all controls".
5. **Face-contraction sieve** (explore; new idea N3). Question: is a (9,3) or (10,4) plain formula already UNSAT on
   the clauses whose chirotope variables all contain one face X (the rank-3 contraction at X, a clause subset, so a
   relaxation)? Power first: all 203 (9,3) maps x 9 faces (all known UNSAT), cap 20 s, 10 shards; then, only on pass,
   the 1117 (10,4) maps x 10 faces. At most 1 session + 1 core-h for the (9,3) part.
   * Kill: 0 of 203 (9,3) maps UNSAT at any single face -> park. Follow-up tree: >= 20 of 203 -> the (10,4) sieve
     (<= 3 core-h); every (10,4) sieve UNSAT with a checked proof removes that map from the item 2 queue (EXACT,
     formula scope); 1-19 of 203 -> record, no (10,4) run.

Not in this week: the note package (queue item 8, after items 1, 3, 4 pass and the owner decides); E-261101-10 (S0 slot).
```

## 3. Answers

### 3.1 Strategy verdict (`STRATEGY.md`)

The evidence since 2026-11-03 does not contradict the stance (exact, jump-first, risky ideas killed fast): the exact
route decided the target case in about 23.5 core-h, while the heuristic engines (genus ladder, solid-first, arrangement
sources, embedded-first) produced nothing. It does contradict §1 as written: the focus target is answered, negatively
and conditionally, and §1 line 15 still reasons about what a (9,3) object "if any" would look like.

**Recommendation** (owner's change to §1, not made here):

* Focus: (10,4), gated by the speed-up benchmark (item 2). If the gate fails, there is no focus target the laptop can
  decide; the owner then chooses between a campaign on Actions, a return to S0, or consolidation only.
* Side track at low compute: consolidate the (8,2)/(9,3) negative result (items 1, 3, 4; then proofs and a reader).
* Keep: exploration one run in two; the follow-up rule; S0 parked.

What would change this: item 1 fails (the claim is suspended, (9,3) reopens and is again the focus); any (10,4) SAT
that realizes (focus becomes the write-up and (11,5)); the benchmark kill rule (strategy question to the owner).

### 3.2 The lab's question (E-261103-07 CONCLUSION, "Next step")

Option 1, in the form of item 2. Option 2 (the same 10 maps at larger caps) only measures F for the default solver; F
then projects a cost of thousands of core-h that nobody would spend, so its outcome changes no decision
(`STRATEGY.md` §2). Of the four listed speed-ups, Aut+ symmetry breaking is dropped: 91 % of (10,4) maps have trivial
Aut+, and certified breaking needs VeriPB (I-261108-02). The benchmark calibrates on (9,3) maps first because only there
is the answer known and the baseline time recorded.

### 3.3 "For the lead" (`CONTINUE_PROMPT.md`)

"The whole (9,3) claim rests on one encoder; idea 1 of review 08c is unscheduled." Scheduled as item 4, preceded by the
multiplicity control (item 1), which tests the part of the encoder no control has touched, and joined by the census
check (item 3), the second single point of failure.

### 3.4 Review 2026-11-08c §4 (note / (10,4) / S0)

* Note: yes as a side track, gated by items 1, 3, 4. Then proof regeneration (about 25 core-h, one night) with
  archiving off git (owner rule 2026-11-08) and a human reader; the owner declined external letters on 2026-11-07,
  so whether a note is a goal is the owner's call.
* (10,4): the new focus, behind the benchmark.
* S0: stays parked. 59 formulas at 13 elements; with F >= 3.3 per element the plain route is far above the (10,4) one.

## 4. Scored table (T D F G R under the recommended strategy; J = jump: 2 reaches the target genus directly, 0 a
ladder step, "-" supporting work; kill cost: s = session, h = core-h)

### 4.1 Focus and consolidation candidates

| ID | Candidate | T D F G R | J | Kill cost | Disposition |
|---|---|---|---|---|---|
| new N1 | multiplicity >= 3 positive control | 2 2 2 2 2 | - | 1s + 0h | **Week 1, first** |
| new (I-261031-02, kissat, options) | (10,4) speed-up benchmark | 1 2 2 2 2 | 2 | 1s + 12h | Week 2 |
| new N5 | independent census of (8,2), (9,3) | 2 2 2 1 2 | - | 2s | Week 3 |
| E-261101-09 / I-261031-03 / 08c §7.1 | second encoder on six maps | 2 2 1 2 2 | - | 2s + 1h | Week 4 |
| new N3 | face-contraction sieve | 1 2 2 2 2 | 2 | 1s + 1h | Week 5, explore |
| ROADMAP.md:49 TODO, new N4 | Actions calibration wave on known (9,3) maps | 1 2 2 1 2 | - | 1s + 0 laptop | Conditional on item 2 (160 < P <= 1,000) |
| E-261103-07 option 2 | the 10 probe maps at larger caps | 0 1 2 0 2 | 2 | 1 night | **Below gate** (T + D = 1); follow-up rule |
| I-261108-02, I-261029-43 | Aut+ symmetry breaking (VeriPB) | 1 1 2 0 2 | - | 1s | Backlog: 9 % of (10,4) maps |
| new N2 | certified incremental SAT per pattern (IDRUP) | 1 2 2 2 1 | 2 | 1s + 1h | Backlog; a benchmark variant if CaDiCaL incremental proofs work |
| (10,4) symmetric | uniform formulas of maps with a face-free rotation | 1 1 2 1 2 | 2 | 1s + 2h | Backlog, explore: at (8,2)/(9,3) every uniform symmetric formula was UNSAT (C2, C3); count the maps first |
| E-261101-12 / H-261101-07 | maximal face-neighbourly polyhedra exist (umbrella) | 2 2 2 2 2 | 2 | via item 2 | Umbrella; genus 2, 3 excluded conditionally, 4-5 open |
| note package | proofs regenerated and archived, write-up, reader | 1 2 1 1 2 | - | 1 night + 2s | Queue item 8; after items 1, 3, 4 and the owner's decision |
| E-261101-11, I-261101-06 | external human review | 2 2 1 2 2 | - | owner | Owner's decision; the note needs a reader |
| E-261101-06 / I-261030-29 | rank-3 relaxation (contraction at infinity) | 2 1 1 2 2 | - | 1s + 0.5h | Backlog; N3 is its per-face version and goes first |
| E-261108-02 follow-up | cores on 7-8 faces | 1 0 1 1 2 | 0 | 1s | Parked (unchanged) |
| I-261103-04, E-261107-01, E-261108-01 | arrangement-first / solid-first at (9,3) | 1 0 2 1 2 | 2 | - | Consumed: the target case is decided |
| E-261103-04/-05/-06, I-261103-01/-03/-05/-06 | ladder, solid-first, embedded-first, C3 ansatzes at (9,3) | 1 0 1 1 1 | - | - | Consumed with the target case; at (10,4) only with a benchmark-ladder pass (`STRATEGY.md` §2) |
| I-261029-57, -45, I-261030-32 | realizability branch | 2 2 2 2 2 | 2 | 1h on a model | Conditional on the first SAT model |

### 4.2 Unchanged (no evidence since 2026-11-08 bears on them)

Every other focus idea keeps its score and disposition from `reviews/strategy-review-2026-11-08.md` §5.2. The parked
S0 / twelve-face S1 rows (E-261101-03, -04, -05, -08, -10, -14 to -20, -24, the S0 hypotheses, the S0-only ideas) are
listed there and stay parked; the low-cost S0 slot E-261101-10 (one session per two weeks) stays, outside this week.

## 5. Proposed queue (in order)

| # | Item | Hypothesis | Cheapest falsifying test | Outcomes change | Budget | Stop rule |
|---|---|---|---|---|---|---|
| 1 | N1 multiplicity control | the encoder accepts real m = 3, 4 segment pairings | pinned own-map SAT on a grooved box | fail: 19 S5 UNSATs suspended, (10,4) blocked | 1s | the control decided |
| 2 | (10,4) speed-up benchmark | some variant is >= 10x cheaper on (10,4) | Phase A on six known (9,3) maps | which compute route (laptop, Actions, none) | 1s + <= 12h | Phase A kill, or Phase B done |
| 3 | independent census | 2 / 240 / 203 classes are complete | count (8,2) first (minutes) | coverage two-algorithm; a missing map reopens (9,3) | 2s | agreement or a listed difference |
| 4 | second encoder | the two encoders agree | map 40 in both | the encoder caveat; a disagreement suspends the claim | 2s + 1h | six maps + controls |
| 5 | face-contraction sieve (**explore**) | some formulas are UNSAT at one face | 203 (9,3) maps x 9 faces at 20 s | a cheap pre-filter for 1117 (10,4) maps | 1s + 1h | power test result |
| 6 | Actions calibration wave | Actions decides known (9,3) maps at a stated core-h rate | 20 jobs on map 7-class maps | whether a (10,4) campaign is possible | 1s, 0 laptop h | 20 jobs complete or fail |
| 7 | (10,4) completion or campaign | - | - | the (10,4) answer | per item 2's tree | per its PLAN |
| 8 | note package | - | - | a citable (8,2)/(9,3) result | 1 night + 2s | owner's decision |

**Single first item: N1, the multiplicity >= 3 positive control.**

## 6. New ideas (untested proposals, not evidence)

1. **N1. Grooved-box control for multiple segments.** A box with k V-grooves cut across one edge gives two faces
   (top and front) that share k + 1 collinear segments; it is genus 0, cubic after tilting the groove walls, and has
   12 faces for k = 2. Why: the multi-segment pairing clauses for m >= 3 have no positive control, and 128 S5 formulas
   of ours depend on them. Cheapest test: k = 2, pinned own-map formula, minutes.
2. **N2. Certified incremental SAT across a pattern.** All (10,4) formulas share the rank-4 OM part on 11 elements;
   one CaDiCaL session per pattern with selector literals per map keeps the learned OM lemmas, and incremental proof
   formats with a checker (IDRUP / LIDRUP from the SAT-competition incremental track; CLAIMED, not checked here) keep the
   result certifiable. Cheapest test: six `(1^4,2)` (9,3) maps in one session against separate solving; >= 2x makes it a
   benchmark variant. Overlaps E-261101-20 (S0 form).
3. **N3. Face-contraction sieve.** In oriented-matroid terms the clauses on chi(X, ., ., .) describe the rank-3
   contraction at face X: the line arrangement in the plane of X with X's polygon on it. Each is a clause subset of the
   plain formula, so an UNSAT is an exact exclusion of the whole map, and each sub-formula is small. The core study
   E-261108-02 grouped clauses by constraint faces, not by contraction, so it does not answer this. Cheapest test: the
   203 known-UNSAT (9,3) maps at 20 s.
4. **N4. Actions as the (10,4) compute.** Public repository: standard runners are free (CLAIMED), 20 parallel jobs of up
   to 6 h on the free plan (CLAIMED). Calibrate on known (9,3) maps (map 7, 1239 s on the laptop) to get a laptop/runner
   speed ratio and test proof checking inside the job's disk limit. Needs the lab branch pushed or a workflow on `main`;
   the owner decides.
5. **N5. Independent census.** Enumerate the (9,3) candidate maps as genus-3 rotation systems of K_9 plus three extra
   edges with CP-SAT and canonical-form deduplication (or Lutz-style lexicographic surface enumeration), share no code
   with E-261103-01, and compare classes and hashes. Why: FD3 had two enumerators for the 59 types; the S5 census has one
   for the full list (`experiments/E-261103-01-s5-map-census/CONCLUSION.md:27-29`: the independent algorithm covered
   only the free-C3 sub-list).

## 7. Audit

| ID | Where | Finding | Fix |
|---|---|---|---|
| A1 | `experiments/E-261103-03-s5-exact-decision-8-2-9-3/CONCLUSION.md:521`; `STATUS.md:207` | The run controls are genus-0 convex polyhedra with pinned planes and no multiple pairs; the genus-3 controls (Roest-Vigh, Mizhaev) have only doubled pairs. No control has a pair with m >= 3, while 18 (9,3) maps, one (8,2) map and 109 (10,4) maps have one (EXACT counts; `SPEC.md` change log 2026-11-08) | week item 1; until it passes, the caveat of the (9,3) claim should name "m >= 3 pairings untested by a positive control" |
| A2 | `experiments/E-261103-01-s5-map-census/CONCLUSION.md:27-38` | Full census coverage rests on one enumerator plus PROVED-1 arguments; the independent algorithm covered the free-C3 sub-list only | week item 3 |
| A3 | `ROADMAP.md:231` | S5 credence (9,3) 0 / 1 / 0: a weight of exactly 1 on a PROVED-1, single-encoder, single-enumerator result | 0.05 / 0.95 / 0 until items 1, 3, 4 pass (§8) |
| A4 | `STRATEGY.md:12-17` | §1 still describes the open (9,3) case ("a (9,3) object, if any, is asymmetric or has a symmetry of order 2") | owner's §1 change (§3.1) |
| A5 | `experiments/E-261103-07-s5-10-4-census-symmetry/README.md:60`; `PLAN.md` predictions | The cost model ("about 73 core-h") and prediction (1) (>= 5/6 fast maps at 300 s, "about 60 %") ignored the per-element growth already visible from (8,2) to (9,3) (plain 5.3 and 12.4 s vs pattern medians 27-497 s, NUMERICAL); the prediction failed 0/6 | use the (8,2) -> (9,3) ratio as the prior for F in item 2's PLAN; calibrate predictions on existing data before stating a percentage |
| A6 | E-261103-07 CONCLUSION, "Next step" | Option 2 (larger caps on the same maps) is a cap-only follow-up | not queued (`STRATEGY.md` §2) |
| A7 | working tree at the cut | The E-261103-07 conclusion, STATUS 3w, ROADMAP, log and `results/probe/` are uncommitted; `results/launch.pids` is untracked in E-261103-03 and E-261103-07 | lab commits the conclusion and evidence; `launch.pids` and `*.lock` into `.gitignore` or deleted, never committed |
| A8 | `experiments/E-261103-07-s5-10-4-census-symmetry/README.md:3` | Title "Census and symmetric sub-list" no longer describes the experiment (census by E-261103-01, then a cost probe) | wording fix at the next ledger edit |
| A9 | `ROADMAP.md:49`; `gh run list --workflow experiment.yml` | The Actions runner, listed as a TODO since 2026-11-01, has never run an experiment (last five runs skipped); the only compute lever that could carry a (10,4) campaign is unbuilt | queue item 6, conditional on item 2 |
| A10 | process | Four lead reviews dated 2026-11-08 (`-08`, `-08b`, `-08c`, this one). Each followed a decision point, but the pace of reviews now matches the pace of nights | next lead review after week items 1-4 or after item 2's verdict, whichever is first |

Claims checked against evidence: the (9,3) claim in STATUS 3d and the E-261103-03 CONCLUSION is scoped correctly (EXACT
for formulas; PROVED-1, conditional, for the geometry; not CERTIFIED, no archived proofs, no second implementation). The
E-261103-07 conclusion correctly reports only lower bounds for F and makes no existence claim. Documentation versus
compute: E-261103-03 spent about 23.5 core-h over a long amendment chain (pilot, grid, tranche, items 1a, 1b, 5a), but
the chain ended in a gate decision, so it does not need stopping. Follow-up chains to stop: E-261108-01 Phase B and the
E-261108-02 7-8-face cores stay unqueued; every (9,3) heuristic engine is consumed by the decision.

## 8. Scenario credences (subjective planning weights, not evidence)

| Case | exists / does not / cannot tell | Change | One line of evidence |
|---|---|---|---|
| (8, 2) | 0.03 / 0.97 / 0 | -1 -> 0.97 on "does not" | 2/2 plain UNSAT-VERIFIED; one map has a tripled pair with no positive control (A1) |
| (9, 3) | 0.05 / 0.95 / 0 | -0.05 on "does not" | 203/203 UNSAT-VERIFIED (EXACT); residual weight for an encoder or census error (A1, A2) |
| (10, 4) | **0.15 / 0.40 / 0.45** | -0.15 / +0.10 / +0.05 | both smaller minimal-genus S5 cases are empty at the OM level (inductive, weak); F > 3.3 measured, 10-40 estimated, so the exact route may be out of reach |
| S0 A / B / C | 0.20 / 0.55 / 0.25 | unchanged | S0 has no extra adjacencies, like (7,1), which exists; the (8,2)/(9,3) analogy cuts both ways |

The (10,4) move is 0.15, so `experiment-conclude` or the owner applies it only with this review's approval. Reversal:
item 1 fails -> (9,3) back to about 0.30 / 0.40 / 0.30 until the encoder is fixed and re-run; a (10,4) SAT that
realizes -> "exists" 1.

## 9. Three things to do first

1. **Owner:** decide `STRATEGY.md` §1: (10,4) as the gated focus, the (8,2)/(9,3) consolidation as the side track,
   and whether a note with a human reader is a goal.
2. **Lab session:** week item 1, the grooved-box multiplicity control.
3. **Lab session:** pre-register week item 2 (`PLAN.md` with kissat pinned, the cube format and the projection
   formula), then one owner launch of at most 2 h.
