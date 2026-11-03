# Strategy review, 2026-11-03

Independent senior review of the research under the new `STRATEGY.md` (focus S5 at (9, 3), stretch (10, 4), S0 parked),
written against `REVIEW_PROMPT_2026-11-03.md`. The reviewer is an AI session; by `SPEC.md` §5 it is not an independent
human reviewer, so nothing here raises an evidence label. The review changes no ledger file; it adds this report and two
reproducibility files in `reviews/` (the sampler script and the sampled maps, Appendix A).

**Labels.** **[V]** VERIFIED: checked in code or data in this session (commands and outputs in Appendix A). **[P]**
PLAUSIBLE: follows from documents read or from an argument given here but not machine-checked. **[C]** CONJECTURE: my
judgement. Third-party statements keep the project's label CLAIMED.

**What I read.** `STRATEGY.md`, `STATUS.md`, `ROADMAP.md`, `SPEC.md`, `PROTOCOL.md` §2 and §8a, `CONTINUE_PROMPT.md`,
`reports/NIGHT_REPORT_2026-11-02.md` and `-03.md`, the `CONCLUSION.md` of E-261101-23, -25, -07, E-261102-01, -03, -04,
`reviews/strategy-review-2026-11-01.md`, `literature/review-2026-11-03.md` (project notes first), `literature/README.md`,
`literature/primary-reads-2026-11-01.md`, `map/graph.json` (253 nodes: 90 open ideas, 25 open hypotheses, 19 planned
experiments), the READMEs of E-261101-12, -16, -22, -26, E-261029-19, E-261030-01, the hypotheses H-261101-07, -10, -17,
H-261029-07, the ideas I-261103-01, I-261101-20, -07, -08, -14, I-261030-07, -11, -19, and the code of
`verify_candidate.py` (S5 branch), `ladder_exact.verify`, `control_rost_vigh.py`, `enum_k12.c` (header), `omsat.py`
(header), `omsat_sym.py` (header), `solid_first.py`, `solid_cpsat.py`, `genus_ladder.py`, `tubes.py`,
`theory/mathematical-model.md` §5.

**What I ran.** `verification/verify_all.py --quick`: 15 PASS, 1 SKIP (archive), ALL PASS, 13 s **[V]**. A flip-walk
sampler of face-neighbourly triangular maps (the dual maps of S5 candidates) with four controls, about 25 minutes of
single-core compute in runs of at most 4 minutes each (Appendix A). Its results drive sections 1-3.

---

## 0. Verdict (ten lines)

1. **The move to S5 at (9, 3) is right, and the evidence of this session makes it better than the owner knew.** The
   candidate maps exist and are few: a random walk saturates at **240** isomorphism classes of (9, 3) maps, of which
   **203** survive the cheapest geometric filter, **8** admit a C3 rotation and **2** of those a D3 action **[V, sampled;
   completeness C]**. The (8, 2) case has **2** candidate maps, both C2-symmetric **[V, sampled]**. (10, 4) has several
   hundred (113 seen in 3 minutes, unsaturated) **[V]**.
2. The decisive consequence: at 9 planes the full exact pipeline (map census, OM-SAT per map with a 10-element rank-4
   chirotope of 210 bases, realization or final polynomial) is affordable on the laptop, map by map. (9, 3) can be
   **decided**, not just searched. That is the dress rehearsal of the S0 pipeline at a size where it completes **[P]**.
3. The "jump, do not climb" stance is justified for (10, 4) and S0, **not for (9, 3)**: the target genus is 3, below the
   claimed ravine, and the genus-ladder engine passes R5 at genus 3 in half the seeds. For (9, 3) the ladder on 9 faces is
   the cheapest geometric engine and should run as the explore item, not be parked **[V, from STATUS 3b]**.
4. `STRATEGY.md` conflates two facts (section 6, finding 1): night 7 shows that no engine reaches genus 3 *from random
   planes*; it says nothing about genus 3 to 4. The ravine rests on DR1's genus-4 failures (LOW-YIELD) and on k_tau = 0 on
   one map (7 realizations x 3 arms) **[V]**.
5. The OM-SAT encoder cannot express doubled adjacencies (`STATUS.md` 3b). That is the one infrastructure gap between the
   project and an exact S5 decision; it is the second item in the queue.
6. Keep (9, 3) as the headline, but run (8, 2) first *on the exact side*: two maps, hours of compute, the first complete
   decision of a face-neighbourly case either way, and the calibration of every S5 tool on the two (8, 3) objects **[C]**.
7. No S0 evidence arrived since 2026-11-01; the S0 credences stay. Proposed S5 credences: (9, 3) exists 0.40 / does not
   0.35 / cannot tell 0.25; (8, 2) 0.25 / 0.55 / 0.20 **[C]**.
8. Novelty: nothing at (8, 2) to (11, 5) is in print (CLAIMED, secondary search); these objects are necessarily
   *non-equivelar* (2E/F is not an integer), so the equivelar literature cannot contain them **[V, arithmetic]**.
9. Audit: one conflation in `STRATEGY.md`, one state inconsistency in `ROADMAP.md`, one wording gap in `SPEC.md` S5
   (tripled adjacencies), one robustness bug in `ladder_exact.verify` that the S5 pipeline will hit, and three follow-up
   chains to stop (section 6).
10. First item: **the pre-registered census of (7, 1), (8, 2), (9, 3), (10, 4) candidate maps with controls**, two
    sessions, minutes of CPU; everything geometric waits for it.

---

## 1. Is (9, 3) the right focus? (Q1)

### 1.1 The cases side by side

Counts of maps are from the sampler (Appendix A.3-A.5); "admissible" = every corner triple distinct (section 2.1).
Dimensions: F planes have 3F parameters; the projective group removes 15; OM elements = F planes + the plane at infinity.

| Case | V, E | extra adj. | candidate maps (sampled) | admissible | symmetric admissible | free params | OM bases | our engines at this genus | novelty | value for S0 |
|---|---|---|---|---|---|---|---|---|---|---|
| (8, 2) | 20, 30 | 2 | **2** (saturated in 20 s) **[V]** | 2 | both C2 (half-turn, 6 fixed edges); the |Aut+| = 6 map's C3 fixes 2 faces, not realizable by an isometry **[V, P]** | 9 | 126 | genus 2 reached routinely at 12 faces; (8, 2) itself only by black-box engines at session budgets (E-261029-19, underpowered) | new (CLAIMED absent) | low directly; high as pipeline calibration |
| **(9, 3)** | 26, 39 | 3 | **240** (saturated, 5 walks) **[V]** | **203** | 8 with a free C3 (2 of them D3), 24 with an involution, 0 reflexible | 12 | 210 | genus 3 reached from parents (R5 5/10), never from random planes (R4 0/26 pooled) | new | the full exact pipeline at a size where it finishes; a second data point for the structural priors (convex vertices, spikes) |
| (10, 4) | 32, 48 | 3 | >= 113 in 3 min, Chao1 ~460 **[V, C]** | >= 106 | 4 with an involution, no C3 or C5 seen | 15 | 330 | never reached (ten engines, nights 3-5) | new | the first crossing of the ravine, if it is one |
| (11, 5) | 38, 57 | 2 | not sampled | - | - | 18 | 495 | never | new | nearly S0 in size |
| (12, 6) = S0 | 44, 66 | 0 | 59 (FD3) | 59 | FD5: none realizable symmetric | 21 | 715 | genus 3 | open in print | the defining problem |

**What I could not check.** Whether Roest-Vigh or Mizhaev tried (8, 2) or (9, 3) (not in the texts read; ask them,
section 3 item 7); the Roest-Vigh method paper they announce; Arseneva et al. 2024 (the question's source, not read);
Grunbaum-Szilassi 2009 (genus 1 only, abstract). The claim "no (8, 2) to (11, 5) object in print" is an AI-written secondary
search (CLAIMED) and stays unverified scope. One arithmetic fact closes part of the gap **[V]**: 2E/F = 7.5, 8.67, 9.6,
10.36 for the four cases, so none of them is equivelar, and the equivelar censuses (McMullen-Schulz-Wills, Brehm-Wills,
Schulte-Wills) cannot contain them. The remaining E-261101-22 reads are hygiene for (7, 1) and S0, not for the focus.

### 1.2 Recommendation

**Keep (9, 3) as the focus target.** It is the smallest case that is new, non-trivial (203 maps) and decidable with our
tools; (8, 2) is too small to be a programme (2 maps) and (10, 4) is where the engines have no pass. But change the order of
the first week: **decide (8, 2) first, on the exact side**, because its two maps cost hours, the result is a theorem either
way ("no 8-face genus-2 face-neighbourly polyhedron" would be the first non-existence result for a face case), and every
S5 tool (encoder, realizer, symmetric clauses, `--target S5`) is calibrated on the two (8, 3) objects on the way. This is
within `STRATEGY.md` §1 ("worth doing only if it costs less than a session or calibrates the (9, 3) method"): it does both.

**What would make me switch.**
* To (8, 2) as the headline: nothing; two maps are a lemma, not a focus.
* To the symmetric subset of (9, 3) only: if the per-map OM-SAT decision takes more than about an hour median at 10
  elements (then 203 maps are a campaign, 8 are a night).
* To (10, 4): if (9, 3) is decided either way within two weeks; take the census count and the symmetric sub-list along.
* Back to S0: a (9, 3) realization found by a method that passes R4 (full genus-3 map from random planes), or a (9, 3)
  non-existence proof whose UNSAT cores show a structure that recurs across maps (then H-261101-02 for S0 revives).

---

## 2. How do we find a (9, 3) object? (Q2)

### 2.1 Combinatorics first: the candidate maps

**Definition.** The dual of an S5 polyhedron at (F, g) is an oriented triangular map with F vertices, E = 3(F + 2g - 2)
edges and 2E/3 triangles, loopless, whose underlying simple graph is K_F; the E - C(F, 2) extra edges are parallel copies
(a pair may share 2 or more edges). This is a map with multiple edges, not a simplicial complex, so the simplicial censuses
miss it (`literature/review-2026-11-03.md` note 2, confirmed).

**What the sampler found [V]** (Appendix A; walk = Metropolis random walk on edge flips over all triangular maps with the
given (V, g), loops and multiple edges allowed, objective = non-adjacent pairs + 2 x loops; hits canonicalised by a BFS
code, minimum over all 2E roots and both orientations, and re-checked by an independent surface check):

| (V, g) | classes found | runs | saturation evidence | admissible (distinct corner triples) | |Aut+| histogram (admissible) | reflexible (admissible) |
|---|---|---|---|---|---|---|
| (7, 1) control | 1 | 3 | the Csaszar-Mobius K7 torus, |Aut+| = 42, chiral: correct | 1 | 42: 1 | 0 |
| (8, 2) | 2 | 2 | every class seen > 3,600 times | 2 | 6: 1, 2: 1 | 0 |
| (9, 3) | **240** | 5 (seeds 1-5, 90-240 s) + 1 from a Roest-Vigh-derived start | identical code sets in all walks; 99 % of classes by 27 s of a 240-s run; every class seen >= 9 times | **203** | 1: 173, 2: 22, 3: 6, 6: 2 | 0 |
| (10, 4) | 113 | 1 (180 s) | not saturated: 99 seen once, Chao1 ~460 | 106 | 1: 102, 2: 4 | 0 |
| (8, 3) control | 22,666 | 1 (150 s) | far from saturated; the Roest-Vigh and Mizhaev dual maps (built from their planes, |Aut+| = 8 and 2) were not among them: a power statement about the walk at 8 extra edges, not a failure | - | - | - |
| (12, 6) control | 0 hits in 120 s | 1 | the walk finds no neighbourly 12-vertex map in 2 min; the 59 types canonicalise to 59 distinct codes with |Aut+| in {1, 2, 3, 4, 6, 12} and 6 reflexible, as in FD3 | - | - | - |

Reading. The flip graph of triangulations of a surface with a fixed set of marked points (loops and multiple edges allowed,
i.e. ideal triangulations) is connected **[P, classical: Mosher 1988, Hatcher 1991; citation from memory, verify]**, so the
walk is ergodic in principle, and the saturation at 240 from six independent starts is strong evidence that **240 is the
complete count up to isomorphism and mirror [C, to be proved by the census]**. The count 2 at (8, 2) is firm for the same
reason. The (8, 3) and (12, 6) controls show the walk has little power when the space is large (8 extra edges) or the
target is rare (neighbourly 12-vertex maps): they validate the encoding of the known maps and the canonical form, not the
completeness claim. A census must settle completeness.

**The cheapest geometric filter [V, argument P].** In general position three planes meet in one point, so two distinct
polyhedron vertices cannot lie on the same three faces: every corner triple of the map must be distinct
(`ladder_exact.verify` computes exactly this as `corner_triples_distinct`). 37 of the 240 (9, 3) maps have a repeated
triple (two dual triangles on the same vertex set) and are excluded from geometry; the one reflexible class is among them,
so **every (9, 3) polyhedron on an admissible map is chiral [C, pending census]**. Both (8, 2) maps are admissible.

**Structure of the admissible (9, 3) maps [V].** Degree sequences (= face sizes): (8^6, 9, 10, 11), (8^6, 10^3),
(8^5, 9^3, 11), (8^5, 9^2, 10^2), (8^4, 9^4, 10), (8^3, 9^6). Extra-edge patterns: a perfect matching of 3 doubled pairs
(33 maps), a path of 2 plus a disjoint doubled pair (95), a path of 3 (48), a star of 3 at one face (14), a triangle of 3
doubled pairs (3), and 10 maps with a *tripled* pair plus a doubled one. Among the 8 maps with a free order-3 automorphism:
6 have the perfect matching (the three doubled pairs are one C3 orbit, exactly the ansatz `STRATEGY.md` names), 2 have the
triangle; the two D3 maps (|Aut+| = 6) both have the matching. Each C3 automorphism fixes 0 faces, 0 edges and exactly 2
polyhedron vertices (Riemann-Hurwitz: quotient torus with 2 branch points **[V, from the fixed-point data; P for the
reading]**); each involution fixes 1 face and 3 edges.

**Which symmetries are geometrically possible [P].** A rotation of order 3 cannot fix a face (an invariant plane would be
perpendicular to the axis; two such are parallel, but every two faces are adjacent, so at most one; 9 is 0 mod 3 and a face
fixed by C3 would force two more), so the geometric C3 maps are exactly those with a free order-3 automorphism: the 8 above.
A half-turn may fix a face (plane perpendicular to or containing the axis) and edges whose midpoints lie on the axis, so the
24 involution maps are candidates for C2 and the 2 D3 maps for D3. For (8, 2): both maps allow a half-turn (6 fixed edges, no
fixed face); the order-3 automorphism of the |Aut+| = 6 map fixes 2 faces and is not realizable. Mirror symmetry needs an
orientation-reversing automorphism: none among admissible (9, 3) or (8, 2) maps.

**How to enumerate completely (the first queue item).** Reuse the design of `enum_k12.c` (vertex rotations, rule Delta,
canonical code over all flag labellings) generalised to multiple edges: the rotation of a vertex is a cyclic word over the
other V - 1 vertices in which some letters repeat (degree = V - 1 + excess), a triangle is a triple of darts rather than a
triple of vertices, and the pairing of parallel copies is explicit (the gem / (phi, alpha) representation of the sampler is
the simplest correct data structure). Isomorph rejection by the sampler's BFS code (min over 2E roots x 2 orientations), or
by canonical augmentation. Controls, all pre-registered: (7, 1) gives exactly 1 class with |Aut+| = 42; (12, 6) with excess
0 gives 59 with the FD3 automorphism orders (if the Python version is too slow, write it in C like `enum_k12.c`); the (9, 3)
and (8, 2) censuses contain every sampled class (`reviews/strategy-review-2026-11-03-maps.json`); the (8, 3) census, if
feasible, contains the Roest-Vigh and Mizhaev maps. Output per map in the project format (`links`, repeats = multiple
adjacencies), with |Aut+|, reflexibility, the fixed-point data of each automorphism and the admissibility flag. Budget: two
sessions, minutes to hours of CPU. A cross-check for the symmetric sub-list: construct the C3 maps directly as Z_3
voltage-graph lifts of torus maps with 3 vertices, 13 edges and 8 + 2 triangles (I-261030-18 made concrete) **[C]**.

### 2.2 Geometry: engines, order, controls, kill criteria

The exact route first (it is the one that can *decide*), the cheap heuristic engine as the explore run, the new engines
behind pilots. Every engine is scored on rungs with known answers before the target (PROTOCOL 8a), and the S5 rungs are the
two (8, 3) objects (R2: from their own planes; R3: from random symmetric planes), then the 2 (8, 2) maps.

1. **OM-SAT per map (jump 2, exact).** Extend the encoder (`omsat.py`) to multiple adjacencies and F != 12: the lemma 5.1
   predicate "F_X cap F_Y = the shared edges" becomes "the shared edge segments", i.e. for a pair with m copies the m
   segments on L_XY are disjoint and ordered, with endpoints at the 2m triple points of the partner faces; the IN / E /
   REFLEX predicates are unchanged in form. Validation as for FD2: the Roest-Vigh and Mizhaev chirotopes (8 planes + infinity)
   must satisfy their maps' formulas (`Eval` backend), 0 mismatches between `Eval` and exact geometry on random perturbations
   of both objects and of Szilassi, and a negative control (the Roest-Vigh planes against Mizhaev's map must fail). Then:
   the 2 (8, 2) maps (9 elements, 126 bases, with and without C2 clauses from `omsat_sym`), the 8 C3 (9, 3) maps with C3
   clauses, the 24 involution maps with C2 clauses, then all 203 asymmetric instances. For every SAT model: the two existing
   realizers (hinge and two-stage, at 9 planes) and the final-polynomial LP (with the 120-s limit); keep CNF, DRAT and
   certificates. **Kill**: a predicate that cannot be written in the chirotope (then the exact route is out for S5), or a
   median SAT time above about an hour per (9, 3) map (then restrict to the 32 symmetric maps and let the heuristics run).
   Cost to first kill: 1-2 sessions of coding, then hours.
2. **Genus ladder on 9 faces (jump 0; explore).** `genus_ladder` with `tubes` removes handles from each admissible (9, 3)
   map down to a 9-vertex sphere (a simplicial 3-polytope, always realizable), then climbs M0 -> M1 -> M2 -> M3 with the
   exact verifier at every level; `--target S5` at the top. The engine already passes R1 and R5 at genus 3, and per seed its
   outcome is decided in about 3 minutes (E-261102-04), so one night covers hundreds of (map, seed) units. The S0 "ravine"
   evidence does not apply below genus 4 (section 6, finding 1). **Kill**: no S5 PASS in one night over all admissible maps,
   with the per-level failure statistics recorded (which level fails, and whether the (9, 3) R5 analogue holds).
3. **Symmetric solid-first (jump 2; explore).** The Roest-Vigh route: sample C3 (one orbit of 3 planes plus two more
   orbits, about 7 free parameters after the symmetry), D3 and C2 arrangements of 9 planes, decide each with the CP-SAT inner
   solver (`solid_cpsat.best_solid`) extended to 1-3 edge runs per pair with E = 39 in total (the README notes it is S0-only
   today). Controls: R2 (the Roest-Vigh planes give their 28 pairs with 8 doubled; Mizhaev's likewise), R3 (rediscover one
   (8, 3) object from random D2 or S4 two-orbit planes within a session). **Kill**: R3 fails in a session. Pilot one session,
   then one night.
4. **Embedded first, planar later (I-261103-01; jump 2; explore).** Pilot exactly as the idea file says, but with the S5
   rungs: R1 (Szilassi from a torus), then an (8, 3) object from a smooth genus-3 surface split by its map. **Kill**: the
   planarity energy plateaus above zero on R1 with the barrier active.
5. **Rank-3 normals census on 9 elements (filter).** E-261101-06 re-scoped: the uniform rank-3 oriented matroids on 9
   elements are few (4,382 reorientation classes **[P, from memory; verify]**), so the Gauss-class conditions (degree -2,
   covering, >= 7 saddles) can be tabulated for every (map, normal class). Useful only if item 1 is slow; otherwise skip.
6. **Chirotope-first and the k-face ladder** at 9 faces: the face ladder is monotone and the frontier was k = 10 at 12 faces,
   so a 9-face instance is inside the engine's reach **[P]**; but item 1 decides the same instances exactly, so run it only
   as the realizer of item 1's models.

**Positive controls in one list.** Szilassi (`--target S5` PASS, in `verify_all`); Roest-Vigh and Mizhaev through
`ladder_exact.verify` (EMBEDDED, 20 + 8 pairs; `--target S5` must reject them as not maximal, in `verify_all`); the two
(8, 3) chirotopes satisfy the S5 formulas; R3 rediscovery for any heuristic engine. **Negative controls**: random 9-plane
arrangements fail; a map with a permuted pairing of parallel edges is rejected by the encoder's consistency check; the
37 non-admissible (9, 3) maps must be UNSAT (or rejected before solving) in item 1.

---

## 3. The re-ranked queue (Q3)

### 3.1 Scores of the planned experiments

Scores T D F G R as in `ROADMAP.md` ("Scoring"); **jump** = 2 if the method reaches the focus target's genus without a
ladder, 0 for a ladder step, n/a for non-construction items; **kill** = cost to the first result that could park it.

| ID | Under `STRATEGY.md` | T D F G R | jump | kill | Proposed state |
|---|---|---|---|---|---|
| E-261101-12 | the focus row; split into the S5 rows below | 2 2 2 2 2 | - | - | keep as the umbrella row, link the S5 rows to it |
| E-261101-26 | the S0 ladder is done for its purpose (R4 is the wall); the S5 ladder (R2, R3, (8, 2) maps) is new | 1 2 2 2 2 | n/a | 1 session | close for S0 (folder says done); new S5 row |
| E-261101-22 | the remaining reads cannot contain the focus objects (non-equivelar); keep the two contacts | 1 1 2 1 1 | n/a | 1 session | demote to hygiene; the S5 letter to Roest-Vigh and Mizhaev moves to E-261101-11 |
| E-261101-16 | the S5 version is engine 3 above; the S0 version (symmetric arrangement, asymmetric solid) stays parked | 2 2 2 1 2 | 2 | 1 session (R3) | re-scope to S5; S0 part parked |
| E-261101-06 | rank-3 census on 9 elements is cheap and reusable; on 12 elements S0-only | 2 2 2 2 2 | n/a | 1 day | keep, lower priority (filter for item 1) |
| E-261101-09 | encoder comparison; the shared predicates also underpin the S5 encoder | 1 2 1 1 2 | n/a | 1 day | keep alive at low cost (step 1 only) |
| E-261101-11 | owner's e-mails; zero compute; now also the S5 question to the Szeged authors | 2 2 1 1 2 | n/a | 0 | keep, do now |
| E-261101-10 | the shareable S0 theorem; sessions, no compute | 2 1 1 1 2 | n/a | 0 | keep at one session per two weeks |
| E-261101-21 | fold-locus identity; theory for both targets but no decision depends on it now | 1 2 2 2 2 | n/a | 1 session | park |
| E-261101-18 | MUS cores of the 50 symmetric S0 instances | 2 2 2 2 2 | n/a | 1 night | S0-only, park |
| E-261101-15 | cube-and-conquer pilot, S0 | 2 2 1 1 2 | n/a | 300 core-h | S0-only, park |
| E-261101-20 | incremental SAT across S0 types | 1 2 2 1 2 | n/a | hours | S0-only, park |
| E-261101-24 | Farkas descent, S0 climbing | 2 2 2 1 2 | 0 | 5 core-h | S0-only, park |
| E-261101-19 | barrier continuation genus 3 -> 4, S0 | 2 2 1 2 2 | 0 | 1 night | S0-only, park (the one S0 construction item worth a night later) |
| E-261101-17 | realization-space geometry, S0 archive | 1 2 2 1 2 | n/a | 10 core-h | S0-only, park |
| E-261101-03 | type-0 dossier | 1 2 2 1 2 | n/a | 0 | S0 hygiene, park |
| E-261101-08 | S1 at 12 faces, genus 7 | 1 2 2 1 2 | 2 | 1 night | S1, park behind S5 |
| E-261101-04, -14 | below gate | 1 1 2 1 2 | n/a | - | stay below the gate |

### 3.2 Open ideas and hypotheses, grouped

Of the 90 open ideas, the ones that bear on the focus and their fate:

| Idea | Fate under the focus |
|---|---|
| I-261101-07, I-261030-10 (maximal cases, ladder over n) | the focus itself; H-261101-07 is its hypothesis |
| I-261030-07 (symmetric orbit ansatz), I-261101-08 (arrangement first), I-261101-20 (few convex vertices) | engine 3 and its catalogue weights |
| I-261030-11, I-261030-19 (8-face objects as bench, canonical comparison) | done in part here: the two dual maps are distinct, |Aut+| = 8 (Roest-Vigh, D4 as the paper says) and 2 with a reflection (Mizhaev, C4 generated by a rotoreflection) **[V]**; the rest is the S5 ladder rungs |
| I-261030-18, I-261030-04 (voltage lifts) | the symmetric sub-census cross-check (section 2.1) |
| I-261030-31 (n = 8 exact OM-SAT) | becomes the (8, 2) exact decision, item 3 of the queue |
| I-261101-21, I-261101-18, I-261102-01 (chirotope-first, face ladder, adaptive seeds) | realizer role inside item 3; no own run |
| I-261103-01 (embedded first) | engine 4, pilot |
| I-261029-45, I-261029-57 (final polynomials, realizability audit) | parts of item 3 |
| I-261029-42, -43, I-261031-01, -02 (OM axioms, symmetry breaking, rank-3 counts, cubes) | item 1's machinery, used as needed |
| I-261101-13, -14, I-261101-05, -09 (fold map, tightness, chambers, widths) | theory and S0 diagnostics; park |
| the 1-9 black-box engines (I-261029-29 to -40), near-miss repair (-13, -51), the physics analogies (-09, -10, -18, -20), MCTS / LLM (-06, -39), the rest of the 2026-10-29 pool | S0-only or engine-agnostic; park, no change; the exploration quota draws from them only with a stated change |

Hypotheses: H-261101-07 (S5 objects exist for genus 2-5) is now *the* focus hypothesis; its evidence line should record the
map counts and admissibility (section 6, finding 6). I propose three new ones for the working session to file:
**H-S5-1** "(9, 3) has exactly 240 candidate maps, 203 admissible, 8 with a geometric C3" (test: the census); **H-S5-2** "a
(9, 3) polyhedron exists on one of the 8 C3 maps" (test: item 3 with C3 clauses; a C3-symmetric object would also be the
first face-neighbourly polyhedron with a 3-fold axis); **H-S5-3** "both (8, 2) maps are OM-UNSAT" (test: item 3; rival: a
model realizes, the first genus-2 face-neighbourly polyhedron). The S0 hypotheses H-261101-01 to -06, -08 to -17 are
unchanged and parked with their experiments; H-261101-10 (handles are the wrong move) keeps its scope "S0 maps at genus 3
to 4" and is *not* evidence about (9, 3).

### 3.3 Proposed `ROADMAP.md` queue (not applied)

IDs are placeholders; the working session assigns E-YYMMDD-NN when it creates the folders. Explore = counts towards the
one-in-two exploration share.

| # | ID (slug) | Hypothesis | Cheapest falsifying test | Outcomes | Budget | Stop rule | Explore |
|---|---|---|---|---|---|---|---|
| **1** | **E-S5-01 `s5-map-census`** | H-S5-1 | orderly enumeration of (7, 1), (8, 2), (9, 3), (10, 4) maps with controls (1 class / 59 types / contains every sampled class / contains the two (8, 3) maps); admissibility and automorphism data; output in `links` format | 240 and 203 confirmed: the geometric plan below stands; more maps: re-plan with the count; fewer: the sampler had a bug, fix before anything else | 2 sessions, minutes-hours of CPU | the census with all controls, or a written reason why (10, 4) does not finish | no |
| 2 | E-S5-02 `s5-omsat-encoder` | the lemma 5.1 predicates extend to multiple adjacencies | Roest-Vigh and Mizhaev chirotopes satisfy their maps' formulas; 0 mismatches on random perturbations; negative control fails; `ladder_exact.verify` guarded against repeated corners | pass: item 3 runs; a predicate that cannot be expressed: the exact route is out for S5, heuristics lead | 1-2 sessions | the three controls, or the written obstruction | no |
| 3 | E-S5-03 `s5-exact-decision` | H-S5-3, then H-S5-2 | OM-SAT for the 2 (8, 2) maps (plain and C2); the 8 C3 (9, 3) maps with C3 clauses; the 24 C2 maps; then all 203; realizers and final polynomials on every model; DRAT kept | realized model: `candidate-check`, `--target S5`; all UNSAT: a non-existence theorem for the case (CERTIFIED after soundness write-up); non-realizable models only: C rises | hours for (8, 2); one night for (9, 3) | every map decided, or median SAT time above 1 h per (9, 3) map | no |
| 4 | E-S5-04 `s5-genus-ladder-9-faces` | the (9, 3) analogue of R5 holds: the ladder realizes an admissible (9, 3) map from its genus-2 parents | one night, every admissible map x seeds, exact verifier per level | an S5 PASS: `candidate-check`; none: per-level statistics (which level fails) and the ladder parks for S5 | one night, 10 cores | the night, or the first S5 PASS | yes |
| 5 | E-S5-05 `s5-symmetric-solid-first` | H-S5-2 by the Roest-Vigh route | R2 (their planes give their objects), R3 (rediscovery from random D2 / S4 planes in a session); then C3 / D3 / C2 catalogues of 9 planes with the extended inner solver | R3 fails: park with the failure mode; R3 passes: one night on the catalogue | 1 session + 1 night | R3, then the night or the first solid with 36 pairs | yes |
| 6 | E-S5-06 `embedded-first-pilot` (I-261103-01) | an embedded surface with the right map can be planarised without leaving embedding | R1 from a torus; then an (8, 3) object from a smooth genus-3 surface | R1 fails: park; R1 and R2' pass: a pre-registered (9, 3) night | 1 session | as in the idea file | yes |
| 7 | E-261101-11 (S5 letter) | - | the owner writes to Roest-Vigh and Mizhaev: have they tried (8, 2) / (9, 3); method details; offer the census | a reply changes the novelty row either way | 0 compute | 4 weeks | no |
| 8 | E-S5-07 `s5-10-4-census-and-symmetry` | the (10, 4) maps are a few hundred with a usable symmetric sub-list | the census of item 1 extended; C2 / C5 sub-list | prepares the stretch; no geometry before (9, 3) is decided | minutes-hours of CPU | the count, or a written reason | no |

S0 items kept alive at low cost (not in the queue): E-261101-11 (first e-mail, owner), E-261101-10 (write-up, one
session per two weeks), E-261101-09 step 1 (predicate equality; it also audits the S5 encoder's shared predicates),
E-261101-06 (rank-3; shared code). Everything else S0 is parked, not dropped (section 3.1).

**The first item is E-S5-01, the census.** Nothing geometric should start before it: the maps are the input of every
engine, and the sampler's counts are not a census.

---

## 4. Risky ideas we are missing (Q4) - all [C]

1. **Census-free exact search: tope selection inside the oriented matroid (oriented matroids + SAT).** Solid-first picks
   bounded cells of a fixed arrangement with CP-SAT; the arrangement is coordinates. Do it one level up: variables for the
   rank-4 chirotope on 10 elements (210 signs) *and* for the set of bounded topes (cells) forming the solid, with the
   face-structure conditions (one disk face per plane, 1-3 edge runs per pair, cubic vertices) written on cocircuits and
   topes. One SAT instance then asks "does any (9, 3) polyhedron exist with any map", without a census, and a model gives a
   chirotope to realize. Cheapest test: 7 planes (8 elements) must return Szilassi's chirotope. Why risky: tope sets of a
   rank-4 OM are implicit in the chirotope and the encoding may be large; why worth it: it is the exact form of the
   Roest-Vigh "construction procedure from the planes alone".
2. **Interval branch-and-bound over the C3 ansatz (validated numerics, computer-assisted-proof style).** A C3-symmetric
   (9, 3) polyhedron has about 7 free parameters. Every realizability condition is a sign of a polynomial in them. Cover the
   compact parameter box by interval boxes: a box is discarded when some sign is constant and wrong for every admissible
   map, kept and refined otherwise; a leaf with all signs decided is an exact candidate. Outcome: either an object or a proof
   "no C3-symmetric (9, 3) polyhedron" over the box. Cheapest test: a 2-parameter slice of the Roest-Vigh D2 family must
   bracket their solution. Transfers to S0's one loophole (symmetric arrangements with asymmetric solids, I-261101-08).
3. **Ninth-plane sweep on the known 8-plane arrangements (lifting from a known object).** Add one plane (3 parameters) to the
   Roest-Vigh or Mizhaev arrangement and ask the extended inner solver for a 9-face all-adjacent solid of genus 3 on the 9
   planes; sweep the 3-parameter family on a grid (thousands of positions, a minute each). Why it might work: the eight known
   planes already carry a face-neighbourly solid; the solver re-selects cells, so the 8 doubled pairs may be traded for 3.
   Cheapest test: 1,000 random ninth planes in one night. Kill: the maximal adjacency never exceeds 28 + 8 = 36 pairs.
4. **Spectral start for embedded-first (algebraic graph theory).** I-261103-01 needs an embedded genus-3 surface with the
   target map as its starting point. Build it from the dual: a Colin-de-Verdiere / Tutte-type vector representation of the
   cubic 1-skeleton (26 vertices) in R^3 (nullspace or low-eigenvector embedding of a Laplacian with the face cycles as
   constraints) gives straight edges and face polygons that are near-planar by construction; triangulate the faces and run
   the barrier planarisation from there. Cheapest test: the Szilassi map's spectral drawing is already close to a
   realization (measure the planarity energy).
5. **Z_3 voltage construction with geometry attached (crystallography of the map).** For the 8 C3 maps, the quotient is a
   torus map with 3 vertices, 13 edges and 2 branch points. Build the polyhedron as three copies of a *fundamental piece*
   (3 planes, one third of the surface) under a 120-degree rotation: the piece is a planar-faced surface with boundary whose
   boundary matches its rotated image. This turns the symmetric ansatz into a boundary-matching problem for a small patch,
   the way crystallographers build a unit cell, and the two fixed vertices on the axis fix the chart. Cheapest test: the
   Roest-Vigh object as two D2 pieces must be recovered from one piece.

---

## 5. What transfers back to S0 (Q5)

| Focus outcome | What transfers | S0 move |
|---|---|---|
| **A (9, 3) object found** | the complete exact pipeline, validated end-to-end (census -> OM-SAT with symmetry -> realization -> certificates); a second face-neighbourly object beyond 8 faces for the structural priors (convex vertices, hull, spikes, I-261101-20); if found by engine 2 or 3, an engine with a measured pass at genus 3 from parents or from symmetric planes; the (10, 4) stretch becomes the test of the ravine | A up by at most 0.05 (a different map, different face count); the construction queue for S0 re-opens only with a method that passes R4 |
| **Non-existence proved** (all admissible maps OM-UNSAT, certified) | a theorem publishable with the (8, 2) decision; UNSAT cores on 9 faces are small enough to read: a recurring core would be the first candidate for the structural lemma H-261101-02 wants | B up by 0.05 by analogy with Schewe's vertex case; E-261101-18 (cores) gains a method |
| **Failure without proof** (timeouts, models that neither realize nor certify) | engine scores on the S5 ladder; a measured cost of the exact route at 10 elements, which bounds the 13-element S0 campaign from below | none on credences; the decision rule: if 10 elements do not finish in two weeks, the S0 exact campaign is not ours to run alone (join `polyhedraproof`) |

S0 items worth keeping alive (zero or low compute): the first e-mail to the `polyhedraproof` author (E-261101-11; it is the
cheapest strong evidence for FD2 / FD4 soundness, which the S5 encoder inherits); the FD6 write-up with the improper-isometry
lemma (E-261101-10); the Zenodo DOI for the DRAT archives; E-261101-09 step 1. The rank-3 SAT (E-261101-06) is worth building
only in the 9-element form first (engine 5), which then runs on 12 elements for free.

---

## 6. Audit (Q6)

### 6.1 Claims stronger than their evidence

1. **`STRATEGY.md:29-31`** ("Evidence suggests a ravine between genus 3 and 4 ... night 7: no engine passes R4"). R4 is a
   full genus-3 map *from random planes*; R5 (from genus-2 parents) is passed by the ladder. Night 7 is evidence that no
   engine reaches genus 3 from scratch, not evidence about 3 -> 4. The ravine rests on DR1 (genus 4 never, LOW-YIELD, not
   REFUTED) and on k_tau = 0 for 7 realizations x 3 arms of one map **[V, `STATUS.md:59-61`]**. Consequence: jump-first is
   right for (10, 4) and S0; for (9, 3) the ladder is not disfavoured by any evidence and is the cheapest engine (queue item
   4). Suggested wording: "no scored engine reaches a genus-3 map from random planes (R4); the ladder reaches it from parents
   (R5); genus 4 was never reached by ladders at 12 faces".
2. **`STRATEGY.md:12`** ("a genus our engines already reach"): reached from parents in half the seeds and never from random
   planes, on 12-face maps with 48 of 66 pairs. A (9, 3) run must build its own parent chain (M0 -> M3); nothing is
   "already reached" for 9 faces **[V, from STATUS 3b]**.
3. **`SPEC.md:39`** (S5: "doubled adjacencies allowed"): 10 of the 203 admissible (9, 3) maps and one of the two (8, 2) maps
   have a *tripled* pair; `verify_candidate.py --target S5` accepts any multiplicity (it checks only all pairs adjacent, F =
   F_max(g), EMBEDDED) **[V, `verify_candidate.py:67-70`]**. Decide and write it: I recommend "multiple adjacencies allowed"
   (a tripled pair is three collinear shared segments, a legitimate polyhedron), with the multiplicity reported.
4. **`literature/review-2026-11-03.md` note 2** ("the number of candidate maps is unknown, not small by default"): now bounded
   below (240 / 203 for (9, 3), 2 for (8, 2)); update after the census, with the mod-12 remark kept.

### 6.2 Inconsistencies and bugs the S5 pipeline will hit

5. **`ROADMAP.md:70`** E-261101-26 State `open` versus `experiments/E-261101-26-engine-benchmark-ladder/README.md:5`
   `status: done` **[V]**. Pick one; proposal: done for S0 (R4 is the wall), new S5 ladder row.
6. **`code/ladder_exact.py:138`**: `verify` raises `ValueError` ("not enough values to unpack") on a map two of whose
   consecutive corners coincide (a repeated corner triple), instead of returning a report with `EMBEDDED: False`;
   `corner_triples_distinct` is computed at `:71` but not used to bail out **[V, crashed on 37 sampled maps with random
   planes]**. Any S5 pipeline that feeds maps from a census will hit this; add a guard (return the report early when the
   triples are not distinct).
7. **`hypotheses/H-261101-07-maximal-face-neighbourly-exist.md:24-26`** ("What would move it: literature check, then
   (8, 2)"): stale under `STRATEGY.md`; the evidence line should record the map counts and that the (8, 3) objects are two
   of at least 22,666 candidate maps at (8, 3) **[V]**.
8. **`STATUS.md` 3b** ("R2 / R3 not expressible in the OM-SAT encoder"): correctly stated, but it is the blocking gap for
   the exact S5 route and should be a queue row (item 2), not a footnote.

### 6.3 Follow-up chains to stop (`STRATEGY.md` §2, follow-up rule)

9. E-261102-03 "the open knob is the SAT cost at k >= 10" and E-261102-04 "more seeds, not more minutes": neither outcome
   changes a decision in the S0 table or the focus plan; stop both (their `CONCLUSION.md` "Next step" lines). The
   chirotope-first engine re-enters only as the realizer inside queue item 3.
10. E-261101-04, E-261101-14 (below gate), E-261101-19 / -17 / -24 (S0 climbing diagnostics), I-261102-01 (adaptive seed
    budget): park; none bears on (9, 3).
11. The 2026-11-01 review's own recommendation "(9, 3) is harder than (8, 2); leave (9, 3) to (11, 5) until the engine has
    found one of the two" (`strategy-review-2026-11-01.md` §4) is superseded by the map counts: at the exact level (9, 3) is
    tractable now.

### 6.4 Underpowered verdicts

12. DR15 ("n = 8 genus-2 rung: poor analogue, LOW-YIELD as benchmark, existence OPEN-LOW"): with 2 candidate maps and a
    126-base OM instance, (8, 2) is now the best *exact* rung the project has; re-score (queue item 3).
13. The S0 construction verdicts (DR1, DR6, DR7) are fairly labelled and unchanged; nothing since 2026-11-01 moves them.

### 6.5 Scenario credences

S0 (unchanged; no S0 evidence since 2026-11-01): A 0.20 / B 0.55 / C 0.25.

Proposed S5 table, next to it (all **[C]**; "cannot tell" = not decided within the strategy's horizon by our tools):

| Case | exists | does not exist | cannot tell | One line of evidence each |
|---|---|---|---|---|
| (9, 3) | 0.40 | 0.35 | 0.25 | 203 admissible maps is many tickets; at (8, 3) the two known objects are 2 of >= 22,666 maps, so realizable maps may be rare **[V, C]**; a 10-element OM instance per map is small, so "cannot tell" is bounded by the realizability stage (non-realizable models without a biquadratic final polynomial) |
| (8, 2) | 0.25 | 0.55 | 0.20 | only 2 maps; both C2 but no C3; a 9-element instance decides in minutes, so "cannot tell" is small; the known (8, 3) objects suggest that 8 faces needed 8 extra adjacencies, not 2 |
| (10, 4) | 0.30 | 0.30 | 0.40 | several hundred maps, almost no symmetry in the sample, no engine pass at genus 4 |

Rules: if (8, 2) and (9, 3) are both decided non-existent, write the note and move the focus to (10, 4) with the
census; if (9, 3) exists, the (10, 4) stretch starts from the method that found it; if item 3 stalls on non-realizable
models, build the realizability stage (I-261029-57) before any more SAT, as the S0 rule says.

---

## 7. Three things to do first

1. **E-S5-01, the census** (two sessions): orderly enumeration of (7, 1), (8, 2), (9, 3), (10, 4) with the four controls,
   admissibility and automorphism data, output in `links` format; confirm or correct 240 / 203 / 8 and 2 / 2. Pre-register
   with H-S5-1. Fix finding 6 on the way (one guard in `ladder_exact.verify`).
2. **E-S5-02 + the (8, 2) half of E-S5-03** (two sessions, hours of compute): the S5 encoder validated on the Roest-Vigh and
   Mizhaev chirotopes, then the two (8, 2) maps decided with DRAT. The first complete decision of a face-neighbourly case,
   whichever way it goes.
3. **The 8 C3 (9, 3) maps through OM-SAT with C3 clauses**, and in parallel the one-night ladder on 9 faces (E-S5-04,
   explore) once the census is in. Owner: the S5 letter to Roest-Vigh and Mizhaev (zero compute).

---

## Appendix A. Checks run in this review

All in `research/12-faced-polyhedron/`, 2026-11-03, single core, system `python3 -I` for the sampler and the venv
`~/.venvs/polyhedra` for the controls that import project code. The sampler and its controls are in
`reviews/strategy-review-2026-11-03-flipwalk.py`; the sampled maps with their invariants are in
`reviews/strategy-review-2026-11-03-maps.json` (240 (9, 3) and 2 (8, 2) classes, `links` format, admissibility flag).

### A.1 Evidence suite

`~/.venvs/polyhedra/bin/python verification/verify_all.py --quick`: 15 PASS, 1 SKIP (archive), ALL PASS, 13.3 s wall.

### A.2 The sampler

State: oriented triangles as triples of darts, `alpha` the edge involution, `tail[d]` the vertex label of a dart;
`sigma(d) = alpha(prv(d))` is the vertex rotation, so vertices are sigma-cycles. Start: the canonical 4g-gon with one
vertex and a centre vertex (2 vertices, 6g edges, 4g triangles), then V - 2 stellar subdivisions. Move: a random edge flip
(the two triangles must be distinct); accepted by Metropolis at T = 0.6 on f = (non-adjacent pairs) + 2 (loop edges), with
the incremental f re-derived from scratch every 200,000 acceptances (assert). Hit: f = 0; canonical code = lexicographic
minimum over all 2E roots and both orientations of the BFS code (label order; per dart the labels of its triangle successor
and of its alpha partner); |Aut+| = number of roots attaining the minimum; reflexible iff the mirror orientation attains it
too. Every new class passes an independent check: alpha a fixed-point-free involution with consistent labels, one
sigma-cycle per label, no loop, all pairs adjacent, V - E + F = 2 - 2g, connected. Automorphisms are read off the roots
with the minimal code and reported as (order, fixed vertices, fixed edges, fixed triangles), i.e. for the polyhedron (order,
fixed faces, fixed edges, fixed vertices).

Commands and outputs (seconds of wall time are the budget argument):

```
python3 -I reviews/strategy-review-2026-11-03-flipwalk.py 7 1 15 1
  (V, g) = (7, 1): 3,234,243 steps, 9,874 hits; 1 class; |Aut+| 42, reflexible False      # Csaszar-Mobius torus, chiral
python3 -I reviews/strategy-review-2026-11-03-flipwalk.py k12control 120
  59 types canonicalised: 59 distinct codes; |Aut+| in [1, 2, 3, 4, 6, 12]; reflexible 6; walk (12, 6) 120 s: 0 hits
python3 -I reviews/strategy-review-2026-11-03-flipwalk.py 8 2 120 1
  2 classes; |Aut+| {6: 1, 2: 1}; extra patterns one tripled pair / two disjoint doubled pairs; each class seen >= 3,616 times
python3 -I reviews/strategy-review-2026-11-03-flipwalk.py 9 3 240 1   (and seeds 2, 3, 4 at 240 / 150 / 150 s, seed 5 at 90 s)
  240 classes in every run; |Aut+| {1: 205, 2: 25, 3: 7, 6: 3}; reflexible 1; every class seen >= 9 times;
  first-seen quantiles (s) 0.1 / 3.5 / 13.0 / 26.5 / 42.8; seeds 3 and 4: 240 and 240 codes, 240 common
python3 -I reviews/strategy-review-2026-11-03-flipwalk.py 10 4 180 1
  113 classes; seen once 99, twice 14 (Chao1 ~463); |Aut+| {1: 108, 2: 5}
~/.venvs/polyhedra/bin/python -I reviews/strategy-review-2026-11-03-flipwalk.py control83 150
  Roest-Vigh dual map: |Aut+| 8, reflexible False; Mizhaev: |Aut+| 2, reflexible True; distinct;
  walk (8, 3) 150 s: 22,666 classes, neither known map found (median first-seen 74 s: unsaturated)
~/.venvs/polyhedra/bin/python -I reviews/strategy-review-2026-11-03-flipwalk.py rvstart 90
  (9, 3) from a stellar subdivision of the Roest-Vigh dual map: 240 classes, all in the seed-3 set
```

Admissibility (distinct corner triples) over the sampled classes: (8, 2) 2 of 2; (9, 3) 203 of 240, with |Aut+| {1: 173,
2: 22, 3: 6, 6: 2}, reflexible 0, 8 with a free order-3 automorphism (fixed faces 0, fixed edges 0, fixed vertices 2);
(10, 4) 106 of 113.

### A.3 The two (8, 2) maps (links; face X's cyclic neighbour list, repeats = multiple adjacencies)

```
|Aut+| 6, chiral, one tripled pair {1, 5}, face sizes 7^6 9^2, involution fixes 6 edges, order-3 element fixes 2 faces:
[[2,1,5,3,7,4,6],[2,5,6,3,5,4,7,5,0],[0,6,7,3,4,5,1],[1,6,4,2,7,0,5],[5,2,3,6,0,7,1],[4,1,3,0,1,7,6,1,2],[0,4,3,1,5,7,2],[2,6,5,1,4,0,3]]
|Aut+| 2, chiral, doubled pairs {0, 7} and {1, 5}, face sizes 7^4 8^4, involution fixes 6 edges:
[[6,7,3,2,4,5,7,1],[0,7,2,5,4,3,5,6],[7,4,0,3,6,5,1],[6,2,0,7,5,1,4],[7,6,3,1,5,0,2],[2,6,1,3,7,0,4,1],[3,4,7,0,1,5,2],[6,4,2,1,0,5,3,0]]
```

### A.4 The two D3 (9, 3) maps (the other six C3 maps are in the JSON file, `aut_plus` 3 with `autos` containing (3, 0, 0, 2))

```
|Aut+| 6, chiral, doubled pairs {1,6} {2,4} {7,8} (one C3 orbit), face sizes 8^3 9^6:
[[2,3,1,6,4,5,7,8],[3,7,5,6,8,4,2,6,0],[4,3,0,8,5,4,7,6,1],[7,1,0,2,4,6,5,8],[1,8,7,2,5,0,6,3,2],[8,3,6,1,7,0,4,2],[8,1,5,3,4,0,1,2,7],[8,0,5,1,3,8,6,2,4],[6,7,3,5,2,0,7,4,1]]
|Aut+| 6, chiral, doubled pairs {1,8} {2,3} {5,7}, face sizes 8^3 9^6:
[[6,7,8,1,4,5,3,2],[7,5,8,6,2,4,0,8,3],[1,6,0,3,8,5,7,3,4],[8,2,0,5,6,4,2,7,1],[1,2,3,6,8,7,5,0],[8,1,7,6,3,0,4,7,2],[0,2,1,8,4,3,5,7],[1,3,2,5,4,8,0,6,5],[3,1,0,7,4,6,1,5,2]]
```

All four were accepted by `ladder_exact.verify` as abstract maps (V E F chi = 20 30 8 -2 and 26 39 9 -4, all pairs adjacent,
corner triples distinct) with random planes; the 37 non-admissible (9, 3) maps made `verify` raise (finding 6).

### A.5 Scope of these checks

Sampling is not enumeration: the counts are lower bounds, with saturation as the only evidence of completeness (section
2.1). The K7 control validates the walk, the canonical form and the check on a case with a known answer; the K12 and (8, 3)
controls validate the encoding of known maps and the automorphism computation (59 distinct codes with the FD3 orders; the
two 8-face maps with the automorphism groups their papers state) but not the walk's power on large spaces. No geometry was
run; nothing here is a candidate, a witness or evidence about realizability.
