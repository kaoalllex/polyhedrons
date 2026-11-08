# Strategy review, 2026-11-08 (weekly lead review)

Evidence cut: `6ad2fb5` on `lab/2026-11-07`. Covers everything after the 2026-11-04 review's cut (`dfbc81f`):
E-261103-03 stages 3e-3i, E-261103-05 (3g), E-261103-04 (3j-3s), E-261107-01 (3t), E-261103-06 (3u). No dated
review prompt exists; the questions are those of the skill and of "For the lead" in `CONTINUE_PROMPT.md`.
This report advises and changes no ledger file. Labels are `SPEC.md` §5; **Recommendation** and **Untested** mark
judgments and proposals, which are not evidence. One new analysis was run (seconds, committed data only):
`reviews/strategy-review-2026-11-08-runtime-patterns.py`.

## 1. Verdict in ten lines

1. **Recommendation:** keep S5 (9, 3) as the focus, (10, 4) as stretch, S0 parked. Nothing since 11-04 argues against it.
2. **EXACT:** 19 of 203 admissible (9, 3) maps have UNSAT-VERIFIED plain formulas, all 8 uniform free-C3 formulas
   are UNSAT-VERIFIED, 0 SAT in 100 target formulas; 73 maps time out (60-300 s), 111 are unattempted.
3. **NUMERICAL (new, §3.1):** solve time depends on the multiple-adjacency pattern. Maps whose extra segments meet
   at one face are fast (13 of 14 attempted, 22-76 s); maps with spread-out doubled pairs are slow (0 of 21 and
   1 of 32 at 60 s). The 184 undecided maps are almost all of the slow kind.
4. So the hard tail has never been measured: no cap above 300 s was tried, the cap bound 66 of 80 tranche units,
   and the interim note "new exact method rather than longer caps" (`ROADMAP.md:73`) has no evidence behind it.
5. The four explore pilots of the week (E-261103-04, -05 target, -06, E-261107-01) gave no target signal. They were
   cheap in compute, but E-261103-04 was very expensive in text (§8).
6. **Compute is not the binding constraint.** All S5 runs since 2026-11-03 total about 3 core-h; the laptop offers
   about 80 core-h a night. The binding constraint is session time spent on documentation.
7. **Recommendation, first item:** an E-261103-03 stratified long-cap pilot (12 hard maps at 1800 s, 13 fast-pattern
   maps at 60 s, a nine-face positive control). Owner launch, 1-2 h wall, at most 15 core-h.
8. Its outcome picks the next step: a full (9, 3) night (one night can decide the rest), or one exact speed-up
   pilot, or "cannot tell" for the hard classes.
9. **Audit (§8):** the S5 literature check that `STRATEGY.md:18` puts before any compute was never done. The
   nine-face embedding formula has never returned SAT on any input (no positive control at F = 9).
10. **Credences (§9):** (9, 3) moves from 0.40 / 0.35 / 0.25 to 0.35 / 0.40 / 0.25 (the C3 ansatz is used up);
    the other tables are unchanged.

## 2. Week plan (ready to paste into `ROADMAP.md`, replacing the interim block)

```
## Week plan (lead review 2026-11-08, reviews/strategy-review-2026-11-08.md; replaced by the next lead review)

Lab sessions take these in order (PROTOCOL.md §8b). Anything outside a follow-up tree goes to "For the lead".
Laptop: at most 10 cores in total; item 1 uses 8 workers, so items 2-3 may run beside it on at most 2 cores.

1. **E-261103-03 stratified long-cap pilot** (exploit). Question: do the slow (9,3) plain formulas finish
   with longer caps, and does the pattern stratification hold? Prep (one lab session): one amendment of
   at most 15 lines; the runner's solver/checker caps as parameters; units (a) the 13 unattempted maps with
   patterns (1,1,1,3) and (1,2,3), solver 60 s / checker 120 s; (b) 12 unresolved maps, the lowest indices
   of each class: 5 of pattern (1^6), 5 of (1^4,2), 2 of (1,1,2,2)/(2,3); solver 1800 s, checker at most
   2700 s; time to solve recorded; (c) **positive control at F = 9**: one E-261107-01 Phase B solid
   (exact check first), its own map through the `submap=True` path with its planes pinned: SAT required.
   Then an owner launch (8 workers, 1-2 h wall, at most 15 core-h; the bounded startup check of PROTOCOL §8
   first). Predictions: (a) at least 10/13 UNSAT-VERIFIED; (b) has no prediction, it measures.
   Kill: control (c) fails -> stop, escalate (the 0-SAT record would be void). Follow-up tree:
   * any SAT -> stop dispatch; check the model exactly, run the saved-OM realizer (E-261103-04 path),
     `verify_candidate.py --target S5`, `candidate-check`; if it does not realize: one final-polynomial
     attempt (at most 1 session);
   * (b) >= 8/12 decided -> item 5a; 3-7/12 -> item 5a for the classes with >= 3/5 decided, item 5b for the
     rest; <= 2/12 -> item 5b only;
   * (a) < 7/13 -> drop item 3 (the pattern observation failed).
2. **S5 literature check** (no compute, one session; literature-researcher subagent only with the owner's
   consent). Question: is any (8,2), (9,3), (10,4) maximal face-neighbourly polyhedron, or a non-existence
   result, published or claimed? Sources: Roest-Vigh 2026, Mizhaev 2026, Bokowski-H. 2025, the Szilassi
   and Grünbaum-Szilassi papers, arXiv and MathOverflow searches. Kill: two sessions. Outcome goes to
   E-261101-22 and the STATUS §6 sources line; a published (9,3) object or proof -> escalate (focus question).
3. **Concentrated-multiplicity core study** (explore, new idea from this review §7.1). Question: does the
   fast UNSAT of maps whose extra segments meet at one face have a local cause on few faces? Test:
   face-grouped minimal cores of the saved plain formulas of the 13 fast maps (patterns (1,2,3), (2,2,2),
   (1,1,1,3)), plus item 1(a)'s new ones; at most 1 session + 1 core-h. Kill: no core on <= 6 of the 9
   faces in >= 3 maps -> park. Follow-up tree: pass -> a PROVED-1 lemma draft (at most 1 session) and an
   exact count of the (10,4) maps it would exclude (minutes).
4. **Arrangement-source sweep for solid-first** (explore; I-261103-04 with the 36-pair trigger fixed, plus
   C2 arrangements). The E-261107-01 engine unchanged; 300 arrangements: 100 Roest-Vigh planes + a random
   ninth plane, 100 Mizhaev + ninth, 100 random arrangements with an involution; cap 60 s per unit; at most
   2 core-h, one shard; after item 1 finishes or on <= 2 cores beside it. Power: 0/300 bounds the density of
   36-pair solids from these sources below 1 % (95 %). Kill: no 36-pair solid -> park arrangement-first for
   (9,3) with that bound. Follow-up tree: a 36-pair solid -> `verify_candidate.py --target S5` +
   `candidate-check`; best Phase B >= 34 pairs -> 1000 more arrangements from the same source (<= 5 core-h).
5. **Conditional on item 1.** (5a) One owner night: every remaining unresolved (9,3) map of the selected
   classes, fast patterns first, solver 1800 s, checker separate, ceiling 60 core-h, first-SAT stop, the
   control of 1(c) in every shard (`overnight-run-script`). (5b) Exact speed-up micro-benchmark: CaDiCaL
   default vs `--unsat`, kissat, and cube-and-conquer with cubes on the segment variables of the three
   doubled pairs; calibration maps 30, 40, 48, 19 (known UNSAT, 30-76 s) + 2 slow (1^6) maps at 1800 s;
   at most 1 session + 4 core-h. Kill: no variant >= 3x faster on the calibration maps and no slow map
   decided -> escalate ("cannot tell" for the hard classes). Follow-up tree: 5a decides every map UNSAT ->
   the (10,4) cost probe (10 maps of mixed patterns at 300 s, at most 1 core-h) and escalate for the note.
```

The quota: items 3 and 4 are explore runs and items 1 and 5 are exploit runs, so the share is about one in two
(`STRATEGY.md` §2). Item 2 is reading. The order of execution can interleave: item 1 prep, launch; items 2-3 during
the run; item 4 after it; item 5 on its outcome.

## 3. Evidence since 2026-11-04 and the strategy verdict

| Experiment | What happened | Label | What it changes |
|---|---|---|---|
| E-261103-03 (3e-3i) | 8/8 uniform free-C3 UNSAT-VERIFIED; plain: 19 UNSAT-VERIFIED, 73 TIMEOUT (60-300 s), 0 SAT | EXACT formulas; geometric reading PROVED-1 conditional | C3 ansatz used up; the exact route works but has a slow tail |
| E-261103-05 (3g) | disk-aware solid-first recovers both (8,3) objects from their own planes and Roest-Vigh from random D2 planes (seed 4 of 5) | EXACT | the engine is calibrated at 8 planes |
| E-261107-01 (3t) | 30 nine-plane arrangements, all INFEASIBLE in 6-21 s; best Phase B 32 pairs | EXACT per arrangement | at 9 planes the engine costs ~13 s per exact decision; 0/30 bounds the density only below ~10 % |
| E-261103-04 (3j-3s) | hinge ladder fails both (8,3) controls; saved-OM models of intermediates realize in seconds | EXACT / PROVED-1 | ladder parked; the realizer is a useful tool for a future SAT model |
| E-261103-06 (3u) | embedded-first R1 blocked by local mesh folds after 3-6 steps | EXACT, instance scope | UNDERPOWERED; parked |

**Verdict.** The evidence supports the focus. It does not support two working assumptions. First, "compute is
scarce" (`STRATEGY.md:27`): about 3 core-h of runs in five days, against ~80 core-h a night. Second, "the hard tail
needs a new method" (`ROADMAP.md:73`): see §3.1. The jump-first stance holds: every jump engine was killed cheaply
at pilot size, which is how the stance is meant to work. **What would change the strategy:** a SAT model or an S5
PASS (the realization stage, then the stretch from the same method); every (9,3) map decided UNSAT (the note,
then (10,4) by the S5 rule, after the (10,4) cost probe); the hard classes still unresolved at 1800 s and no 3x
speed-up in 5b (then (9,3) becomes "cannot tell" by exact means; consider a constructive-only campaign on the
slow-pattern maps, or an owner decision on the target); a published (9,3) result (item 2).

### 3.1 The (9,3) runtime structure (new, this review)

Patterns from `maps_9_3.json`. Excess = extra edges at a face (degree - 8); multiplicity per extra pair. Outcomes
are the plain cells of E-261103-03 (STATUS 3e-3i). Reproduce with the script named above.

| Face-excess pattern | Pair multiplicities | Shape of the extra adjacencies | Solved (<= 76 s) | Unresolved | Unattempted |
|---|---|---|---:|---:|---:|
| (1,1,1,1,1,1) | 2,2,2 | three disjoint doubled pairs | 0 | 21 | 12 |
| (1,1,1,1,2) | 2,2,2 | two doubled pairs share a face | 1 | 31 | 63 |
| (1,1,2,2) | 2,2,2 | a path of three doubled pairs | 4 | 13 | 23 |
| (1,1,2,2) | 2,3 | tripled pair, disjoint doubled pair | 1 | 7 | 0 |
| (1,1,1,3) | 2,2,2 | one face in three doubled pairs | 2 | 1 | 11 |
| (1,2,3) | 2,3 | tripled pair and doubled pair sharing a face | 8 | 0 | 2 |
| (2,2,2) | 2,2,2 | triangle of doubled pairs | 3 | 0 | 0 |

* **EXACT** (counts): the table itself; 18 admissible maps have a tripled pair (not 10, §8 M1).
* **NUMERICAL** (runtime observation): a face carrying three extra segments, or a triangle of doubled pairs, gives a
  fast UNSAT (13 of 14). Spread-out doubled pairs give the slow formulas (1 of 53 attempted in the first two rows).
  No solve below 22 s anywhere, and none of the 19 solved maps needed more than 76 s.
* **Consequence.** The fast classes are nearly exhausted (13 unattempted). A parametric fit to the pooled data
  (median ~130 s; it projects ~10 core-h for everything) is invalid: it is driven by the fast classes. The slow
  classes have no measured solve time at all, which is why item 1 measures them before any night.
* **Untested hypothesis (not evidence):** the Roest-Vigh (8,3) map also has spread-out doubled pairs (each face in
  exactly two). If a (9,3) object exists, it is more likely on a slow-pattern map. So the slow formulas may also be
  where a SAT model is, and item 1 is also the cheapest construction attempt.

## 4. Answers to "For the lead" (`CONTINUE_PROMPT.md:21-24`)

1. *Nine-plane engine is cheap; coverage is limited by the arrangement source.* Agreed (EXACT timings, 3t). Fund one
   sweep with a density kill (week item 4), not longer caps. Fixed: the I-261103-04 trigger (36 pairs plus E = 39
   and genus 3, not "above 36"). Three sources are named so that a hit identifies its source.
2. *Fund a repaired flattening for embedded-first?* **No, not this week.** R1 is a rung every engine passes. The
   failure (local folds at ring <= 1) is a mesh-engineering problem: tangential regularisation, IPC-type contact and
   remeshing are several sessions with T = 1. Nothing suggests that a working flattening scales from (7,1) to
   (9,3). Keep it parked with its failure mode. Reopen it only if a library (for example an IPC toolkit) makes the
   repair a one-session job, or if the exact route and the arrangement sweep both fail. Record the j = 4
   start defect in the README; do not fix it.

## 5. Re-scored candidates

Inventory (`map/graph.json` at the cut): 94 open ideas, 26 open hypotheses, 20 planned experiments, 1 running.
Since 11-04, E-261103-04/-05/-06 and E-261107-01 have closed. Scores follow the ROADMAP 0-2 definitions under the
focus. J = 2: reaches (9,3) without a ladder; 0: a ladder step; "-": supporting work. Kill cost: s = session,
h = core-h. Rows not listed in 5.1 were re-scored and are **unchanged** from `reviews/strategy-review-2026-11-04.md`
§6, because no evidence since bears on them (5.2).

### 5.1 Focus candidates whose score or disposition changes, plus the week items

| ID | Candidate | T D F G R | J | Kill cost | Disposition |
|---|---|---|---|---|---|
| E-261103-03 | stratified long-cap pilot, then the remaining (9,3) maps | 2 2 2 1 2 | 2 | prep 1s + <= 15h | **Week 1 (first)** |
| new (§7.1) | concentrated-multiplicity core study / lemma | 2 1 2 2 2 | - | 1s + 1h | Week 3, explore |
| I-261103-04 + E-261107-01 | arrangement-source sweep, 300 arrangements | 1 2 2 1 2 | 2 | 1s + 2h | Week 4, explore |
| E-261101-22 (S5 form) | literature: is (8,2)-(10,4) published? | 1 2 2 1 1 | - | 1s | Week 2 (was demoted; the S5 part is a prerequisite of any note) |
| I-261031-02 | cube-and-conquer, cubes on the doubled-pair segment variables | 2 2 1 2 2 | 2 | 1s + 4h | Week 5b, conditional (D 1 -> 2: the 60-s gate failed for the slow classes) |
| I-261029-43 | symmetry breaking (21 unresolved maps have Aut+ >= 2) | 2 1 2 1 2 | - | 0.5h | Backlog: lex-leader clauses break plain DRAT; needs certified (VeriPB) breaking (§7.4) |
| E-261103-07 | (10,4) preparation | 1 2 2 2 2 | - | 1h | Follow-up of 5a only: a cost probe, no census |
| H-261103-02 | C3 object on a free-C3 map | 2 0 2 1 2 | 2 | 0 | **Consumed:** 8/8 uniform formulas UNSAT; status -> weakened (§8 M2) |
| I-261103-03, I-261103-06 | interval B&B of the C3 ansatz; Z3 fundamental piece | 2 0 0 1 1; 2 0 1 1 2 | 2 | - | Below gate: C3 used up (only the coverage proof is open) |
| E-261103-06, I-261103-01, I-261103-05, I-261029-05 | embedded-first, spectral start, planarization flow | 1 1 1 2 1 | 2 | >= 2s | Below gate (D 2 -> 1): R1 blocked; §4 answer 2 |
| E-261101-06 / I-261030-29 | rank-3 relaxation in S5 form | 2 1 1 2 2 | - | 1s + 0.5h | Backlog; a 5b alternative if cubes fail |
| I-261029-12 | local-search SAT (probSAT / yalsat) on the slow maps | 1 1 2 1 2 | 2 | 0.5h | Below gate; a failure says nothing |
| I-261029-57, I-261030-32, I-261029-45, I-261029-11, I-261029-35 | realizability branch | 2 2 2 2 2 | 2 | 1h on a model | Conditional on the first SAT model (item 1 tree) |
| E-261101-09, I-261031-03, I-261029-47 | encoder agreement / ground truth | 2 2 1 2 2 | - | 1s + 0.25h | Audit backlog; polyhedraproof has no multi-adjacency; one session before any note |
| E-261101-11, I-261101-06 | external human review | 2 2 1 2 2 | - | owner | Parked by the owner (2026-11-07); a (9,3) note would need it (owner's decision) |
| H-261101-07, E-261101-12, I-261101-07 | maximal face-neighbourly polyhedra exist (umbrella) | 2 2 2 2 2 | 2 | via item 1 | Queue umbrella; no separate run |

### 5.2 Unchanged (re-scored, same values and dispositions as the 11-04 review §6)

* Focus backlog, B or A: I-261029-02, -06, -08, -09, -10, -16, -19, -20, -21, -22, -24, -25, -28, -37, -39, -40,
  -46, -48, -50, -62; I-261030-01, -03, -07, -08, -10, -11, -14, -22, -23; I-261031-01; I-261101-04, -08, -12, -13,
  -17, -18, -20, -22; I-261103-02; E-261101-21; H-261101-02 (now feeds week item 3), H-261101-14.
* Consumed controls (C): I-261029-23, I-261030-18, I-261030-31.
* Parked S0 / twelve-face S1 (P; listed separately, not dropped): E-261101-03, -04, -05, -08, -10, -14, -15, -16,
  -17, -18, -19, -20, -24; the S0 hypotheses H-261029-01 to -10 (open ones), H-261101-01, -03, -04, -05, -06, -08 to
  -13, -15 to -17; the S0-only ideas of the 11-04 §6.2 table. The low-cost S0 slot (E-261101-10, one session per
  two weeks) stays; it is not in this week's plan because the exact (9,3) decision needs those sessions.

## 6. Proposed queue (top items, in order)

| # | Item | Hypothesis | Cheapest falsifying test | Outcomes -> change | Budget / stop | Explore |
|---|---|---|---|---|---|---|
| **1** | **E-261103-03 stratified long-cap pilot** | the slow (9,3) formulas finish within 1800 s | 12 slow maps at 1800 s + F = 9 positive control | >= 8/12: night 5a decides (9,3); <= 2/12: 5b or "cannot tell"; SAT: realization | prep 1s; <= 15 core-h, 1-2 h wall; stop on control failure | no |
| 2 | S5 literature check | no (8,2)-(10,4) result is published | one session of targeted reads | published -> re-plan the focus; none -> a note would be new | 1-2 s, no compute | no |
| 3 | concentrated-multiplicity cores | the fast UNSAT has a local cause on few faces | grouped cores of the 13 fast formulas | pass: a lemma + (10,4) pruning; fail: park | 1s + 1h; stop: no small core in 3 maps | **yes** |
| 4 | arrangement-source sweep | 36-pair solids arise at density >= 1 % from RV/Mizhaev+1 or C2 sources | 300 arrangements at 60 s | hit: candidate-check; 0/300: arrangement-first parked with a bound | 1s + 2h | **yes** |
| 5 | 5a night or 5b speed-up | per item 1 | per item 1 | 5a: (9,3) decided or a model; 5b: a 3x method or "cannot tell" | 60 core-h / 1s + 4h | no |
| 6 | (10,4) cost probe | 11-element formulas are within ~10x of the 10-element ones | 10 mixed-pattern maps at 300 s | decides exact versus constructive for the stretch | <= 1h | no |
| 7 | E-261101-09 step 1 (predicate equality) before any note | our predicates agree with an independent implementation | shared instances | mismatch stops dependent claims | 1s + 0.25h | no |
| 8 | E-261101-10 FD6 write-up | - | - | S0 low-cost slot | 1s per two weeks | no |

**First item: 1**, the prep session. Its outcome dominates every other choice in the table.

## 7. Missing ideas (untested proposals, not evidence)

1. **Line-order obstruction for concentrated multiplicities** (discrete geometry + proof mining). Faces a, b with a
   tripled pair share three segments of the line h_a ∩ h_b. Each segment endpoint is a vertex (a, b, c) with c
   fixed by the map, so the order of those points along the line is a rank-2 restriction of the chirotope. When
   several multiple pairs share a face, these orders interact. Why: this may explain §3.1 in human-readable form.
   Cheapest test: week item 3's grouped cores, then a brute-force check (7! orders per line) on the 203 maps.
   Controls: the two (8,3) maps must pass. It may turn out implied by weaker clauses and prune nothing new.
2. **A positive control at nine faces from solid-first by-products** (metamorphic testing). E-261107-01's Phase B
   solids are exact embedded 9-face solids with up to 32 adjacent pairs. Their maps through the `submap=True` path
   test the full embedding clauses at F = 9, where no SAT has ever been observed. Minutes. In week item 1(c).
3. **Structure-aware cubes** (SAT practice). Cube on the variables that place the segments of the three doubled pairs
   (their order and side along each shared line): 2^k cubes, k <= 6, each with its own DRAT. A cube cover is a
   tautology, so the proofs compose without a new soundness argument. Cheapest test: week item 5b.
4. **Certified symmetry breaking for the Aut+ >= 2 maps** (Bogaerts-Gocht-McCreesh-Nordström 2022, VeriPB).
   21 unresolved maps have a map automorphism. Lex-leader clauses could shorten their proofs, but plain DRAT cannot
   certify them; VeriPB can. Cheapest test: 2 maps with BreakID clauses, timing only (0.5 core-h). Certify only after
   a >= 3x gain.
5. **The slow formulas as the construction target** (§3.1 hypothesis). Run a SAT-oriented arm (`cadical --sat`
   configuration, or kissat) beside the UNSAT-oriented one on the 33 (1^6) maps. A model is the first target model;
   a failure means nothing. Cheapest test: as a portfolio arm inside 5b, ~1 core-h.

## 8. Audit findings

Locations are relative to `research/12-faced-polyhedron/`. These are proposed corrections for a working session;
this review edits none of these files.

| Priority / location | Finding | Proposed fix |
|---|---|---|
| H1 `ROADMAP.md:73` | "Needs a new exact method rather than longer caps": no cap above 300 s was ever tried; the cap bound 66/80 tranche units; the slow classes are a different population (§3.1). The row's own stop rule (`ROADMAP.md:89`, "median SAT time above ~1 h per map") was never tested | replace with week item 1 |
| H2 `STRATEGY.md:18-19`; `SPEC.md` S5 row | "First step before any compute: the literature check": after five days of S5 compute it has not been done (E-261101-22 demoted, `ROADMAP.md` S0 queue). A (9,3) note, positive or negative, cannot be written without it | week item 2 |
| H3 `experiments/E-261103-03-.../pilot.py:327-332` | The nine-plane control is `defs_only` (definitions + GP, pinned): SAT. The full embedding formula at F = 9 has never returned SAT on any input. With 0 SAT in all target formulas and 30/30 INFEASIBLE solid-first runs, that is a constant diagnostic (`CLAUDE.md` rule, review 11-01 §5.1) | week item 1(c) before any night |
| M1 `STATUS.md:171`; `SPEC.md:106` | "Ten admissible (9,3) maps have a tripled pair": the exact census has **18** (10 with the doubled pair sharing a face, 8 with it disjoint), EXACT recount by the script of this review; the 11-03 review counted only the first kind | wording fix |
| M2 `hypotheses/H-261103-02-...md:4`; `STRATEGY.md:13-14` | Status still `open` after 8/8 uniform free-C3 UNSAT-VERIFIED plus a conditional coverage draft; the strategy still calls C3 the natural first ansatz | status `weakened` (conditional PROVED-1); the owner may update the strategy line |
| M3 `experiments/E-261103-04-.../PLAN.md` (868 lines), `CONCLUSION.md` (794 lines) | 24 commits, ~1,840 lines of Markdown and ~2,320 of Python since 11-04 for ~0.5 core-h of recorded runs; ten bounded audits (STATUS 3j-3s) in a row before a gate decision, on an explore item with J = 0 | no action beyond compaction; PROTOCOL §8b (at most two amendments) now covers it |
| M4 `STATUS.md:3-17`, sections 3d-3s | "As of 2026-11-05" while sections run to 11-07; the header grows like a change log; sections 3d-3s (~400 lines) are far over the 8-line budget, and every session reads them | one wording-only compaction: one section per experiment, numbers once, links to CONCLUSION |
| M5 `ROADMAP.md:89`; `experiments/E-261103-03-.../README.md:5` | State `running` with no process for four days | state `open` |
| M6 `experiments/E-261107-01-.../CONCLUSION.md:24` | "Configuration parked" at 0/30: the power covers only densities of ~10 % or more (95 %); at 8 planes the D2 density was 1 in 5 | call it UNDERPOWERED below 10 %; week item 4 tests it with power |
| L1 `ROADMAP.md:92`; `map/index.html:95-96` | E-261103-06 is `killed` (shown as "failed") while its CONCLUSION says UNDERPOWERED and parked | add a `parked` ROADMAP state (the map already has it) |
| L2 `ROADMAP.md:189` | The (9,3) credence evidence line is stale ("203 admissible maps (many tickets)") | the line in §9 |
| L3 `experiments/E-261103-07-.../README.md` | The stop rule still asks for the finished census (flagged on 11-04, still open) | make it the (10,4) cost probe |

**Process cost.** In five days the S5 lab spent ~3 core-h and produced ~3,000 lines of PLAN/CONCLUSION text, plus
~25 STATUS sections. The 11-07 budgets fix the rate going forward. The remaining cost is reading: `STATUS.md` (640
lines) is read by every session. **Underpowered verdicts:** M6; the E-261103-03 tranche "LOW-YIELD" (`STATUS.md:288`)
is right in form but was read as "longer caps are pointless" (H1). **Claims stronger than evidence:** H1 and M1 only;
the experiment CONCLUSIONs scope their claims correctly. **Follow-up chains to stop:** E-261103-04 (no more
hinge/ladder audits); embedded-first repair (§4); all C3-only work (I-261103-03, I-261103-06, a nonuniform C3
encoder); any (8,2) work; S0 nights.

## 9. Scenario credences (subjective planning weights, not evidence)

| Case | exists / does not / cannot tell | Change | One line of evidence |
|---|---|---|---|
| (9, 3) | **0.35 / 0.40 / 0.25** | -0.05 / +0.05 / 0 | the strategy's named first ansatz (free C3) is UNSAT on all 8 maps (EXACT formulas, conditional coverage PROVED-1); 19 plain UNSAT and 0 SAT, but on a biased (fast-pattern) subset, so little weight |
| (8, 2) | 0 / 1 / 0, conditional | unchanged | the conditions (census coverage, encoder soundness, PROVED-1) stay attached |
| (10, 4) | 0.30 / 0.30 / 0.40 | unchanged | no (10,4) evidence; item 6 measures the exact cost |
| S0 A / B / C | 0.20 / 0.55 / 0.25 | unchanged | no S0 evidence since 11-01 |

Reversal conditions: item 1 at <= 2/12 together with 5b failing moves (9,3) "cannot tell" to ~0.35. A SAT model moves
"exists" up only after realization; a model that does not realize moves nothing until a final polynomial excludes it.

## 10. Three things to do first

1. Approve the week plan (§2); a working session pastes it into `ROADMAP.md` and applies the wording fixes M1, M2,
   M5 and L1-L3 (no checks needed beyond the diff and links).
2. A lab session prepares week item 1: the amendment, the cap parameters, the F = 9 positive control and the
   bounded startup check. The owner launches it on 8 workers (1-2 h).
3. Meanwhile, week item 2 (literature, no compute). Then item 3 on <= 2 cores. Item 5 follows from item 1's count.
