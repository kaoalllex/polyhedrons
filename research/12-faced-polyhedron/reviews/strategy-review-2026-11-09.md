# Strategy review, 2026-11-09: weekly lead review of the week plan of review 2026-11-08d/e

Lead review of the five week items of `reviews/strategy-review-2026-11-08d.md` as amended by `-08e` (all done) under
`STRATEGY.md` of 2026-11-08. Evidence cut: `427639f` on `lab/2026-11-08`, clean tree. This report advises and changes no
ledger file. Labels are `SPEC.md` §5; **Recommendation** and **Untested** mark judgments and proposals, not evidence.
Checks run this session (seconds each): `E-261103-07/pattern_census.py` (the (10,4) pattern counts below, EXACT);
per-pattern (9,3) default-CaDiCaL solve times recomputed from `E-261103-03/results/**/results.jsonl` (198 maps,
NUMERICAL); `gh run list --workflow experiment.yml`. `verify_all.py --quick` was not run: no code changed and no
decision here depends on it.

## 1. Verdict in ten lines

1. **The strategy holds; its gate has an answer.** E-261108-03 lands in the middle branch: kissat decides four (10,4)
   maps in 188-2749 s (UNSAT-SOLVER), P(4) = 475 core-h without DRAT (NUMERICAL, a scenario, not a bound). Neither the
   two-night branch (<= 160) nor "no route" (> 1,000). The (10,4) exact route is affordable as a multi-night sweep.
2. **The week's audits passed** (m = 3, 4 control; second census; second encoder on six maps), so the (8,2)/(9,3) result
   now has two enumerators and a partial second encoder. Still PROVED-1, conditional, cubic, no human review.
3. **The union of matched solids is parked** (0 of 256 samples; 99 % of A draws rejected for pole crossing). Answer to
   "For the lead": no later stage of I-261108-11 this week; only its S0 combinatorial filter stays, in the S0 list.
4. **The (10,4) cost is concentrated** (scenario from this session's per-pattern rescaling, **Untested**): stratum
   `(1^4,2)` about 190 core-h, `1^6` about 180, all other 360 maps together about 51 core-h.
5. **First item: a first-witness sweep of those 360 maps in one laptop night** (kissat, no DRAT, fastest patterns first,
   first-SAT stop, <= 80 core-h). It is the only witness search that fits one night, and its times replace the n = 1-2
   projection for the remaining 757 maps.
6. **Actions calibration runs in parallel** (no laptop cost). The trigger on `experiment/<ID>` branches conflicts with
   the one-branch-per-week rule. Its terms of use (CLAIMED, not checked here) need the owner's reading before a campaign.
7. **Negative claims at (10,4) are blocked by proof checking**, not by solving: checked DRAT beyond 1-1.5 h of
   solving does not fit 48 GB (E-261108-03 amendment 2). New idea N1 tests an LRAT route inside the Actions wave.
8. **Side track:** the note's one-way soundness chain (review 08e Q3) is now the gate of the note. It is session work
   with no compute, done while the night runs.
9. **Credences:** (10,4) 0.15 / 0.40 / 0.45 -> **0.15 / 0.50 / 0.35**: the route is priced, existence evidence unchanged.
   (9,3) -> 0.03 / 0.97; (8,2) -> 0.02 / 0.98, because the audits passed. S0 unchanged.
10. **Process:** the week was cheap and on plan (about 9 core-h, five items, one review). Fix four items: core-hour
    accounting, an experiment run without a PLAN (E-261109-02), a stale STATUS header, and one caveat called "lifted"
    on the strength of one configuration.

## 2. Week plan (ready to paste into `ROADMAP.md`, replacing the week plan block)

```
## Week plan (lead review 2026-11-09, `reviews/strategy-review-2026-11-09.md`; replaced by the next lead review)

Lab sessions take these in order (PROTOCOL.md §8b). Anything outside a follow-up tree goes to "For the lead".
Laptop: at most 10 cores in total; every splittable run uses 8-10 shards (owner, 2026-11-08). Item 1 is one owner
night; item 2 uses GitHub Actions only and may run during that night; items 3 and 5 need no compute; item 4 is a day run.
Aggregate core-hour caps override per-unit caps. Search runs skip DRAT (owner, 2026-11-08): their UNSATs are
UNSAT-SOLVER, which may skip or rank a map but are never a negative result.

1. **(10,4) first-witness sweep, stratum C** (exploit, jump; follow-up of E-261108-03, new experiment). Question: does any
   of the 360 admissible (10,4) maps outside the patterns `(1^4,2)` and `1^6` have a SAT plain S5 formula, and what does
   each pattern cost? Queue (frozen in the PLAN with the `maps_10_4.json` SHA-256), in this order: `(1,2,3)/(2,3)` 38,
   `(1,1,1,3)` 58, `(1,1,2,2)/(2,3)` 70, `(1,1,2,2)/(2,2,2)` 186, `(2,2,2)/(2,2,2)` 7, `(3,3)/(4)` 1; maps 146 and 845
   reuse their E-261108-03 records. Solver: kissat rel-4.0.4 (binary hash of E-261108-03), E-261103-02 encoder,
   `submap=False`, no DRAT, solver cap 3600 s per unit; positive and negative pinned controls in every shard.
   * Budget: 1 prep session (PLAN, queue, smoke test); one owner night, 10 shards, <= 80 core-h, <= 10 h wall.
     Scenario 51 core-h (this review §3.2, untested).
   * Kill: a control fails -> stop that shard and escalate. Aggregate cap reached with < 300 units decided -> stop,
     record, escalate (the per-map cost model is wrong by > 1.5x).
   * Follow-up tree (nothing starts without the owner):
     * any SAT -> first-SAT stop of all shards; exact model check against the clauses; the realization stage with the
       E-261103-04 saved-OM tools (I-261029-57); realized -> `verify_candidate.py --target S5`, `candidate-check`; not
       realized in one session -> final polynomials (I-261029-45) and escalate. An OM model alone is not a result;
     * all decided, 0 SAT -> per-pattern table (n, median, max, censored); price strata A and B with the measured
       C ratios; laptop price <= 4 nights -> propose stratum A as the next nights (fastest maps first, same design);
       otherwise Actions after item 2, if the owner accepts its terms;
     * > 10 % of units censored at 3600 s -> no A/B proposal; escalate (route LOW-YIELD at this cap for those
       patterns, not refuted).
2. **Actions calibration wave** ([I-261108-07](ideas/I-261108-07-actions-calibration-wave.md), infrastructure; plus new idea N1 of the review). Question: how fast are
   free runners on our formulas, and does proof checking fit them? Trigger `workflow_dispatch` with `--ref` the lab
   branch (no `experiment/<ID>` branch, `PROTOCOL.md` §7); the job builds kissat rel-4.0.4 and records its hash.
   At most 10 jobs, 4 processes each: (10,4) maps 96, 85, 146, 845 with kissat, no DRAT (known laptop times); (9,3) maps
   7, 87, 130, 165, 29, 184 with kissat DRAT checked by drat-trim inside the job; one job with CaDiCaL `--lrat` and an
   LRAT checker on map 7 (N1). Record per unit: runner/laptop time ratio r, peak RSS, proof size and checker time.
   * Budget: 1 prep session, 0 laptop core-h, jobs <= 3 h each. The owner reads GitHub's Actions terms before launch.
   * Kill: the build or the workflow fails twice -> Actions parked for this research; laptop-only route.
   * Follow-up tree: answers disagree with the records -> stop, escalate (environment bug); r <= 2 and no OOM ->
     strata A/B become an Actions campaign proposal (PLAN after item 1, owner approves); r > 2 or OOM -> laptop-only
     route; the LRAT job checks map 7 within 8 GB -> LRAT becomes the proof route for any (10,4) negative claim and
     for the note's proof regeneration; it fails -> record, keep drat-trim for (9,3).
3. **Note: the one-way soundness chain** (side track; review 08e Follow-up Q3; theory, no compute). Write
   `theory/s5-soundness-chain.md`: (a) S5 uniformization with multiple segments (cubic scope); (b) geometry to an
   admissible exported map (dart representative, lossless paired links); (c) necessity of INCONS, RFCONS, REFLEX1 and
   POC for multiple boundary runs, with an extension of every Tseitin variable; (d) the gauge units `SB_REORIENT` /
   `SB_MIRROR` for F = 8, 9; (e) the census-to-CNF manifest of the 205 formulas (options, hashes). At most 2 sessions.
   * Kill: a link that cannot be written in 2 sessions -> name it, narrow the note's statement, escalate (re-solving
     (9,3) without that clause family is about 13 core-h, an owner decision).
   * Follow-up tree: all links written -> one `adversarial-verifier` pass (a filter, not an independent review; ask the
     owner first) -> the lead proposes the proof-regeneration night and the note draft.
4. **Cube-and-conquer pilot** (explore; [I-261031-02](ideas/I-261031-02-cube-and-conquer-rank3-split.md), the open V2 of E-261108-03). Question: does
   splitting cut the summed core-seconds on the slow strata? Cubes from march_cu, or from the segment-order variables of
   the doubled pairs; each cube by kissat, no DRAT; maps 96 (1073 s) and 85 (2749 s), 8-10 shards. If march_cu cannot be
   built in the prep session, use the segment-order cubes; no other substitution.
   * Budget: 1 prep session + <= 3 core-h, day run.
   * Kill: summed cube time >= 0.7x of monolithic kissat on both maps -> park cube-and-conquer at this budget.
   * Follow-up tree: <= 0.5x on both -> the A/B proposal of item 1 uses cubes; in between -> record, no change.
5. **Defect-bounded boundary census pilot** (explore, optional; [I-261108-10](ideas/I-261108-10-defect-bounded-boundary-census.md), review 08e §5). Only if items 1-4
   leave a session. Question: are the non-cubic (8,2) maps a small finite list reachable by <= 2 contractions of cubic
   precursors? Start with the two (8,2) precursors and the square-pyramid round-trip control. 1 session, <= 1 core-h,
   8 shards, stop at 1000 maps.
   * Kill: a failed round trip, or the cap -> the note stays "cubic" (no loss). Follow-up tree: a bounded list -> a
     separately registered concurrence pilot on one map, after the lead.

Not in this week: strata A (520) and B (237) of the sweep (item 1 or 2 proposes them); proof regeneration and the
note draft (after item 3); the empirical hardness model (N2) and the kissat configuration screen (N3); every
I-261108-11 stage. The low-cost S0 slot (E-261101-10) stays outside the week.
```

## 3. Answers

### 3.1 Strategy verdict (`STRATEGY.md`)

The evidence of this week supports §1 and §2 as written. The gate was built to choose between two laptop nights, an
Actions campaign, and none; the answer is "an Actions campaign or about five laptop nights", and stratum C fits one
night. The stance (exact first, jump first, risky ideas killed fast) also held: the one explore item (union) was killed
in one session at 0.03 core-h with its failure mode written down.

**Recommendation** (owner's change to §1, not made here): replace the "Gate" bullet by its outcome. Kissat is the
solver for search runs. The route is a stratified first-witness sweep without DRAT, fastest patterns first; stratum C
on the laptop now, strata A/B on the laptop or on Actions after calibration. A negative (10,4) claim additionally needs
a proof route that fits memory (item 2, N1). Stance, exploration share and S0 parking unchanged.

What would change it: a SAT model in item 1 (the focus becomes realization and verification; the rest of the sweep
stops); stratum C costs > 1.5x its scenario or > 10 % censored (the laptop route is LOW-YIELD at this cap; Actions only,
or consolidation); Actions fails or its terms exclude this use and the owner declines five laptop nights (then
consolidation, the note, and the owner's choice between S0 and a structural slot, per `STRATEGY.md` §1).

### 3.2 Where the (10,4) cost sits (scenario, **Untested**)

Pattern counts (EXACT, `pattern_census.py`): `(1^4,2)` 520, `1^6` 237, `(1,1,2,2)/(2,2,2)` 186, `(1,1,2,2)/(2,3)` 70,
`(1,1,1,3)` 58, `(1,2,3)/(2,3)` 38, `(2,2,2)/(2,2,2)` 7, `(3,3)/(4)` 1. The E-261108-03 stratum C sample (146, 845) has
the two fastest patterns only, 45 of its 360 maps. (9,3) default-CaDiCaL means by pattern (NUMERICAL, 198 recorded
UNSAT-VERIFIED maps): 242, 498, 103, 96, 80, 37, 30 s. Kissat at (10,4) divided by the (9,3) pattern mean is 4.4, 5.5, 5.1
on maps 96, 85, 845. Map 146 is the outlier at 23x, but (2,2,2)/(2,2,2) has a single (9,3) map. With factor 5.5:

| Stratum | maps | scenario core-h | laptop nights (about 80 core-h each) |
|---|---:|---:|---:|
| A `(1^4,2)` | 520 | 192 | 2.4 |
| B `1^6` | 237 | 180 | 2.3 |
| C (six patterns) | 360 | 51 (29 of them `(1,1,2,2)/(2,2,2)`) | 0.6 |
| all | 1117 | 424 (P(4) = 475 includes x1.25) | 5.3 |

This is a planning number that assumes the (9,3) pattern ranking carries over. Item 1 tests it on 360 maps.

### 3.3 "For the lead" (`CONTINUE_PROMPT.md`): next stages of I-261108-11

Park every stage aimed at (10,4) or (9,4): general genus-0 pieces, the (9,4) sources and the rigid (9,3) cross-check.
Reasons. The item's own tree forbids harder pieces after a failure. Stage 1 gave 0 of 256, with the best clean A sample
at genus 2 and 35/45 pairs. The valid A samples are the pole-free 0.9 % of the registered box, so the three-ball
mechanism is rare where it was sampled. A (10,4) witness search now has a priced exact route, so a heuristic source must
beat about 50 core-h per 360 maps to earn a slot; this one has no rate to compare. The union code is kept as a tool. The
seconds-scale S0 filter (does a K12 type split as two 7-vertex torus pieces joined by five tubes?) goes to the parked S0
list; it runs only when S0 resumes.

### 3.4 E-261108-03 "the lead decides": Actions calibration or cube-and-conquer

Both, as items 2 and 4, behind item 1. Calibration costs no laptop time, and the A/B decision needs it. Cube-and-conquer
is the one mechanism-level speed-up left from item 2 of the last week. A 2x gain on A/B saves about two laptop nights,
which is worth one session and 3 core-h.

## 4. Scored table (T D F G R; J = jump: 2 reaches genus 4 directly, 0 a ladder step, "-" supporting work; kill
cost: s = session, h = core-h)

### 4.1 Focus and side-track candidates

| ID | Candidate | T D F G R | J | Kill cost | Disposition |
|---|---|---|---|---|---|
| new (E-261108-03 follow-up) | (10,4) first-witness sweep, stratum C | 2 2 2 1 2 | 2 | 1s + 1 night (<= 80h) | **Week 1, first** |
| I-261108-07 + N1 | Actions calibration with LRAT probe | 1 2 2 1 2 | - | 1s, 0 laptop h | Week 2 |
| 08e Q3 | note soundness chain | 2 2 1 2 2 | - | 2s | Week 3 |
| I-261031-02 | cube-and-conquer on 96, 85 | 1 2 2 2 2 | 2 | 1s + 3h | Week 4, explore |
| I-261108-10 | defect-bounded boundary census | 2 1 2 2 2 | - | 1s + 1h | Week 5, explore, optional (D 2 -> 1: the note can stay cubic) |
| new | strata A, B sweep (757 maps) | 2 2 2 1 2 | 2 | ~370h scenario | Conditional on items 1, 2 |
| N2 (new) | empirical hardness model for queue order and pricing | 1 2 2 1 2 | - | 1s, 0h | Queue after item 1 |
| N3 (new) | kissat configuration screen | 1 1 2 1 2 | 2 | 1s + 3h | Backlog: only if item 4 fails and A/B exceed 4 nights |
| new | `enc2` on a (10,4) sample (96, 85, 146, 845) | 2 1 2 1 2 | - | 1s + 1h | Only before any (10,4) negative claim |
| note package | proof regeneration, draft, reader | 1 2 1 1 2 | - | 1 night + 2s | After item 3; owner |
| I-261108-09 | universal local perturbation lemma | 2 1 1 2 1 | - | 1s | Optional after item 3 |
| I-261108-05 | incremental SAT per pattern | 1 1 2 2 1 | 2 | 1s + 1h | Backlog (D 2 -> 1: kissat has no incremental interface; CaDiCaL is 2-3x slower here) |
| I-261108-06 | face-contraction sieve | 1 1 2 2 2 | 2 | 1s + <= 10h | **Below gate** (D 2 -> 1): a full kissat solve (~0.15-0.8 h per map) now costs about what the sieve's power test risks; reopen if proof memory blocks (10,4) negatives (short sub-proofs) |
| I-261108-11 stages 2+ | union: genus-0 pieces, (9,4), rigid (9,3) | 1 1 2 1 2 | 2 | 1s + 1h | **Below gate** (§3.3) |
| I-261108-01 | concentrated-multiplicity lemma | 2 1 2 2 2 | - | 1s | Backlog; E-261108-02 found no core on <= 6 faces |
| I-261108-02, I-261029-43 | Aut+ symmetry breaking (VeriPB) | 1 1 2 0 2 | - | 1s | Backlog (9 % of (10,4) maps) |
| I-261103-02 | census-free OM / tope search | 1 1 1 2 1 | 2 | >= 2s | Backlog |
| (10,4) symmetric | uniform formulas, face-free rotations | 1 1 2 1 2 | 2 | 1s + 2h | Backlog (unchanged) |
| I-261029-57, -45, I-261030-32 | realizability branch | 2 2 2 2 2 | 2 | 1h on a model | Conditional on the first SAT (item 1 tree) |
| H-261101-07, E-261101-12 | maximal face-neighbourly polyhedra exist (umbrella) | 2 2 2 2 2 | 2 | via item 1 | Umbrella |
| E-261101-11, I-261101-06 | external human review | 2 2 1 2 2 | - | owner | Declined by the owner (2026-11-07); the note says so |
| E-261103-07 option 2 | probe maps at larger caps | 0 1 2 0 2 | 2 | - | Below gate (unchanged) |

### 4.2 Unchanged

Every other focus idea keeps its score and disposition from `reviews/strategy-review-2026-11-08d.md` §4 and
`reviews/strategy-review-2026-11-08.md` §5.2 (no evidence since bears on them). Parked S0 and twelve-face S1 rows
(E-261101-03 to -24 as listed there, the S0 hypotheses, the S0-only ideas) stay parked and listed. Added to that list:
the I-261108-11 S0 filter (`1 1 2 1 2`, seconds). The low-cost S0 slot E-261101-10 stays.

## 5. Proposed queue (in order)

| # | Item | Hypothesis | Cheapest falsifying test | Outcomes change | Budget | Stop rule | Explore |
|---|---|---|---|---|---|---|---|
| **1** | stratum C sweep | some C map is SAT; C costs ~51 core-h | the night itself, fastest patterns first | SAT: realization, focus result; 0 SAT: price A/B, the night plan | 1s + <= 80h | first SAT, cap, control failure | no |
| 2 | Actions calibration + LRAT | runners are <= 2x slower and proofs fit | 10 jobs on known maps | Actions or laptop for A/B; the proof route for negatives | 1s, 0 laptop | two failed builds | no |
| 3 | soundness chain | every link of geometry -> CNF can be written | link (c), the optional clause families | the note's statement | 2s | 2 sessions | no |
| 4 | cube-and-conquer | cubes cut summed time by >= 2x on slow maps | maps 96, 85 | A/B cost by about 2 nights | 1s + 3h | >= 0.7x on both | **yes** |
| 5 | defect census pilot | non-cubic (8,2) maps are few | (8,2) precursors + round-trip control | the note's scope beyond cubic | 1s + 1h | cap or failed round trip | **yes** |
| 6 | strata A, B sweep | no SAT, or the first SAT | the first A night | the (10,4) witness search complete (UNSAT-SOLVER) | ~370h | first SAT, per its PLAN | no |
| 7 | N2 hardness model | 30-s probe features rank solve times (Spearman >= 0.7) | (9,3) times and item 1 times, no new solving | queue order and pricing of item 6 | 1s | rho < 0.5 -> drop | no |
| 8 | note package | - | - | a citable (8,2)/(9,3) result | 1 night + 2s | owner | no |

**Single first item: week item 1, the stratum C first-witness sweep** (prep session today, owner night tonight).

## 6. New ideas (untested proposals, not evidence)

1. **N1. LRAT as the proof route for long solves.** CaDiCaL 2.x writes LRAT natively (`--lrat`), and LRAT checking is
   forward and needs only the clauses in use. Tools: `lrat-trim`, `cake_lpr`, a verified checker (CLAIMED, SAT-tooling
   literature, not checked here). Why: the 48 GB wall of drat-trim on solves beyond 1-1.5 h (E-261108-03 amendment 2)
   blocks every negative (10,4) claim and makes the note's proof regeneration heavy. Cheapest test: map 7 (1240 s with
   CaDiCaL), proof size and checker RSS against drat-trim, one Actions job (item 2).
2. **N2. Empirical hardness model for the queue.** From algorithm selection (SATzilla-style runtime prediction): fit the
   log solve time on cheap features: pattern, face sizes, |Aut+|, CNF size, and a 30-s kissat probe (conflicts per
   second, learnt-clause growth). Use it to order strata A and B by expected time; for a first-witness search that
   order maximises maps per hour. Price the campaign by quantiles, not by n = 1-2 means. Cheapest test: the 198 (9,3)
   times plus item 1's 360 times, leave-one-pattern-out rank correlation; no new solving if the probe is skipped.
3. **N3. Kissat configuration screen.** Automated configuration often gains 1.5-3x on a homogeneous instance family
   (CLAIMED, SMAC/irace literature). Our 1117 formulas share one encoder and differ only in the map. Cheapest test:
   8 option sets (e.g. `--sat`/`--unsat` profiles, `--chrono`, `--tier1`, `--walkinitially`) on the slow known maps 7, 87,
   130, <= 3 core-h. Only if item 4 fails and A/B exceed 4 laptop nights.

No fourth or fifth idea: the brainstorm of 2026-11-08 already holds 25 divergent proposals with five tests. None of
them beats the priced exact route this week, and filling the quota would dilute it.

## 7. Audit

| ID | Where | Finding | Fix |
|---|---|---|---|
| A1 | `experiments/E-261109-02-independent-census/README.md:1-2` | Run without a committed `PLAN.md` ("not pre-registered") and concluded without a `CONCLUSION.md`. The `CLAUDE.md` hard rule requires a committed PLAN. Harm is low: the pass criterion (set equality) was fixed by the ROADMAP row | add a short `CONCLUSION.md`; a ROADMAP row counts as a PLAN only if the owner says so |
| A2 | E-261109-03 CONCLUSION "Runs"; E-261108-03 CONCLUSION "Runs" | Manifests print 2.49 core-h for a 0.18 core-h run (`workers: 14` times wall) or no core-hours at all; `STATUS.md` §7 calls the ledger exact | the runner records processes x wall (or CPU time) per shard; one-line fix in the manifest writer |
| A3 | `STATUS.md` §3y; `CONTINUE_PROMPT.md` handover; E-261109-01 CONCLUSION | "Lifts the item 1 caveat" rests on one configuration: a single multiple pair in a genus-0 box. The (9,3) maps with a tripled pair also have a doubled pair, and E-261109-01 itself lists that as not covered | wording: "addressed by one positive configuration (EXACT, instance scope); several multiple pairs in one map untested" |
| A4 | E-261108-03 PLAN strata; this review §3.2 | Stratum C was sampled by its two fastest patterns (45 of 360 maps); P(4) = 475 pools the rest by assumption. The conclusion reports it as a scenario, correctly | item 1 measures C; future strata come from `pattern_census.py`, not by hand |
| A5 | `.github/workflows/experiment.yml` (push trigger on `experiment/<ID>`); `PROTOCOL.md` §6 vs §7 | The documented trigger needs a branch per experiment, which the weekly-branch rule forbids. The workflow builds no SAT solver. It has never run an experiment (last runs skipped) | item 2 uses `workflow_dispatch --ref lab/...` and adds a pinned kissat build; `PROTOCOL.md` §6 wording follows |
| A6 | `PROTOCOL.md` §6 "free standard runners" | GitHub's Actions terms restrict use to activity related to the repository's software project (CLAIMED, from memory; not checked this session). A campaign of hundreds of core-h is a gray area | the owner reads the current terms before item 2's follow-up campaign |
| A7 | E-261109-04 CONCLUSION "Samples" | 18,571 of 18,733 A draws were rejected (pole crossing), so "parked at this resolution" refers to a 0.9 % sub-box of the registered box | already scoped in "What may NOT be claimed"; STATUS 3ab could name the sub-box |
| A8 | `STATUS.md:3-12` | The "As of" line is a six-line chronology; the "No active process" paragraph still says "next: week item 1" of the previous week | rewrite both in two lines at the next ledger edit |
| A9 | `ROADMAP.md:8`, `:278` | "As of 2026-11-07" is stale; the (10,4) evidence line still says "exact route may be out of reach", which E-261108-03 superseded | apply with this review's credences |
| A10 | E-261108-03 CONCLUSION (77 lines) | Three times the 25-line CONCLUSION budget (`PROTOCOL.md` §8b); the content is good but repeats the PLAN's projection rules | keep tables, cut restated rules next time |

Claims against evidence: E-261108-03 is scoped correctly (UNSAT-SOLVER, scenario, not a bound); E-261109-02/-03 say
PROVED-1 for their arguments and AI authorship; E-261109-04 is a sampled negative. Underpowered verdict: the kissat
"winner" passes the 2x sum-B rule at 2.04x with n = 1 per slow stratum (stated in its conclusion); item 1 retests it at
scale. Follow-up chains to stop: I-261108-11 (all stages, §3.3); I-261108-06 (below gate now); E-261103-07 option 2
(stays dropped). Documentation versus compute: 24 commits, +1,449 lines of Markdown and +1,614 of code for about 9 core-h.
Every item was an audit or a one-session pilot needing little compute, so the ratio is acceptable. No amendment
chain ran without a gate decision.

## 8. Scenario credences (subjective planning weights, not evidence)

| Case | exists / does not / cannot tell | Change | One line of evidence |
|---|---|---|---|
| (8, 2) | 0.02 / 0.98 / 0 | -0.01 | m = 3, 4 control passed (E-261109-01); census reproduced (E-261109-02) |
| (9, 3) | 0.03 / 0.97 / 0 | -0.02 | the same plus two encoders agree on six maps (E-261109-03); still PROVED-1, no human review |
| (10, 4) | **0.15 / 0.50 / 0.35** | 0 / +0.10 / -0.10 | E-261108-03: four maps decided in <= 2749 s, sweep priced at about 424-475 core-h (scenario); four UNSAT-SOLVER maps are not existence evidence; the proof route for negatives is still open (N1) |
| S0 A / B / C | 0.20 / 0.55 / 0.25 | unchanged | no S0 evidence |

The (10,4) move is 0.10, so the owner approves it. Reversal: stratum C > 1.5x its scenario, or Actions unusable and no
laptop nights -> "cannot tell" back to 0.45. Any realized SAT -> "exists" 1.

## 9. Three things to do first

1. **Owner:** approve week item 1 (one night, <= 80 core-h, <= 10 h) and the credence move; read GitHub's Actions
   terms before item 2; merge `lab/2026-11-08` into `main` by PR with `verify` green and open `lab/2026-11-09`.
2. **Lab session:** week item 1 prep (PLAN, frozen queue, smoke test), so the owner can launch tonight.
3. **Lab session, during the night:** week item 2 prep (dispatch on the lab branch, kissat build, LRAT job), then
   week item 3 (soundness chain).
