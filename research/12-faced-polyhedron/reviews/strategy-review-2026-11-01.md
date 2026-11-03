# Strategy review, 2026-11-01

Independent senior review of the 12-face (Szilassi-12) research, written against the prompt in
`REVIEW_PROMPT_2026-11-01.md`. The reviewer is an AI session; by `SPEC.md` §5 it is not an independent human
reviewer, so nothing here raises an evidence label. The review changes no file but this one.

**Labels used below.** **[V]** VERIFIED: I checked it in code or data in this session (the commands and
outputs are in Appendix A). **[P]** PLAUSIBLE: follows from documents I read or from an argument I give but did
not machine-check. **[C]** CONJECTURE: my judgement. Third-party statements keep the project's label CLAIMED.

**What I read.** `STATUS.md`, `ROADMAP.md`, `SPEC.md`, `PROTOCOL.md`, `CONTINUE_PROMPT.md`, `results.md`, the
last 120 lines of `experiment-log.md`, `reports/NIGHT_REPORT_2026-11-01.md`, `theory/theory-notes.md`,
`theory/mathematical-model.md` §1-§3, `theory/proof-roadmap.md`, `proof-no-symmetric-immersion/README.md`,
`reviews/fresh-eyes-review.md`, `literature/README.md`, `literature/literature-review.md` §6-§7,
`literature/TODO_world_research_2026.md`, `witnesses/README.md`, `code/README.md`, the seven hypotheses
H-261101-01..07, the READMEs of 14 experiments, and the code of `gauss_gate.py`, `kdrift.py` (header),
`omsat_sym.py`, `local_viol.py`, `nf_control.py`, `ladder.py` (header).

**What I ran.** `verification/verify_all.py --quick`: 13 PASS, 1 SKIP (archive), 11.7 s wall **[V]**. Four
small checks of my own (Appendix A): the chart-dependence of the Gauss gate, the local violations of all 1005
near-miss seeds, the behaviour of `hemisphere_margin`, and the symmetry relation for improper isometries.

---

## 0. Verdict (ten lines)

1. The workflow is sound and unusually honest for a one-person project: exact verifiers, pre-registration, scoped
   labels, a passing one-command suite **[V]**. Keep it.
2. The question is open in both directions; nothing I found moves it. The combinatorics (59 types) and the two
   25/25 certificate sets are reproducible as described **[V]**.
3. The strongest asset is the impossibility toolkit (encoder, controls, DRAT pipeline). The weakest spot is the
   diagnosis of the constructive plateau, part of which rests on a measurement that cannot measure **[V]**.
4. FD6 is overclaimed as stated. The 25 immersion instances cover only automorphisms realised by *rotations*
   (`det rho = eps = +1`); improper isometries never entered any run **[V]**. The gap closes with a short
   geometric lemma (§5.2, **[P]**), so the fix is cheap, but the statement must change before anyone cites it.
5. The "pinned hemisphere margin" (DR2, E-261101-07) is an artefact: `hemisphere_margin` returns exactly 0 for
   every non-hemispheric set, and `kdrift`'s energy asked for a value the function cannot return **[V]**.
6. The Gauss-gate explanation of the type-0 genus-4 plateau survives a projective change of chart on the witness
   I tested (40 charts, `k_tau` never -1) **[V, one realization]**: the obstruction is a property of handle
   ladders at (nearly) fixed planes, not of the affine chart.
7. Next three months: rank-3 per-type SAT first; then join, not duplicate, the exact per-type campaign; then a
   corrected continuation study inside the genus-3 realization spaces. Constructive work only where symmetry is
   still allowed (S1 at 12 faces, genus 7; the (8, 2) object).
8. The exact campaign is affordable: the third party's own estimate (~19,000 core-h, CLAIMED) is about ten days of
   saturated free Actions **[P]**. What must be true first is an agreed, human-reviewed encoding and a proof
   checking policy, not more compute.
9. Publish one short note (FD5 + FD6 with the corrected statement, the type-0 witness as positive counterpart)
   to recruit a human mathematician; the `polyhedraproof` author is the natural first contact **[P]**.
10. Three factual errors with file:line are in §9. None touches the combinatorics or the certificates.

---

## 1. Where should the next three months go? (Q1)

Ranked by expected value of information per unit of effort. Costs assume one owner plus agents, laptop nights
and free Actions. The full table is §7.

### 1.1 Rank-3 (normals-only) feasibility per type, with model counting (ROADMAP E-261101-06, brought to the top)

* **Hypothesis.** At least one of the 59 types is infeasible already at the level of the 12 normals: rank-3
  chirotope of 12 vectors + plane at infinity, gauge `W = +1`, degree -5 at a generic direction, positive
  covering, >= 13 saddles, face-winding `w_X <= 1`, edge-type rule F4, face-turning F6. Rival: every type is
  rank-3 feasible with astronomically many models.
* **Cheapest falsifying test.** Encode once (the clause families exist: `omsat_gauss.py`, `gauss_gate.py`,
  fresh-eyes §2.1), run all 59 types with CaDiCaL; minutes each. Controls: Szilassi normals (n = 7) SAT; the
  normals of the 94 genus-3 realizations SAT for their own sub-maps (target 1 - g); random normals mostly UNSAT.
  Then `#SAT` estimates (ApproxMC) on three types.
* **What each outcome changes.** UNSAT for any type: the first per-type theorem, with a DRAT proof of a formula
  small enough for a human to read the core; it also tells which clause family bites (ablation). All SAT: the
  Gauss class alone kills no type, H-261101-02 is dead at the normal level, and the model count calibrates how
  much cube-and-conquer gains by splitting on the rank-3 contraction first (§2).
* **Cost.** 2-4 agent days, hours of compute. **[C]** My prior: all 59 SAT (the annealers find admissible normals
  in seconds), so the main payoff is calibration, and the result is decisive either way.

### 1.2 Join the exact per-type campaign (E-261101-09 + E-261101-15, merged and brought forward)

* **Hypothesis.** A per-type exact decision costs ~300 core-h (the third-party pilot: 2 formulas, 648.5 core-h,
  31,187 leaves, CLAIMED) and the proofs can be checked on the fly inside 6-hour shards.
* **Cheapest falsifying test.** (a) Compare encoders on three symmetric instances by *predicate equality*, not
  by solver time: evaluate both encoders' predicates on 1,000 random exact configurations (the project already
  has this harness, `omsat_validate.py`) **[P]**. (b) Re-check the two published refutations, if their LRAT files
  or cube lists are public, with `cake_lpr`; map their numbering to ours (`compare_literature.py`). (c) Run one
  trivial-automorphism type as a 256-shard Actions matrix with per-leaf LRAT + `cake_lpr`, discarding checked
  proofs and keeping cube lists, verdicts and hashes.
* **What each outcome changes.** A decided asymmetric type (UNSAT) is the first exclusion of a type and fixes the
  campaign's cost per type to one significant digit. A SAT chirotope is the most interesting outcome of all:
  realise it (12 parameters per plane set, hinge-loss fitting then exact) or prove it non-realizable (biquadratic
  final polynomials by LP). Predicate disagreement between encoders stops everything until resolved.
* **Cost.** One week of agent time, ~300 core-h of Actions. **[P]** Feasible on the free tier: `PROTOCOL.md` §6
  states 4 CPU, 6 h per job, 20 concurrent jobs, i.e. about 1,900 core-h per day.

### 1.3 Repair the obstruction theory of the ladder (E-261101-07 re-scoped, plus the FD6 lemma)

* **Hypothesis ("handles are the wrong move").** No connected component of the realization space of an archived
  genus-3 polyhedron contains a point at which some handle has `k_tau = -1`. Rival: such points exist, and the
  night-4/5 drift missed them because its objective was broken (§5.1).
* **Cheapest falsifying test.** Replace `hemisphere_margin` by a measure that is negative beyond the wall (e.g.
  the signed solid angle of the handle sphere's PL image, continuous in the normals, target -4 pi), then run the
  drift again on the 7 type-0 and 33 type-53 genus-3 realizations with the exact embedding check at every
  accepted step. 1-2 hours of compute per realization.
* **What each outcome changes.** Paths exist: the ladder is revived with a correct objective and the plateau was
  an artefact of the energy. No path, with a proof: the first REFUTED verdict in the project (handle ladders at a
  fixed plane set cannot pass genus 3), which stops a whole family of engines by theorem rather than by budget.
* **Cost.** Two or three sessions. The FD6 lemma (§5.2) is one more session and belongs in the same theory push.

### 1.4 Constructive side line where symmetry is still legal (E-261101-08 + E-261101-12, made concrete)

* **Hypothesis.** All-pairs-adjacent 12-face polyhedra exist once three doubled pairs are allowed (S1, genus 7:
  `E = 69`, `d = 3`, since `d = 6g - 36` must be a multiple of 3 **[V, arithmetic]**), and they are findable
  with a C3 ansatz in which the three doubled pairs form one orbit (four free planes).
* **Cheapest falsifying test.** Calibrate the engine on Roest-Vigh's D2 two-orbit ansatz (must rediscover their
  object from random starts), then run the C3 ansatz for one night. In parallel, (8, 2) with a two-orbit
  ansatz: the 2026 eight-face objects were found exactly this way.
* **What each outcome changes.** An object: the first 12-face polyhedron with every pair adjacent (publishable on
  its own), and the only principled seed for an undoubling ladder (I-261030-09). Nothing after calibration passed:
  evidence that doubling is not the easy relaxation, and E-261101-08 is closed with a power statement.
* **Cost.** One week plus two nights. Keep it under 25 % of compute, as the ROADMAP says.

### 1.5 The lemma factory: realizability audit of SAT models and UNSAT cores (E-261101-05 plus fresh-eyes idea 3)

* **Hypothesis.** OM-level models (the C2 #48 instance without SIMPLE is SAT; rank-3 models from 1.1) are mostly
  non-realizable, so OM-SAT alone cannot decide SAT types and the campaign in 1.2 needs a realizability stage.
* **Cheapest falsifying test.** Hinge-loss fitting of the 12-parameter C2 model; cores of the 80 `r = 0` UNSAT
  instances with ablation by clause family (`q10_core.py`).
* **What each outcome changes.** Realizable models give concrete "near-polyhedra" in the right topological class,
  something no HackerPoet seed is (FD11). Recurring small cores give candidate lemmas. Dense cores: stop mining.
* **Cost.** Two sessions, < 5 core-h.

**Demoted.** E-261101-04 (power study): the fresh-eyes Wendel estimate (~1.6e-10 of a random 9-dimensional
subspace meeting an orthant **[P]**) already predicts that fixed-normal sampling has no power whatever the truth;
spend 2 core-h at radii 0.005-0.02 to confirm the trend, write the estimate into the conclusion, and stop.
E-261101-03 (dossier): keep only the second verifier and the canonical form (§6: the owner's job); the novelty
search is publication hygiene, not research. E-261101-13 and -14 stay below the gate.

---

## 2. Is the impossibility route realistic? (Q2)

**Yes, and it is nearer than the ROADMAP's threshold suggests.** The decision point says "campaign only if the
extrapolation is below ~2,000 core-hours per type" (`ROADMAP.md:70`). The only data point, the third-party pilot,
is ~324 core-h per formula (CLAIMED). The binding constraints are elsewhere:

1. **Encoding soundness, reviewed by a human.** FD2 (Lemma 5.1) and FD4 are PROVED-1 by AI sessions. Two
   independent encodings (ours and `polyhedraproof`) that agree predicate-by-predicate on random exact
   configurations would be strong evidence; a two-page human-checked proof of Lemma 5.1 is the real requirement.
   The project's own `SPEC.md` §5 demands it for a public claim.
2. **Proof handling.** The symmetric cases produced 30-45 MB of DRAT for 60-160 s of solving **[V]**. A 300 core-h
   type checked naively would produce terabytes. The accepted practice (Keller, Schur 5, bbchallenge) is to check
   each cube's proof on the fly with a verified checker, keep the cube list, per-leaf verdicts and hashes, and
   regenerate on demand. Decide this before the first shard.
3. **A plan for SAT outcomes.** An OM-SAT instance that is SAT yields a chirotope, not a polyhedron. In Schewe's
   vertex case all 59 were UNSAT at the OM level; the face version may not be so kind. Prepare the realizability
   stage (numerical fitting, then exact; biquadratic final polynomials for non-realizability) before it is needed.
   **[C]** My estimate: 60-70 % that all 59 types are OM-UNSAT, 20-30 % that some are SAT with non-realizable
   models, under 10 % that a realizable model appears.

**Cost of a credible campaign.** ~19,000 core-h (CLAIMED) is ten days of saturated free Actions, realistically one
to two months with checking overhead and re-runs **[P]**. Coordinating with `polyhedraproof` (whose author asks for
collaborators) halves it and gives two encodings for free.

**Structural lemma killing many types at once.** The only cheap place to look is the normal level (§1.1). The
project's proved invariants (degree -5, >= 13 saddles, `w_X <= 1`, F4, F6, the parity theorem) are all satisfied
by annealed normals within seconds, so **[C]** I expect no type to die there; the value of §1.1 is calibration. A
genuinely new obstruction would have to couple normals and offsets, which is exactly what the UNSAT cores of
§1.5 might reveal. Do not budget on it.

**Cube-and-conquer specifics.** Split on the rank-3 contraction (the 220 signs `chi(X, Y, Z, inf)` in the gauge),
because the fixed-normal inner problem is linear (FD8) and every cube is then "fixed combinatorial normals". The
model count from §1.1 is the number of cubes before symmetry breaking; if it is ~10^6 or less per type, the
campaign is small.

---

## 3. Is the construction route realistic? (Q3)

**Low probability, but two or three concrete, cheap and untried things remain.** What the data say: every known
numerical near-miss is in the wrong topological class (FD11; re-checked, §A.2 **[V]**); genus 3 is robustly
reachable and genus 4 never was; in-class normals exist but their offset problems are UNSAT even at `r = 0`; and
every symmetric S0 ansatz is excluded (FD5). So the search space is the 24-dimensional asymmetric one, and the
realization region, if it exists, is thin in normal directions (the control was SAT at `r = 0.05` and UNSAT at
`r = 0.1`).

Assessment of the classes the prompt names:

* **Partial symmetry not in the 25 classes.** For S0 there is none: any non-trivial isometry group of an embedded
  realization contains a half-turn or a 3-fold rotation (theory-notes §4; results.md Track 2), and both are
  covered **[P]**. Projective symmetries reduce to isometries (idea I-261029-15, **[P]**; I checked the finite-order
  argument only in outline). For immersions, improper involutions are excluded by the lemma in §5.2 **[P]**. So
  "approximately symmetric" is not a constraint class, only a seed choice. Symmetric ansatzes are legal for S1
  (doubled pairs) and for ladder rungs, and that is where they should be used (§1.4).
* **A parametrised family.** The one that exists is the realization space of each genus-3 object: open, with 94
  exact points archived. It has not been explored as a *space*: all climbing engines perturb and re-solve. A
  continuation inside it with a correct objective (§1.3) is the untried parametrised family.
* **Continuation from a degenerate configuration.** A SAT search over *non-uniform* chirotopes (four planes
  through a point allowed) would find degenerate "polyhedra" to perturb from. Untried; **[C]** low prior, because
  the embedding predicates are only proved for general position and a degenerate embedded configuration need not
  perturb to an embedded one. Rank it below §1.3-§1.5.
* **Lifting from a known object.** From Szilassi: impossible, no 7 faces of any type span a punctured torus
  (results.md "No Szilassi embryo", **[P]**). From the 8-face genus-3 octahedra to 12 faces: each new face must
  meet all existing ones in an edge; there is no move in the project's toolkit that does this, and I see no
  natural one. From the type-0 genus-3 witness: this is the ladder, blocked at fixed normals (§1.3 says whether
  it is blocked at all).
* **Projective re-charting of the genus-3 witness (idea P1, DR14).** I tested it: 40 random planes missing the
  solid sent to infinity, exact embedding preserved in all 40, `k_tau` of the three extendable handles stayed 0
  in 119 of 120 cases and was +1 once, never -1 **[V, one realization]**. So this move does not unlock type 0.
  Drop P1 as a constructive idea; keep the result as support for DR3.
* **Realise SAT OM models as seeds (new in the queue).** The C2 #48 instance without SIMPLE is SAT (fresh-eyes
  §2.4). If realizable, it is a C2-symmetric 12-plane configuration with the right local structure and
  non-simple faces, the first seed in the correct topological class. Then break the symmetry and repair the faces
  with the exact inner solver. Cheap (§1.5).

What would break the genus-3 plateau, if anything **[C]**: not another engine on the pair energy, but a move that
changes normals and offsets together while keeping an exact certificate (continuation), or a seed that is already
in class (realised OM model). Both are in §1.3 and §1.5.

---

## 4. Which intermediate goals are worth reaching for their own sake? (Q4)

| Goal | New? | Feasible? | What it teaches about Szilassi-12 |
|---|---|---|---|
| (8, 2): 8 faces, genus 2, 2 doubled pairs | **[P]** open: neither 2026 paper claims it, per the project's partial reads; confirm in the primary texts | Medium. Black-box engines stalled at 1-2 violations at session budgets (E-261029-19); the methods that found (8, 3) were symmetric two-orbit ansatzes with "significant computational resources" (Roest-Vigh, CLAIMED). One night with a symmetric ansatz is the right test | Little directly: doubled pairs are a different local mechanism. Much indirectly: it calibrates the engine that §1.4 needs |
| (9, 3), 3 doubled pairs | **[C]** new | Unknown; harder than (8, 2) | The first case where doubled pairs and genus both grow; a data point for "does doubling get easier with genus" |
| (10, 4), (11, 5) | **[C]** new | (11, 5) is nearly S0 in size (11 planes, 2 doubled pairs) and may be as hard | Most informative of the ladder; (11, 5) is the real analogue |
| 12 faces, S1, genus 7 (3 doubled pairs) | **[C]** new; not in the ROADMAP as such | Symmetric ansatz legal; one night after calibration | Same plane count and normal-space dimension as S0; the natural object for an undoubling ladder |
| Genus-4 analogue of the octahedra (8 faces) | Combinatorially awkward: `E = 42`, average 10.5 sides, 14 extra adjacencies **[V, arithmetic]** | Probably, with more doubling | Almost nothing; skip |
| Publish result 1 (no symmetric embedding) | Reproduction of Moki & Julio 2026 (CLAIMED), independently certified | Ready after the soundness write-up | Credibility; invites review of the encoding |
| Publish result 2 (no symmetric immersion) | **[P]** new, but only for *rotations* until the lemma of §5.2 is written | 2-3 sessions plus one human reader | Shows the symmetric obstruction is local, which guides the asymmetric campaign |

**Recommendation.** Publish 1 and 2 together as one short arXiv note with the corrected statement, the
25 + 25 certificate table, the positive controls, and the type-0 genus-3 witness as a positive counterpart. Its
purpose is to recruit a reader (§6), not to be a result in itself. Of the objects, pursue (8, 2) and S1-12
(genus 7) first; they share an engine. Leave (9, 3) to (11, 5) until that engine has found one of the two.

---

## 5. Are the verdicts and hypotheses right? (Q5)

### 5.1 A verdict built on a measurement that cannot measure: the pinned hemisphere margin

`gauss_gate.hemisphere_margin` (`code/gauss_gate.py:218-230`) solves `max t s.t. V w >= t, |w_j| <= 1` and
returns `min_i <v_i, w/|w|>`, or `t` when `w = 0`. If the six vectors are not in an open hemisphere the optimum
is `t = 0` at `w = 0`, so the function returns exactly 0 **for every such set**, however far across the wall it
is. Check **[V]**: the six octahedron axes `(+-e1, +-e2, +-e3)` return `-0.0` while the true value
`max_w min_i <v_i, w>` is about -0.58; of 200 random 6-vector sets, 105 returned exactly 0, 95 a positive value,
none a negative one (Appendix A.3).

Consequences:

* `kdrift.py` adds `20 * max(0, margin + 0.05)` to its energy (`code/kdrift.py:8-11, 31`), i.e. it asks for a
  margin of -0.05 that the function can never return; once in class the drift carries a constant penalty of 1.0
  that no move can reduce. "Margin pinned at exactly 0" (`reports/NIGHT_REPORT_2026-11-01.md:67, 78`,
  `STATUS.md:58`) is the floor of the function, not a wall.
* The relation itself is a tautology, and `kdrift.py:4` says so in its own header: `k_tau` is the degree of the
  handle sphere spanned by the six normals, which is 0 whenever they lie in an open hemisphere (the PL image then
  misses the antipodal region) **[P]**. So `k_tau = -1` implies "not in an open hemisphere" implies the function
  returns 0: 153/153 was guaranteed.
* **E-261101-07** ("why does every class-reaching drift end at margin 0?", `ROADMAP.md:54`, scored T D = 2 2) is
  therefore answered: by construction. Re-scope it to the question in §1.3 (can the handle normals be pushed
  *past* the wall while the genus-3 object stays embedded?), with a measure that can go negative. The verdict
  for DR2 should read: "k-drift reached the class 153 times; what happened beyond the wall is unmeasured".

### 5.2 A claim stronger than its evidence: FD6 as a statement about all isometries

`proof-no-symmetric-immersion/README.md:9-12` states the theorem for an immersion "invariant under a non-trivial
isometry of R^3"; `STATUS.md:25` and `STATUS.md:101` repeat it ("stronger than Moki & Julio's embedding
statement"). The 25 instances impose `chi(gS) = eps(g) chi(S)` with `det rho(g) = eps(g)` by construction
(`code/omsat_sym.py:9-13`, `build_sym` at `:339-351`), and every C2 class has `eps = +1` (`results.md`, Track 2,
observation 1: no type has an orientation-reversing involution). So every instance models a *proper* rotation.
For an embedding this is complete, because an improper isometry preserves the solid and hence reverses the
surface orientation, and no such automorphism exists **[P]**. For an *immersion* there is no solid, and a mirror
or a point reflection may well induce an orientation-preserving involution; that case was never run **[V]**.

It cannot be run with the present encoder either: with `eps = -1` on the involution, `sym_consistency` reports
15 forced-zero quadruples per C2 class (checked on Lutz #36, #48, #59 **[V]**, Appendix A.4), i.e. the symmetric
configuration is never in general position, and the uniform-chirotope machinery does not apply.

The gap closes by hand **[P, reviewer's argument; needs a second reader]**. Let `g` be an improper involution
realising an automorphism; it acts freely on faces (results.md Track 2, observation 2), so `g(a) != a` for every
face `a`, and all 12 planes are distinct (adjacent faces are not coplanar, model §2).

* *Point reflection* `g = iota`: `iota(a)` has the same normal and opposite offset, so `a` and `iota(a)` are
  parallel or equal; equal is excluded, and parallel planes share no edge, yet every two faces are adjacent.
* *Mirror* `g = sigma` in the plane `Pi`: the line `L = a ∩ sigma(a)` is `sigma`-invariant, so `L ⊂ Pi` or
  `L ⊥ Pi`. If `L ⊥ Pi`, then `sigma(a)` contains both `L` and the fixed line `a ∩ Pi`, which span `a`, so
  `sigma(a) = a`: excluded. Hence `L ⊂ Pi` is fixed pointwise. The edge `e_{a, sigma a} ⊂ L` has endpoints
  `P_{a, sigma a, c}` and `P_{a, sigma a, c'}` where `{a, sigma a, c}` and `{a, sigma a, c'}` are the two
  triangles on that edge. `sigma` maps the first triangle to `{sigma a, a, sigma c}`, which must be one of the two;
  `sigma c = c` is excluded, so `sigma c = c'`, and the second endpoint is `sigma` of the first. Both lie on the
  pointwise-fixed `L`, so they coincide: a zero-length edge, excluded by `SPEC.md` §3.

Order-4 improper elements (rotoreflections) have a proper half-turn as square and are covered by the C2
instances; orders 5, 7 and 11 do not occur in any automorphism group (orders are 1, 2, 3, 4, 6, 12, `results.md`
Track 2) **[V, from the table]**. With this lemma written and checked, the theorem as stated holds; without it,
state it for rotations. Add the lemma to the write-up (E-261101-10) and to `STATUS.md` FD6 as a caveat until then.

### 5.3 Smaller overstatements

* `STATUS.md:30` (FD11): "all 1005 ... have the wrong Gauss degree and are not immersions (>= 7 vertices with two
  reflex corners each)". Re-check of all 1005 seeds with `local_viol.local_violations` **[V]**: multi-reflex
  vertices min 4, median 14, max 22; three seeds have fewer than 7 (two with 4, one with 6); none has 0; no seed
  is an immersion. And `results.md` (PI addendum) records 12 seeds whose own gauge has degree -5 but fails
  covering. Correct wording: "all 1005 fail the Gauss class (degree or covering) and have >= 4 multi-reflex
  vertices; none is an immersion". The source of the ">= 7" is `results.md`, where it was stated for the first
  300 seeds only. `STATUS.md:61` (DR5) inherits the wording.
* `hypotheses/H-261101-07-maximal-face-neighbourly-exist.md:19`: "(8, 2) ... untested" contradicts E-261029-19
  and `STATUS.md:71` (DR15): the n = 8 genus-2 rung with two doubled pairs *is* (8, 2) (`code/ladder.py:4-6`
  **[V]**) and plateaued at 1-2 violations. The honest status is "tested only by black-box engines at session
  budgets, no symmetric ansatz, no attempts saved" (`literature/TODO_world_research_2026.md`, item 3): underpowered,
  not untested.
* `theory/theory-notes.md:160, 246`: "normals mod GL(3) = 15 dims" should be 16 (fresh-eyes §1.3); not corrected.
* `STATUS.md:59` (DR3): "k_tau = 0 on 21/21" is 7 realizations x 3 extendable handles of one map, not 21 handles
  **[V]** (`experiments/E-261030-06-gauss-gate/results/gate/results.jsonl`, 7 type-0 records; `arms_of` returns 3
  arms for the witness). Not wrong, but say so; and add the chart-independence check of §A.1 as support.

### 5.4 Underpowered verdicts

* **DR15 / DR6 on (8, 2)** (above): the positive-control rule of `PROTOCOL.md` §3 was not applied; the methods
  that succeeded on (8, 3) were never tried on (8, 2).
* **DR2** is correctly labelled low-power by the project; §5.1 makes the drift part of it unmeasured as well.
* **DR8** ("8/8 timeouts at 2.2 h") is correctly OPEN. Note that 2.2 core-h is 1/150 of the claimed per-type cost;
  it says nothing about feasibility.
* **DR4** (closure-first) and **DR16** are fairly labelled.

### 5.5 Are H-261101-01..07 the right rivals?

Keep 01, 02, 05, 06 (with the threshold of 06 rewritten, §2). Restate 03 precisely (§8). Demote 04 to a
calculation (Wendel estimate plus a 2 core-h check). Correct 07's evidence line. Missing rivals, each with the
experiment that discriminates it:

| New hypothesis | Rival to | Discriminating experiment |
|---|---|---|
| **H-R1 Thin realization region.** The S3/S0 realization regions are so thin in normal directions that any fixed-normal or normals-first scheme has near-zero power regardless of existence | H-04 | E-261101-04 at radii 0.005-0.02 compared with the Wendel estimate; if the control SAT rate at `r = 0.02` is below ~10 %, H-R1 holds and normals-first is retired by theory |
| **H-R2 OM-SAT but non-realizable.** For some types the OM instance is SAT and every model is non-realizable | H-01, H-06 | E-261101-15 on two types; the realizability audit of the C2 #48 no-SIMPLE model (§1.5) |
| **H-R3 Handles are the wrong move.** No component of a genus-3 realization space reaches `k_tau = -1` | H-03 | §1.3 with a non-saturating measure and exact checks |
| **H-R4 No improper symmetric immersion** (the lemma of §5.2) | FD6 as stated | a second reader; no compute |
| **H-R5 Rank-3 feasibility excludes no type** | H-02 | E-261101-06 (§1.1) |
| **H-R6 S1-12 exists at genus 7 with a C3 orbit of doubled pairs** | H-07 | §1.4 |

### 5.6 Prior work that already answers something or makes an item redundant

* **`polyhedraproof` (Pirozhkov, CLAIMED):** two of the 59 formulas refuted with cube-and-conquer and `cake_lpr`
  (`literature/literature-review.md` §7.2). If the certificates or cube lists are public, re-checking them is a
  day's work and would make two types third-party-certified; the type mapping is needed first. This makes a
  from-scratch pilot on those two types redundant, and E-261101-09 should start by exchanging predicate tests,
  not timings.
* **Moki & Julio 2026 (CLAIMED):** 36 instances including larger groups; our 25 cyclic classes imply theirs for
  embeddings **[P]**. The overlap check in E-261101-10 is a table, not work.
* **Bokowski & Kevin H. 2025 (CLAIMED, Sec. 4 and 8.3 unread):** numerical search over the 59 dual types, no
  embedding found; the conjecture that embeddable regular maps embed symmetrically. The review's warning stands:
  the sentence about "neighborly oriented matroids ... the empty set" most likely concerns the vertex version;
  read §8.3 before citing. Nothing there answers our question.
* **Schewe 2010 (CLAIMED):** settles the vertex version only; polarity does not transfer (idea I-261029-41 is
  correctly parked).
* **Map censuses (Conder; Wedd):** only for the novelty check of the genus-3 witness; irrelevant to the main
  question. Sulanke-Lutz enumerations may cover 12-vertex genus-3 triangulations **[C, not checked]**.

---

## 6. How should the work be organised? (Q6)

**The owner personally.**

1. **Write the second verifier.** `verify_candidate.py` is the only success criterion and has one implementation
   family (FD10 caveat). A verifier written by the owner from `SPEC.md` §1 alone, in a different representation
   (vertex coordinates and polygons, as E-261101-03 step 1 specifies), without reading `ladder_exact.py`, is the
   one place where a software engineer adds genuine independence. Mutation tests (`test_mutants.py`) into
   `verify_all` the same week.
2. **Gatekeeping.** Approve every `PLAN.md` before compute; read every `CONCLUSION.md`; own the labels in
   `STATUS.md`. Agents drift towards overclaiming (§5.2 is an example); the owner is the brake.
3. **External contact and publication logistics**: e-mails, Zenodo DOI, the arXiv note (an agent drafts, the owner
   sends), the tag before any external review.
4. **Compute operations**: laptop nights under `caffeinate`, the Actions matrix, storage of certificates.

**Delegate to agents.** Encoders and their validation harnesses; experiment runners with manifests; literature
extraction with exact citations (never from digests); draft proofs labelled PROVED-1; data analysis; the
write-up draft; infrastructure tickets in `ROADMAP.md` Phase 0. Rule of thumb: agents produce artefacts that a
checker can reject (code with controls, proofs with labels, tables with hashes); they do not decide what is true.

**Needs an outside human mathematician.** Review of Lemma 5.1 and the clause-family soundness proofs (the
precondition for any CERTIFIED public claim); the §5.2 lemma; the theorem statement of FD6; the realizability
stage if a SAT chirotope appears (final polynomials are a specialist's tool). Candidates, in order **[P, as of my
knowledge; verify current affiliations]**:

1. **A. Pirozhkov** (`polyhedraproof`): working on exactly this reduction, publicly asking for collaborators;
   shared instances and two encodings for free. First e-mail: one page, the CNF hashes of three shared symmetric
   instances, one question (do our predicates agree?).
2. **J. Bokowski** (TU Darmstadt, emeritus) or **U. Brehm** (TU Dresden): the realization experts for oriented
   matroids and small polyhedral surfaces; the natural readers of the write-up and of a SAT chirotope.
3. **M. Heule** (CMU): for the campaign design (cube-and-conquer, proof policy); a short technical question is
   usually answered.
4. **L. Schewe** (Edinburgh), **F. Lutz** (TU Berlin), **G. Roest and V. Vigh** (Szeged): the vertex-version
   method, the triangulation data, and the only people who have built 8-face all-adjacent polyhedra.

Send a two-page note with exact statements and hashes, not a repository link; ask one question per e-mail.

---

## 7. Ranked table of directions

| Rank | Direction | Hypothesis | Cheapest falsifying test | Cost | Decision value |
|---|---|---|---|---|---|
| 1 | Rank-3 per-type SAT + model counts (E-261101-06) | some type is infeasible at the normal level | 59 instances, minutes each, with Szilassi and genus-3 controls | 2-4 days, hours of CPU | High either way: a theorem, or the cube budget for rank 3 splitting |
| 2 | Join the exact campaign (E-261101-09 + -15) | per-type cost ~300 core-h; on-the-fly LRAT fits 6-h shards | predicate equality of two encoders; re-check the two published refutations; one type on a 256-shard matrix | 1 week + ~300 core-h | Fixes the campaign cost to one digit; first asymmetric exclusion or a chirotope to realise |
| 3 | Corrected continuation inside genus-3 realization spaces + the FD6 lemma (E-261101-07 re-scoped) | no component reaches `k_tau = -1` | drift with a non-saturating measure, exact checks, 40 realizations | 2-3 sessions, ~40 core-h | Revives the ladder or refutes it by theorem; closes the FD6 gap |
| 4 | S1-12 at genus 7 with a C3 orbit; (8, 2) with a two-orbit ansatz (E-261101-08 + -12) | all-adjacent 12-face objects exist with 3 doubled pairs | calibrate on Roest-Vigh, one night each | 1 week + 2 nights | A publishable object and the only in-class seed for undoubling; or a closed side line |
| 5 | Realizability audit of SAT OM models; UNSAT cores at `r = 0` (E-261101-05 + fresh-eyes idea 3) | OM models are mostly non-realizable | hinge-loss fit of the C2 #48 model; 80 cores with ablation | 2 sessions, < 5 core-h | Tells whether SAT outcomes in rank 2 are actionable; candidate lemmas |
| - | E-261101-04 power study | normals-first UNSATs are real evidence | 2 core-h at r <= 0.02 + the Wendel estimate | 2 core-h | Low: theory already predicts the answer |
| - | E-261101-03 dossier | witness correct and new | second verifier (owner), canonical form | 1-2 days | Hygiene; required before publication |

---

## 8. Revised hypothesis table

| Id | Statement | Rival | Status | Moves it |
|---|---|---|---|---|
| H-261101-01 | Szilassi-12 exists (some asymmetric realization of one of the 59 types) | no type is realizable | open | an S0 PASS; per-type decisions |
| H-261101-02 | a short structural obstruction kills many types | obstructions are per type and couple normals with offsets | open, **[C]** unlikely at the normal level | E-261101-06; UNSAT cores |
| H-261101-03 (restated) | **at a fixed plane set, no handle can be attached to an embedded genus-3 polyhedron: the six handle normals of an in-class handle must leave every open hemisphere, and this is incompatible with the embedding of the base object** | in-class handles are reachable inside the realization space; the drift failed for other reasons | open; prior evidence partly artefactual (§5.1); chart-independent on one witness **[V]** | §1.3 with a correct measure |
| H-261101-04 (demoted) | normals-first UNSATs carry evidence about the next level | H-R1: the realization region is too thin for fixed-normal sampling to have power | **[P]** rival favoured by the Wendel estimate | a 2 core-h check, then close |
| H-261101-05 | the type-0 genus-3 object is correct and new | verifier bug or known object | open | owner's second verifier; map census |
| H-261101-06 (rewritten) | a per-type exact decision costs ~300 core-h and its proof can be checked on the fly inside 6-h shards | cost or proof size is an order of magnitude worse | open; one CLAIMED data point | E-261101-15 on one type |
| H-261101-07 (evidence corrected) | maximal face-neighbourly cubic polyhedra exist for genus 2-5 | they stop below genus 6 | open; (8, 2) tested only by black-box engines at session budgets | symmetric ansatz on (8, 2) |
| H-R1 | thin realization region (see 04) | sampling was merely unlucky | **[P]** | E-261101-04 at small radii |
| H-R2 | some types are OM-SAT with only non-realizable models | all 59 are OM-UNSAT, as in the vertex case | open | E-261101-15; realizability audit |
| H-R3 | handles are the wrong move (see 03) | continuation paths exist | open | §1.3 |
| H-R4 | no immersion has an improper symmetry (lemma §5.2) | a mirror-symmetric immersion exists | **[P]** proved in outline here | a second reader |
| H-R5 | rank-3 feasibility excludes no type | at least one type is rank-3 UNSAT | **[C]** | E-261101-06 |
| H-R6 | S1-12 exists at genus 7 with a C3 orbit of three doubled pairs | the smallest all-adjacent 12-face object needs more doubling | open | §1.4 |

---

## 9. Errors and overclaims found

| # | Where | What | Severity |
|---|---|---|---|
| 1 | `proof-no-symmetric-immersion/README.md:9-12`; `STATUS.md:8-9, 25, 101` | FD6 stated for "a non-trivial isometry"; the runs cover rotations only (`code/omsat_sym.py:9-13, 339-351`); improper involutions need the lemma of §5.2 **[V]** | High for the write-up; fix the statement or add the lemma |
| 2 | `code/gauss_gate.py:218-230`; `code/kdrift.py:8-11, 31`; `reports/NIGHT_REPORT_2026-11-01.md:67, 78`; `STATUS.md:58`; `ROADMAP.md:54` (E-261101-07) | `hemisphere_margin` returns 0 for every non-hemispheric set; the drift's target -0.05 is unreachable; "pinned at exactly 0" is a floor and a tautology **[V]** | High for DR2/DR3/E-07; re-scope E-07 |
| 3 | `STATUS.md:30` (FD11), `STATUS.md:61` (DR5) | ">= 7 multi-reflex vertices" false for 3 of 1005 seeds (min 4); "wrong Gauss degree" false for 12 seeds that fail covering instead; conclusion "none is an immersion" holds **[V]** | Low; wording |
| 4 | `hypotheses/H-261101-07-maximal-face-neighbourly-exist.md:19` | "(8, 2) untested" contradicts E-261029-19 and `STATUS.md:71` **[V]** | Low; should read "underpowered" |
| 5 | `theory/theory-notes.md:160, 246` | "15 dims" should be 16 (fresh-eyes §1.3) | Trivial |
| 6 | `ROADMAP.md:70`, `STATUS.md:64`, `hypotheses/H-261101-06-...:3, 11` | the 2,000 core-h gate is already met by the only (CLAIMED) data point; the real gates are encoding agreement and proof policy | Medium; decision criterion mis-specified |
| 7 | `STATUS.md:59` (DR3) | "21/21" is 7 realizations x 3 handles of one map; the statement is about one map and one chart (now 40 charts, §A.1) | Low; scope |

No error was found in the combinatorics (59 types, 25 classes = 21 C2 + 4 C3, re-derived from the automorphism
table **[V]**), in the certificate records, or in the exact witnesses re-run by `verify_all`.

---

## 10. Three things to do first next week

1. **Correct the two artefacts in writing, before any new compute.** Re-word FD6 (rotations only, or add the §5.2
   lemma to E-261101-10 and have one human read it); re-scope E-261101-07 and the DR2 row; fix FD11 and H-07's
   evidence line. One session, no compute. Everything downstream (write-up, external e-mail) depends on it.
2. **Run rank-3 per-type SAT on all 59 types** (§1.1) with the three controls, and record the model-count estimate
   for three types. Two to four agent days. This is the cheapest experiment in the queue with a decisive outcome
   on both branches, and it sets the splitting strategy for the campaign.
3. **Send the first external e-mail** to the `polyhedraproof` author: three shared symmetric instances with CNF
   hashes, the predicate-equality harness, and one question. In parallel, let an agent write the predicate
   comparison (E-261101-09 step 1). The owner writes and sends; nothing else in Q6 can start before a reply.

---

## Appendix A. Checks run in this review

All in the venv `~/.venvs/polyhedra`, from `research/12-faced-polyhedron/`, 2026-11-01. Scripts lived in the
session scratchpad; the essential calls are inlined so they can be repeated.

### A.1 Chart-dependence of the Gauss gate (`k_tau`) on the type-0 witness

Input: `experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable_polished.json`.
`gauss_gate.arms_of(H, tris, 12)` returns 3 extendable arms. For 40 random planes `pi = (m, c)` with
`m . v + c >= rel * span > 0` on all 44 vertices (`rel` uniform in 0.02-1.0), the projective map with matrix
`A = [[I_3, 0], [m, c]]` was applied to the planes (`H' = H A^{-1}`), the result re-verified with
`ladder_exact.verify(H', links, require_all_pairs=False)`, and `k_tau` recomputed with
`gauss_gate.k_tau(int_normals(H'), own_gauge(H', links_M), oM, oR)` for each arm.

Result: EMBEDDED in 40/40 charts; `k_tau` histogram over 120 (chart, arm) pairs: `{0: 119, +1: 1}`; never -1.
Own chart: `(0, 0, 0)`. Runtime 2.6 s. Scope: one realization, one map, 40 charts.

### A.2 Local violations of all 1005 HackerPoet seeds

`overnight/data/seeds.json` (1005 records, planes and triangles as JSON strings);
`local_viol.local_violations(H, links_from(coherent_triangles(tris), 12))` per seed, 1.4 s total.

Result: multi-reflex vertices min 4, median 14, max 22; 3 seeds below 7 (histogram `{4: 2, 6: 1, 7: 2, 8: 109,
...}`); 0 seeds with 0 multi-reflex vertices; 0 seeds with 0 crossings and 0 multi-reflex vertices.

### A.3 `gauss_gate.hemisphere_margin` cannot be negative

`hemisphere_margin([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])` returns `-0.0`; a 20,000-point grid
over unit `w` gives the true `max_w min_i <w, v_i>` as about -0.58. Over 200 random 6-vector sets: 105 values
exactly 0 (`|x| <= 1e-9`), 95 positive, 0 negative.

### A.4 Improper isometries in the symmetric encoder

For Lutz maps #36, #48, #59, C2 class 0: `omsat_sym.sym_consistency(H, eps)` returns 0 forced-zero quadruples with
the run's `eps = +1`, and 15 with `eps = -1` on the involution (the quadruples `{a, g a, b, g b}`): a
mirror- or inversion-symmetric configuration is never uniform, so the 25 instances cannot model it.

### A.5 Evidence suite

`~/.venvs/polyhedra/bin/python verification/verify_all.py --quick`: 13 PASS, 1 SKIP (archive check), ALL PASS,
11.7 s wall.
