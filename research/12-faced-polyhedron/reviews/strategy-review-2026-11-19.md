# Strategy review, 2026-11-19: the rung passed, nine faces undecided; measure the power, then decide the symmetric slices per map

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep nine faces first and keep the stance. Symmetry made formulas 100x faster this week. (11, 5) half-turn formulas took 17-90 s against > 3600 s, and P3-sym found both eight-face objects in seconds. The nine-face formula is still uncalibrated.
2. **Week:** four items done, 19.4 core-h, no candidate. Sieve: OPEN-LOW. N1b: classes 1-5 UNSAT-SOLVER. P3-sym: the rung passed, C3 at nine faces UNKNOWN at 1 h. (11, 5): all 20 half-turn maps UNSAT-SOLVER, closed.
3. **Your Q6-Q7 in one line:** every rung timed only how long it takes to *find* a known object, and no one timed a *refutation* at the same size. So the nine-face UNKNOWN can come from size, from refutation or from the absence of a C3 object. The data cannot tell which.
4. **Approval 1, first item:** the P3-sym power ladder, one evening, <= 20 core-h. C2 4 x 2 at eight faces has 66 orbits and holds both known objects, so it must find a model. C2 (8, 30) and C3 (9, 39) must be INFEASIBLE, because both are decided negatives (STATUS 3d). Your Q5 is answered in the same run: every symmetric (8, 3) map is enumerated by blocking the maps already found.
5. **Session lemma (PROVED-1 sketch, counts EXACT):** every uniform symmetric eight-face solid has a free half-turn, so one C2 formula covers them all. At nine faces only C3 3+3+3 and C2 4 x 2 + 1 remain. Mirrors are out: every mirror class forces zero signs.
6. **Approval 2, main investment:** a census of the symmetric nine-face maps, built by extending the existing C3 tool, then symmetric formulas per map. Gate: the genus-4 census finishes within 1 core-h.
7. **Approval 3:** the `STRATEGY.md` §1 text in §2 drops Cs, adds the per-map route and closes (11, 5). Credences unchanged.
8. **Your idea (numbering):** its exact form is "faces numbered by a group, every face with the same neighbour pattern". That is the Cayley slice: Szilassi and Roest-Vigh fit it, and nine faces at genus 4 is empty (N1). Keep genus 7 as a small check (item 5); drop the rest.
9. **Not recommended:** longer C3 runs before item 1, the curved-face encoder, the map-29 models, (11, 5) mirrors (no uniform formula exists for them).
10. **If item 1 shows no power at 66 orbits and the census does not fit,** nine faces has no route on the laptop. Then the choice is yours: P6, consolidation, or an (8, 3) sweep for a third eight-face object.

## 1. Week plan (for `ROADMAP.md`; <= 10 cores, 8-10 shards, the owner launches every run, no proofs, PLAN with unit tests first)

1. **P3-sym power ladder and the symmetric (8, 3) slice** (follow-up of E-261118-02, new registration; explore, J 0, its pass branch earns a
   J-2 night; 2 2 2 1 2). P3-sym unpinned, 5 workers, one seed: U1 free C2 4 x 2 at (8, 36), cap 1.5 h. On each model, decode, census code,
   bridge, `--all-pairs`, then block that map (a clause over the variables that fix its dual map, with all images under the normaliser of the
   action) and continue. U2 free C2 at (8, 30), cap 1 h, expected INFEASIBLE ((8, 2) negative, 3d). U3 C3 3+3+3 at (9, 39), cap 1 h, expected
   INFEASIBLE ((9, 3) negative, 3d). U4 D2 and S4 at (8, 36) with blocking, 15 min each, run first. <= 20 core-h, one owner evening.
   * Controls: those of E-261118-02, plus both known objects pinned under free C2 (orbit-size-2 gauge reachable). Blocking control: with
     Roest-Vigh's map blocked, U1 must still return Mizhaev's map, and the reverse.
   * Kill and tree: a failed control -> repair. U2 or U3 SAT -> stop, bridge: a PASS contradicts 3d (`candidate-check`, escalate), no PASS
     means P3 and omsat disagree (lead). U1 model and U2, U3 INFEASIBLE in their caps -> one owner night: C3 3+3+3 at E = 45, 51, 57, cap
     max(4 h, 10 x the slowest of these times), <= 60 core-h. U1 model, U3 UNKNOWN -> no C3 night, C3 goes to item 2. U1 UNKNOWN -> P3-sym
     parked for nine faces. A new (8, 3) map realized, `--all-pairs` PASS -> `candidate-check`, escalate (meets E-261112-02's reopening
     condition). Blocking ends INFEASIBLE -> "the symmetric uniform (8, 3) solids have only the known maps", UNSAT-SOLVER (planning only).
   * Lab: Opus, high / Codex gpt-6-astra, high. Why: the blocking soundness decides what is claimed, and a new eight-face object is possible.
2. **Symmetric nine-face census with per-map symmetric formulas** (I-261030-18 + I-261119-01, new registration; explore, J 2; the main
   investment; 2 2 1 2 2). Stage A, one session, <= 1 core-h. Generalise `E-261103-01/c3_crosscheck.py` to (9, 4): three pair orbits, 0, 3
   or 6 fixed triangles, any multiplicity (the code asserts <= 2 now), plus a C2 analogue (one fixed face). Controls: (9, 3) gives exactly the
   census's 8 free-C3 classes and its fixed-face involution classes; (7, 1) gives Szilassi's map; free C2 at (8, 3) gives both known maps.
   Gate: both (9, 4) lists complete within 1 core-h. Stage B (owner run, <= 10 core-h, 10 shards, kissat, cap 600 s): C3 by omsat's C3
   clauses (standard chart), C2 4 x 2 + 1 plane-only (moved chart, E-261118-03 runner). Rung: known maps SAT, (9, 3) formulas UNSAT (3d).
   * Tree: SAT -> bridge, `--all-pairs` nine faces, `candidate-check`, escalate. All UNSAT-SOLVER -> genus 5 (E = 51), priced the same way.
     Gate failed -> item 3. Item 1's U1 and this free-C2 (8, 3) rung must agree map by map (two methods, one slice).
   * Lab: Opus, high / Codex gpt-6-astra, high (a new enumerator; its controls are the result).
3. **P6 equivelar stage A** (E-261117-04 as queued; explore, J 2), only if item 2's census gate fails. Lab: Opus, medium / gpt-6.1-sol, high.
4. **E-261116-09 lemma session** (audit, no compute), extended by I-261118-02 and the lemmas of §2 (owner 5, lead 4). These lemmas carry
   the scope sentences of items 1-2. Lab: Opus, high / gpt-6-astra, high (proofs; at most PROVED-1).
5. **Optional: face-transitive nine-face maps at genus 7** (owner's idea, §5; explore, J 2), after the owner approves the triage: N1's two
   enumerators at valence 14 (Z9, Z3 x Z3), the plain formula at 10 elements on any admissible class; <= 1 session.
   Lab: Opus, medium / gpt-6.1-sol, medium (SAT: Opus, high / gpt-6-astra, high).

Deferred: E-261116-08 (owner), P4, nine-plane sampling, N3, Stage B (reopens on a new (8, 3) map), the asymmetric (8, 3) sweep, the
curved-face encoder, the full deletion sieve, E-261101-08, the (10, 4) replay. Parked: N4. Closed: (11, 5) on the laptop.

## 2. Answers

* **Verdict.** The evidence supports `STRATEGY.md`: the method passed its rung (`E-261118-02/CONCLUSION.md:3-5`), and symmetry is the lever
  that worked (3bc: 17-90 s against censored 3600 s; 3bb: 2.3 s, 5.0 s). It changes on: no power at 66 orbits *and* item 2's census over
  budget (no laptop route; the owner decides); a nine-face SAT; item 1 contradicting 3d (fix the tools first).
* **Lead 1 (longer C3, stronger formula, C2 4 x 2 + 1 or P6?).** None before item 1. A longer cap without a measured power scores D = 0
  (STRATEGY §2). C2 4 x 2 + 1 cannot be written in P3-sym: a moved chart breaks the cell action. It goes per map in item 2. P6 stays the fallback.
* **Lead 2 (Cs).** Agreed and checked: every mirror class forces 3-330 zero signs at 8, 9 and 11 planes (`strategy-review-2026-11-19-orbits.py`,
  EXACT counts). Remove Cs from STRATEGY §1 and ROADMAP:125, and close I-261118-03 as moot, since its (7, 21) control is itself out of domain.
* **Lead 3 (curved-face encoder, map-29 models).** Neither changes a decision: straightening is the full formula, UNSAT-VERIFIED for all 203
  (9, 3) maps (3d); nine faces has no census to sieve; the map-29 models have a defective face by design. Park I-261118-04 (owner may override).
* **Lead 4 (I-261119-01; (11, 5) improper).** S6 (11, 4) and (12, 5) serve the parked S6 target; the nine-face part is item 2. (11, 5)
  improper (PROVED-1 sketch, this session): on an Aut+ = 2 map, a rotoreflection would square to the involution and fix its fixed face,
  which is impossible. An inversion cannot act freely on 11 faces. Mirrors force zero signs, so no uniform formula exists; (11, 5) stays closed.
* **Owner 5 (block known (8, 3) objects).** Yes, as item 1. Lemma (PROVED-1 sketch, this session; counts EXACT): a uniform group on eight
  faces has an element of prime order. Order 3 needs two fixed faces, which is impossible. Orders >= 5 make planes concurrent. A mirror or
  inversion forces zero signs. So the group contains a free half-turn, and C2 4 x 2 at E = 36 holds every symmetric uniform (8, 3) solid,
  D2 and S4 included. Asymmetric (8, 3): >= 34,402 classes (16b check, incomplete), at least a night; priced only if item 1 finds a new map.
* **Owner 6 (other methods that stop at nine).** All of them: P3, P4, P3-sym, the frozen sampler (2.7e-3, 7.1 %, then 0 hits), Stage A,
  per-map OM-SAT ((8, 2) seconds, (11, 5) plain > 1 h), the genus ladder (3, never 4). Every rung timed finding a known object; a target
  run has none. Quads grow 70 -> 126 -> 210, cells 2^F. The exception is symmetric plane-only formulas.
* **Owner 7 (why one face costs so much).** Not yet separable. Free signs alone do not explain it: 72 orbits is about the 70 signs P3 decided
  in 8 s, but the formula has 51,283 variables against 21,150 for the plain eight-face cube. Item 1 separates the causes: U1 tests size, U2
  and U3 test refutation. If both are fast, "no C3 object, or a rare one" remains, still without proof.
* **Proposed `STRATEGY.md` §1 (not applied).** "First: S1, nine mutually adjacent faces, genus free, on the two uniform symmetric families
  C3 3+3+3 and C2 4 x 2 + 1: P3-sym for C3 once its power is measured at the nine-face size on known answers, and per map from a symmetric
  census for both; P6 is the fallback; no nine-plane sampling night without a rung-below rate. Mirror families are outside every uniform
  formula. (11, 5): closed for the laptop (E-261118-03)."

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, P3-sym power ladder + symmetric (8, 3) slice | 2 2 2 1 2 | 0 (pass: 2) | 1 session + <= 20 core-h | first; answers owner 5-7 |
| Item 2, symmetric nine-face census + per-map formulas (I-261030-18, I-261119-01) | 2 2 1 2 2 | 2 | 1 session, <= 1 core-h | main investment |
| Item 3, P6 equivelar stage A (E-261117-04) | 1 2 1 1 2 | 2 | 1 session, 1 core-h | fallback of item 2 |
| Item 4, E-261116-09 lemmas (+ I-261118-02, §2 lemmas) | 2 1 2 2 2 | 0 | 1 session | scope of items 1-2 |
| Item 5, face-transitive nine faces at genus 7 (owner) | 1 1 2 1 2 | 2 | <= 1 session | optional |
| P3-sym C3 longer caps | 1 1 1 1 2 | 2 | 1 night | D = 1 until item 1 measures power |
| Asymmetric (8, 3) sweep; E-261112-02 Stage B, H-261112-01 | 1 1 1 1 2; 2 1 1 1 2 | 0; 2 | >= 1 night; 2 nights | only after a new (8, 3) map |
| Curved-face encoder (I-261118-04); map-29 final polynomials; full deletion sieve | 1 0 1 1 2; 1 0 2 0 2; 1 1 1 1 2 | 0 | 2 sessions; 1; 40-150 core-h | below gate |
| N3 (I-261117-03); P4 host / coupled; adjacency-guided (I-261029-51); deleted-plane sources (I-261116-06) | 1 1 1 1-2 2 | 0-2 | <= 3 core-h each | below gate |
| (11, 5) improper slice; I-261118-03 mirror control | 0 1 0 0 2 | 2 | none | no uniform formula: close |
| Nine-plane sampling, P4 sampler, geo boxes; N4; E-261101-08 | 1 0 1 1 2; 0 1 2 0 2; 1 2 1 2 2 | 2 | 1 night | stopped; parked; deferred |

Parked targets only: S6 (I-261119-01 at (11, 4), (12, 5): 1 2 2 1 2, J 2; E-261116-08, I-261116-05); S5 (I-261116-02; (11, 5) closed);
S0 (E-261101-06, 2 2 2 2 2; the rest as filed). Other open ideas and hypotheses: no new evidence since 2026-11-18, scores kept.

## 4. Queue (in order; first item: 1, main investment: 2)

1. **Item 1** (explore). H: P3-sym finds a model at 66 orbits and refutes at 66-72 orbits within its caps. Falsifier: U1 UNKNOWN.
2. **Item 2** (explore). H: the symmetric (9, 4) census fits in 1 core-h, and its formulas decide in minutes. Falsifier: the stage-A gate.
3. **Item 1's C3 night** (explore, conditional). H: with power measured, a C3 nine-face model appears within 10x the rung time. <= 60 core-h.
4. **Item 4** (audit), then **item 3** (explore, if item 2's gate fails), then **item 5** (explore, optional); each stops by its rule in §1.

## 5. New ideas (untested proposals, not evidence) and the owner's raw idea

* **N1. Known-answer power ladder.** Refutation rungs: the decided negatives (8, 2) and (9, 3) (3d) at the target's orbit size. Discovery
  rung: the free-C2 eight-face formula (66 orbits, the whole symmetric (8, 3) slice by the lemma of §2). Why: no rung has measured
  refutation. Test: item 1. Orbit counts 36 / 34 / 66 / 72 (EXACT, `strategy-review-2026-11-19-orbits.py`).
* **N2. Symmetric map census at nine faces.** The C3 exact cover already reproduces the 8 free-C3 (9, 3) maps (STATUS 3c). Lift it to genus 4
  and add a fixed-face C2 version. Why: per-map symmetric formulas are fast (3bc, 3ba), and these two families are all that is uniform
  (I-261118-02). Test: item 2, stage A.
* **N3. (11, 5) improper reduction** (§2, lead 4), a lemma for item 4. **N4. Cayley nine-face maps at genus 7** (owner's idea): the face
  degree 2E / 9 is an integer only at genus 4, 7, 10, ..., and N1 covered genus 4. Test: item 5.
* **Owner's raw idea (TODO 0.1, 2026-11-19: number faces and edges of known solutions and quasi-solutions, look for a function,
  extrapolate to nine faces), prompt-B triage.** Nothing external was read. Items 1-2
  are the general form of Q1: a group numbering with two or three face orbits instead of one.

| Question | Existing ids | V N L F | Verdict, next step |
|---|---|---|---|
| Q1: are the known solids "group-numbered", with face i seeing its neighbours as i + (fixed pattern)? Szilassi is a Z7 Cayley map with rotation (1, 3, 2, 6, 4, 5) (CLAIMED, memory); Roest-Vigh is order-8 Cayley (EXACT, 3au); Mizhaev is not (two face orbits). Nine faces: Z9, Z3 x Z3 | E-261117-01, I-261117-01 | 3 1 1 2 | keep, small: genus 4 is empty (EXACT), genus 7 is new (item 5, <= 1 session); kill: no admissible class; order unchanged |
| Q2: plane positions or contact places as a function of the face number, fitted on the known solids | cyclic arrangements (parked), geo boxes 0 / 551 (3ay), E-261101-16 | 1 0 1 2 | drop: three solids of different groups and genera fix no function; a family needs a rate >= 1e-2 at eight planes first |
| Q3: where quasi-solutions fail (unrealized models, near-misses) | FD11, E-261118-04, E-261114-04 | 2 0 1 2 | drop: restates done work; near-misses are far from solutions (FD11) |

## 6. Audit

1. **Ledger damage.** `a7ca977b` deleted the heading "## 4. What may and may not be claimed" and left a stray fragment (`STATUS.md:530-531`).
   Section 3bc then went in after the claims block (`STATUS.md:546`). The applying session should restore the heading and move 3bc.
2. **Claim stronger than the evidence.** `E-261118-03/CONCLUSION.md:32-33` says no object "whose map automorphism group contains a proper
   half-turn" is expected. The formulas impose a *geometric* half-turn, and asymmetric realizations of those maps are untouched. Reword it as
   "with a half-turn symmetry". The same wording issue is at `STATUS.md:9`.
3. **Underpowered reading.** `E-261118-02/CONCLUSION.md:42-43`: "a factor 700" compares time-to-SAT on known objects with a censored run of
   unknown answer. It is a lower bound on time to decision, not the price of a face. The UNDERPOWERED verdict is right.
4. **Pilot cost and provenance.** The E-261118-04 pilot had no `run.sh` or manifest, and its map-29 times come from a transcript
   (`CONCLUSION.md:7-11`). It cost 1.1 core-h, over the whole sieve budget (<= 1). Rule: pilots use `run.sh` and stop at projection > budget.
5. **Stale plan text.** `STRATEGY.md:15` and `ROADMAP.md:125` still schedule Cs 4 x 2 + 1, and I-261118-03 is open (§2, lead 2). **Process
   cost fine:** 22 commits, 19.4 core-h, code +1,474 lines (py, sh) against markdown +1,087, at most two gated amendments per experiment.
   E-261118-03 added `controls_12.py` before reading its fast UNSATs (the 2026-11-01 rule). **Chains to stop:** the deletion sieve
   (encoder, models, full sieve), (11, 5) in every form, C3 caps without item 1, plain P3 reruns.

## 7. Credences (all CONJECTURE, planning weights)

* Nine faces 0.45 stays: no nine-face datum this week. Both uniform symmetric slices UNSAT-SOLVER at genus 4 -> about 0.35-0.40.
* (11, 5): closed; the unapplied proposal (0.03 / 0.37 / 0.60) stays. Relaxed Szilassi-12, (10, 4), S6 (10, 3), S0: no new datum.

## 8. Three things to do first

1. Owner: approvals 1-3, plus the triage verdicts (Q1 keep as item 5; Q2 and Q3 drop).
2. Lab (Opus, high / gpt-6-astra, high): item 1's PLAN (units, blocking with its control, both refutation rungs), then the owner's evening run.
3. Lab (Opus, high / gpt-6-astra, high): item 2 stage A (census lift and its (9, 3), (7, 1), (8, 3) controls) while item 1 runs.

## Owner's decisions (2026-11-19)

Approvals 1-3 given ("ok"), the §5 triage of the owner's idea accepted (Q1 kept as E-261119-03, Q2 and Q3 dropped);
applied the same day: `STRATEGY.md` §1 and log, the `ROADMAP.md` week plan and queue rows (E-261119-01..03), `STATUS.md`
(header, focus, the §4 heading restored, 3bc moved), the audit wordings in the E-261118-02 and E-261118-03 conclusions,
ideas I-261119-02, I-261119-03 filed, I-261118-03 closed, I-261118-04 parked.
