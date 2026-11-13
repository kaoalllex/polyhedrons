# Strategy review, 2026-11-13: two runs without information; symmetric (10, 3) first, power controls before nights

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep the strategy, change the order. Both runs ended without information by their
   set-up: Stage A has no positive control at nine planes, the (10, 3) night repeated a pilot that had timed out.
2. **Old items 3 / 4 / 5** are independent. 4 and 5 stay; 3 (thin wedges) waits for the cell enumerator (§3).
3. **New fact of this review (EXACT, no solver):** 12 of the 20 (10, 3) maps have automorphisms that pass the
   necessary conditions of a rotation; 9 of them fit the existing symmetric encoder; Lutz #15 has the rotation group
   of the tetrahedron, which leaves a family of plane arrangements with **one real parameter** (§3).
4. **No new brainstorm now**; call one after items 1-2, on one narrow question (§3, Owner 3).
5. **Approval 1: the week plan of §2** (replaces the 2026-11-12 plan; Stage B and wedges move behind gates).
6. **Approval 2: `STRATEGY.md`** (§3, Owner 2): S6 at (10, 3) first, nine faces second; two standing rules.
7. **Approval 3: checked proofs in item 1.** Its PLAN names the negative claim they are for (a STATUS exclusion row
   for the symmetric formulas); the formulas are small. Without your word the UNSATs are UNSAT-SOLVER.
8. **First item:** symmetric S6 (10, 3): the one-parameter family of Lutz #15, then ten symmetric formulas.
9. **Stage B gets no night now**: first the same enumerator one rung below, where an object is known (item 5).
10. **Not done:** no solver run, no literature check of the symmetric vertex-version objects, no human review.

## 1. Scope and checks

Evidence cut: `f8b8e93d` on `lab/2026-11-09`. Labels: `SPEC.md` §5; **Recommendation** marks a judgment. Run here
(seconds, no solver): `reviews/strategy-review-2026-11-13-symmetry.py` (automorphisms of the 20 imported maps, group
orders equal `maps_10_3.json`). Not run: any formula; `verify_all.py --quick` (no code or evidence changed).

## 2. Week plan (ready for `ROADMAP.md`; at most 10 cores, 10 shards, owner launches every run)

1. **Symmetric S6 (10, 3)** (exploit, jump 2; new experiment, PLAN first).
   * (a) Lutz #15, group T: planes `|x| = |y| = |z| = 1` and the four planes `n_i . p = t`; decide every interval of
     `t` (and the coorientation choices) by exact arrangement cells and the solid engine with 42 single adjacencies.
     (b) `omsat.build(..., sym=...)` with `submap=True`: C3 on #1, 2, 4, 8, 14, 15; free C2 on #6, 12, 20 (two
     involutions): ten formulas, kissat, cap 3600 s, proofs checked in the run (approval 3).
   * Budget: one prep session + <= 10 core-h day run. Controls: the free-C2 formula of an eight-face source SAT
     unpinned and realized by the bridge; S0 symmetric CNF hashes unchanged; a wrong determinant sign UNSAT.
   * Kill: a failed control; if the solid engine cannot take the non-simple arrangement of (a), record it and run (b).
     Follow-up: SAT -> at least 6 models by seed, bridge, `--target S6`, `candidate-check`, escalate; all UNSAT-VERIFIED
     -> STATUS exclusion row (these symmetries, general position, formula scope); > 20 % timeouts -> escalate.
     Lab: Opus, high (may meet a SAT model; the symmetric path at 10 faces is new).
2. **(10, 2) rung: time to SAT and bridge rate** (explore; new experiment, PLAN first).
   * Where SAT is known to occur, how fast does kissat find it and how often does a model realize? Lutz's 865 list
     (untrusted data, same importer), 50 maps by a frozen seed, 3 seeds each, cap 300 s, bridge on <= 6 models per
     SAT map; <= 3 core-h. Kill: importer control fails. Realized objects are controls. Lab: Opus, medium.
   * Follow-up: median SAT < 60 s and none after 300 s -> the (10, 3) timeouts read as "probably UNSAT" for planning
     (never a claim), route = item 4; a heavy tail -> propose a seed-portfolio day run on (10, 3) to the owner.
3. **E-261110-05** (old item 4, unchanged row, tree and budget). Lab: Opus, medium.
4. **Cube-and-conquer pilot** (old item 5, unchanged gate on (10, 4) maps 96 and 85). New follow-up: <= 0.5x on
   both -> first use is the eight (10, 3) maps without symmetry (#3, 5, 7, 9, 10, 11, 13, 18), proposed to the owner;
   (10, 4) strata A + B stay behind it. Lab: Opus, medium.
5. **Rung-below cell census, the gate of Stage B** (explore; prep only this week, PLAN first).
   * Delete one plane of Roest-Vigh (one per symmetry class), enumerate all generic cells of the eighth plane
     (rank-4 enumeration, independent Zaslavsky count), time 50 cells, price the run; the run needs the owner.
     The enumerator must reach the known object unaided; SOLID cells are classed by canonical dual map and genus.
   * Kill: count mismatch, or the planted cell is not found. Follow-up: a map other than the source's -> exact
     `--all-pairs`, `candidate-check`, escalate, Stage B proposed; the source map only -> Stage B parked. Opus, high.

Not this week: thin wedges (after item 5's enumerator); Stage B; (10, 4) A + B; an unchanged or longer-cap rerun of
E-261110-02 (D = 0). Harness items of Phase 0 stay between items.

## 3. Answers

* **Owner 1: continue 3 / 4 / 5?** Independent, any order, none is urgent. 4 and 5 keep their value (the mechanism
  of the S5 negatives; cubes for every asymmetric formula, S0 included). 3 is the weakest row of the plan (T = 1).
* **Owner 2: revise the strategy?** No rewrite. Proposed text (not applied): in §1 swap the order ("First: S6 at
  (10, 3), symmetric realizations first, the asymmetric maps only with a changed solver set-up. Second: nine mutually
  adjacent faces; Stage B gated by the same enumeration one rung below"). Add to §2: "**Score a finite family one
  rung below**: before a target run the enumerator runs where an object is known and must find it unaided." and
  "**A pilot can stop a night**: if every pilot unit ends by the cap, the night needs a changed set-up or the owner."
* **Owner 3: a new dialogue with another strong model?** Not now (Recommendation). Ideas are not the bottleneck:
  five nights used about 126 core-h of some 400 available. Useful later and narrowly: if item 1 is all UNSAT and
  item 2 says SAT is fast, ask how to certify UNSAT of 11-element asymmetric formulas on a laptop. Until then a
  second model is worth more as an adversarial reader of the PROVED-1 statements below than as a strategist.
* **Lead a: S6 (10, 3) after 0 of 20.** Changed set-up, in this order: symmetry (item 1), calibration at (10, 2)
  (item 2), cubes (item 4). A longer cap has no growth data behind it. Screening (EXACT computation; conditions
  PROVED-1, this session): a rotation of an embedded polyhedron meets the surface in an even number of points (fixed
  faces, edges and vertices of the automorphism), and two fixed faces are parallel, hence non-adjacent. Result:
  C3 with one fixed face and one axis vertex on #1, 2, 4, 8, 14, 15; free C2 on #6, 12, 20; C2 with two fixed faces
  on #15, 16, 17, 19, 20; excluded: C7 on #8 (three fixed points), C4 on #17 (its square fixes two faces it swaps).
  C3 and free C2 force no zero quadruple (an invariant 4-set is permuted evenly), so the uniform encoder applies; C2
  with fixed faces does not (E-261103-02). On #15 the three involutions fix exactly the three non-adjacent pairs.
* **Lead b, c: crease lemma, pencil lemma versus clauses.** No session: neither changes a decision in the plan.
* **Lead d: 3 of 6 foreign (10, 2) models not realized** (NUMERICAL). Item 2 measures it; until then every SAT map
  gets at least 6 models. It is the first datum for scenario C on a single-adjacency rung.

## 4. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, symmetric S6 (10, 3) (new) | 2 2 2 2 2 | 2 | 1 session + <= 10 core-h | both outcomes are results |
| Item 2, (10, 2) rung (new) | 1 2 2 2 2 | 0 | 1 session + <= 3 core-h | prices every later (10, 3) run |
| E-261110-05 | 2 2 2 2 2 | 0 | 1 session + <= 3 core-h | unchanged |
| Cube pilot (week item) | 1 2 2 2 2 | 0 | 1 session + <= 3 core-h | G up: (10, 3) and E-261101-15 |
| Item 5, rung-below census (new) | 2 2 2 1 2 | 0 | 1 session + a day run | may yield a new eight-face object |
| E-261112-02 Stage B | 2 1 1 1 2 | 2 | 1 session + 2 nights | D down: a miss changes nothing |
| I-261110-01 thin wedges | 1 2 1 2 1 | 2 | 1 session, no parking result | deferred |
| E-261110-06 (10, 4) A + B | 1 1 2 1 2 | 2 | about 6 nights | D down: 757 UNSAT-SOLVER decide nothing |
| E-261110-02 rerun, longer cap | 2 0 2 2 2 | 2 | 20+ core-h | below the gate |
| I-261108-02 certified symmetry breaking | 1 2 1 2 2 | 0 | 1 session | rises if item 1 is all UNSAT |

As filed, no evidence since: E-261101-08, E-261110-01, -03, -04; I-261110-05..07, I-261108-05, -09..11,
I-261103-01..06; H-261112-01, H-261110-01, H-261110-03 stay open. Parked target only (S0): E-261101-03..24 and the
ideas before I-261103 keep the scores of the 2026-11-09 review; nothing ran.

## 5. Queue (after the week plan)

1. **Item 1** (first). H: some (10, 3) map has a symmetric realization. Test: §2. SAT realized -> a result of the
   class of the eight-face objects; all UNSAT-VERIFIED -> exclusion row, the eight asymmetric maps become the target.
2. **Item 2** (explore). H: SAT at this size is found in seconds. Decides between cubes and seed portfolios.
3. **E-261110-05** (explore): do the S5 negatives say anything about single-adjacency targets? **Cube pilot**
   (explore): stop and park if the summed cube time is >= 0.7x monolithic on both maps.
4. **Item 5 run** (explore; owner's day run, <= 20 core-h, priced by its 50 cells). Decides Stage B: one night for
   Roest-Vigh, <= 80 core-h, only if a second map is found.
5. **Asymmetric (10, 3) with cubes** (exploit): only after 1, 2 and 4; proofs if the PLAN names the claim.
6. **Thin wedges, exact replay of K3** (explore): one session after item 5's enumerator; stop if the replay fails.

## 6. New ideas (untested proposals, not evidence)

* **N1. Symmetric realizations of the (10, 3) maps** (item 1 b). Why: the S0 symmetric formulas were decided where
  the asymmetric ones timed out (FD5, FD6); Roest-Vigh's object is symmetric. **N2. One-parameter tetrahedral
  family for Lutz #15** (item 1 a): six octagons in cube planes, four enneagons in tetrahedron planes; four planes
  meet at forced points (e.g. `(1, -1, t)`), so the arrangement is not simple.
* **N3. Rung-below census** (item 5). Why: the only discovery-power control available for a cell family.
* **N4. (10, 2) census as a calibration ladder** (item 2); the full 865 is a follow-up if 50 maps cost < 0.3 core-h.
* **N5. Fixed-face C2 by symmetric arrangements** for #16, 17, 19, 20 (two parallel planes, four plane pairs; with
  the D2 of #20 six parameters). Cheapest test: Szilassi's own C2 at seven planes against the Gaussian rate 6.4e-4.

## 7. Audit

1. **A pilot that could not stop its night.** `experiments/E-261110-02-face-minimal-10-3-decision/PLAN.md:31` starts
   the night "if every control passes"; `:87` records two pilot timeouts; the unchanged night cost 20 core-h (§3).
2. **Stage A has no discovery-power control** (`experiments/E-261112-01-ninth-plane-stage-a/CONCLUSION.md:15-16`),
   against `STRATEGY.md:47-49`. Stage B as queued (`ROADMAP.md:107-109`) would repeat it for two nights.
3. **E = 39 sweeps are void twice.** `ROADMAP.md:183-184`: both nine-plane sweeps fixed E = 39, that is genus 3,
   which the 203 UNSAT-VERIFIED formulas exclude at formula scope. Before Stage A no registered run had E free.
4. **Stale state.** `STATUS.md:15-17` names S6 (10, 3) as the first target since 2026-11-10; `STRATEGY.md:8-17`
   (2026-11-12) says nine faces first. `ROADMAP.md:298` still says "nothing run with E free".
5. **Process cost.** `STRATEGY.md:79-93`: three focus changes in five days; two nights passed without a run.
6. **Chains to stop** (follow-up rule): (10, 4) A + B as a sweep without proofs (`ROADMAP.md:160`); thin wedges
   before an exact replay (`ideas/I-261110-01-wedge-plate-ansatz.md:35-37`: the matching is close to chance).

## 8. Credences (all CONJECTURE, planning weights)

* (10, 3) S6 exists: **0.25 stays** (a timeout moves nothing). Sub-weight for item 1: a symmetric one exists, 0.10.
* Nine mutually adjacent faces, genus >= 4: **0.55 stays** (Stage A: UNSAT-SOLVER on about 8 % of the forecast
  orbits). New working row, a hit inside the two ninth-plane families (H-261112-01): 0.03.
* (10, 4) at 0.10 / 0.50 / 0.40 and the S0 table: unchanged, nothing ran.

## 9. Three things to do first

1. Owner: the three approvals of the digest. 2. Lab (Opus, high): item 1 prep and its day run. 3. Lab (Opus,
medium), one chained session: the preps of items 2 and 3; their day runs share one launch.
