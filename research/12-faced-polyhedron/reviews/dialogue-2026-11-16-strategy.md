# Dialogue 2026-11-16-strategy: synthesis

Status: approved by the owner (C3, #26, 2026-11-17); additions of 2026-11-17 approved by the owner afterwards
(the vetting note and the P3/P4 split in §2, the geometric-box arm of row 5, the open questions of §6, Appendix A).
Lead claude, critic astra; astra's amendments of #15, #17 and #24 are folded in. Nothing here is evidence: both authors are AI sessions (`SPEC.md` §5). Labels are `SPEC.md` §5; every
number is a session check of the thread unless a repository file is cited. "#n" is a message of the thread, which is
not in git. Nothing is filed, launched or changed outside the thread.

## 1. Owner digest

1. **Verdict on 16b.** The stance stands; three premises fail. Week item 1 (E-261116-06) is empty: eleven faces have no
   free C2 or C3 action (PROVED-1, astra #2). "D2 4+4+1" has no invariant solid and is non-uniform. The ">= 10 of 200"
   gate passes for D2 by expectation (K13) and tests nothing. "(8, 3) census out of reach" was never priced.
2. **No new polyhedron.** K13 found 17 solids, all with Roest-Vigh's known map. Target unchanged: nine mutually
   adjacent faces (S1, genus free); the owner rejects a write-up as a substitute (#16).
3. **Front checks, cheap:** N1, the complete list of face-transitive cubic (9, 4) maps (Cayley maps of Z9, Z3 x Z3), and
   N2, "move infinity, not the planes": fixed-face half-turn families become uniform in a generic chart (owner's B1).
4. **Main investment:** P3, the census-free formula, specification v2, with a decision tree; P4 (patchwork
   chirotopes) as a one-session probe; the owner-approved C3 night (P1).
5. **B1-B3.** Kept: the chart trick (B1), patchwork chirotopes and final polynomials (B2). Parked: projective target,
   chart invariants, curvature, flattening. Dropped: Hodge, complex varieties, intrinsic metric.
6. **Budget.** More nights do not help before a route has a hit rate one rung below; the "1 in 10" forecast is withdrawn.
7. **Needs approval:** new ROADMAP rows for N1, N2, P4 and the P6 price pilot; the amended row and budget of
   E-261116-07; E-261116-06 off the plan; a lab task to check and register the S6 (10, 2) objects (16 files, 13 maps).
8. **Already approved (#7, #13):** P3 two sessions and <= 6 core-h; P4 one session and <= 1 core-h, sampler <= 6 core-h
   gated; one C3 night; ten faces and the non-uniform engine as a side track.
9. **Not done:** no prototype, no solver run on any target, no literature search, no human review.
10. **Open between the models:** only marks and the size of unmeasured costs (§5).

## 2. Strategy shortlist (order of execution; marks V N L F lead / critic; T D F G R as in `ROADMAP.md`)

| # | Item | Target | Cheapest test | Cost (proposal) | Kill rule | V N L F | T D F G R |
|---|---|---|---|---|---|---|---|
| 1 | N1 NEW, Cayley census (inside P6; nearest I-261030-18) | S1, nine faces, cubic, genus 4 | order-8 groups at (8, 3): RV's map must appear; then Z9, Z3 x Z3 | 1 session, <= 1 core-h joint cap | RV's map missing: bug; empty list or all UNSAT-SOLVER: this slice closed for planning | 2 2 1 2 / 2 1 2 2 | 2 2 2 1 2 |
| 2 | N2 NEW, plane-only symmetry in a generic chart (extends I-261113-04, I-261030-12) | S1 nine faces, C2 4 x 2 + 1; S5 (11, 5) maps with Aut+ = 2 | exact Szilassi control in a far rational chart, pinned SAT | 1 session, <= 1 core-h; sampling inside the P1 night | control fails (zero in the input, clause or gauge, solver: told apart); no speed-up at 12 elements: (11, 5) stays priced out | 2 2 3 2 / 2 2 3 1 | 2 2 2 2 2 |
| 3 | P3, census-free formula v2 (I-261103-02, E-261116-07 amended) | S1 nine faces, E = 45, 51, 57 (genera 4-6), uniform cubic | unit tests (pinch, annulus, disk + annulus), L0-L3; N3 as an extra rung | 2 sessions, <= 6 core-h | tree below | 2 2 3 1 / 2 1 3 1 | 2 2 1 2 2 |
| 4 | P4 probe, patchwork chirotopes (I-261029-10 made exact) | chirotopes realizable by construction | C0 certificate test, C1 on the controls | 1 session, <= 1 core-h; sampler <= 6 core-h, gated | no control in the box K: park that box; C2 UNSAT-SOLVER in the box | 2 1 3 1 / 2 1 3 1 | 1 2 1 2 2 |
| 5 | P1, C3 3+3+3 night, frozen engine (owner, #13); C2 4 x 2 + 1 arm if row 2 passes; geometric-box arm (A7) | S1 nine faces, E = 45, 51 | K14 (done) | one night <= 80 core-h, 10 shards | failed control; zero verified hits parks that box and cap | 2 1 2 2 / 2 1 2 1 | 1 2 1 1 2 |
| 6 | P6 price pilot, equivelar slice (I-261101-15, E-261103-01) | S1 nine faces, genus 4, 10-gons | stage A at (8, 3), 7 patterns, costs per stage | 1 session, 1 core-h; stage B has no night before a price | control map absent or pinned control UNSAT | 2 1 2 1 / 2 1 1 1 | 1 2 1 1 2 |
| 7 | Adjacency-guided search (astra; the parked solid-first line with the disk-aware model) | S1, eight then nine planes | funnel diagnostic from the 17 K13 solids, then a matched comparison | 1 session, <= 3 core-h | no recovery advantage, or mostly unresolved inner solves | 2 0 2 2 / 2 1 2 1 | 1 2 1 2 2 |

Conditional or reserve, no slot: P3 coupled with P4 at eight faces (only on branch 3 below); N3, the ninth-plane census
as P3 with eight planes pinned (a linear program tests the ninth plane; no night); N4, one-orbit Z9 arrangements
(reserve); final polynomials (after a failed bridge); the non-uniform cell engine and D5 at ten faces (side track).

**Vetting and split.** N1 and N2 were first raised in R4 and had one critique turn (#24); P3 went through R2-R4. P3
stays the main investment (about two thirds of the build effort, P4 one third; invert if C1 shows the known objects
patchwork at small K) and does not wait for N1 or N2 if either overruns its session.

**P3 decision tree (agreed, #12).** Topology or control failure: repair or park. Sound topology and one unpinned
eight-face model realized to exact coordinates passing `--all-pairs`: P3 earns its nine-face run. Sound topology,
models extracted, bridge fails and P4 recovers a control: one capped coupled recovery test at eight faces; only that
earns a coupled nine-face run. Open proof obligations: the finite-vertex coverage lemma at OM level, the disk and
manifold argument, the equivariant perturbation step of N2.

## 3. Owner's ideas (marks V N L F lead / critic)

| Question | Existing ids | Marks | Verdict and next step |
|---|---|---|---|
| B1-Q1 a face-neighbourly surface in RP^3 contained in no affine chart | I-261030-12, I-261029-63 | 2 2 2 2 / 2 1 1 1 | park: needs a new auxiliary target and a face model |
| B1-Q2 conditions on the plane chirotope without infinity | I-261030-30, E-261116-04 | 3 0 1 2 / 3 0 1 2 | park: restatement of the formula |
| B1-Q3 a Hodge-theoretic invariant | none | 3 0 0 0 / 0 0 0 0 | drop: no reduction to real sign conditions |
| B1, found in R4: moving infinity removes the forced zero of a fixed-face half-turn | I-261113-04, I-261029-15 | 2 2 3 2 / 2 2 3 1 | keep: row 2 |
| B2-Q1 patchwork (Puiseux) chirotopes | I-261029-10 | 2 1 3 1 / 2 1 3 1 | keep: row 4 |
| B2-Q2 biquadratic final polynomials for unrealized models | I-261029-45, I-261029-57 | 3 1 2 1 / 3 1 2 1 | keep, conditional on a failed bridge |
| B2-Q3 complex varieties | I-261029-19 | 3 0 0 1 / 2 0 1 1 | drop: no route specified |
| B3-Q1 curvature beyond FD7 | I-261029-02, I-261101-13, I-261101-14 | 3 0 1 3 / 2 0 1 2 | park: returns "saddles >= 2g + 1"; independence question open |
| B3-Q2 flattening flow from a smooth surface | I-261029-05, I-261103-01, E-261103-06 | 2 0 1 1 / 2 0 1 1 | park until a changed set-up is named |
| B3-Q3 intrinsic flat cone metric | none | 2 1 0 0 / 2 0 0 0 | drop: known theorems subdivide faces |

## 4. Drop or demote

* **E-261116-06** (week item 1): the registered free-action slice is empty; off the active plan (owner, #7). The four
  Aut+ = 3 maps have no C3 realization (two fixed faces would be parallel). The Aut+ = 2 maps return only through row 2.
* **16b item 3** (E-261110-03/04): the D2 gate tests nothing (K13: 7.1 %, one map class); "D2 4+4+1" as written is
  dropped; the families are replaced by row 5.
* **16b ladder of E-261116-07:** replaced by P3 v2: tope-circuit block removed, both directions at infinity, validity
  bits, no-pinch, Euler and eager connectivity, the (9, 39) pricing rung, the bridge gate.
* **Full (8, 3) census and sweep:** replaced by rows 1 and 6. `c3_crosscheck.py` is genus-specific, no reuse at (9, 4).
* **Withdrawn by the lead:** the rate comparison of #3, "milliseconds per unit", lazy disk cuts, the sampler power
  estimate, "1 in 10", the write-up stop rule.
* Not discussed, standing: E-261116-08, E-261116-09.

## 5. Disagreements

* **Feasibility of N1 and N2.** Lead: both are front checks of one session (existing encoder, a short enumeration, an
  exact control). Critic: enumeration, deduplication, per-map solves and the chart-to-engine interface are unpriced,
  F 2 and 1. Decider: the two sessions report cost per stage under the joint caps.
* **Scope of N2.** Both: sound for the one-fixed-face half-turn family given plane-only general position. Critic: SAT
  under plane-only symmetry is a relaxation and does not give a projective half-turn; the perturbation step is unproved.
  Decider: the written lemma and the pinned Szilassi control.
* **Novelty marks.** P3: lead 2 (no SAT form of the plane-only procedure in print as far as read, CLAIMED), critic 1.
  Guided search: lead 0 (parked solid-first), critic 1 (changed inner model and target). No check proposed.

## 6. Computed in this thread, and not checked

| Check | Command | Numbers | Label |
|---|---|---|---|
| K13 (claude) | `work/claude/d2_rate.py 240 d2_rate.json` | D2 2 x 4, eight planes, engine of E-261103-05: 17 SOLID, 223 INFEASIBLE, 0 open; 7.1 % (Wilson 4.5-11.1); all EMBEDDED (24, 36, 8, -4), all with RV's neighbour lists up to per-face reversal; 37.5 s wall | EXACT per object, NUMERICAL rate |
| K14 (claude) | `work/claude/c3_nine.py 80 45 20 c3_nine_e45.json` | C3 3+3+3, nine planes, E = 45: 70 INFEASIBLE, 10 UNKNOWN at 20 s, 0 SOLID; median 13.5 s | NUMERICAL, timing only |
| Orbits (astra) | `work/astra/check_c3_orbits.py` | (012)(345)(678) has 72 orbits on the 210 four-subsets, three fixed | EXACT |

PROVED-1 in the thread, unreviewed: no free C2 or C3 on eleven faces; at most one face fixed by a rotation of an
all-pairs object; P3 cell identification, gauge, edge ends, three runs at nine planes; the patchwork lift at t = 1/25
and the potentials certificate with the factor 4; no strictly patchwork matrix with a sign symmetry; the Sylow
reduction of N1 at (9, 4); the chart-dependence of the zero chi(X, A, B, infinity).

Not checked: every cost and time of §2 except K13 and K14; P3's size and solve time; that an unpinned model
realizes; P4's coverage and conditioning; the number of Cayley maps; the speed of plane-only symmetric formulas; the
orientation gauge with a moving infinity; literature (Celaya, Loho and Yuen 2024 was read by astra, CLAIMED; Orlik-Solomon,
Adiprasito-Huh-Katz, Mnev and Burago-Zalgaller are from memory and carry no decision); novelty of anything; the map
comparison of K13 is weaker than an isomorphism; no astra rerun of K13 or K14. Open questions never answered in the
thread: whether Roest and Vigh tried nine planes (primary source, bears on P1's novelty); the rung-below rates of S4
2 x 4 and C2 3 x 2 + 1 at eight and seven planes (bear on P1 and N2); the project's final-polynomial pipeline
(`verification/certificates/final_polynomial`) was not read (bears on the feasibility mark of B2-Q2).

## Appendix A. Technical specifications (added 2026-11-17, owner-approved)

The thread is not in git; this appendix carries what a lab session needs to build the items of §2. Every argument is
PROVED-1 at most (AI authors, unreviewed) unless labelled otherwise; every size and time is CONJECTURE. "#n" cites the
message where the item was settled.

**A1. P3 v2, census-free formula** (#8, #10, #11, #12). Scope: uniform rank-4 arrangements, hence cubic; one disk face
per plane; non-cubic objects only through I-261108-09.
* Variables: chirotope chi on F + 1 elements (0 = infinity; 210 signs at nine faces) with the 3150 three-term
  Grassmann-Pluecker relations; a selection bit x_T per sign vector T. No tope-circuit block.
* Cells: at a finite vertex t = (i, j, k), sigma_m(t) = chi(i, j, k, m) chi(i, j, k, 0); its eight cells are the
  vectors equal to sigma(t) off {i, j, k}. Validity tau_T = OR over the finite vertices of "sigma(t) agrees with T
  off t"; x_T implies tau_T. Unbounded: for each pair (j, k) and each direction e in {+, -}, the four vectors with
  T_m = e chi(0, j, k, m) off {j, k} (eight per pair, both directions as in `pilot.py:74-82`) get x_T = 0.
* Gauge on chi alone: sigma_m(1, 2, 3) = + for m = 4..9 and sigma_m(4, 5, 6) = + for m = 1, 2, 3 (reorienting m flips
  sigma_m(t) iff m is not in t).
* Facets b(i, U): both cells valid and exactly one selected (2304 bits at nine faces); segments of plane i on line j
  (1024 candidates per plane) are real iff their four cells are valid.
* Vertex: `solid_cpsat.ALLOWED` on the eight occupancy bits plus no-pinch on the quadrant facets of each of the three
  planes and the no-diagonal clause per half-line (`ALLOWED` alone admits the pinched pattern {0, 1, 3, 7}).
* Runs: an end at a vertex of L_ij is an edge on exactly one of its two half-lines; the end bits sum to 2E; a pair is
  adjacent iff it has an end. At nine planes at most three runs per line, automatically.
* Disk: per plane, facets - segments touching a boundary facet + vertices touching one = 1, as `solid_cpsat.py:125-166`.
  Connectivity eager: a root and levels on the 256 facet labels of a plane; every non-root boundary facet has a
  boundary neighbour (one coordinate flipped) of smaller level. The Hamming-boundary cut is a necessary lemma, not a
  replacement. No lazy cuts (the frozen hard path has none).
* Proof obligations: the finite-vertex coverage lemma at OM level; the disk and manifold argument.
* Unit tests: the pinch pattern, an annulus, a disk plus an annulus; every `ALLOWED` pattern passing no-pinch has zero
  or three ends; extraction of the face cycles of a model.
* Ladder: L0 regression (not soundness) against the frozen engine on K13's archived verdicts and planes (hashes, not
  re-solved), RV, Mizhaev and the saved uniform perturbation of Szilassi (`E-261103-02/CONCLUSION.md:34-37`); raw
  Szilassi must be rejected as out of domain. L1 (7, E = 21) free, SAT. L2 (8, 30) and (9, 39) UNSAT-SOLVER as in
  STATUS 3d; (9, 39) undecided in 2 core-h is a budget stop, no forecast; a time ratio to the 203 per-map formulas
  only on a matched solver and machine, without proof time. L3 (8, 36) unpinned: at most 30 distinct signed
  chirotopes in the gauge; report no model / models without coordinates / realized on a known or a new map, with
  distinct OM classes and maps as diagnostics. Gate: one unpinned model realized to exact coordinates passing
  `--all-pairs` at eight faces inside the cap. Budget: L0 0.5, L1-L2 3 (2 of them for (9, 39)), L3 2.5 core-h.
* Targets: E = 45, 51, 57 (genera 4-6): plain, C3 (72 chirotope orbits, three fixed), the N2 cube (66 plane orbits),
  N3. Risk: the validity gating and eager connectivity may dominate the size; CP-SAT may be a better host than a CNF.

**A2. P4, patchwork chirotopes** (#8, #10, #11, #12).
* H (10 x 4), H_ij = s_ij t^(w_ij), integer w in a declared box [0, K]; infinity is an ordinary row. If every 4 x 4
  minor has a unique minimum-weight matching, its leading term gives chi, realized at t = 1/25 (at most 23 other
  terms, 23/25 < 1). Only coherent fields (one weight matrix) are admitted: a polyhedral matching field can give a
  non-realizable OM (Celaya, Loho and Yuen 2024, CLAIMED, read by astra; §1.2 there leaves coverage open).
* Certificate per 4-subset: 16 matching bits; potentials with u_i + v_j = 4 w_ij on the matching and <= 4 w_ij - 1
  off it; one potential fixed to 0, the others bounded by 3 (4K + 1); about 5,000 auxiliaries at ten elements. The
  unscaled version is incomplete ([[0, 0], [0, 1]]); the factor 4 makes it exact (no negative cycle).
* Normalisation inside the box: subtract row minima, then column minima (a zero in every row and column). Fixing the
  first row and column to zero is not box-compatible ([[0, 1], [1, 0]] leaves -2). C1 keeps all 40 sign bits and one
  global sign; the reorientation gauge is for searches only. A finite K never refutes membership.
* No strictly patchwork matrix has a sign symmetry (two equal-weight rows tie every minor containing both), so D2
  acting by column sign flips is excluded; C3, which permutes columns, is not.
* Conditioning: `ladder_exact.verify` rounds planes at 1e-9 (`code/ladder_exact.py:63`) and `pilot.arrangement`
  checks float signs (`pilot.py:64-67`). Choose rational t = 1/q and a small K, recompute every sign exactly, keep
  the first parameters that survive the rounding; chart row 0 to infinity in rationals and clear denominators. If
  none survives, the model is "realized, not verifier-conditioned", which is not a result.
* Calibration: C0 compares the certificate with all 24 costs on tied and uniquely optimal matrices, including the
  embedded 2 x 2 case. C1, fixed chi: Szilassi (perturbed), RV, Mizhaev, the 17 K13 solids, the 16 realized (10, 2)
  objects, coverage per K. C2: Szilassi's map formula AND P4, outcomes UNSAT-SOLVER in the box / timeout / control
  failure. The sampler (fixed units, end-to-end throughput, rejections counted, cap 6 core-h) bounds only itself.

**A3. N1, Cayley census** (#22, #24). Cubic (9, 4), face-transitive: the face stabiliser in Aut+ divides 10, Aut+ is
transitive (index <= 2, nine odd), so a Sylow 3-subgroup of order 9 acts regularly: Cayley maps of Z9 or Z3 x Z3. Dual
rotation: a cyclic order of ten slots (the eight non-identity elements and one inverse pair repeated) with all faces
triangles; at most about 2.2e6 rotations. Face transitivity alone gives only g = 1 mod 3 (E = 21 + 6g, face degree
(14 + 4g)/3 >= 8): g = 7 is not excluded and not enumerated. Rung below: the five groups of order 8, valency 9; RV's
map must appear (a map automorphism, not a geometric symmetry); Mizhaev's map is not face-transitive (#22, not checked). Each (9, 4) map:
plain formula at 10 elements and the free-C3 uniform formula. Report raw rotations, valid maps, distinct maps; one
joint cap of 1 core-h. Covers patterns 9 and 3+3+3 of A6.

**A4. N2, plane-only symmetry in a moved chart** (#22, #24). For a half-turn fixing face X and swapping pairs (A, B),
the forced zero chi(X, A, B, infinity) depends on the chart (`E-261103-02/SOUNDNESS.md`, "Isometry clauses"). In a
generic rational chart H' disjoint from the solid the chirotope is uniform provided the planes themselves are in
general position; the symmetry clauses act on plane-only bases (the half-turn has determinant +1). Open: an
equivariant perturbation step; several fixed faces can force plane-only zeros. Plane-only symmetry is a necessary
relaxation: a SAT model need not carry a projective half-turn. Controls in order: exact plane-only determinants of
Szilassi; a rational H' missing the whole solid; exact transformed signs and embedding; the pinned SAT control with
the correct gauge (`symbreak` normalises against infinity: check, do not presume). Uses: (a) C2 4 x 2 + 1 sampling on
the frozen engine with a far plane as infinity, after the seven-plane rung 3 x 2 + 1 recovers Szilassi (the test of
I-261113-04; planted and unaided recovery apart); (b) formulas for the (9, 4) maps with an involution fixing one face,
and for the 20 (11, 5) maps with Aut+ = 2 whose involution fixes exactly one face, as a new registration. No speed-up
at 12 elements keeps (11, 5) priced out; the 165 infinity signs lose their symmetry and nothing measures what remains.

**A5. N3, ninth plane as one formula** (#22, #24). P3 with the eight-plane sub-chirotope pinned to RV or Mizhaev: 84
unknown signs plus the cells. For a sign vector, s_ijk det(p_i, p_j, p_k, x) > 0 is linear in the ninth plane x over
the fixed old coordinates: the LP tests and, if feasible, realizes the extension; infeasible extensions are blocked;
one cap for solve and LP. A changed method for the parked census E-261112-02 (about 79 core-h), price unmeasured.

**A6. P6, equivelar slice** (#14, #15, #22). E = F (F + 1) / 2 = 3 (F + 2g - 2); for 7 <= F <= 12 only (8, 3), (9, 4),
(12, 8); "faces are (F + 1)-gons" is an extrapolation from two objects (CONJECTURE). The extra-edge multigraph is
2-regular; at nine faces the patterns are 9, 7+2, 6+3, 5+4, 5+2+2, 4+3+2, 3+3+3, 3+2+2+2 (seven at eight faces); a
digon is a pair of multiplicity three. The census caps extra edges at 8 (`census.py:154`, `enum_multi.c:186`); (9, 4)
needs 9 and a re-read of the coverage argument. The extra-degree-zero pruning in `enum_multi.c` never applies here and
`report` scans stored classes linearly: price before ranking. Stage A reports maps enumerated, formulas decided,
models sampled and maps realized, with costs per stage and completion flags; it cannot show that RV and Mizhaev are
alone. Failures told apart: control map absent, pinned control UNSAT, unaided recovery timeout (a bridge diagnosis).
Stage B: census inside the joint cap, partial coverage per pattern; maps with a C3 automorphism are not realizations
constrained to C3.

**A7. P1 and symmetric families** (#3, #6, #12, lead notes). K14 unit: rotation (x, y, z) -> (y, z, x), K13's integer
box, hard model at E = 45, cap 20 s, 13.5 s median, 56 bounded cells: about 21,000 units per night per edge count,
less the capped ones. Zero hits in 299 units rejects p >= 0.01 for that box only. Geometric-box arm: K13's D2 2 x 4
sampler with coefficients +-q^w, q in {2, 3}, a declared K, uniform signs and exponents, the unit a draw with
rejections counted, cap 15 s, K13's SOLID criterion (E = 36), baseline the archived K13; a coefficient-distribution
comparison, linked to P4 only if C1 recovers a hit's chirotope. Symmetry facts: a face fixed by a rotation lies in a
plane perpendicular to its axis, so an all-pairs object has at most one fixed face and C3 on nine planes is 3+3+3
only; groups with the central inversion are out (P and -P parallel); one-orbit C_n and C5v families are cones (all
planes through one axis point); C5 with a horizontal mirror is not excluded; D2 4+4+1 with an invariant ninth plane is
non-uniform.

**A8. Adjacency-guided search** (astra, #17, #24). Rational planes; the disk-aware model hard; maximise A = sum a_ij
with the map reselected each time; an archive of high-A solids with different adjacency graphs; one- and two-plane
moves, restarts; incumbent, bound and timeout recorded apart. Controls: positive and deliberately incomplete solids.
Matched eight-plane comparison with independent draws (same distribution, engine, total time and restart rules; known
solutions only as correctness controls), at most 3 core-h, 8 shards; too few recoveries is UNDERPOWERED. The funnel
(the 17 K13 solids, one plane moved) is a diagnostic: within a uniform chamber the optimum is constant, so a first drop
is expected and informative only with a proved optimum.
