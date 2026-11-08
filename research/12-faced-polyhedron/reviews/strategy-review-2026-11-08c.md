# Strategy review, 2026-11-08 (c): interim, week items 1-4 done, item 5 open

Interim lead review at the owner's request while the week plan is unfinished: assess the finished items and say what
to do next. Evidence cut: `51d74d1` on `lab/2026-11-07` plus the untracked `E-261108-02/results/`. This report advises
and changes no ledger file. Labels are `SPEC.md` §5; **Recommendation** and **Untested** mark judgments and proposals.
Scope is reduced on purpose: candidates whose evidence did not change since `reviews/strategy-review-2026-11-08.md` keep
that review's scores (§5); the full re-scoring belongs to the next weekly review, after item 5a. Checks run (seconds):
hash fields of the 33 E-261108-02 `result.json` files, and a look-up of the four unmatched hashes in E-261103-03 records.

## 1. Verdict in ten lines

1. **Recommendation:** strategy unchanged until item 5a reports; the focus question is now within one night of an
   exact answer at formula scope.
2. **EXACT (formula scope):** 45 of 203 admissible (9,3) plain formulas UNSAT-VERIFIED, 0 SAT, 60 unresolved, 98
   unattempted. All 24 11-gon maps are UNSAT-VERIFIED (item 1).
3. **NUMERICAL:** the decisive new fact is that the slow classes are solvable: 12/12 lowest-index maps of `1^6`,
   `(1^4,2)` and `(1,1,2,2)/(2,3)` finished in 89-914 s at a 1800 s cap (largest 51 % of the cap). The "cannot tell"
   risk for (9,3) was the slow classes; it is much smaller now.
4. **Estimate (untested):** the 158 remaining maps need about 20-35 core-h, 2.5-4 h wall on 10 shards (§3). Item 5a's
   80 core-h / 8 h ceiling covers it with margin, unless high-index maps are much slower than the lowest-index ones.
5. **Blocker for 5a (EXACT, code):** the runner reserves `len(todo) x (1800 + 2700) + 960` s per shard
   (`experiments/E-261103-03-s5-exact-decision-8-2-9-3/tranche.py:344`). For 158 maps on 10 shards that is ~730,000 s
   against an 80 core-h (288,000 s) ceiling, so most shards would refuse to start (item 1 already hit this on shard 8,
   `experiments/E-261103-03-s5-exact-decision-8-2-9-3/CONCLUSION.md:479`). The reservation must be deadline-based.
6. **Items 3 and 4 parked correctly:** core study 0/24 (cores on <= 6 faces), arrangement sweep 0/300 solids. Both
   kill rules fired as pre-registered; no follow-up passes `STRATEGY.md` §2.
7. **Item 2:** literature check found nothing for (8,2), (9,3), (10,4) (CLAIMED, web only). A negative (9,3) result
   would therefore be new.
8. **Credences:** (9,3) moves to 0.30 / 0.55 / 0.15 (§6), a 0.15 move on "does not exist", so the next lead review
   is due right after item 5a.
9. **Audit:** the E-261108-02 evidence (33 `result.json`, 5.6 MB) is not committed; its hash line is off; one
   E-261108-01 sentence claims more than was measured (§5).
10. **First item:** one prep session for 5a (deadline-based reservation, the 158-map queue, controls per shard,
    10-shard startup check), then the owner launches it for one night.

## 2. Week plan: replacement text for item 5 in `ROADMAP.md`

Items 1-4 are done and stay as recorded. Item 5b is not triggered ((b) 12/12 >= 8/12 sends every class to 5a).

```
5. **(9,3) completion night** (exploit; E-261103-03 item 5a; amended by `reviews/strategy-review-2026-11-08c.md`).
   Question: are all 203 admissible (9,3) plain formulas UNSAT?
   * Prep (one lab session): queue of the 158 unresolved and unattempted maps, ordered fast patterns first
     ((1,1,2,2)/(2,3) 5, (1,1,2,2)/(2,2,2) 36, (1^4,2) 89, 1^6 28), lowest index first within a pattern;
     controls `control-f9` and `control-f9-neg` at the head of every shard; solver 1800 s, checker 2700 s;
     deadline-based budget (each shard reserves at most the night's wall, 8 h; ceiling 80 core-h on 10
     shards), so no shard refuses to start; first-SAT stop; evidence option A (PROTOCOL §5); record cadical
     process time per map; bounded 10-shard startup check (PROTOCOL §8).
   * Launch: one owner night, 10 shards, `launch.sh`.
   * Predictions: controls pass; >= 150/158 decided; 0 SAT; solver time per pattern within 2x of item 1's.
   * Kill: a control fails -> stop, escalate. Follow-up tree:
     * any SAT -> stop dispatch; exact model check, saved-OM realizer, `verify_candidate.py --target S5`,
       `candidate-check`; a model that does not realize: one final-polynomial attempt (at most 1 session);
     * all 203 UNSAT-VERIFIED -> record "every admissible (9,3) plain formula is UNSAT-VERIFIED" (EXACT,
       formula scope; geometric reading PROVED-1, conditional on census coverage and encoder soundness);
       stop focus compute and call the lead review (the strategy question of §4); the (10,4) cost probe
       (E-261103-07, <= 1 core-h, all patterns represented) may run before it;
     * 1-8 maps TIMEOUT -> list them; item 5b (micro-benchmark) on those maps only, at most 1 session + 4 core-h;
     * > 8 maps TIMEOUT or the deadline cuts the queue -> record the per-pattern times; escalate for a second night.
6. **Housekeeping** (no compute, beside item 5): commit the E-261108-02 `result.json` and manifests; owner decides on its
   15,177 sub-formula SAT models (983 MB, §5 A1); wording fixes A2, A3.
```

## 3. Cost estimate for item 5a (untested)

Remaining maps by pattern (`reviews/strategy-review-2026-11-08.md` §3.1 minus items 1(a) and 1(b), EXACT counts):
`1^6` 28, `(1^4,2)` 89, `(1,1,2,2)/(2,2,2)` 36, `(1,1,2,2)/(2,3)` 5; total 158. Mean solver time from item 1: 708 s,
246 s, unmeasured above 60 s (taken as 246 s), 113 s. Checker taken as 0.6 x solver (item 1: 588 s at 914 s). Sum:
about 82,000 s = 23 core-h; with a factor 1.5 for unknown high-index behaviour, 35 core-h. Worst case (every map at
both caps) is 197 core-h, which the deadline cut handles. The lowest-index maps are not a sample, so this is an
estimate, not a prediction with a stated power.

## 4. Answers to "For the lead"

`CONTINUE_PROMPT.md` has no open "For the lead" question. The strategic question this week raises:

**What if item 5a decides all 203 maps UNSAT?** Then the focus target S5 at (9,3) has a conditional negative answer
(PROVED-1 geometric reading), and `STRATEGY.md` §1 names no successor beyond the stretch (10,4). **Recommendation:**
decide among three options at the next lead review, not now:

1. a note "(8,2) and (9,3) maximal face-neighbourly polyhedra do not exist (conditional)": needs regenerated and
   archived proofs (about the same core-h as 5a, owner rule 2026-11-08), and human review of the census coverage
   and the encoder argument, today PROVED-1 by AI only; the external contact declined on 2026-11-07 is the cheapest
   such review, so the owner may wish to revisit it then;
2. the (10,4) exact route: 1117 admissible maps, one more element per formula; the E-261103-07 cost probe tells
   within 1 core-h whether it is one week or a campaign;
3. return to S0 with the exact pipeline (transfer test): not cheap (~19,000 core-h estimated earlier).

## 5. Audit

| ID | Where | Finding | Fix |
|---|---|---|---|
| A1 | `experiments/E-261108-02-concentrated-core-study/results/` | The 33 per-unit `result.json` (5.6 MB, statuses and CNF/proof hashes of every sub-formula) that `CONCLUSION.md` cites are untracked after the conclusion commit `51d74d1`. Beside them: 15,177 `*.model.json` (983 MB), SAT models of sub-formulas, not candidates | commit `result.json` + `manifest.txt` + `pip-freeze.txt`; do not commit the models (the "SAT models are kept" rule targets models of full formulas); owner: delete or keep local |
| A2 | `experiments/E-261108-02-concentrated-core-study/CONCLUSION.md:14` | "27 of 30 maps; 40, 48, 5, 6 have no local record" is wrong twice: 26 matched via `result.json`, and 40 and 48 do have records that match (`E-261103-03/results/grid_9_3/summary.json`, `targets/map40_plain_t300`, `map48_plain_t300`; `cores.py:103` looks only in `result.json` files). Correct: 28 of 30 match, 5 and 6 have no local record | one-line fix |
| A3 | `experiments/E-261108-01-s5-arrangement-source-sweep/CONCLUSION.md:27` | "zero near-feasible signals" while the same file says no pair-count diagnostic was run: nothing about near-feasibility was measured | "no near-feasibility diagnostic was run" |
| A4 | `experiments/E-261103-03-s5-exact-decision-8-2-9-3/tranche.py:344` | Per-shard up-front reservation `len(todo) x (SOLVER_CAP + CHECKER_CAP)` cannot fit a 158-map queue under 80 core-h | deadline-based reservation in the 5a prep; test it in the startup check |
| A5 | process | Three lead reviews on 2026-11-08 (`-08`, `-08b`, this one). Each was cheap, but the next one should wait for item 5a | no review before 5a reports |
| A6 | follow-up chains | E-261108-02 leaves cores on 7-8 faces open (94 TIMEOUTs at k = 8, 20 s cap); E-261108-01 dropped Phase B. Neither outcome changes a decision while 5a can decide every map directly | do not queue either (`STRATEGY.md` §2) |

Claims checked against evidence: the item 1 claim "every 11-gon (9,3) plain formula is UNSAT-VERIFIED" is scoped
correctly (EXACT, formula scope, conditional geometric reading; the controls are genus 0). The E-261108-01 density bound is
correctly marked heuristic (i.i.d. assumption). The E-261108-02 null is supported by working controls (C1 detects a
planted core, C2 gives k_min 6), so it is not a constant artefact of the measurer.

## 6. Scores and credences

Changed scores only (T D F G R / jump / cost to first kill); everything else as in `reviews/strategy-review-2026-11-08.md` §5.

| Candidate | T D F G R | jump | cost to first kill | Note |
|---|---|---|---|---|
| E-261103-03 item 5a (completion night) | 2 2 2 2 2 | 2 | one night, ~25-35 core-h | the only item that can settle the focus question |
| E-261103-03 item 5b (micro-benchmark) | 1 1 2 1 2 | 0 | 1 session + 4 core-h | only for 5a's TIMEOUTs |
| E-261103-07 (10,4) cost probe | 1 2 2 2 2 | 2 | <= 1 core-h | after 5a; D rises to 2 because 5a may hand the focus to (10,4) |
| E-261108-02 follow-up (7-8-face cores) | 1 0 1 1 2 | 0 | 1 session | parked; T + D < 3 |
| Arrangement-first at (9,3) (I-261103-04) | 1 0 2 1 2 | 2 | - | parked by E-261108-01's kill rule |

Scenario credences (subjective planning weights, not evidence):

| Case | exists / does not / cannot tell | Change | One line of evidence |
|---|---|---|---|
| (9, 3) | **0.30 / 0.55 / 0.15** | -0.05 / +0.15 / -0.10 | 45 plain UNSAT, 0 SAT; the slow classes now decide in <= 914 s, so "cannot tell" shrinks; 0/330 solids from arrangement sources, weak |
| (8, 2) | 0 / 1 / 0, conditional | unchanged | conditions (census coverage, encoder soundness, PROVED-1) attached |
| (10, 4) | 0.30 / 0.30 / 0.40 | unchanged | no (10,4) evidence; the cost probe measures it |
| S0 A / B / C | 0.20 / 0.55 / 0.25 | unchanged | no S0 evidence since 11-01 |

Reversal: any 5a SAT that realizes moves "exists" to 1; a non-realizing SAT moves nothing until a final polynomial
excludes it; > 8 TIMEOUTs at 1800 s returns "cannot tell" to ~0.25.

## 7. New ideas (untested proposals, not evidence)

1. **Second encoder on five maps.** An independently written plain (9,3) encoder (a different formulation, e.g. 3-term
   Grassmann-Pluecker plus face-cycle orientation, not sharing `pilot.build`) decides five maps of different
   patterns (fast ones, <= 1 core-h). Why: if 5a decides everything, the whole claim rests on one encoder whose
   soundness is PROVED-1 by AI only; agreement of two codes is not a proof but removes the likeliest failure, an
   implementation bug. Cheapest test: map 40 (62 s) in both. Overlaps E-261101-09 step 1 (predicate equality).
2. **Pattern census of (10,4) before the cost probe.** Count the 1117 admissible (10,4) maps by face-excess pattern
   (minutes, the `maps_10_4.json` data); choose the probe's 10 maps across the strata so that 5a's per-pattern times
   give a cost model. Without it, the probe repeats the biased-sample problem of the (9,3) tranche.

## 8. Three things to do first

1. Prep session for item 5a: deadline-based reservation (A4), the 158-map queue, controls per shard, startup check.
   The owner launches it for one night.
2. Beside it, no compute: A1-A3.
3. After 5a: if all UNSAT, the (10,4) pattern census (idea 2) and cost probe, then the lead review on §4's question.
