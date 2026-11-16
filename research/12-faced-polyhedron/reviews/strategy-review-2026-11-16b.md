# Strategy review, 2026-11-16b: every listed target is decided or priced out; nine faces by map-free methods

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep the stance; replace the target list again. The week plan ended in one day, no candidate.
2. **Exact per-map route hit the laptop wall at 12 elements** (NUMERICAL): kissat medians 0.29 / 2.8 / 55 / >= 3597 s at 9 / 10 / 11 / 12
   elements; (11, 5) priced at >= 41 nights (6 of 10 TIMEOUT at 1 h, STATUS 3aq). S0 has 13 elements: its price probe stays closed.
3. **S6 (10, 3): all 20 normalised formulas UNSAT-SOLVER** (3as), polar transfer 0 of 56137 charts (3at). S6 (10, 2) exists (C1, C2).
4. **Session check (NUMERICAL, 10 min):** the (8, 3) map census is huge (>= 34,402 classes after 551 of 1806 patterns), so nine faces
   cannot go map by map. Route: **map-free**: one OM-SAT formula per (F, g) (I-261103-02) and scored plane families (E-261110-03/04).
5. **Approval 1: week plan §1. First item: the (11, 5) symmetric slice** (24 maps, minutes; registered follow-up I-261116-04).
6. **Approval 2:** reopen E-261110-03/04 (you parked them 2026-11-12 for the ninth-plane cells, now done / parked) and the STRATEGY §1 text (§2).
7. **Approval 3 (yes / no):** consolidation: price the S6 (10, 3) proof replay (claim: paper D3) and one lemma session. Note stays deferred.
8. **Not done:** no target formula run, no proofs; the census check is not ledger evidence; no human review.

## 1. Week plan (for `ROADMAP.md`; <= 10 cores, 10 shards, the owner launches every run; proofs only in item 4)

1. **(11, 5) symmetric slice** (I-261116-04; exploit, J 2). The 24 admissible maps with Aut+ 2 or 3; uniform free-C2 / free-C3 formulas
   as in E-261103-03 / E-261113-01 (b). The PLAN lists which maps have a free action; a fixed-face involution is out of scope for
   uniform formulas (`E-261103-02/SOUNDNESS.md:65-78`) and is recorded as "not decidable here", not run. Cap 3600 s, <= 2 core-h.
   * Controls: the free C2 / C3 positive controls of E-261103-02 through the same runner. Kill: a failed control.
   * Follow-up: SAT -> 30 models and the bridge, `--target S5`, `candidate-check`, escalate. Otherwise (11, 5) closes at laptop scale
     for this encoder: no further (11, 5) item. Lab: Opus, medium (SAT conclusion: high) / Codex gpt-6.1-sol, medium (SAT: gpt-6-astra, high).
2. **Census-free S1 formula, ladder pilot** (I-261103-02; explore, J 2 via its tree). One SAT instance per (F, g): rank-4 chirotope on
   F + 1 elements plus tope variables for the solid (tope iff orthogonal to every circuit; disk face per plane, 1-3 runs per pair,
   every pair adjacent, cubic, orientable, E fixed by g). No map is given.
   * Ladder: (7, 1) must be SAT with Szilassi's chirotope accepted; (8, 3) must accept both known chirotopes (Roest-Vigh, Mizhaev) as
     pinned models and then solve unpinned; (8, 2) must be UNSAT-SOLVER (agrees with B2). <= 1 core-h.
   * Kill: (7, 1) unpinned not solved in 10 min, a known chirotope rejected -> park with the cause; (8, 2) SAT contradicts B2 -> stop, escalate.
   * Follow-up: ladder passes and (8, 3) unpinned <= 1 h -> one day run at (9, 4) and (9, 5) (E = 45, 51), a 10-configuration portfolio
     (seeds / phases) on 10 shards, <= 20 core-h. SAT -> realize (bridge), `--all-pairs` with nine faces, `candidate-check`, escalate.
     UNSAT-SOLVER -> planning only (never "no nine-face object"). Lab: Opus, high (a new encoder whose soundness is the result) /
     Codex gpt-6-astra, high.
3. **Scored plane families, then nine planes** (E-261110-03 reduced, then E-261110-04; explore, J 2). Inner solver of E-261112-01
   (all pairs, genus free). Families at 8 planes, E in {36, 42}, cap 60 s, <= 3 core-h: D2 with two 4-orbits (200), isotropic (200),
   and N1: two planes deleted from each realized (10, 2) S6 object (all pairs of planes). Report p per family with a Wilson interval;
   every SOLID through the exact verifier and its map against the two known (8, 3) maps.
   * Controls: Roest-Vigh and Mizhaev planes return their objects; a tetrahedron-type negative is INFEASIBLE. Kill: failed control.
   * Follow-up: a family with >= 10 positives -> its 9-plane relative (D2 4+4+1; one plane deleted from a (10, 2) object), E in {45, 51},
     N set for detection >= 0.95 at p / 10 (a stated transfer assumption, not a measurement), one owner night <= 80 core-h. SOLID ->
     `--all-pairs` nine faces, `candidate-check`, escalate. None -> LOW-YIELD@budget with that power statement. < 10 positives in every
     family -> UNDERPOWERED, no night. A nine-face hit sends the 12-plane D2 3x4 (E-261101-08) to the lead.
   * Lab: Opus, medium / Codex gpt-6.1-sol, high (the prep can waste a night); a SOLID conclusion: Opus, high / gpt-6-astra, high.
4. **S6 (10, 3) replay pricing** (I-261116-05; audit, J 0; only with approval 3; named claim: OUTLINE D3, formula-scope exclusion).
   One session, <= 2 core-h: rebuild the fastest and slowest CNF by hash (763 s, 2734 s with `--sat`), kissat DRAT + drat-trim and
   CaDiCaL LRAT + a linear checker; proof size, check time, peak memory; extrapolate to 20.
   * Gate: <= 1 night and <= 200 GB transient -> owner night, proofs checked and deleted, hashes and transcripts kept; above -> lead.
   * Lab: Opus, medium / Codex gpt-6.1-sol, high (it prices a night).
5. **Lemma session** (approval 3; audit, J 0; no compute beyond exact local checks). (a) N2: uniform position is no loss for cubic
   embedded objects (asymmetric formulas). (b) I-261108-09, its universal local check as filed. Output: PROVED-1 text or a counterexample.
   * Kill: a counterexample patch -> keep "uniform" / "cubic" in every statement. Lab: Opus, high / Codex gpt-6-astra, high (proof level).

Deferred: E-261116-03 (gate failed), the (10, 4) replay (I-261116-02, yours), Stage B, wedges, I-261113-04, I-261114-04, the full 865.

## 2. Answers

* **Verdict.** The stance worked: (10, 4) A + B and S6 (10, 3) were decided at solver level within one night each, as priced. The
  targets did not: (11, 5) is priced out (>= 41 nights, `E-261116-01/CONCLUSION.md:12-15`), the S0 gate failed, S6 (10, 3) is
  exhausted, nine faces are parked. Price = maps x time per map; at 12 elements both factors are too large for one laptop.
  Would change it: an (11, 5) symmetric SAT (item 1); the census-free formula solving (8, 3) in minutes (item 2); a family p >= 0.05.
* **Proposed `STRATEGY.md` §1 (not applied).** "First: S1, nine mutually adjacent faces with the genus free, by map-free methods
  scored one rung below: the census-free formula (I-261103-02), then scored plane families (E-261110-03/04). S5 (11, 5): the
  symmetric slice only; the asymmetric sweep is priced out. S6: parked after (10, 3) (all normalised formulas UNSAT-SOLVER). The S0
  price probe is withdrawn. Per-map sweeps at 12 or more elements are not planned on the laptop."
* **Lead 1, next S6 step.** None on the laptop. S6 (11, 4) has 12 elements, and S6 formulas cost more per element than S5 (median
  1277 s at 11 elements against 55 s for (10, 4), `E-261116-05/CONCLUSION.md:14`). Park S6 with (10, 2) positive and (10, 3) UNSAT-SOLVER.
* **Lead 2, price the replay I-261116-05?** Yes if you want paper item D3 as a statement (approval 3, item 4). It is the cheapest named
  claim (about one night against >= 2 for (10, 4)) and the clearest new contrast: S6 exists at (10, 2), and at (10, 3) the vertex version
  realizes (HLZ, CLAIMED) while the face version is UNSAT-SOLVER. Without approval 3 nothing is replayed.
* **Lead 3, H-261110-03 and S0 A/B/C.** H-261110-03: the (10, 3) part has solver-level support for the rival; the status stays open
  until a replay. (11, 4) is untestable here. S0: §7.

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, (11, 5) symmetric slice (I-261116-04) | 1 2 2 1 2 | 2 | 1 session + <= 2 core-h | last cheap S5 shot |
| Item 2, census-free formula (I-261103-02) | 2 2 1 2 2 | 2 | 1-2 sessions, <= 1 core-h | complete over maps; encoder risk |
| Item 3, family scoring (E-261110-03 reduced) + N1 | 2 2 2 1 2 | 0 | 1 session + <= 3 core-h | gate of the J 2 night |
| Item 3 follow-up, nine planes (E-261110-04) | 1 2 1 1 2 | 2 | 1 night | only after >= 10 positives |
| Item 4, S6 (10, 3) replay (I-261116-05) | 1 2 2 1 2 | 0 | 1 session | D only with approval 3 |
| Item 5, N2 + I-261108-09 lemmas | 2 1 2 2 2 | 0 | 1 session | lifts "uniform", "cubic" |
| E-261101-08 relaxed Szilassi-12, D2 3x4 | 1 2 1 2 2 | 2 | 1 night | after a nine-face hit |
| I-261030-18 voltage-graph quotient census | 1 1 1 2 2 | 2 | 2 sessions | symmetric maps only; below item 2 |
| I-261116-02 (10, 4) replay | 1 1 2 1 2 | 0 | >= 2 nights (est.) | parked by the owner |
| (11, 5) `--sat` re-probe of the six TIMEOUTs | 0 1 2 1 2 | 2 | <= 10 core-h | below gate: needs >= 10x to matter |
| E-261116-03 S0 price probe | 1 1 2 2 2 | 2 | <= 40 core-h | below gate: curve predicts TIMEOUT |
| S6 (11, 4) asymmetric; (8, 3) / (9, 4) map census | 1 1 0 1 2 | 2 | >> 1 night | below gate (session check) |
| E-261112-02 Stage B; I-261110-01 wedges | 2 1 1 1 2; 1 1 1 2 1 | 2 | 2 nights; 1-2 sessions | parked / deferred |
| I-261116-01 other realizations; I-261113-04; I-261114-04 | 0 1 2 0 2 | 2 | 1 session | D = 0 after 3as, 3at |
| I-261108-10 defect-bounded census | 1 1 1 1 2 | 0 | 1-2 sessions | subsumed if I-261108-09 holds |

Parked target only (S0): E-261101-06 rank-3 SAT per type (2 2 2 2 2, the cheapest if S0 returns); E-261101-09, -15 and all other open items as filed.

## 4. Queue (top items, in order)

1. **Item 1** (exploit). H: a symmetric (11, 5) formula is SAT. Test: <= 24 free-action formulas at 3600 s. SAT -> result candidate;
   otherwise (11, 5) closes here. Budget 1 session + 2 core-h. Stop: all formulas recorded or a failed control.
2. **Item 2** (explore). H: one map-free formula decides (8, 3) in minutes. Test: the (7, 1) / (8, 2) / (8, 3) ladder. Pass -> (9, 4),
   (9, 5) day run; fail -> park I-261103-02 with the cause. Budget 2 sessions + 1 core-h (+ 20 on a pass). Stop: kill rule of item 2.
3. **Item 3** (explore). H: some plane family has p >= 0.05 for all-pairs solids at 8 planes. Test: 600 + N1 arrangements, 60 s each.
   >= 10 positives -> nine-plane night; else UNDERPOWERED. Budget 3 core-h (+ 80 on a pass). Stop: all units, a failed control.
4. **Item 4** (audit, approval 3). H: the 20 S6 proofs fit one night. Test: two CNFs priced. Stop: both priced.
5. **Item 5** (audit, approval 3). H: uniformity and the perturbation lemma hold. Test: exact local cases. Stop: proof or counterexample.
6. **E-261101-08** (exploit, lead) only after a nine-face object; **I-261030-18** only if item 2 is killed by size and symmetry helps.

## 5. New ideas (untested proposals, not evidence)

* **N1. Deleted-plane sources from the realized (10, 2) S6 objects** (item 3). Why: they are the only exact arrangements we own with a
  10-face genus-2 solid on 36 adjacent pairs, a family independent of the two (8, 3) sources behind Stage A and E-261113-03.
  Deleting two planes gives a scorable 8-plane rung, deleting one a 9-plane target. Cheapest test: the 8-plane arm of item 3 (minutes).
* **N2. Uniformity lemma.** For a cubic embedded polyhedron, a small generic perturbation of the face planes (and of the plane at
  infinity) keeps every vertex, edge, face and the embedding, since all vertices are simple and embeddedness is open; so the uniform
  asymmetric formulas lose no cubic object. It would remove "non-uniform" from B2-B4 and D3 (`E-261116-05/CONCLUSION.md:27`).
  Cheapest test: item 5 (a), one page; check that no step needs a symmetric arrangement (FD5 objects excluded by hypothesis).
* Re-scored, not new: **I-261103-02** (item 2) was filed 2026-11-03 and never tested; the census wall makes it the natural route now.

## 6. Audit

1. **A pilot cap below the element curve cost a cycle.** E-261114-01 stopped at NO-DAY-RUN with both pilots TIMEOUT at 1200 s (STATUS
   3am); E-261116-02 then decided the same two maps in 2176 and 2526 s monolithic (`E-261116-02/CONCLUSION.md:15-16`). The 2026-11-14
   lead review set that cap. Rule proposal: a pilot cap is at least 3x the expected median at its element count.
2. **Stale target text.** `STRATEGY.md:10-25` and `ROADMAP.md:3-6` still present finished work as current targets; `STATUS.md:3-24`
   has grown into 22 lines of decision history duplicating §0 and the STRATEGY log. Trim to five lines in the applying session.
3. **Weak inputs to the element curve.** The 9-element median comes from the 2 (8, 2) maps, the 11-element one mixes plain stratum C
   and normalised A + B (`E-261116-01/CONCLUSION.md:16-17` says so). This review uses the curve as a scenario, never as a bound.
4. **Good practice.** E-261116-04 met an all-zero outcome with a second-sign control after the run (Szilassi 1 / 307 PASS,
   `E-261116-04/CONCLUSION.md:8-10`), as the 2026-11-01 rule asks; every CONCLUSION names its scope and what was not run.
5. **Process cost.** Five experiments, about 20.6 core-h (8.53 + 3.43 + 7.27 + 1.37), one day, no amendment chain. Repeated caveats
   (no continuous sleep audit, failed `nice: setpriority` starts, `E-261116-02/CONCLUSION.md:13-14`): add the launcher heartbeat (N5 of
   2026-11-16) inside item 3's prep, not as an item. E-261116-05 ran from a dirty tree (`E-261116-05/CONCLUSION.md:10`, inputs hash-matched): the
   launcher should refuse a dirty tree outside documentation.
6. **Chains to stop.** Further S6 (10, 3) solving and polar charts of other realizations; S6 (11, 4) and the (11, 5) asymmetric sweep;
   a `--sat` re-probe of the (11, 5) TIMEOUTs (the 41-night price needs >= 10x to reach the 4-night branch); E-261116-03; any map census
   at (8, 3) or (9, 4) (`strategy-review-2026-11-16b-census-8-3.json`; the enumerator caps extra edges at 8, `census.py:154`).

## 7. Credences (all CONJECTURE, planning weights)

* (10, 4): **0.10 / 0.50 / 0.40 -> 0.03 / 0.87 / 0.10**, re-proposed (2026-11-16 review §7, not applied; no new datum).
* (11, 5) S5 (new row, exists / does not / cannot tell): **0.03 / 0.37 / 0.60**: 4 of 10 UNSAT-SOLVER, 6 TIMEOUT; no sweep affordable.
* S6 (10, 3): **0.25 -> 0.05**: all 20 normalised formulas UNSAT-SOLVER (3as), symmetric formulas too (3ag), 0 of 56137 polar charts
  (3at); the rest is solver, encoder and normalisation soundness (PROVED-1) and non-uniform objects (item 5).
* Nine faces, genus >= 4: **0.55** stays: no datum this week (the census check measures cost, not existence).
* S0: **A 0.20 -> 0.17, B 0.55 -> 0.60, C 0.25 -> 0.23** (as proposed 2026-11-16); one more weak datum in the same direction: at
  (10, 3) the vertex version realizes and the face version fails at solver level.

## 8. Three things to do first

1. Owner: approvals 1 and 2; a yes / no on approval 3. 2. Lab (Opus, medium / gpt-6.1-sol, medium): item 1, minutes of compute.
3. Lab (Opus, high / gpt-6-astra, high): item 2's ladder; item 3's prep (Opus, medium / gpt-6.1-sol, high) for the owner's day run.

## Owner's decisions (2026-11-16)

Approvals 1-3 given ("ok"); applied the same day. Credences of §7 not applied (not asked).
