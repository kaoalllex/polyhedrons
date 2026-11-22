# Strategy review, 2026-11-22: the symmetric nine-face route has reached its laptop limit; score and price the equivelar slice (P6)

## Owner digest (ten lines; the rest is reference; revised after the owner's questions, 2026-11-22)

1. **Verdict (Recommendation).** Keep nine faces first and keep the stance, but change the route. The symmetric nine-face route has reached its laptop limit: all 12562 genus-4 per-map formulas are UNSAT-SOLVER, C3 has no genus-5 map, and the random 10 % at genus 5 is 97830 of 97830 UNSAT-SOLVER (your full run). A C2 genus-6 census would cost about 70 times more. P6, the fallback the strategy already names, becomes the main nine-face line.
2. **Your question: why do unaided searches at (8, 3) find only the two known maps?** Every search so far was local, group-limited, underpowered or never run on the full list. The rung-below census looked only next to Roest-Vigh's planes. P3-sym with D2 / S4 was confined to those groups. P3-sym with a free C2 found both known maps within 2.5 min, then gave UNKNOWN for 1.5 h: it neither finds nor excludes a third. The strong per-map formula ran on only 4 of the 822 free-C2 (8, 3) records, the known maps. The other 788 map classes were never tested, although a record takes about 0.1 s.
3. **Hence a new first item: the full free-C2 (8, 3) pass.** All 822 (map, action) records, unchanged runner, about 10 min, the lab runs it itself. By L4 this covers every symmetric uniform eight-face solid except the C1, Cs, C7 and C7v groups. Two outcomes: only the two known maps come out SAT, so the symmetric (8, 3) slice holds just them (UNSAT-SOLVER, formula scope); or a third map realizes, which is a new eight-face object and goes to `candidate-check`.
4. **Your question: the parity pass's chances.** Exact exclusions are certain: the session check already counts 166 (9, 4) maps excluded for any realization and 1313 under the action; the finished 10 % would add about 6650 and 23700. The chance that it finds an object is 0 by construction. The chance that it closes a slice is about 0 as well: 76-89 % of maps stay open, and no stratum exceeds 42 %. Recommendation: not now; it is a 20-min lab run when the paper is written.
5. **Item 3 (P6) did not run, and that was correct.** Its trigger, "neither census family advances", meant "neither passes its census gate", and both passed; the plan had no branch for "all UNSAT-SOLVER". P6 now follows item 1. Both known eight-face solids are equivelar (every face a 9-gon). Plain nine-face formulas refute most priced maps in seconds (3bi). So for maps without symmetry the likely limit at genus 4 is the map list, not the solver.
6. **Approvals:** (1) item 1, the (8, 3) pass; (2) item 2, P6 rung and price (one session plus <= 3 core-h, no night before a price); (3) the `STRATEGY.md` §1 text in §2 and the nine-face credence 0.45 -> 0.35.
7. **Your decisions, recorded in the closing section:** the remaining 90 % is postponed. The lab runs any job of <= 50 min wall itself, after a one-line heads-up (cores, minutes); only longer runs are owner launches. A night gets a queue sized to fill about 8 h.
8. **Why nights ended early.** The prices were right (pass 1: 1.8 priced, 1.83 used; the (9, 5) census: 12 and 12.4; the 10 %: 14 and ~13.6 core-h). The plans' caps (10, 40, 20 core-h) were ceilings, 3-5 times above the price, not forecasts. No queued job needed 80 core-h, and the only one that would (the 90 %, ~122 core-h) is postponed.
9. **Not recommended:** a C2 genus-6 census; P3-sym at nine faces (no refutation power, 3bd); C3 at genus 6 (below the gate; §5 N1); L6 at k = 5, 6 before the note.
10. **If P6 prices the (9, 4) equivelar slice above two nights,** nine faces has no laptop route beyond spot checks. The choice is then yours: the 90 %, consolidation and the note, or parking nine faces.

## 1. Week plan (for `ROADMAP.md`; <= 10 cores, 8-10 shards, no proofs, PLAN or amendment with unit tests first; jobs <= 50 min wall the lab launches itself after a heads-up, longer ones the owner)

1. **Free-C2 (8, 3) per-map pass** (E-261119-02 amendment 7; explore, J 0; 2 2 2 1 2). Stage B's runner unchanged on the whole free-C2
   (8, 3) list of stage A (790 classes, 822 (map, action) records: 766 one action, 16 two, 8 three; `stageb.records_for('C2_8_3', ...)`),
   cap 30 s, lean except SAT units, 10 shards, about 10 min wall; parity is not added. Controls: the runner's pilot controls, and the 4
   rung records repeat their status and hashes (Roest-Vigh SAT under 2 of 3 groups, Mizhaev SAT).
   * Tree: SAT only on the known maps -> "the free-C2 (8, 3) formulas hold only the two known maps" (UNSAT-SOLVER, formula scope; owner Q5
     of 2026-11-19); compare with E-261119-01 U1 on common maps. A SAT on another map -> bridge, `--all-pairs` PASS -> `candidate-check`,
     escalate (a new eight-face object; reopens E-261112-02). A SAT whose bridge fails -> the map stays open, to the lead. UNKNOWNs -> pass 2
     at 600 s inside 1 core-h, else to the lead. A failed control -> repair.
   * Lab: Opus, high / Codex gpt-6-astra, high (a new eight-face object is possible).
2. **P6 equivelar rung and price** ([E-261117-04](../experiments/E-261117-04-equivelar-price-pilot/), explore; J 0 at (8, 3), J 2 at
   (9, 4); 2 2 2 1 2; it has no PLAN yet). Stage A at (8, 3): census of the seven 2-regular extra-edge patterns (every face a 9-gon);
   the plain `submap=True` formula (E-261103-03, 9 elements) on every class if <= 300, else on a stratified price sample of 30 plus both
   known maps. Stage A' at (9, 4): census cap raised to 9 extra edges with the coverage argument re-read (or `symcensus.py` with the
   trivial group; the PLAN names one), the eight patterns at <= 10 min each, a tree-size estimate where capped (§5 N2), the plain formula
   at 10 elements on a price sample of <= 30 maps, cap 60 s. Budget <= 1 session + 3 core-h, 10 shards.
   * Controls: both known (8, 3) maps pinned SAT and unpinned SAT, bridged, `--all-pairs` PASS; a wrong pairing UNSAT. Overlap: the
     (9, 4) list holds the 119 symmetric equivelar records of E-261119-02 (104 C2, 15 C3; `strategy-review-2026-11-22-parity.json`)
     with their actions, and the (8, 3) list holds item 1's equivelar free-C2 maps (two enumerators on one slice).
   * Tree: a known map absent or not SAT, or an overlap fails -> repair; a second failure -> escalate. A third (8, 3) map with
     `--all-pairs` PASS -> `candidate-check`, escalate. A nine-face SAT -> bridge, `--all-pairs`, `candidate-check`, escalate. The full
     (8, 3) slice priced <= 1 night -> owner run (the discovery rung). The (9, 4) census plus formulas priced <= 2 nights -> owner run, only
     after the (8, 3) slice recovered both maps. Above that -> the lead, with the price.
   * Lab: Opus, high / Codex gpt-6-astra, high (a census change whose coverage argument decides the claim; a new eight-face object is possible).
3. **E-261119-02 close-out** (no new method). Conclude amendment 6: the 10 % is complete; its power line is the rule of three, < 3.1e-5
   SAT maps per map (95 %), nothing about one rare map. The 90 % is postponed by the owner; parity waits for the paper. STATUS, README,
   log and the ledger fixes of §6 items 1, 4, together with item 1's conclusion. Stop: no C2 census at genus 6.
   * Lab: Sonnet, medium / Codex gpt-6.1-sol, medium (reading and reuse).

Deferred: the C2 (9, 5) remainder (owner, 2026-11-22), the parity pass (to the paper), E-261116-08, L6 at k = 5, 6, P4, nine-plane sampling, I-261117-03,
the asymmetric full (8, 3) sweep and E-261112-02 Stage B (both reopen on a new (8, 3) map), the curved-face encoder, the deletion sieve, E-261101-08, the (10, 4)
replay, C3 at genus 6. Parked: P3-sym for nine faces (3bd), I-261117-04. Closed for the laptop: (11, 5), face-transitive nine faces (genus 4, 7), C2 at genus >= 6.

## 2. Answers

* **Verdict.** The evidence supports the target and its fallback clause, not the symmetric route as the main investment. By L3 (PROVED-1,
  3bi) a symmetric cubic nine-face object whose group is not Cs carries C3 3+3+3 or C2 4 x 2 + 1. Both genus-4 lists are complete, all
  UNSAT-SOLVER (3be, 3bf). At genus 5, C3 is empty (EXACT, 3bg) and C2 has 978228 maps (EXACT, 3bh), its 10 % all UNSAT-SOLVER (not yet
  concluded). The C2 census grows per genus 0.17 -> 11.5 core-h, 12444 -> 978228 maps (x67, x79; NUMERICAL), so genus 6 projects to
  ~800 core-h (CONJECTURE). It changes on a SAT, on P6's (8, 3) rung missing a known map, or on a (9, 4) price above two nights (digest 10).
* **Owner Q1, parity** (`python3 -I reviews/strategy-review-2026-11-22-parity.py`, 174 s wall, 10 workers; all 12562 (9, 4) records and
  the first 500 of each 10 % chunk, a random sample of the frozen order; every certificate re-checked; counts EXACT, rates NUMERICAL):

  | Records | SEG inconsistent: no realization at all | SEG+SYM inconsistent: none under the action |
  |---|---|---|
  | C2 4 x 2 + 1 (9, 4), all 12444 | 166 (1.3 %) | 1313 (10.6 %) |
  | C3 3+3+3 (9, 4), all 118; the 119 equivelar records of both | 0 | 0 |
  | C2 4 x 2 + 1 (9, 5), random 5000 | 340 (6.8 +- 0.7 %) | 1209 (24.2 +- 1.2 %) |

  The SEG+SYM rate rises with multiplicity-3 pairs (C2 (9, 4): 6.5, 16, 30 % for 0, 1, 2), up to 42 % in a (9, 5) stratum. Cost 0.094
  core-s per record (parity 0.0037): ~26 core-h for all 990790 records, ~2.9 for the (9, 4) list and the 10 %. It decided nothing at
  (9, 3) (0 of 32, 3bi) and settles no nine-face slice: exact side (`STRATEGY.md` §2), paper items B5 / B8, a lab run when the paper is due.
* **Owner Q2, item 3:** digest 5 (`ROADMAP.md:142`, reconcile row 5). **Q3, only the two known (8, 3) maps:** digest 2; sources 3ak (4 SOLID cells, all
  Roest-Vigh), 3bb (D2, S4), 3bd (U1 UNKNOWN after two maps), `results/stageB-rung_8_3` (4 records, SAT in 0.08 s), 3be (the 790-class list).
* **For the lead 1-3:** a plain pass over the symmetric lists asks only whether these maps have realizations without the symmetry; (9, 4)
  left 10 of 33 UNKNOWN at 5 s (3bi); unpriced, 1 1. L6 at k = 5, 6 serves only the deferred note: defer with it. P3-sym: agreed (3bd),
  parked for nine faces until a refutation rung decides. Overruns and under-blocking: §6 item 3.
* **Proposed `STRATEGY.md` §1 "First" (not applied):** "S1, nine mutually adjacent faces, genus free. The symmetric route (C3 3+3+3, C2 4 x 2 + 1)
  is UNSAT-SOLVER at genus 4 for both families and empty for C3 at genus 5; on the laptop it ends there (the C2 genus-5 remainder and C3 at genus 6
  only by the owner's exception). Main line: P6, the equivelar slice for any symmetry (E-261117-04), scored at (8, 3) on the two known equivelar maps,
  then priced at (9, 4) before any night. No nine-plane sampling night without a rung-below rate; P3-sym parked (3bd); mirrors only by plain formulas (L1)."

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, free-C2 (8, 3) per-map pass (E-261119-02 amendment 7) | 2 2 2 1 2 | 0 | ~10 min wall | first; owner Q3 |
| Item 2, P6 rung + price (E-261117-04, amended) | 2 2 2 1 2 | 0 / 2 | 1 session + <= 3 core-h | main nine-face line |
| Parity pass, (9, 4) list + decided 10 % | 2 0 2 1 2 | 0 | 2.9 core-h | to the paper |
| C2 (9, 5) remaining 90 %; C3 3+3+3 at (9, 6), b = 2 (§5 N1) | 1 1 2 0 2; 1 1 2 1 2 | 2 | ~122 core-h; <= 2 core-h | postponed (owner); below gate |
| C2 4 x 2 + 1 census at (9, 6); P3-sym at nine faces; face-transitive genus >= 10 | 1 1 0 1 2; 0 1 1 1 2; 0 1 2 0 2 | 2 | ~800 core-h; >= 1 night; 1 session | close; park; below gate |
| L6 at k = 5, 6 (I-261108-09); XOR-aware solving (I-261110-05), I-261108-01; equivelar literature (E-261101-22) | 1 1 2 2 2; 1 1 2 1 2; 1 1 2 1 2 | 0 | 1 session each | the note only; Lemma P is their linear part; P6's premise |
| Asymmetric full (8, 3) sweep; E-261112-02 Stage B, H-261112-01 | 1 1 1 1 2; 2 1 1 1 2 | 0; 2 | >= 1 night; 2 nights | reopen on a new (8, 3) map |
| Curved-face encoder, deletion sieve; I-261117-03, P4, I-261029-51, I-261116-06; nine-plane sampling; E-261101-08 | as 2026-11-19 | | | no new evidence |

Parked targets only (S6: I-261119-01, E-261116-08, I-261116-05; S5: I-261116-02; S0: E-261101-06 and the rest): scores kept. H-261101-07 -> weakened (§6.4).

## 4. Queue (in order; first item: 1)

1. **Item 1** (explore). H: the free-C2 (8, 3) formulas are SAT only on the two known maps. Falsifier: one more SAT that realizes (a new
   object). Outcome: no SAT -> the symmetric (8, 3) slice holds only them (UNSAT-SOLVER). ~10 min, lab-run; stop by its tree.
2. **Item 2** (explore). H: the (8, 3) equivelar slice is small and its plain formulas recover both known maps; the (9, 4) equivelar slice
   fits <= 2 nights. Falsifier: stage A' (the price) and the rung. <= 3 core-h. **3. Item 3** (close-out), no plan change.
4. **(8, 3) equivelar owner run** (explore, the rung, after item 2): a third map <= 0.05 (CONJECTURE); a known map missing -> no (9, 4)
   night. **5. (9, 4) equivelar owner run** (explore, J 2, after 4): all UNSAT-SOLVER -> slice closed, credence -> ~0.28. <= 2 nights.
6. **C2 (9, 5) remainder** (postponed by the owner; ~0.04 chance, CONJECTURE, ~122 core-h). **7. C3 at (9, 6)** (below gate, <= 2 core-h).

## 5. New ideas (untested proposals, not evidence)

* **N1. Axis alternation for C3.** With no fixed face, the axis meets the surface only at fixed vertices, crossing in and out alternately: b is even, the rotation numbers equal.
  Riemann-Hurwitz, b = g + 2 - 3h, and b <= 3 give b = 0 at genus 4 and 7, 2 at genus 6, none at 5 (PROVED-1 sketch; Codex 2026-11-19 §5 had b = 0
  at genus 4). Test: the 32 b = 3 (9, 4) maps are UNSAT-SOLVER (3be, 3bf; consistent, not a proof). Use: C3 censuses skip void maps.
* **N2. Tree-size estimation for census pricing** (Knuth 1975; also used for #SAT): random root-to-leaf probes give unbiased node and leaf counts per pattern;
  the (8, 3) check of 16b stopped at 551 of 1806 patterns with a lower bound only. Test: on item 2's exact (8, 3) equivelar count the 95 % interval covers it.
* **N3. Density hypothesis.** Refutation speeds up with extra-edge density (plain at 5 s: 0 of 32 (9, 3), 23 of 33 (9, 4), 36 of 36 (9, 5); 3bi), parity
  exclusions rise with multiplicity-3 pairs, none of the 119 equivelar records fails: realizable maps, if any, sit near the (8, 3) density. Test: item 2's timings.
* **N4. Owner's raw idea, TODO 0.1** ("A Society of AI Scientists", alphaXiv, 2026-11-21; abstract page read, PDF not; CLAIMED): no mathematics for
  this problem; one practice kept: execution-tested review (objections rerun on the data overturned headlines far more often than text-only review); folded into step 2 of the cycle below. Drop the rest.

## 6. Audit

1. **Stale handover, power line owed.** `CONTINUE_PROMPT.md:12-16` says the 10 % stopped at 49194. The untracked `results.jsonl` files
   of `results/stageB5-pass1-c000..c009` hold 97830 of 97830 maps UNSAT-SOLVER (5 SKIPPED-STOP rows rerun; max 2.0 s at the 5 s cap, mean
   0.16 s; session count, NUMERICAL). Its reading needs the power (`STRATEGY.md` §2): < 3.1e-5 per map at 95 %.
2. **Amendment chain.** E-261119-02 has six amendments since 2026-11-19 (`PLAN.md:68-247`) against two (`PROTOCOL.md:212-213`); each carried an owner decision,
   but amendments 3-6 run 37-40 lines against 15 (`PROTOCOL.md:216`). Rule: an owner decision is one amendment line plus a link to where it was priced.
3. **Budget overruns.** E-261119-01: 8.5 core-h in a discarded first launch, stop reason never recorded (`CONCLUSION.md:8-15`); E-261119-03: 1.7 core-h in
   an aborted 10-worker launch against a 0.2 core-h line, i.e. 72 s at 10 workers (`CONCLUSION.md:6-10`). Rule: a new stage's first launch runs one worker for
   <= 2 min, and every stop writes its reason into the manifest. The under-blocking (`E-261119-01/PLAN.md:84-90`) was repaired there; E-261119-02 blocks nothing.
4. **Hypothesis status.** `hypotheses/H-261101-07-maximal-face-neighbourly-exist.md:5` is "open". But its own rule (:32-33) fired for
   genus 2 and 3 (:70-72), which contradicts "exist for genus 2-5" at formula scope -> weakened. E-261119-02 and -03 list it under `tests:`
   (README:8, :10), though (9, 4), (9, 5) and (9, 7) are not maximal cases: leave `tests:` empty or file a nine-face hypothesis.
5. **Coverage gap and chains to stop.** Stage A listed 790 free-C2 (8, 3) classes, but stage B ran only the 4 known records (`stageb.py:135-138`).
   Item 1 closes that gap. Stop: the symmetric nine-face route after this week, P3-sym at nine faces, face-transitive slices past genus 7.
   Cost: 40 commits, code +2,879 lines against markdown +2,016, about 59 core-h, no candidate.

## 7. Credences (all CONJECTURE, planning weights)

* **Nine faces 0.45 -> 0.35.** Symmetric non-Cs genus-4 objects would sit in two complete lists (L3), all UNSAT-SOLVER; genus 5: C3 empty, C2 a clean 10 %;
  face-transitive empty at genus 4, 7 (EXACT); predicted 0.35-0.40; asymmetric and mirror genus-4 maps untouched. The other credences unchanged.

## 8. Three things to do first

1. Owner: the Codex cross-review of this draft (step 2), then the final version (step 3) and the approvals (1)-(3) of digest 6.
2. Lab (Opus, high / gpt-6-astra, high), after approval: item 1 (amendment 7, a one-line heads-up, the ~10 min run), then item 2's PLAN, stages A, A'.
3. Lab (Sonnet, medium / gpt-6.1-sol, medium): item 3, the 10 % conclusion and the ledger fixes, together with item 1's conclusion.

## Owner's decisions (2026-11-22, on the first version of this review)

* The C2 (9, 5) remainder (chunks 10-99) is postponed. The parity pass: the owner asked for its chances (digest 4); deferred to the paper.
* Launch rule: a lab session runs any job of <= 50 min wall itself after a one-line permission (cores, minutes); longer jobs stay owner launches;
  a night gets a queue that fills about 8 h. Strategy cycle: draft with the owner's corrections, Codex cross-review, final version approved by the
  owner. Both applied in this session to `PROTOCOL.md` §8b, `STRATEGY.md` §3 and log, `CLAUDE.md`, `AGENTS.md` and the `strategy-review` skills.
