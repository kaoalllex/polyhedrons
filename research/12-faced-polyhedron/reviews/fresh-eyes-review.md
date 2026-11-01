# Fresh-eyes review (2026-10-29)

Reviewer: mathematical researcher who had not seen the project before. Read: sprint-board,
results, solution-portrait, proof-roadmap, mathematical-model §1-7, theory-notes (including the PI
addendum), literature-review §6, 7, 11, 12. I read code only where a claim needed checking:
`gauss_degree.py`, `gauss_search.py`, `q10_core.py`, `local_viol.py`, `immersion_sat.py`, and
`omsat.build` / `omsat_sym.build_sym`. Labels: **[P]** proved here (proof given), **[K]** known
(cited), **[C]** conjecture, **[N]** numerical or computational observation. New scripts are in
`code/fresh_eyes/` (§6).

## 0. Summary

Critique, most important first:

1. **The Gauss-map prefilter is correct.** I re-derived it independently, including the
   sign and orientation conventions (§1.1). The fact that it excludes all 1005 near-misses is
   plausible, not suspicious. As a *constructive* filter, though, it is weak: 12 out of 12
   Gauss-admissible normal sets that I tested fail an exact closure LP in at most 10 s (§2.3). So
   the overnight `gnormals` job spends z3 time on normal sets that a much cheaper test rejects.
2. **The Q10 result ("UNSAT already from LOCAL conditions") is mis-described.** For fixed
   admissible normals the obstruction is the closure LP, and within it the 36 *period* (handle)
   conditions. Per-face closure together with legal junction labels is satisfiable in 12/12 cases.
   So the fixed-normal obstruction is cohomological (the structure of Penrose's impossible
   figures), not local (§2.3).
3. **"The symmetric obstruction is local" (A1) holds for embeddings; I found no artifact**
   (§1.2). Two caveats:
   - "Local" only means that the forbidden-triple clauses are absent. The chirotope axioms
     themselves carry global geometry.
   - The evidence came from groups with 2-8 free parameters. New data at 12 parameters (§2.4):
     for Lutz #48 under C2 the immersion instance is **UNSAT in 91 s**, but **SAT in 114 s once
     face simplicity is dropped**. It also cost about the same as the embedding instance (about
     92 s), so it was not cheaper.
4. **The Q12c "always even" counts are forced by a parity theorem** (§2.2):
   Σ(face self-crossings) + Σ_v C(r_v,2) ≡ χ (mod 2) for *every* configuration in general
   position. The parity therefore carries no information. The Banchoff analogy does not apply.
5. **Minor points.**
   - theory-notes §3.1 "normals mod GL(3) = 15 dims" should read 16.
   - Positive admissibility is certified only at the sampled directions.
   - G3 tested one gauge per normal set.

New results:
- face-winding identity r_X = σ_X + 2w_X − 2·rot_X [P];
- the parity theorem [P];
- the fixed-normal obstruction is cohomological [N];
- the first C2 immersion instance is UNSAT, and simplicity is essential to it [N].

## 1. Critique

### 1.1 Gauss-map prefilter (theory-notes, PI addendum)

**Verdict: correct [P, re-derived].** The implementation (`gauss_degree.py`) matches the statement.

Independent derivation:

- **(i) Vertex term.** Take a vertex v whose faces X, Y, Z appear counter-clockwise seen from
  outside, with outward normals N. The link of v is a closed curve made of three great-circle arcs
  whose lengths are the corner angles.
  - *Corner* (three convex face corners): the link is a convex spherical triangle, so
    δ_v ∈ (0, 2π).
  - *Saddle* (exactly one reflex corner): the long arc contains a pair of antipodal points. A
    closed curve through antipodal points has length ≥ 2π, and in general position the inequality
    is strict: equality would need a great semicircle built from arcs of two distinct great
    circles. The angle sum is also < 4π. Hence δ_v ∈ (−2π, 0).
  - The Gauss image of the rounded vertex disk is the 2-chain ε[Δ_v] + c[S²], where Δ_v is the
    geodesic triangle with area a ∈ (0, 2π). (Three independent vectors span a cone inside an open
    half-space.) Its signed area is εa + 4πc = δ_v. Since |δ_v| < 2π, this forces c = 0 and
    ε = sign δ_v.
  - The boundary is traversed N_X → N_Y → N_Z along short arcs, so ε = sign det(N_X, N_Y, N_Z).
  - Therefore **corner ⇔ det > 0 and saddle ⇔ det < 0**. This agrees with theory-notes 1.2
    (derived there from turn signs) and with the Szilassi check at all 14 vertices.
- **(ii) The gauge equals the outward normal when K carries the outward orientation.**
  - Explicit check on the cube's top face T [P]. The link order E→N→W→S is counter-clockwise about
    +e3. The triangle (T,E,N) is positive, det(e3,e1,e2) = +1, and the vertex is convex.
  - In general: walking along ∂F_X with F_X on the left, one arrives at v along e_{XB_i} and
    leaves along e_{XB_{i+1}} exactly when (X, B_i, B_{i+1}) is the counter-clockwise order at v.
  - Reversing K's orientation turns the gauge into inward normals and gives D(u) ↦ D(−u) = D.
  - The global flip g ↦ −g gives D ↦ −D.
  - Because all 2^12 sign vectors are searched, the result depends neither on the orientation
    stored in the data file nor on chirality.
- **(iii) Degree.** For *any* normals, D(u) is the degree of the PL map K → S² (each triangle is
  sent to its geodesic triangle), so it is automatically independent of u. For a realization it
  equals χ/2 [K: Hopf; Gauss–Bonnet].
- **(iv) Covering.** For a generic u, the maximum of ⟨u,·⟩ on S is attained at a vertex.
  - That vertex is not a saddle: by (i) its link contains points w, −w with ⟨u,w⟩ ≠ 0.
  - The solid near it is the octant lying below it. Otherwise the compact solid U would contain
    points above max_S⟨u,·⟩, but a linear function attains its maximum on U at ∂U = S.
  - Hence u lies in that vertex's outward normal cone, i.e. in a positive triangle.

Points that should be stated explicitly:

- **The degree condition is immersion-level; the covering condition is embedding-level.**
  - Hopf's theorem holds for immersions, so the degree must be −5 for any immersion.
  - For an immersion the extremal corner's normal may point either up or down, which gives only
    p(u) + p(−u) ≥ 1 [P].
  - So "the near-misses fail the prefilter" mixes two statements. L1 (every seed has ≥ 7
    multi-reflex vertices) shows they already fail at the immersion level, which is the more
    informative statement.
- **The `continue` on a zero vertex determinant is sound.** If three normals of a vertex triangle
  are coplanar, that vertex does not exist for those normals.
- **Exclusions are exact; positive claims are not.** "Admissible normals exist" (G2, G3, Q5) is
  checked only at sampled directions (3000 in the annealer, 64 in the exact recheck), so label
  those claims [N].
- **Controls.**
  - The tetrahedron and cube fix the absolute sign.
  - Szilassi fixes the relative corner/saddle sign at its 14 vertices. Its degree, 0, cannot
    detect a sign error.
  - A perturbed, non-convex L-prism (genus 0, with saddles, target +1) would test the complete
    formula. Optional.

**Is "all 1005 seeds excluded" suspicious? No.**
- The seeds are non-immersions (L1).
- The admissible region is small: 100 out of 100 random normal sets also fail.
- The near-misses were optimized for a count that does not see local overlaps.

**What does deserve attention is that the prefilter is weak.** Annealed admissible normals fail
a closure LP immediately (§2.3).

### 1.2 "The symmetric obstruction is local" (A1)

What the clauses assume (checked in the code):

- **SIMPLE.** The clause ¬E(X,W1,W2) ∨ ¬E(X,W2,W1), for non-adjacent edges of face X, says that
  no two non-adjacent edges cross. In general position this is equivalent to simplicity: adjacent
  edges meet only at their common corner, and a corner lying on a non-adjacent edge would need 4
  concurrent planes [P].
- **REFLEX1.** At most one of the three parity-defined reflex bits at a vertex is set. For simple
  polygons the parity bit equals geometric reflexness. SIMPLE + REFLEX1 ⇔ polyhedral immersion
  [P]: with at most one reflex corner, the three sectors meet pairwise only along their common
  edges (explicit in the affine coordinates of theory-notes 1.1).
- **POC + gauge.** Sound for simple faces.
- **SYM.** The clauses χ(gS) = det ρ(g)·χ(S), with h_{gX} = ρ(g)h_X (WLOG for a free action), the
  orbit-flip normalization over a GF(2) basis, and the mirror normalization are all valid for
  embeddings [P, checked].
  - For *immersions* these instances cover only automorphisms realized by rotations. Without a
    solid, an improper isometry could also realize an orientation-preserving automorphism.
  - This matters only if one wants to state "no symmetric immersion"; it is irrelevant for
    embeddings.

**So the UNSAT is not an artifact.** What can mislead is the word "local" and the extrapolation:

- **"Local" means only that there are no forbidden-triple clauses.** The 3-term Grassmann–Plücker
  relations encode a global object, and in the fixed-normal analogue (§2.3) the obstruction
  turns out to be homological.
- **The groups so far had few parameters:** T, D3 and C3 have 2, 4 and 8. The first C2 case,
  with 12 parameters, gives UNSAT, but only with SIMPLE (§2.4). So **face simplicity is
  essential**. Note also D3, where simplicity alone is already UNSAT.
- **The immersion instance was not cheaper:** 91.3 s against about 91.8 s for the embedding
  instance (G4). The roadmap's expectation "UNSAT and cheaper" is not supported in this case.

### 1.3 Reduction: general position, plane at infinity, 59 types

- **Openness and general position.** The realization space is open without first assuming general
  position. By compactness, non-incident cells keep a positive distance under small
  perturbations, and incident cells are controlled by the non-degenerate local models at edges and
  vertices. Hence general position of the 13 planes is WLOG [P].
- **Plane at infinity.** General position here means that no two face planes are parallel and no
  three normals are coplanar. This is WLOG [P].
- **Combinatorics.** The dual is simplicial and neighborly [P, model §1.2-1.3]; there are 59 types
  [K, ABS96; N, re-enumerated here].
- **Lemma 5.1 (⇐).** I checked the interval argument; it is complete.
- **Slip in theory-notes §3.1.**
  - The normals are 12 points of RP² modulo PGL(3): 24 − 8 = **16** dimensions, not 15.
  - The offsets give 12 − 4 = 8 (translations and scalings).
  - Total 16 + 8 = 24 = 36 − 12 [P].
- **One gauge per normal set.** G3/Q10 imposed only the annealer's gauge. This is harmless given
  §2.3.

### 1.4 Board entries to re-label

| Entry | Current | Suggested |
|---|---|---|
| Q10 | "local structure is the bottleneck" | face closures + labels are SAT; the 36 handle periods fail (cohomological), §2.3 |
| Q12c | "parity invariant? cf. Banchoff" | DONE: forced by §2.2, carries no information |
| Q14 | KILL (vertex rule only) | still KILL with the F6 flip counts added (22/24 SAT, §2.1) |
| G3 / `gnormals` | KEEP | add the closure-LP stage before z3, or replace the objective (idea 2) |
| A1 | DONE | extend to all 21 C2 classes (idea 1); #48: UNSAT, simplicity essential |

## 2. New results

### 2.1 Face-winding identity [P]

**Setting.** Any configuration in general position of an oriented type (coherent link orders),
with arbitrary signs of the face normals g_X. For a face X with link B_1..B_11:

| Symbol | Definition |
|---|---|
| p_B | projection of g_B to g_X^⊥ |
| w_X | winding number about 0 of the closed polygon p_{B_1}..p_{B_11} in g_X^⊥ (oriented by g_X); this is the local degree, near g_X, of X's star in the PL normal map |
| ε_i | sign det(g_X, g_{B_i}, g_{B_{i+1}}) |
| σ_X | #{i : ε_i = −1} |
| rot_X | turning number of the polygon F_X about g_X |
| r_X | number of corners of F_X turning clockwise about g_X |

**Identity:** `r_X = σ_X + 2 w_X − 2 rot_X`.

*Proof.*
1. Edge i is traversed in direction μ_i (g_X × g_{B_i}) = μ_i |g_X| R_90 p_{B_i}, with μ_i = ±1.
2. The exterior angle at corner i is therefore the short rotation from μ_i p_{B_i} to
   μ_{i+1} p_{B_{i+1}}.
3. The short rotation from p_{B_i} to p_{B_{i+1}} has sign ε_i, and these rotations sum to
   2π w_X.
4. If μ_i = μ_{i+1}, the two rotations agree. Otherwise they differ by −π ε_i.
5. Let A^± = #{i : μ_i ≠ μ_{i+1}, ε_i = ±1}. Then 2π rot_X = 2π w_X − π (A^+ − A^−).
6. A corner turns clockwise exactly when (μ_i = μ_{i+1} and ε_i = −1) or
   (μ_i ≠ μ_{i+1} and ε_i = +1). Hence r_X = σ_X − A^− + A^+.
7. Eliminating A^+ − A^− gives the identity. ∎

**Consequences for a realization, in the gauge** (rot_X = 1; reflex corners occur only at
saddles) [P]:
- r_X = σ_X + 2w_X − 2. **The number of reflex corners of each face is determined by the normals
  alone.**
- Face X has a_X = 2 − 2w_X convex corners at saddle vertices, and this number equals the number
  of edge-type changes around X. Hence **w_X ≤ 1** for every face, and σ_X + 2w_X ≤ 10.
- Analogy: this is a Maekawa-type count (origami: mountain − valley = ±2 around a flat vertex),
  taken around a face instead of a vertex.

Checks:
- [N] **Szilassi**: the identity holds on all 7 faces. (σ, w, r) per face:
  (3,0,1), (3,0,1), (5,−1,1), (5,−1,1), (2,1,2), (4,−1,0), (2,1,2).
- [N] **24 annealed normal sets** (types 0, 5, 58; seeds 0-7; all exactly re-verified as
  admissible):
  - all counting conditions hold, with w_X ∈ [−4, 1] and r_X ∈ [0, 5];
  - the κ-CSP (vertex rule + flip counts) is SAT in 22/24;
  - the two failures each have a face with w_X = 1.
  - **The F6-strengthened κ-prefilter is therefore nearly toothless.**

### 2.2 Parity theorem [P] (settles Q12c)

**Statement.** Let a closed orientable cubic polyhedral map have planar faces in general
position, and choose any face gauges. Let c_X be the number of self-crossings of polygon X and r_v
the number of reflex corners at vertex v. Then

`Σ_X c_X + Σ_v C(r_v, 2) ≡ χ(S) (mod 2)`.

*Proof.*
- **(a) Vertex term.** Around a positive triangle (X,Y,Z), the three turn signs multiply to
  ε_v = sign det(g_X, g_Y, g_Z). Each μ occurs twice, and μ_X(Y) = μ_Y(X) because adjacent faces
  traverse their common edge in opposite directions. So r_v is odd ⇔ ε_v = −1.
  - For r ≤ 3, C(r,2) ≡ ⌊r/2⌋ (mod 2).
  - Hence Σ_v C(r_v,2) ≡ (R − q)/2, where R = Σ_X r_X and q = #{v : ε_v = −1}.
- **(b) Face term.** Sum §2.1 over all faces.
  - Σ σ_X = 3q.
  - Σ_X w_X = (1/2π) Σ_t ε_t·(angle sum of spherical triangle t) = (p − q)/2 + 2D. Here each
    angle sum is π + area, Σ_t ε_t area_t = 4πD, and D is the degree of the normal map.
  - So (R − q)/2 = V/2 + 2D − Σ rot_X.
- **(c) Whitney** [K: H. Whitney, Compositio Math. 4 (1937)]. A generic closed polygon has
  c_X ≡ rot_X + 1 (mod 2).
- **(d) Conclusion.**
  - Adding (a)-(c) gives a total ≡ V/2 + F ≡ F − V/2 = χ (mod 2), since E = 3V/2.
  - General position makes the polygons generic: a triple self-intersection, or a corner lying on
    a non-adjacent edge, would need 4 concurrent planes. ∎

**For F = 12.**
- The count used by `local_viol.py` (crossings + #{v : r_v ≥ 2}, and #{r_v ≥ 2} ≡ Σ C(r_v,2)) is
  always even.
- With simple faces, the number of non-immersion vertices is even. Topologically, these vertices
  are the endpoints of double curves, like Whitney umbrellas.

**Checks [N].** Even crossings + multi on 1005/1005 seeds. The 157 seeds with simple faces all
have an even multi-reflex count. 334 non-simple seeds have an odd multi-reflex count, compensated
by odd crossings.

So the even counts in Q12c are forced and say nothing about realizability. The smallest
non-zero local count is 2.

### 2.3 For fixed admissible normals the obstruction is cohomological [N]

**Setup** (`closure_and_parity.py`, `penrose_lp.py`, `controls.py`). Integer gauge normals,
annealed and exactly re-verified as admissible. Unknowns: edge labels κ_e, a global sign s, and
offsets e ∈ R^12. Constraints:
- vertex rule;
- per-face flip count 2 − 2w_X, which is the condition rot = 1 (§2.1);
- each edge is traversed in direction s·κ_e·(g_X × g_B): 66 homogeneous strict linear
  inequalities in e, normalized to ≥ 1.

This is Q10's local system written in turning form, without parity predicates.

**Results.**

| Test | Result |
|---|---|
| Full system (offsets) | **UNSAT for 12/12** normal sets (types 0, 58, 5; seeds 0, 1, 2, 4), 0.0-9.4 s each |
| Control: Szilassi (n = 7) | SAT |
| Control: random 12-plane configurations with their own orientation pattern (labels dropped) | SAT (2/2) |
| Without periods: one scalar α_e per edge, edge vector α_e(g_X × g_Y), sign(α_e) = sκ_e, each face polygon closes | **SAT for 12/12**, ≤ 0.4 s |

The relaxation drops exactly the 36 = 12 × 3 period conditions, i.e. the conditions that the
edge vectors integrate around the 12 handles. Indeed Λ = Λ_loc ∩ {periods = 0} [P]: integrating
the edge vectors gives vertex positions, and the vertices of each face are then coplanar with
normal g_X. Dimensions: 66 − 21 (independent face closures) − 36 = 9 = 12 − 3.

**Interpretation.**
- [N → C] Every face can be closed with legal trihedral junction labels, but the faces cannot be
  assembled into a compact surface. The defect lies in H_1(S; R^3).
- This is the structure of impossible figures:
  - [K: R. Penrose, "On the cohomology of impossible figures", Leonardo 25 (1992)];
  - and of Sugihara's realizability LP for labelled line drawings [K: K. Sugihara, *Machine
    Interpretation of Line Drawings*, MIT Press 1986]. Its junction labels are Huffman–Clowes
    trihedral labels, and the vertex rule F4 is exactly such a junction catalogue.
- **Heuristic [C].** For fixed normals the offset image Λ is a 9-dimensional subspace of R^66. A
  uniformly random 9-dimensional subspace meets a fixed open orthant with probability
  2^-65 Σ_{i≤8} C(65,i) ≈ 1.6e-10 [K: Wendel 1962; Cover 1965]. Closable normals are therefore
  very special, which is consistent with H-a, Q1, Q2, G3 and Q10.

### 2.4 First C2 immersion instance [N]

Lutz #48 under C2 (one conjugacy class); 8527 variables, 443,310 clauses; CaDiCaL 1.9.5 via
pysat; no proof file.

| Clause set | Result |
|---|---|
| SIMPLE + REFLEX1 + POC, no forbidden triples | **UNSAT, 91.3 s** |
| Same, without SIMPLE | **SAT, 114.3 s** (model not analysed) |

## 3. New directions, ranked by (probability of real progress) × (cheapness)

None of these is on the sprint board.

| # | Idea | Correspondence | Test (≤ 10 min or one page) | Outcome → belief |
|---|---|---|---|---|
| 1 | **C2 immersion sweep** over all 21 half-turn classes, each with a no-SIMPLE control | 12-parameter analogue of A1 | `c2_immersion.py MAP CLASS 900 [nosimple]`, about 2 min each | Any SAT: the asymmetric immersion instance of that map is SAT too (a C2 chirotope, renormalized, is a model), so the local proof route is dead for that map; try to realize it (it would be the first polyhedral immersion). All UNSAT: H-IMM holds under every half-turn; certify with DRAT; compare cost with the embedding instances |
| 2 | **Period-defect ("Penrose") search** for closable admissible normals | Penrose's cohomology of impossible figures; Sugihara's line-drawing LP | LP: m(g,κ) = min ‖periods‖₁ subject to face closures and sκ_eα_e ≥ 1; anneal g inside the admissible class, κ from the CSP; 10 min, types 0 and 58 | m → 0: closable admissible normals exist; run the full gauge SMT on them. m bounded away from 0 across restarts: evidence for [C] "no locally consistent closed configuration of degree −5 exists" |
| 3 | **Realizability audit of SAT OM models** (C2 #48 without SIMPLE; A2 type 0 simple-only) | Bokowski–Richter-Gebert final polynomials; realizability of rank-3 contractions | Hinge-loss sign fitting of the rank-3 contraction at ∞ and of each face contraction (12 points/lines in the plane, seconds), then of the C2 rank-4 configuration (12 parameters) | Non-realizable: OM-level relaxations are too weak, and contraction-realizability clauses may make local instances UNSAT cheaply. Realizable: a concrete C2 configuration that is locally consistent but has non-simple faces, to study |
| 4 | **Farkas certificate mining** for the period obstruction | Maxwell–Cremona reciprocity (structural engineering): the dual is a set of in-plane vectors ρ_X plus period functionals b_γ ∈ R^3 | scipy/HiGHS dual for the κ found by `penrose_lp`, over 100 admissible sets; record the support and which handles carry b | A recurring pattern (b concentrated on few handles, tied to the local degrees w_X) suggests a lemma "degree −5 ⇒ nonzero period", i.e. a human proof route. Dense, unstructured certificates: none |
| 5 | **Turning-defect diagnostics** for the immersion annealer (Q12) | identity §2.1 | for every state record rot_X per face, the multi-reflex vertices and the crossings; by Whitney, rot_X ∈ {0, 2} forces odd crossings | Shows whether the 12-violation plateau consists of face-turning defects or vertex defects; choose moves that keep rot = 1 |
| 6 | **Continuous violation depth** Φ = Σ over violated triples of min over the 3 faces of the distance to the face boundary (zero ⇔ embedded in general position, by Lemma 5.1) | Hougardy–Lutz–Zelke intersection-edge functional; cloth untangling by intersection contours (Baraff–Witkin–Kass 2003) | about 60 lines of code; CMA-ES/Nelder–Mead on 24 parameters from the 20 best seeds and from closable normals, 10 min | Φ → 0: candidate. Reproducible positive local minima: landscape evidence; replaces flat count plateaus |
| 7 | **First-moment calibration** | random-CSP first-moment method; Wendel's theorem | count κ-CSP solutions N_κ for admissible normals (enumeration or ApproxMC); compare N_κ·1.6e-10 with the observed 0/12 | Quantifies how rare closable normals should be; if the expected count is ≪ 1 per normal cell before simplicity, prioritize proof over search |
| 8 | **Pinkall/Arf invariant of the three-face annuli** A_XYZ = F_X ∪ F_Y ∪ F_Z | regular homotopy of immersions [K: Pinkall, Topology 24 (1985)]; an embedded surface has Arf(q) = 0 and q vanishes on a Lagrangian | for any immersion found (ideas 1 and 3, Q12): compute q(γ_XYZ) = lk(∂A_XYZ) mod 2 and Arf(q) | Arf = 1: that immersion's regular-homotopy class contains no smooth embedding. This is an embedding-level invariant obtained from three-face data |
| 9 | **Face-local types with a prescribed reflex count** | roadmap direction 3, coupled to §2.1 | per face, list the 11-line arrangements whose polygon has r_X = σ_X + 2w_X − 2 reflex corners and edge-orientation pattern μ fixed by the normal cell | Prunes the per-face join over the 13 contractions |
| 10 | **Two charts at infinity** | projective invariance: any plane missing S can be sent to infinity | OM-SAT with a 14th element π (all 44 vertices on one side), and Gauss degree and covering also at π | Low prior (redundant constraints did not help in G4) |

## 4. Most promising: idea 1 now, then idea 2

**Idea 1: C2 immersion sweep (ready to run).**
- Script: `code/fresh_eyes/c2_immersion.py MAP CLASS TIMEOUT [nosimple]` (Lutz numbering).
- It builds GP + SYM + orbit/mirror normalization + SIMPLE + REFLEX1 + POC, without TRIPLE.
- Run every C2 class (21 classes in 19 maps, as enumerated by the `sym` job). For each map, the
  script prints its class count; use CLASS = 0..k−1.
- Add `--proof` handling (copy it from `omsat_sym.main`) and check every UNSAT with drat-trim.
- Run each case a second time with `nosimple`.
- Budget: about 21 × 2 × 2 min ≈ 1.5 h on one core.

Reading the outcomes:
- **A SAT with SIMPLE** refutes H-IMM at the OM level for that map. Save χ and realize it
  numerically (12 C2 parameters); a realization would be the first polyhedral immersion of the
  12-face map.
- **All UNSAT** supports H-IMM. If, as for #48, the cost matches the embedding instances, the local
  route gives cleaner certificates but no speed-up; plan the asymmetric campaign accordingly.
- **"nosimple" SAT everywhere** makes face simplicity the key ingredient. Then invest in idea 9 and
  in roadmap direction 2 (simplicity cores).

**Idea 2: period defect (constructive and evidential).**
- For integer gauge normals g, a κ-CSP solution and a sign s, minimize
  Σ_{γ in fundamental cycles} ‖Σ_{e∈γ} ±α_e t_e‖₁, where t_e = g_X × g_Y.
- Constraints: face closures and s κ_e α_e ≥ 1.
- This is an LP: 66 + 3·23 variables, using the 23 fundamental cycles of the edge graph modulo a
  spanning tree.
- Outer loop: anneal g among admissible normals, re-solving κ (minimum-change) every few moves.
- **m = 0 means closable.** Feed such normals to `fixed_normals_gauge` or `q10_core`, which then
  test simplicity and embedding exactly.

## 5. New hypotheses

| Label | Statement | Test |
|---|---|---|
| H-FE1 [C] | In every type, Gauss-admissible normals are almost never closable; the realization space projects to a set of tiny measure inside the admissible region | ideas 2 and 7 |
| H-FE2 [C] | In all 21 C2 classes the immersion instance is UNSAT and its no-SIMPLE version is SAT | idea 1 |
| H-FE3 [C] | Fixed-normal closure failures are always cohomological: no-period relaxation SAT, full LP UNSAT | `penrose_lp.py` on more than 100 admissible sets (minutes) |

## 6. Reproducibility and limitations

**Scripts** (all in `code/fresh_eyes/`, run with `python3`; z3, numpy and pysat as installed):

| Script | What it does | Runtime |
|---|---|---|
| `winding_lemma.py` | §2.1: Szilassi check + κ-CSP on 24 normal sets | ~1 min |
| `closure_and_parity.py` | §2.2 seed parity + §2.3 full closure LP | ~2 min |
| `penrose_lp.py` | §2.3 no-period relaxation | ~1 min |
| `controls.py` | Szilassi and random-plane controls, crossing-parity check | ~1 min |
| `c2_immersion.py 48 0 240 [nosimple]` | §2.4 | ~2 min |

**Limitations.**
- The normal sets come from one annealer (a biased sample, only 12-24 sets).
- Only one C2 instance was run, without a DRAT proof.
- The proofs of §2.1 and §2.2 are mine and unrefereed; they are corroborated on Szilassi and on
  1005 seeds.
- The OM predicates were not re-audited line by line.
- I read no primary literature beyond the project's own summaries.
