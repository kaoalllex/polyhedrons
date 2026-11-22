# Strategy review, 2026-11-22: the symmetric nine-face route has reached its laptop limit; score and price the equivelar slice (P6)

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep nine faces first and keep the stance, but change the route. The symmetric route has reached its laptop limit: all 12562 genus-4 per-map formulas are UNSAT-SOLVER, C3 has no genus-5 map, and the random 10 % at genus 5 is 97830 of 97830 UNSAT-SOLVER. That run finished after the handover was written. A C2 genus-6 census would cost about 70 times more. P6, the fallback the strategy already names, becomes the main line.
2. **Your parity question, measured this session.** The pass costs 0.094 core-s per map, 95 % of it the formula build. For any realization it excludes 1.3 % of the C2 (9, 4) maps and 6.8 % of 5000 random (9, 5) maps. Under the C2 action it excludes 10.6 % and 24 %; C3 maps, none. It cannot find an object, so it does not replace the remaining 90 %, and it changes no decision (T + D = 2). It is worth it only as a 3 core-h add-on, if you want exact certificates for the paper plan (approval 3).
3. **Item 3 (P6) did not run, and that was correct.** Its trigger, "neither census family advances", meant "neither passes its census gate", and both passed. The plan had no branch for "both families complete and all UNSAT-SOLVER". This review adds that branch, and P6 becomes item 1.
4. **Why P6 now.** Both known eight-face solids are equivelar: every face is a 9-gon (checked on the stored maps). Plain nine-face formulas, with the symmetry clauses dropped, refute most priced maps in seconds (3bi: 36 of 36 at (9, 5), 23 of 33 at (9, 4) within 5 s). So for maps without symmetry the likely limit at genus 4 is the map list, not the solver. P6 keeps only maps where every face is a 10-gon. It is scored first at (8, 3), where both known maps must be found unaided.
5. **Approval 1, first item: P6 rung and price** (E-261117-04). The (8, 3) equivelar census must recover both known maps through the plain formula; then the (9, 4) equivelar census is priced. Budget: one session plus <= 3 core-h. No night before a price.
6. **Approval 2: close out item 2.** Conclude the 10 % and apply the ledger fixes of §6. The remaining 90 % (~122 core-h, about 1.5 nights) scores T + D = 2, below the gate, so it runs only by your exception, on nights item 1 does not need. A clean 10 % sample says little about a single rare object: it misses any one map with probability 0.9.
7. **Approval 3:** the parity add-on of line 2, yes or no. **Approval 4:** the `STRATEGY.md` §1 text in §2, and the nine-face credence 0.45 -> 0.35.
8. **New lemma (PROVED-1 sketch, this session).** A C3 rotation axis crosses the surface an even number of times. So the 32 C3 (9, 4) maps with three fixed vertices are geometrically void (all UNSAT-SOLVER anyway), and C3 at genus 6 needs exactly two fixed vertices. That slice is below the gate (1 1); an exception costs one session.
9. **Not recommended:** the 90 % before item 1's price; a C2 genus-6 census; P3-sym at nine faces (no refutation power, 3bd); a parity pass over the full list without the 90 %; L6 at k = 5, 6 before the note.
10. **If P6 prices the (9, 4) equivelar slice above two nights,** nine faces has no laptop route beyond spot checks. The choice is then yours: the 90 %, consolidation and the note, or parking nine faces.

## 1. Week plan (for `ROADMAP.md`; <= 10 cores, 8-10 shards, the owner launches every run, no proofs, PLAN with unit tests first)

1. **P6 equivelar rung and price** ([E-261117-04](../experiments/E-261117-04-equivelar-price-pilot/), explore; J 0 at (8, 3), J 2 at
   (9, 4); 2 2 2 1 2; it has no PLAN yet). Stage A at (8, 3): census of the seven 2-regular extra-edge patterns (every face a 9-gon);
   the plain `submap=True` formula (E-261103-03, 9 elements) on every class if <= 300, else on a stratified price sample of 30 plus both
   known maps. Stage A' at (9, 4): census cap raised to 9 extra edges with the coverage argument re-read (or `symcensus.py` with the
   trivial group; the PLAN names one), the eight patterns at <= 10 min each, a tree-size estimate where capped (§5 N2), the plain formula
   at 10 elements on a price sample of <= 30 maps, cap 60 s. Budget <= 1 session + 3 core-h, 10 shards.
   * Controls: both known (8, 3) maps pinned SAT and unpinned SAT, bridged, `--all-pairs` PASS; a wrong pairing UNSAT. Overlap: the
     (9, 4) list holds the 119 symmetric equivelar records of E-261119-02 (104 C2, 15 C3; `strategy-review-2026-11-22-parity.json`)
     with their actions (two enumerators on one slice).
   * Tree: a known map absent or not SAT, or the overlap fails -> repair; a second failure -> escalate. A third (8, 3) map with
     `--all-pairs` PASS -> `candidate-check`, escalate (E-261112-02's reopening condition). A nine-face SAT -> bridge, `--all-pairs`,
     `candidate-check`, escalate. The full (8, 3) slice priced <= 1 night -> owner run (the discovery rung: both maps unaided). The (9, 4)
     census plus formulas priced <= 2 nights -> owner run, only after the (8, 3) slice recovered both maps. Above that -> the lead, with the price.
   * Lab: Opus, high / Codex gpt-6-astra, high (a census change whose coverage argument decides the claim; a new eight-face object is possible).
2. **E-261119-02 close-out** (no new method). Conclude amendment 6: the 10 % is complete. Its power line is the rule of three: < 3.1e-5
   SAT maps per map (95 %), nothing about one rare map. Then STATUS, README, log, and the ledger fixes of §6 items 1, 4. With approval 3:
   Lemma P (SEG, SEG+SYM) on the 12562 (9, 4) and 97830 decided (9, 5) records, `parity.py` functions unchanged, certificates re-checked
   and stored, ~2.9 core-h, ~20 min wall; labels: SEG inconsistent -> no cubic embedded realization of the map (certificate EXACT,
   reading PROVED-1); SEG+SYM inconsistent -> that formula UNSAT, EXACT. Only on the owner's exception: build chunks 10-99 (amendment 6's
   streaming build) and resume pass 1 on idle nights, the parity post-pass after it if approved. Stop: no C2 census at genus 6.
   * Lab: Sonnet, medium / Codex gpt-6.1-sol, medium (reading and reuse). A SAT in the 90 %: Opus, high / gpt-6-astra, high.

Deferred: E-261116-08, L6 at k = 5, 6 (the note's scope), P4, nine-plane sampling, I-261117-03, the asymmetric full (8, 3) sweep and E-261112-02
Stage B (both reopen on a new (8, 3) map from item 1), the curved-face encoder, the deletion sieve, E-261101-08, the (10, 4) replay; C3 at
genus 6 and the C2 (9, 5) remainder (owner exceptions). Parked: P3-sym for nine faces (3bd), I-261117-04. Closed for the laptop: (11, 5), the
face-transitive nine-face slice (genus 4, 7), C2 4 x 2 + 1 at genus >= 6. None is refuted.

## 2. Answers

* **Verdict.** The evidence supports the target and its fallback clause. It does not support the symmetric route as the main
  investment any longer. By L3 (PROVED-1, 3bi), a symmetric cubic nine-face object whose group is not Cs carries C3 3+3+3 or C2 4 x 2 + 1.
  Both genus-4 lists are complete, and every formula on them is UNSAT-SOLVER (3be, 3bf; planning only). At genus 5, C3 is empty (EXACT, 3bg), C2 has
  978228 maps (EXACT, 3bh) and its 10 % is all UNSAT-SOLVER (session count, below; not concluded). The C2 census grows per genus from 0.17 to
  11.5 core-h and from 12444 to 978228 maps (x67, x79; NUMERICAL), so genus 6 projects to ~800 core-h and ~7e7 maps (CONJECTURE). It
  changes on a SAT; on P6's (8, 3) rung failing to recover the known maps (the per-map plain route then lacks discovery power: stop nine
  faces on the laptop); on a (9, 4) equivelar price above two nights (digest 10).
* **Owner Q1, parity** (`python3 -I reviews/strategy-review-2026-11-22-parity.py`, 174 s wall, 10 workers; all 12562 (9, 4) records and
  the first 500 of each 10 % chunk, a random sample of the frozen order; every certificate re-checked; counts EXACT, rates NUMERICAL):

  | Records | SEG inconsistent: no realization at all | SEG+SYM inconsistent: none under the action |
  |---|---|---|
  | C2 4 x 2 + 1 (9, 4), all 12444 | 166 (1.3 %) | 1313 (10.6 %) |
  | C3 3+3+3 (9, 4), all 118; the 119 equivelar records of both | 0 | 0 |
  | C2 4 x 2 + 1 (9, 5), random 5000 | 340 (6.8 +- 0.7 %) | 1209 (24.2 +- 1.2 %) |

  Projected to all (9, 5) maps: ~66,500 maps and ~236,500 (map, action) pairs. The SEG+SYM rate rises with multiplicity-3 pairs (C2
  (9, 4): 6.5, 16, 30 % for 0, 1, 2 such pairs), SEG alone does not. Cost: 0.094 core-s per record, 0.0037 of it parity: ~26 core-h for
  all 990790 records, ~2.9 for the (9, 4) list plus the decided 10 %; inside the lean runner (kissat skipped on an inconsistent system)
  almost free, an amendment only if the 90 % runs. Reading: the project's first solver-free per-map exclusion, tiny certificates; nothing
  at (9, 3) (0 of 32, 3bi), 76-89 % left open at nine faces: it settles no slice. Exact side (`STRATEGY.md` §2), paper items B5 / B8.
* **Owner Q2, item 3:** as digest 3; the lab followed the tree (`ROADMAP.md:142`, the reconcile row 5).
* **For the lead 1** (parity, then the plain formula, versus the 90 %): parity as above. A plain pass over the symmetric lists asks only
  whether these maps have realizations without the symmetry; (9, 4) left 10 of 33 UNKNOWN at 5 s (3bi); unpriced, 1 1; see item 1.
* **For the lead 2, 3:** L6 at k = 5, 6 serves only the deferred note's "cubic" scope: defer with the note. P3-sym: agreed (3bd), parked
  for nine faces until a refutation rung decides. Overruns and under-blocking: §6 item 3.
* **Proposed `STRATEGY.md` §1 "First" (not applied):** "S1, nine mutually adjacent faces, genus free. The symmetric route (C3 3+3+3,
  C2 4 x 2 + 1) is UNSAT-SOLVER at genus 4 for both families and empty for C3 at genus 5; on the laptop it ends there (the C2 genus-5
  remainder and C3 at genus 6 only by the owner's exception). Main line: P6, the equivelar slice for any symmetry (E-261117-04), scored at
  (8, 3) on the two known equivelar maps, then priced at (9, 4) before any night. No nine-plane sampling night without a rung-below rate;
  P3-sym parked for nine faces (3bd); mirror families are covered only by plain formulas (L1)."

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, P6 rung + price (E-261117-04, amended) | 2 2 2 1 2 | 0 / 2 | 1 session + <= 3 core-h | first; every outcome moves the plan |
| Parity add-on, (9, 4) list + decided 10 % | 2 0 2 1 2 | 0 | 2.9 core-h | exact side; approval 3 |
| C2 (9, 5) remaining 90 % | 1 1 2 0 2 | 2 | ~122 core-h | below gate; owner exception |
| C3 3+3+3 at (9, 6), b = 2 (§5 N1) | 1 1 2 1 2 | 2 | 1 session, <= 2 core-h | below gate; owner exception |
| Plain formula on the symmetric (9, 4), (9, 5) lists | 1 1 2 1 2 | 2 | unpriced, >= 10 core-h | equivelar part inside item 1 |
| C2 4 x 2 + 1 census at (9, 6); P3-sym at nine faces; face-transitive genus >= 10 | 1 1 0 1 2; 0 1 1 1 2; 0 1 2 0 2 | 2 | ~800 core-h; >= 1 night; 1 session | close; park; below gate |
| L6 at k = 5, 6 (I-261108-09); XOR-aware solving (I-261110-05), I-261108-01; equivelar literature (E-261101-22) | 1 1 2 2 2; 1 1 2 1 2; 1 1 2 1 2 | 0 | 1 session each | the note only; Lemma P is their linear part; P6's premise |
| Asymmetric full (8, 3) sweep; E-261112-02 Stage B, H-261112-01 | 1 1 1 1 2; 2 1 1 1 2 | 0; 2 | >= 1 night; 2 nights | reopen on a new (8, 3) map |
| Curved-face encoder, deletion sieve; I-261117-03, P4, I-261029-51, I-261116-06; nine-plane sampling; E-261101-08 | as 2026-11-19 | | | no new evidence |

Parked targets only: S6 (I-261119-01 at (11, 4), (12, 5); E-261116-08; I-261116-05), S5 (I-261116-02), S0 (E-261101-06, 2 2 2 2 2; the
rest as filed): no new evidence, scores kept. Hypotheses: H-261101-07 -> weakened (§6 item 4); the other open ones unchanged.

## 4. Queue (in order; first item: 1)

1. **Item 1** (explore). H: the (8, 3) equivelar slice is small and its plain formulas recover both known maps unaided; the (9, 4)
   equivelar slice fits <= 2 nights. Falsifier: stage A' (the price) and the rung. Budget <= 3 core-h; stop by its tree.
2. **Item 2** (close-out; the add-on is exact side). H (add-on): ~1 % of (9, 4), ~7 % of (9, 5) maps carry a certificate; no plan change.
3. **(8, 3) equivelar owner run** (explore, the rung, after item 1). H: both known maps unaided; a third map <= 0.05 (CONJECTURE). A known
   map missing -> no (9, 4) night. **4. (9, 4) equivelar owner run** (explore, J 2, after 3): all UNSAT-SOLVER -> slice closed, credence -> ~0.28.
5. **C2 (9, 5) remainder** (explore, exception): chance of a symmetric genus-5 object ~0.04 (CONJECTURE), ~122 core-h, resumable.
   **6. C3 at (9, 6)** (explore, exception): census and formulas, <= 2 core-h, b = 2.

## 5. New ideas (untested proposals, not evidence)

* **N1. Axis alternation for C3.** A C3 rotation of a solid with no fixed face meets the surface only at fixed vertices, transversally,
  alternating entry and exit, so b is even with equal rotation numbers. Riemann-Hurwitz gives b = g + 2 - 3h (quotient genus h) and
  b <= 3, so b = 0 at genus 4 and 7, b = 2 at genus 6, none at 5 (PROVED-1 sketch; Codex 2026-11-19 §5 proposed b = 0 at genus 4). Test:
  the 32 b = 3 (9, 4) maps are UNSAT-SOLVER (3be, 3bf; consistent, not a proof). Use: C3 censuses skip void maps.
* **N2. Tree-size estimation for census pricing** (Knuth 1975, backtracking analysis; also used for #SAT): random root-to-leaf probes
  give unbiased node and leaf counts per pattern; the (8, 3) check of 16b stopped at 551 of 1806 patterns with a lower bound only. Test:
  on item 1's exact (8, 3) equivelar count the 95 % interval must cover it. Overlap with a symmetric list (item 1) is the census control.
* **N3. Density hypothesis.** Refutation gets faster with extra-edge density (plain at 5 s: 0 of 32 (9, 3), 23 of 33 (9, 4), 36 of 36
  (9, 5); 3bi), and parity exclusions rise with multiplicity-3 pairs, but none of the 119 equivelar symmetric (9, 4) records is
  inconsistent. If realizable nine-face maps exist, they sit near the (8, 3) density. Test: item 1 records plain time against the face-degree spread.

## 6. Audit

1. **Stale handover, power line owed.** `CONTINUE_PROMPT.md:12-16` says the 10 % stopped at 49194. The untracked `results.jsonl` files
   of `results/stageB5-pass1-c000..c009` hold 97830 of 97830 maps UNSAT-SOLVER (5 SKIPPED-STOP rows rerun; max 2.0 s at the 5 s cap, mean
   0.16 s; no process running; session count, NUMERICAL). Its reading needs the power (`STRATEGY.md` §2): < 3.1e-5 per map at 95 %.
2. **Amendment chain.** E-261119-02 has six amendments since 2026-11-19 (`PLAN.md:68-247`). `PROTOCOL.md:212-213` allows two ("a third
   need is an escalation"). Each carried an owner decision, so nothing ran unapproved. Amendments 3-6 run 37-40 lines each against the 15-line
   budget (`PROTOCOL.md:216`), and the PLAN is 247 lines. Rule: an owner decision is one amendment line plus a link to where it was priced.
3. **Budget overruns.** E-261119-01 spent 8.5 core-h in a discarded first launch whose stop reason was never recorded (`CONCLUSION.md:8-15`).
   E-261119-03 spent 1.7 core-h in an aborted 10-worker launch against a 0.2 core-h line, which is 72 s at 10 workers (`CONCLUSION.md:6-10`).
   Rule: the first launch of a new stage runs on one worker for <= 2 min and measures cost per unit, and every stop writes its reason into
   the manifest. The normaliser under-blocking (`E-261119-01/PLAN.md:84-90`) was repaired there (`copy_perms`); E-261119-02 blocks nothing.
4. **Hypothesis status.** `hypotheses/H-261101-07-maximal-face-neighbourly-exist.md:5` is "open". But its own rule (:32-33) fired for
   genus 2 and 3 (:70-72), which contradicts "exist for genus 2-5" at formula scope -> weakened. E-261119-02 and -03 list it under `tests:`
   (README:8, :10), though (9, 4), (9, 5) and (9, 7) are not maximal cases: leave `tests:` empty or file a nine-face hypothesis.
5. **Chains to stop:** the symmetric route after this week, P3-sym at nine faces, face-transitive slices past genus 7, parity as a
   stand-alone pass. **Process cost:** 40 commits since the review, code +2,879 lines (py, sh, c) against markdown +2,016, about 59 core-h
   (conclusions; the 10 % at 0.50 core-s per unit), no candidate.

## 7. Credences (all CONJECTURE, planning weights)

* **Nine faces 0.45 -> 0.35.** By L3, every symmetric non-Cs genus-4 object would sit in two complete lists, all UNSAT-SOLVER. Genus 5:
  C3 empty (EXACT), C2 a clean 10 %. The face-transitive slice is empty at genus 4 and 7 (EXACT). The previous review predicted 0.35-0.40
  for this outcome; maps without symmetry and mirror maps at genus 4 are untouched, which keeps it from going lower.
* Relaxed Szilassi-12 0.40, (10, 4) 0.10, S6 (10, 3) 0.25, S0 A 0.20: no new datum; (11, 5) closed, the unapplied proposal stays.

## 8. Three things to do first

1. Owner: approvals 1-4 (P6 first; the 90 % and C3 genus 6 as exceptions or not; the parity add-on; the `STRATEGY.md` text and 0.35).
2. Lab (Opus, high / gpt-6-astra, high): item 1's PLAN (census route, coverage, controls, the price rule), then stage A and A' in the session.
3. Lab (Sonnet, medium / gpt-6.1-sol, medium): item 2, the 10 % conclusion and the ledger fixes; the parity add-on if approved.
