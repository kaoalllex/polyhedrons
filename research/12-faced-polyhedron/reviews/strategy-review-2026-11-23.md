# Strategy review, 2026-11-23 (cycle step 1, draft): P6 is spent at genus 4; nine faces keeps two cheap gates, the full (8, 3) rung first

Inputs: `STRATEGY.md`, `STATUS.md` 3bk-3bn, `ROADMAP.md`, `SPEC.md`, `PROTOCOL.md` §2, §8, E-261117-04 and E-261119-02 conclusions, 2026-11-22 reviews, `map/graph.json`, the handover. K1, K2 (§9): session checks; prices and credences: planning judgments.

## Owner digest
1. **Verdict.** P6, the main line, is spent at genus 4: all 1071 admissible equivelar (9, 4) plain formulas are UNSAT-SOLVER (3bn), after the same pipeline recovered both known (8, 3) solids unaided (3bk). With the symmetric route closed last week, nine faces has no main line left on the laptop. Recommendation: keep nine faces first for one more week behind two cheap gates; if both close, parking it is your call (line 8).
2. **Why gates, not a sweep.** The only genus-4 maps never run are the non-equivelar ones, and their full census is out of reach (order 10^7 classes, >= 1000 core-h; K1 extrapolation, CONJECTURE). A slice of it earns a night only if the rung below shows realizable maps outside the equivelar slice. Nobody has checked: stage A ran 796 (8, 3) maps of an estimated 30-48 thousand admissible ones.
3. **First item (new): the full (8, 3) census and plain pass.** Priced in this session: the census costs ~1.7-2.6 core-h (K1: 214155 classes, 19745 admissible from 64 % of the inputs in 9 min), a formula ~0.3 s (K2: 240 random asymmetric non-equivelar maps, all UNSAT-SOLVER, max 1.1 s). About 4-13 core-h in total, in lab jobs of <= 50 min.
4. **What it decides.** Realizable non-equivelar (8, 3) maps exist -> that stratum is priced at (9, 4); none -> non-equivelar genus 4 has no rung and stays closed. It also yields either a complete classification of cubic eight-face face-neighbourly polyhedra at formula scope ("only Roest-Vigh's and Mizhaev's", a paper item) or a third eight-face object (~0.05, CONJECTURE).
5. **Step 0 of item 1 (minutes): a missing control.** ~111 thousand nine-face formulas are UNSAT-SOLVER, and no SAT control at 10 elements has doubled pairs (f9 is a convex genus-0 solid). Cut one convex vertex of Roest-Vigh's solid with a ninth plane: a genus-3 nine-face polyhedron with eight doubled pairs. Its plain formula must come out SAT unaided; if not, every nine-face UNSAT-SOLVER is suspect.
6. **Second item (explore, jump): P3 with face-label symmetry breaking.** The census-free formula failed on refutation power (3aw, 3bd), and its 8! / 9! relabelling symmetry was never broken (its gauge fixes orientations only). Kill test: the known negatives (8, 30) and (9, 39) INFEASIBLE within 1 h; a pass lets the lead price (9, 45) without any census.
7. **Approvals now:** (O1) the `STRATEGY.md` §1 text in §2; (O2) the nine-face credence 0.35 -> 0.28 (the 2026-11-22 draft forecast ~0.28 for this outcome); (O3) one-line permissions for items 1 and 2.
8. **Decisions later:** (O4) if item 1 leaves only the known maps: does the eight-face classification earn the note path (checked proofs, priced in 10 min, likely one night; L6 at k = 5, 6)? Default no. (O5) if both gates close: park nine faces and consolidate, or run the C2 (9, 5) remainder (~122 core-h, two nights, ~0.04)?
9. **Not recommended:** plain formulas on the 12562 symmetric (9, 4) maps (at (8, 3) plain SAT never left symmetric SAT), equivelar genus 7 (census out of reach, Cayley slice empty), nine-plane sampling, parity before the paper.
10. **The week was lean:** 7 commits, 6.7 core-h of new compute, predictions P1-P12 held. The audit finds two ledger slips (H-261101-07 not marked weakened as approved; E-261117-04 carries the `tests:` mislink removed last week) and 30 duplicate control files.

## 1. Week plan (for `ROADMAP.md`; replaces the 2026-11-22 plan; branch `lab/2026-11-23`, created after `lab/2026-11-22` merges)
Rules as before: <= 10 cores, 8-10 shards, no proofs, PLAN and tests before compute, UNSAT = UNSAT-SOLVER; jobs <= 50 min wall the lab launches after a
one-line permission, longer ones the owner; elapsed budget and stop reason in every manifest; success only `--all-pairs` PASS, then `candidate-check`.
1. **Full (8, 3) classification at formula scope** (new E-261123-01, PLAN first; J 0, the rung for any non-equivelar (9, 4) stratum; 2 2 2 2 2).
   * Step 0, the 10-element power control (minutes): Roest-Vigh's solid (`code/control_rost_vigh.py`) with one of its four convex vertices
     (I-261101-20) cut by a ninth plane; `verify_candidate.py` EMBEDDED, (V, E, F, chi) = (26, 39, 9, -4); its plain sub-map formula at 10
     elements, unpinned, by stage C's path must be SAT and bridge-realized; the same for Mizhaev's solid. A failure stops the item -> lead.
   * Census: all 1806 inputs of `census.extra_graphs(8, 8)` through `census.run` in input-slice units (`p6.py census-b` generalised, a completion
     flag per input). Controls: stage A's 97 equivelar classes record for record, the 790 free-C2 codes, the six face-transitive classes (3au), the
     (8, 2) census (2 classes) by the same path. Lean: admissible records committed if <= 20 MB, else SHA-256 only. Expected ~330-520 thousand
     classes, ~30-48 thousand admissible (K1, NUMERICAL).
   * Formulas: every admissible class not decided in stage A; plain, 9 elements, code orientation, kissat cap 60 s, lean, 10 shards; a chunk 0
     stratified by extra-edge degree sequence (~2000) prices the rest. Each SAT: bridge, 30 models if needed, `--all-pairs`.
   * Tree: step 0 fails -> lead. Only the two known maps SAT -> "every admissible cubic (8, 3) map other than Roest-Vigh's and Mizhaev's has an
     UNSAT-SOLVER plain formula" (formula scope, planning only) with the zero rate per stratum; non-equivelar (9, 4) closed for the laptop; O4.
     Another map SAT and realized -> `candidate-check`, escalate (O4 of 2026-11-22; reopens E-261112-02 Stage B); if non-equivelar, a <= 10 min
     census probe of the matching (9, 4) degree pattern, priced for the lead. SAT unrealized after 30 models -> open, lead. UNKNOWN -> 600 s pass.
   * Budget: census <= 4 core-h, formulas <= 12 core-h; lab jobs <= 50 min wall, otherwise an owner day run.
   * Lab: Opus, high / Codex gpt-6-astra, high (a census path whose coverage decides the claim; a new eight-face object is possible).
2. **Census-free formula with face-label symmetry breaking, refutation rung** (new E-261123-02 from E-261116-07, whose parked rule asks for "a
   changed search measured first", `ROADMAP.md`:323; explore, J 2 through the tree; 1 2 2 2 2).
   * `p3.py` (CP-SAT) plus static label breaking: faces ordered by size, then the multiplicity matrix lex-<= its image under each adjacent
     transposition (Codish, Miller, Prosser, Stuckey 2013: every orbit's lex-leader satisfies them); soundness with the sign gauge and mirror fix
     PROVED-1 in the PLAN. Tests: (7, 21) still finds the K7 torus; both known (8, 36) chirotopes, relabelled to their lex-leader, satisfy it pinned.
   * Rungs: (8, 30) and (9, 39) must be INFEASIBLE (decided negatives, 3d), paired with the same cubes and caps without the breaking; then (8, 36):
     both known maps unaided, then INFEASIBLE with both blocked (compare item 1).
   * Kill: (8, 30) not INFEASIBLE within 1 h on 8 workers -> P3 parked for nine faces, failure mode recorded. Both INFEASIBLE -> the lead prices
     (9, 45); no night without that price. A model at (8, 30) or (9, 39) -> encoding bug, one repair.
   * Budget: 1 prep session + <= 3 core-h. Lab: Opus, high / Codex gpt-6-astra, high (a new encoding whose soundness decides every INFEASIBLE).
3. **Conditional, O4** (only if item 1 leaves the two known maps and the owner asks): a checked replay priced on 200 random admissible (8, 3)
   formulas (proof sizes, drat-trim time, <= 10 min); the full replay one owner night if it fits. Lab: Sonnet, medium / Codex gpt-6.1-sol, medium.
4. **Ledger fixes** (no compute, with item 1's conclusion): H-261101-07 -> weakened (genera 2-3, formula scope; final 2026-11-22 point 13);
   E-261117-04 `tests:` emptied; a nine-face hypothesis file (credence 0.28) for the nine-face links; one copy per queue of each shard-identical
   control file, plus hashes. Lab: Sonnet, medium / Codex gpt-6.1-sol, medium.

Deferred: the C2 (9, 5) remainder (O5), parity (paper), plain formulas on the symmetric (9, 4) maps, C3 at (9, 6), E-261116-08, P4, I-261117-03,
curved faces, the deletion sieve, E-261101-08, the (10, 4) replay. Parked: P3-sym for nine faces (3bd). Closed for the laptop: (11, 5),
face-transitive nine faces (genus 4, 7), C2 at genus >= 6, the equivelar (9, 4) slice (3bn), equivelar genus 7.

## 2. Answers
* **Verdict.** `STRATEGY.md` §1 made P6 the main line; its pre-registered all-UNSAT-SOLVER branch fired (`ROADMAP.md`:152-153). The evidence
  supports the target, not a main line: on the analogous slice the SAT rate fell from 2 of 51 at (8, 3) to 0 of 1071 at (9, 4) (95 % bound
  0.28 %, >= 14 times lower), 0 of 12562 on the symmetric lists (NUMERICAL, formula scope). It changes on step 0 failing, a new (8, 3) map,
  item 2 passing, or any nine-face SAT.
* **For the lead 1 (60 s cap nearly bound, max 54.9 s):** no plan reuses these formulas at a lower cap; a replay for a note would run at
  >= 120 s with its own price, and none is proposed (no claim named).
* **For the lead 2 (non-equivelar (9, 4) maps never run):** correct, and out of reach as a whole. K1 puts the equivelar share at (8, 3) at 97 in
  ~330-520 thousand (2-3e-4); with 4118 equivelar (9, 4) classes that is ~1.4-2e7 classes, >= 4e5 admissible even at 3 %, >= 1200 core-h at
  11 s (CONJECTURE, order of magnitude). Only a stratum with a rung reason (item 1) or a census-free formula (item 2) can reach them.
* **Proposed `STRATEGY.md` §1 "First" (not applied):** "**First (owner, 2026-11-16b, confirmed 2026-11-17, -18, -19, -22 and -23): S1, nine
  mutually adjacent faces with the genus free.** The symmetric route ends at genus 4 on the laptop (2026-11-22) and P6 at the equivelar slice
  (all 1071 admissible equivelar (9, 4) plain formulas UNSAT-SOLVER, E-261117-04). Two gates decide whether nine faces keeps a laptop route:
  the full (8, 3) rung (E-261123-01; a SAT map outside the equivelar slice opens that stratum at (9, 4), otherwise non-equivelar (9, 4) maps are
  not run) and the census-free refutation rung (E-261123-02; the known negatives (8, 30) and (9, 39) INFEASIBLE before any (9, 45) run). If
  both close, the owner chooses between parking nine faces and the C2 (9, 5) remainder. P3-sym parked; mirror families only by plain formulas
  (L1); no nine-plane sampling night without a rung-below rate. Success is only `verify_candidate.py FILE --all-pairs` PASS with nine faces,
  then `candidate-check`." Log: "2026-11-23 (owner's approval of `reviews/strategy-review-2026-11-23-final.md`): nine faces stay first behind
  two gates; P6 ends at the equivelar slice; credence 0.35 -> 0.28. Stance, S0 parking and the side track unchanged."

## 3. Scores (T D F G R; J = jump; cost to the first result that could park it)
| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, full (8, 3) classification (E-261123-01) | 2 2 2 2 2 | 0 | step 0 minutes; census ~2 core-h | first; gate of every non-equivelar (9, 4) stratum |
| Item 1 step 0, truncated-solid control (N2) | 2 2 2 1 2 | 0 | minutes | power of every 10-element UNSAT-SOLVER |
| Item 2, P3 + label symmetry breaking (E-261123-02, N1) | 1 2 2 2 2 | 2 (tree) | 1 session + 1 h on (8, 30) | explore; replaces P3-sym (0 1 1 1 2, parked 3bd) |
| (9, 4) stratum of a non-equivelar (8, 3) SAT map (N4) | 1 2 2 1 2 | 2 | 10 min census probe | only after item 1 realizes one |
| (8, 3) checked replay (N3); L6 at k = 5, 6 (I-261108-09) | 1 2 2 2 2; 1 1 2 2 2 | 0 | 10 min price; 1 session | owner O4; the note only |
| C2 (9, 5) remainder, chunks 10-99 | 1 1 2 0 2 | 2 | ~122 core-h | postponed (owner); O5 |
| Plain formulas on the 12562 symmetric (9, 4) maps | 1 1 2 0 2 | 2 | ~38 core-h | on the 790 free-C2 (8, 3) maps plain SAT = the two known (3bk) |
| C3 3+3+3 at (9, 6); equivelar genus 7; face-transitive genus >= 10 | 1 1 2 1 2; 0 1 0 1 2; 0 1 2 0 2 | 2 | <= 2 core-h; out of reach; 1 session | below gate; close; close |
| E-261112-02 Stage B, H-261112-01 | 2 1 1 1 2 | 2 | 2 nights | reopens on a new (8, 3) map (item 1) |
| Parity pass (B5, B8); equivelar literature (E-261101-22) | 2 0 2 1 2; 1 1 2 1 1 | 0 | 2.9 core-h; 1 session | paper; no {10, 3} nine-face object in print so far (CLAIMED) |
| Curved faces, deletion sieve, I-261117-03, P4, I-261029-51, I-261116-06, nine-plane sampling, E-261101-08, N5 | as 2026-11-19; N5 1 1 2 1 2 | | | no new evidence |
Parked targets only (scores kept, no new evidence): S6 (H-261110-03, I-261119-01, E-261116-08, I-261116-05), S5 (I-261116-02), S0 (E-261101-03
to -24, H-261029-*, H-261101-01 to -17 except -07, the 2026-10-29 to -11-03 ideas). H-261101-07: weakened (audit 2).

## 4. Queue (in order; first: item 1 step 0)
1. **Item 1 step 0.** H: the 10-element plain formula is SAT, unaided, on a realized genus-3 nine-face map with doubled pairs. Falsifier:
   UNSAT-SOLVER. SAT -> stage C's UNSAT-SOLVERs keep their reading; UNSAT -> encoder bug, every nine-face UNSAT-SOLVER suspended, lead. Minutes.
2. **Item 1, census and pass.** H: only the two known (8, 3) maps are SAT (~0.9, CONJECTURE). Falsifier: another SAT map. Outcomes: §1.
   Scenario move: only the known maps -> nine faces 0.28 -> 0.25; a realized non-equivelar map -> 0.33. <= 16 core-h; stop by its tree.
3. **Item 2 (explore).** H: label breaking gives P3 refutation power at (8, 30) within 1 h (~0.25, CONJECTURE). Falsifier: UNKNOWN at 1 h.
   Pass -> (9, 45) census-free priced, the only J 2 route at genus 4; fail -> P3 parked for nine faces. No credence move. <= 3 core-h.
4. **(9, 4) stratum** (explore, J 2), only if item 1 realizes a non-equivelar map: census probe <= 10 min, price, then the lead. **5. O4, the
   classification replay** (owner). **6. O5, the C2 (9, 5) remainder** (owner; ~0.04 to hold a SAT formula, CONJECTURE).

## 5. New ideas (untested proposals, not evidence)
* **N1. Label symmetry breaking for census-free formulas** (Codish et al., IJCAI 2013; SAT Modulo Symmetries, Kirchweger-Szeider 2021). P3 v2 and
  P3-sym never refuted a known negative (3aw: 48 of 48 cubes UNKNOWN; 3bd: (8, 30) UNKNOWN at 1 h); each labelled solution has up to 8! (9!) copies
  refuted one by one, and `p3.py` breaks only orientations (`E-261116-07/PLAN.md`:17-19). Test: item 2.
* **N2. An unaided positive control at every new element count, built from a known solid.** Truncating a convex vertex gives F + 1 faces, the
  same genus and the doubled pairs: a realized map whose formula must be SAT. Test: item 1 step 0; reuse it for any later element count.
* **N3. The eight-face classification note.** If item 1 leaves only the two known maps, "every face-neighbourly eight-face polyhedron with vertices
  of degree <= 4 and genus <= 3 has Roest-Vigh's or Mizhaev's map" needs a checked replay (formulas of ~0.3 s), (8, 2) (3d) and L6 (3bi): the
  strongest result in reach for the deferred note. Test: the 10-min replay price (item 3).
* **N4. A stratum transfer rule.** Price a non-equivelar (9, 4) stratum only for an extra-degree pattern holding a SAT (8, 3) map, and report each
  (8, 3) stratum's zero-rate bound (rule of three). Test: item 1's per-stratum table.
* **N5. Correction-set distance as a map-search heuristic** (MaxSAT minimal correction sets): rank UNSAT maps by the fewest face pairs to relax for
  SAT and try map moves from the closest. Test at (8, 3): are the known maps one move from low-distance maps? Below the gate until item 1.

## 6. Audit
1. **Missing power control at 10 elements.** About 111463 nine-face formulas (3bf, 3bm, 3bn) are UNSAT-SOLVER. The 10-element SAT controls are the
   convex genus-0 f9 (`E-261103-03/control_f9.json`:182) and convex runner controls; unaided SAT with handles exists at 9 elements (3bk) and with
   single adjacencies at 11 (3ah). The constant-diagnostic rule (`CLAUDE.md`; `strategy-review-2026-11-01.md` §5.1) asks for one. Fix: item 1 step 0.
2. **An approved change not applied, a mislink repeated.** Final 2026-11-22 point 13 (`strategy-review-2026-11-22-final.md`:40) made H-261101-07
   weakened at genera 2-3; the file still says open (`hypotheses/H-261101-07-maximal-face-neighbourly-exist.md`:5, :137, :144). `E-261117-04/README.md`:10
   lists `tests: [H-261101-07]`, but (8, 3), (9, 4) are not maximal (SPEC S5): last week's removed mislink. Fix: item 4.
3. **Text budget.** E-261117-04 amendment 2 runs 34 lines against 15 (`PLAN.md`:98-131; `PROTOCOL.md` §8b).
4. **Lean output.** Four control files are committed 30 times each, byte-identical (`E-261117-04/results/stageC_c*/*/attempt_*/controls/`, e.g.
   `nine_plane_control.model.json`, 7842 lines a copy). Fix: item 4.
5. **Prices.** The last review priced stage C at 5-31 core-h (3.43 used) and stage B at ~4 (3.1). Chunk-0 pricing worked (13753 projected,
   11479 used). Keep it.
6. **Cost, chains, claims.** 7 commits, code +960 / markdown +420 lines, 6.7 core-h new compute, two amendments, P1-P12 held. Stop: P6 beyond the
   equivelar slice, plain formulas on symmetric maps, P3-sym at nine faces. STATUS 3bk-3bn are scoped correctly; `E-261117-04/README.md`:25
   ("cannot show that Roest-Vigh and Mizhaev are alone") stays true until item 1.

## 7. Credences (CONJECTURE, planning weights)
* **Nine faces, genus >= 4: 0.35 -> 0.28.** The slice analogous to the only realizable (8, 3) one is empty at (9, 4) at formula scope (3bn), as is
  the symmetric genus-4 slice (3bf); if ~0.3 of the mass sat in the equivelar genus-4 slice, ~0.27 remains. The 2026-11-22 draft forecast ~0.28
  for this outcome (`strategy-review-2026-11-22.md`:101). Non-equivelar genus 4 and genus >= 5 are untouched.
* **Relaxed Szilassi-12, genus >= 7: 0.40 -> 0.25 (optional).** It exceeds nine faces with no data of its own (`ROADMAP.md`:355), while every
  measured rung above eight faces is negative at formula scope. The others are unchanged: no new datum.

## 8. Three things to do first
1. Owner: Codex cross-review (step 2), final version (step 3), O1-O3. 2. Lab (Opus, high / gpt-6-astra, high): item 1's PLAN, step 0, census and
pass, after a one-line permission (10 cores, <= 50 min a job). 3. Lab (same): item 2 and its (8, 30) rung; item 4 with item 1's conclusion.

## 9. Session checks (scripts and outputs in `strategy-review-2026-11-23-checks/`, ~1.15 core-h, commit 354e6f81)
* **K1** (`k1_full_census_8_3.py`: `census.run(8, 3)` on the 1806 inputs split mod 8, enumerator cap 330 s per process, 531 s wall, 4068 core-s):
  incomplete by design, 1159 of 1806 inputs; 214155 classes, 19745 admissible (Aut+ 1: 19409, 2: 319, larger: 17); controls partial as expected
  (25 of 97 equivelar, 321 of 790 free-C2). Projection ~330-520 thousand classes, ~30-48 thousand admissible (inputs done; free-C2 share). NUMERICAL.
* **K2** (`k2_plain_sample_8_3.py`: stage A's `tranche.submap_formula` at 9 elements, kissat 4.0.4, cap 60 s, 8 processes, 26 s wall): 240 random
  admissible trivial-Aut+ non-equivelar classes from K1 (seed 2611230201), 240 UNSAT-SOLVER, solve mean 0.30 s, median 0.24, max 1.12. Pass price
  30-48 thousand x 0.3-0.8 s (stage A's ledger: 0.78 s a unit) = 2.5-10.4 core-h. NUMERICAL.
