# Strategy review, 2026-11-18: no nine-face object this week; the census-free formula on symmetric quotients is next

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep nine faces first and keep the stance. Change the method: no more nine-plane sampling nights. Next: complete formulas on symmetric quotients, scored on the eight-face rung.
2. **Week:** five items done, 71.4 core-h, no candidate. N1: the slice is empty (EXACT). N2: the gate passed. P3: no eight-face model (UNDERPOWERED). P4 built Szilassi's type by construction (EXACT). The night gave 0 hits (p < ~9e-4 per decided arrangement).
3. **Session count (EXACT; the speed is a prediction):** under C3 the nine-face P3 formula has 72 chirotope orbits. Under D2 and S4 the eight-face formula has 36 and 34. P3 solved the seven-face formula, with 70 signs, in 8 s.
4. **Session lemma (PROVED-1 sketch, unreviewed):** D2 and S4, the symmetries of the eight-face objects, cannot act on nine faces. One C3 3+3+3 formula per E covers every nine-face solid with an order-3 rotation. The only other uniform families are a mirror with one fixed face and a half-turn with one fixed face (the latter in a moved chart).
5. **Approval 1: the week plan in §1.** First item: N1b, the five unrealized face-transitive (8, 3) maps (minutes). Main item: 2, P3-sym. Its D2 / S4 rung must return Roest-Vigh's and Mizhaev's objects unaided before the C3 nine-face run.
6. **Approval 2:** item 3, the (11, 5) plane-only price probe (<= 4 core-h). It is the last measurement that could earn (11, 5) a night.
7. **Approval 3 (yes / no):** nine-face credence 0.55 -> 0.45 (§7). The earlier unapplied proposals stand.
8. **Your raw ideas (§5):** the two ETH preprints (both real, read) and Degen's identity: drop. Neither gives anything for this problem.
9. **If item 2's rung fails and P6 prices above a night,** nine faces have no laptop route left. That is your decision: park the constructive focus or consolidate.
10. **Not done:** no target run, no human review. The lemma and the size estimate come from this session and are not ledger evidence.

## 1. Week plan (for `ROADMAP.md`; <= 10 cores, 8-10 shards, the owner launches every run, no proofs except item 4)

1. **N1b, the five unrealized face-transitive (8, 3) classes** (E-261117-01 by-product; exploit, J 0; new row, 2 1 2 1 2). Plain and normalised
   formulas at 9 elements, kissat, cap 600 s, 10 shards, <= 0.2 core-h. Controls: Roest-Vigh's class SAT, its planes on another class. Bridge on any SAT.
   * Kill: Roest-Vigh's class not SAT -> repair. Follow-up: realized, `--all-pairs` (eight faces) PASS -> `candidate-check`, escalate (a third
     eight-face object, a rung control for item 2). All UNSAT-SOLVER -> no follow-up. Lab: Opus, medium / Codex gpt-6.1-sol, medium (SAT: Opus, high / gpt-6-astra, high).
2. **P3-sym, the census-free formula on symmetric quotients** (new registration from E-261116-07, the stated change is equivariance; explore,
   J 2; the main investment). An opt-in plane action in `p3.Formula`: a permutation, orientations transported along orbits, and the det sign on
   chi. Cells and all derived variables follow the action; the default and the stage-A regression stay unchanged.
   * Controls: Roest-Vigh (D2) and Mizhaev (S4, improper) pinned SAT under their groups; one orbit's signs flipped INFEASIBLE; gauge reachability
     (orbit gauge or gauge off; check the C3 argument of §5 N2). Negative: Cs 3 x 2 + 1 at (7, 21) INFEASIBLE if the census marks (7, 1) chiral.
   * Rung (known answers, eight faces, E = 36): D2 2 x 4 and S4 2 x 4 unpinned, 5 workers each, cap 30 min. Side unit: plain cube 5 with 8 workers,
     15 min (tells workers from symmetry). <= 6 core-h. Kill: a failed control -> repair or park; no rung model -> park P3-sym with the cause, go to item 5.
   * Follow-up: a rung model realized by the bridge with `--all-pairs` PASS -> C3 3+3+3 at nine faces, E = 45, 51, 57, cap max(3 x rung time, 1 h),
     <= 40 core-h, one owner run. Cs 4 x 2 + 1 (110 orbits, near the unsolved eight-face size) only if C3 decides at all three E. SAT -> bridge,
     `--all-pairs` nine faces, `candidate-check`, escalate. UNSAT-SOLVER -> slice closed for planning (never "no nine-face object"). UNKNOWN -> UNDERPOWERED.
   * Lab: Opus, high / Codex gpt-6-astra, high (equivariant soundness and the gauge are the result).
3. **(11, 5) plane-only price probe** (N2 follow-up, new registration; explore, J 2; 1 2 2 1 2). Two of the 20 Aut+ = 2 maps (the PLAN lists fixed
   faces; more than one is out of scope), `omsat.build(sym_planes_only=True)` in a moved chart, 4 seeds per map, cap 1800 s, 8 shards, <= 4 core-h;
   baseline: the 12-element median of E-261116-01 (>= 3597 s).
   * Gate: both maps at median <= 360 s -> the 20 maps in one owner night (<= 80 core-h); SAT -> bridge, `--target S5`, `candidate-check`. Otherwise
     (11, 5) closes for the laptop. Kill: the N2 Szilassi chain fails through the runner. Lab: Opus, medium / Codex gpt-6.1-sol, high (it prices a night).
4. **S6 (10, 3) replay pricing** (E-261116-08 as registered; approved 16b for paper D3; audit, J 0). Any free session; blocks nothing.
   Lab: Opus, medium / Codex gpt-6.1-sol, high (it prices a night).
5. **P6 equivelar price pilot, stage A** (E-261117-04 as queued; explore, J 2), only if item 2's rung fails or overruns. Roest-Vigh's equivelar
   {9, 3} map must appear at (8, 3); costs per stage; no night before a price. Lab: Opus, medium / Codex gpt-6.1-sol, high.

Deferred: P4 (host, sampler, coupled P3 + P4: only behind P3 models that fail the bridge), every nine-plane sampling arm, N3, Stage B,
adjacency-guided search, I-261030-18 (fallback of item 2's C3 slice), E-261116-09 (add the §5 lemma), the (10, 4) replay. Parked: N4.

## 2. Answers

* **Verdict.** The target stands; the method mix failed. Nine-plane sampling bounds p only below ~1e-3 per decided unit, with 10-19 % of units
  at the cap (`E-261110-04/CONCLUSION.md:41,47`); P3 did not scale from seven to eight faces at one worker (`E-261116-07/CONCLUSION.md:3-6`).
  What worked was symmetry: both eight-face objects carry a free order-4 group (D2, S4: `literature/primary-reads-2026-11-01.md:49-53,72-78`),
  and C2 beat the asymmetric sampler 12x at seven planes (STATUS 3av). The stance changes on a rung pass of item 2 (P3-sym becomes the route),
  on a rung failure plus a P6 price above a night (nine faces parked, owner), or on a nine-face SAT.
* **For the lead 1, a nine-face arm?** No. Nothing predicts p; the seven- and eight-plane rates (2.7e-3, 7.1 %) came from families matched to a
  known object. A sampling arm returns only with a rate >= 1e-2 at a rung with a known answer and a stated transfer reason. Item 2 replaces the C3 arm.
* **2, uniform box.** Agreed; one line in "Parked methods": +-q^w boxes are sterile at eight planes (0 / 551, 0 / 557 classes).
* **3, faster P4 host.** Not this week. P4 filters realizability, the bridge already realizes the known types, and the bottleneck is finding
  chirotopes. Revisit only if item 2 returns models that fail the bridge (the coupled branch of the P3 tree).
* **4, P3 rerun.** Yes, as item 2, with symmetry as the stated change; the plain cube-5 unit rides along. Only a longer cap scores D = 0.
* **5, plane-only formulas.** (11, 5) Aut+ = 2: item 3, price first. (9, 4) one-face-involution maps: no census exists; that slice is
  C2 4 x 2 + 1 and needs a moved-chart P3, so not this week.
* **Proposed `STRATEGY.md` §1 (not applied).** "First: S1, nine mutually adjacent faces, genus free, by complete formulas on symmetric quotients
  (P3-sym: C3 3+3+3, then Cs 4 x 2 + 1), scored on the D2 / S4 eight-face rung. No nine-plane sampling night without a measured rate one rung
  below; P6 (equivelar slice) is the fallback. (11, 5): one plane-only price probe, then a night or closed."

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 2, P3-sym (I-261103-02 + equivariance) | 2 2 2 2 2 | 2 | 1 session + <= 6 core-h | main; C3 at nine faces is rung-sized |
| Item 1, N1b five face-transitive (8, 3) classes | 2 1 2 1 2 | 0 | minutes | rung control, possible witness |
| Item 3, (11, 5) plane-only price probe | 1 2 2 1 2 | 2 | 1 session + <= 4 core-h | the last (11, 5) gate |
| Item 4, E-261116-08 replay pricing | 1 2 2 1 2 | 0 | 1 session, <= 2 core-h | paper D3, approved |
| Item 5, P6 equivelar pilot (E-261117-04) | 1 2 1 1 2 | 2 | 1 session, 1 core-h | fallback of item 2 |
| Plain P3 cube 5, 8 workers | 1 2 2 1 2 | 2 | <= 1 core-h | side unit of item 2 |
| I-261030-18 voltage census, symmetric (9, g) maps | 1 1 1 2 2 | 2 | 2 sessions | per-map fallback for C3 |
| N3 (I-261117-03); P4 host, coupled P3 + P4 (I-261029-10) | 1 1 1 1 2; 1 1 1 2 2 | 2; 0 | after item 2 | below gate; only behind bridge failures |
| Adjacency-guided search (I-261029-51); deleted-plane sources (I-261116-06) | 1 1 1 2 2; 1 1 2 1 2 | 0; 2 | <= 3 core-h | below gate: no rate to expect |
| Stop: P4 sampler, nine-plane sampling arms, geo boxes | 1 0 1 1 2 | 2 | 1 night | C1 1 / 20; follow-up rule |
| N4 one-orbit Z9 (I-261117-04) | 0 1 2 0 2 | 2 | none | park: no Z9 Cayley map at (9, 4) (N1) |
| E-261112-02 Stage B; H-261112-01 | 2 1 1 1 2 | 2 | 2 nights | parked; H-261112-01 to "weakened" (3ae 0 / 2004, 3ak) |
| E-261116-09 lemmas (+ §5 lemma) | 2 1 2 2 2 | 0 | 1 session | queue |
| E-261101-08 relaxed Szilassi-12; I-261116-02 (10, 4) replay | 1 2 1 2 2; 1 1 2 1 2 | 2; 0 | 1 night; >= 2 nights | after a nine-face object; parked by the owner |

Parked target only (S0): E-261101-06 rank-3 SAT (2 2 2 2 2, the cheapest if S0 returns); E-261101-09, -15, -16 to -24, -03, -10 as filed.

## 4. Queue (in order; first item: N1b, main item: P3-sym)

1. **N1b** (exploit). H: a second face-transitive (8, 3) map is SAT. Test: ten formulas at 9 elements; SAT gives a witness and a rung control. <= 0.2 core-h.
2. **P3-sym** (explore). H: equivariance lets the census-free formula decide eight faces within 30 min. Test: the D2 / S4 rung; a pass leads to the
   C3 nine-face run (<= 40 core-h), a failure parks P3 for this host and sends the lab to item 5. Stop: its kill rule.
3. **(11, 5) probe** (explore). H: plane-only C2 is >= 10x faster at 12 elements. Pass: one night for 20 maps; fail: (11, 5) closed. <= 4 core-h.
4. **E-261116-08** (audit). H: the 20 S6 proofs fit one night. Stop: both CNFs priced or a hash mismatch.
5. **P6 stage A** (explore, conditional). H: the equivelar (9, 4) slice is enumerable within a night. Stop: price, failed control or cap.
6. **E-261116-09** (audit, no compute), with the §5 lemma. 7. **Cs 4 x 2 + 1** at nine faces: inside item 2 only, after C3.

## 5. New ideas (untested proposals, not evidence) and the owner's raw ideas

* **N1. Equivariant census-free formula (P3-sym).** Add a group action on the planes to P3; decide all G-symmetric solids of one (F, E) in one
  formula. Why: orbit counts (this session, EXACT, `itertools`): C3 on nine faces 72 of 210 quads, D2 and S4 on eight 36 and 34 of 126; P3
  decided the 70-sign seven-face formula in 8 s, and cells shrink by the same factor (that presolve merges the equalities: CLAIMED). Test: item 2's rung.
* **N2. Symmetric slices at nine faces (PROVED-1 sketch, this session).** (a) A symmetry fixing a face keeps its outward normal, so the face is
  perpendicular to a rotation axis or has its normal in a mirror; no inversion or rotoreflection fixes a face. (b) A rotation fixes at most one
  face (dialogue §6, PROVED-1). (c) A rotation of order >= 4 sends a plane to >= 4 planes through one axis point (non-uniform). Hence D2 and S4
  have only 4-orbits on nine faces (impossible); every order-3 rotation acts freely, and an equivariant perturbation makes it uniform with
  infinity, so C3 3+3+3 covers D3, C3v, C3h. Uniform families: C3 3+3+3 and Cs 4 x 2 + 1 (standard chart), C2 4 x 2 + 1 and Cs 3 x 2 + 3 (moved
  chart). With orbits {0,1,2}, {3,4,5}, {6,7,8}, P3's gauge (vertices 012, 345, both fixed) is constant on orbits and set by flipping whole
  orbits, so it is equivariant. Test: E-261116-09 and item 2's reachability control.
* **N3. Mirror family and its negative control.** No known face-neighbourly object has a mirror. If Szilassi's map is chiral (CLAIMED from memory:
  the K7 torus map is {3, 6}_(2,1)), the (7, 21) Cs formula is a free negative control. Test: the census flag, then item 2.
* **Owner's raw ideas (TODO 0.1), prompt-B triage.** Read in a scratch folder, no code run. Both preprints exist (OpenAI, 25 Oct 2026; Anthropic,
  26 Oct 2026, Lean-formalized); their theorems are CLAIMED.

| Idea / question | Existing ids | V N L F | Verdict, next step |
|---|---|---|---|
| ETH Q1: is the 2^O(n loglog n / sqrt(log n)) #k-SAT algorithm faster on our CNFs (4,891-12,968 variables, ~151k clauses)? | none (DR8) | 2 0 0 0 | drop: Anthropic's preprint says no gain over brute force unless n > 10^(10^8), none in general unless n > 10^7 |
| ETH Q2: exact counting for uniform chirotope sampling (JVV self-reduction) | I-261031-01 (S0) | 2 1 1 1 | park under I-261031-01; practical counters exist; no decision needs a count |
| ETH Q3: do the corollaries (circuit lower bounds, Max-k-SAT) bear on realizability (ER-hard)? | none | 1 0 0 0 | drop |
| Impagliazzo-Paturi 2001 (ETH, SETH; sparsification in IPZ01) | none | 2 0 0 0 | drop: definitions only (CLAIMED, from memory) |
| Degen Q1: does the eight-square identity parametrize or certify arrangements? (constraints are 4 x 4 determinant signs; symmetries need permutation-sign matrices or quaternions) | none | 2 0 0 2 | drop |
| Degen Q2: octonion / Fano structure (K7's 14 triangles = two Fano planes) as a guide for 8, 9, 12 faces | none | 1 0 0 2 | drop: composition algebras only in dims 1, 2, 4, 8 (Hurwitz); S1 dual maps have multiple edges (CLAIMED) |

## 6. Audit

1. **Pre-registration claim stronger than the evidence.** The P3 PLAN said `test_p3.py` passed; 2 of 6 failed at the registration commit
   (`E-261116-07/CONCLUSION.md:23`). Rule: `experiment-start` runs the unit tests and records their output in the PLAN commit.
2. **Dirty run, again.** The P4 pilot ran with an uncommitted `p4.py` fix, and ~0.09 core-h of probes have no manifest
   (`E-261117-03/CONCLUSION.md:6-7`). The 16b audit (item 5) asked for a dirty-tree refusal; `overnight/launch.sh:93` still refuses on cores only.
   Add it in item 2's prep.
3. **Discovery power at nine planes unmeasured.** STATUS 3ay says "per decided arrangement"; `ROADMAP.md:141` and `CONTINUE_PROMPT.md:15` drop
   "decided", with 10-19 % of units censored and no nine-plane positive control. Fix the wording; never cite the bound as a family rate.
4. **Manifest gap.** The E-261117-01 manifest lacks `wall_seconds` (crash in a summary print, `CONCLUSION.md:7`); fixed, not rerun; acceptable.
5. **Process cost fine.** 35 commits, 71.4 core-h, code +4,172 lines against docs +2,949, at most one amendment per experiment; P4's pilot stop
   went to the owner. Good practice: the constant geo outcome was checked by `classes.py` before interpretation (2026-11-01 rule).
6. **Chains to stop:** the P4 sampler; C3 / C2 nine-plane sampling at this box and cap; geo boxes; N4; a plain P3 rerun with only a longer cap.

## 7. Credences (all CONJECTURE, planning weights)

* **Nine faces, genus >= 4: 0.55 -> 0.45.** Zero hits in both uniform symmetric nine-plane families sampled, the face-transitive slice empty
  (EXACT), Stage A 0 of 2004 and the rung-below census returning only its source; none is a negative result.
* Relaxed Szilassi-12 0.40 stays (no datum at twelve faces). (10, 4), (11, 5), S6 (10, 3), S0: no new datum; the unapplied proposals stand
  (0.03 / 0.87 / 0.10; 0.03 / 0.37 / 0.60; 0.05; A 0.17, B 0.60, C 0.23). Item 3 moves (11, 5).

## 8. Three things to do first

1. Owner: approvals 1-3. 2. Lab (Opus, medium / gpt-6.1-sol, medium): item 1, minutes. 3. Lab (Opus, high / gpt-6-astra, high): item 2's
PLAN, the equivariant build and its controls; then the owner launches the rung (<= 6 core-h).
