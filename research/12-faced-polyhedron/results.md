# Results

Only results with evidence. Each section states what is proved, what is computed, and what is
merely observed.

## PI: reductions (2026-10-29)

* [P] The Series-1 parameters (F=12, E=66, V=44, 11-gons, genus 6) follow from the definition
  (mathematical-model.md §1).
* [P] Face-plane formulation: a candidate is a set of 12 planes; planarity is automatic; the
  realization space of each combinatorial type is open in R^36 (§2).
* [P] Embedding ⇔ 176 forbidden-triple conditions (Lemma 5.1), all expressible in the uniform
  chirotope of 13 vectors (12 planes + plane at infinity) (§4–§5).

## Track 2: combinatorial enumeration

(combinatorial-topology researcher, 2026-10-29. Data: `data/`, code: `code/`, definitions:
`data/README.md`. All statements are about abstract triangulated surfaces; nothing here
concerns realizability in R^3.)

**Main result.** [N, computer-assisted, two independent programs] There are exactly **59**
orientable neighborly triangulations of the genus-6 surface with 12 vertices (equivalently
triangular embeddings of K12 in the orientable surface of genus 6) up to combinatorial
isomorphism (relabelling, orientation reversal allowed). This confirms [K] Altshuler–Bokowski–
Schuchert 1996. Up to orientation-preserving isomorphism there are 53·2 + 6 = **112** oriented types.

Method and evidence:
* `code/enum_k12.c`: rotation-system backtracking (WLOG rotation of vertex 0 = (1 2 … 11);
  branch on the directed edge with fewest consistent third vertices; rule Δ forces
  succ[a][b]=v, succ[b][v]=a; premature cycles in any rotation forbidden). Isomorph rejection by
  canonical form = lex-min code over all 264 flag labellings. 12,455,137 nodes, **12,144** labelled
  solutions, **59 classes, 18.9 s on one core**. Orbit–stabiliser check: every class has exactly
  264/|Aut| labelled solutions (Σ = 39·264 + 9·132 + 88 + 7·66 + 2·44 + 22 = 12,144).
* `code/enum2_k12.c` (different algorithm: unoriented triangle sets, branch on the
  lexicographically smallest edge in < 2 triangles, link graphs with no short cycles,
  orientability by parity union-find; no isomorph rejection): **12,144** labelled orientable
  solutions, 214,073,339 nodes, 64.6 s. `code/classify_enum2.py` (uses only the checker's
  routines) assigns each of the 12,144 to exactly one of the 59 entries by brute-force
  isomorphism, hitting every entry exactly 264/|Aut| times.
* `code/check_triangulations.py` (independent of the enumerators, uses only the `triangles`
  field): all 59 entries are 44-triangle simplicial surfaces with edge graph K12, each edge in
  2 triangles, all links 11-cycles, coherently oriented, χ = −10; aut orders and canonical strings
  recomputed; all 1711 pairs non-isomorphic by brute force over 264 flag maps; positive
  control (random relabel + mirror recognised) and 4 negative controls (flipped triangle,
  duplicate type, wrong |Aut|, broken edge) behave correctly. Runtime 4.7 s.
* A cheap invariant (multiset over the 220 vertex triples of the sorted triple of link
  distances d_a(b,c)) already separates all 59 types [N].

**Agreement with external lists** [N]: both `literature/HackerPoet-NeighborlyPolyhedra/topologies.txt`
(59 entries, numbering apparently ABS96) and the Lutz-format
`literature/Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt` (59 entries, Lutz numbering) map
bijectively onto our 59 classes (canonical form + brute-force isomorphism confirmation);
mapping table `data/k12_literature_map.json`. The (|Aut|, |Aut⁺|) pairs in the external
`automorphisms.json` agree with ours for all 59.

**Automorphism groups** [N] (full group incl. orientation reversal; Aut⁺ = orientation preserving):

| # types | Aut | Aut⁺ | our ids |
|---:|---|---|---|
| 39 | trivial | trivial | all others |
| 9 | C2 | C2 | 4, 10, 25, 29, 45, 48, 50, 53, 54 |
| 1 | C3 | C3 | 18 |
| 1 | C2×C2 | C2×C2 | 27 |
| 6 | C4 | C2 | 39, 40, 52, 55, 56, 57 |
| 2 | S3 | S3 | 26, 32 |
| 1 | A4 | A4 | 58 (= ABS96 no.58 = Lutz #54 = Sage `GenusSix()`) |

Observations [N] (all from `data/k12_invariants.json`, recomputed by brute force):
1. **No type has an orientation-reversing involution.** The only orientation-reversing
   automorphisms are the 12 elements of order 4 in the six C4 types (achiral types: 39, 40, 52,
   55, 56, 57; the other 53 are chiral).
   Consequence [P, given the enumeration]: a symmetry of an embedded closed surface in R^3
   preserves the bounded complementary region, hence reverses the surface orientation iff it
   is an improper isometry; the symmetry group of a realization with 44 non-coplanar vertices
   injects into Aut. Hence **no realization of any type can have a mirror plane or a centre of
   symmetry**. Possible symmetric realizations: rotations realizing elements of Aut⁺, and in
   the six C4 types an S4 rotoreflection (whose square is a 2-fold rotation).
2. **Every nontrivial automorphism acts freely on the 12 vertices** (= faces of the polyhedron):
   all vertex orbits have size |Aut| (A4 type 58 is vertex-transitive, regular on vertices).
   So in a symmetric realization no face plane is invariant under any symmetry.
3. Every involution swaps exactly 6 edges (a perfect matching of the vertices) and fixes no
   vertex/triangle: a 2-fold rotation axis would pass through exactly 6 polyhedron edge
   midpoints (perpendicular to those edges). Every order-3 element fixes exactly 2 triangles and
   nothing else: a 3-fold axis would pass through exactly 2 polyhedron vertices.
   Both are consistent with Riemann–Hurwitz (quotient genus 2 in both cases). Order-4
   orientation-reversing elements fix nothing.
4. Vertex-orbit counts: 12 (39 types), 6 (9 C2 types), 4 (C3), 3 (C2×C2 and the six C4),
   2 (S3 types), 1 (A4). Smallest symmetric parameter counts for realization searches thus
   come from types 58 (A4: one orbit of planes), 26/32 (S3: two orbits), 27/39/40/52/55/56/57.

[N, side check, not needed for R^3] `enum2_k12 all` (no orientability pruning) finds
non-orientable neighborly 12-vertex triangulations (χ = −10) in large numbers: a partial run
(stopped after ~257 s CPU) already gave 2,192,916 labelled ones, i.e. > 8,300 non-orientable types
(lower bound only; irrelevant for embeddings in R^3).

## PI: benchmark from prior numerical work (2026-10-29)

Source: HackerPoet/NeighborlyPolyhedra (MIT, commit 7f8fbd6), 1797 near-miss `.obj` files
converted by `code/import_hackerpoet.py` (planes fitted per face; relative planarity residual
<= 2.8e-6). Violation count = number of non-triangle triples whose point lies in all three closed
faces (`code/fastviol.py`, float). It agrees with the source's own "crossings + intersections"
on 1049/1797 files; differences are +-1..5, consistent with float32-stored coordinates of
optimized (near-boundary) configurations; our counter agrees with an independent direct
point-in-polygon float check on 503/514 sampled cases (the 11 differences trace to the loose
tolerance of the direct check at coordinates ~2e5).

* [N] Best count overall: **4** (maps with symmetry, e.g. HackerPoet topology 37, 42, 58).
* [N] Best count on maps with trivial automorphism group (necessarily asymmetric realizations):
  **5** (HackerPoet topology 33 and 36), then 6 (topologies 2, 20, 41, 47), 7 (46 files).
* Since symmetric realizations are claimed impossible (Moki & Julio 2026), the relevant
  benchmark is the asymmetric one.

## Track 3: OM-SAT (2026-10-29)

**Encoder** `code/omsat.py` (general n; faces 0..n−1, ∞=n). Variables χ(sorted 4-set), χ(ordered
tuple)=sgn(sorting perm)·χ(sorted) with χ(abcd)=sign det(h_a,h_b,h_c,h_d), h_∞=(0,0,0,1). Clause
families and their soundness (every clause true for every embedded realisation in general position,
which is WLOG by openness, §2):

| family | content | justification |
|---|---|---|
| F1 GP | 3-term Grassmann–Plücker, 16 six-literal clauses per ({a,b},{c,d,e,f}) (411,840 for n=12) | Plücker identity with all terms ≠0 ⇒ not all three products of equal sign; for uniform χ alternating+3-term GP ⇔ chirotope |
| F2 TRIPLE | ¬IN[X;Y,Z]∨¬IN[Y;Z,X]∨¬IN[Z;X,Y] for the 176 non-triangles, IN as in §5.2 | Lemma 5.1 (re-proved; ⇒ direction suffices for soundness) |
| F3 INCONS (opt.) | IN along L_XY ≡ IN along L_XZ | both equal the true membership; in fact implied by F1 (IN[X;·] depends only on the rank-3 contraction χ/X, a pseudoline arrangement) |
| F4 REFLEX1 (opt.) | at most one reflex corner per vertex | two reflex corners of X,Y at v both contain the open ray −r_XY near v ⇒ F_X∩F_Y ⊋ e_XY |
| F5 RFCONS (opt.) | reflex bit along L_XY ≡ along L_XZ | both rays start in the same open sector |
| F6 POC (opt.) | RTURN ⊕ REFLEX constant over the 11 corners of each face | simple polygon: convex corners turn with the orientation, reflex against it; RTURN = sign(t_B−t_A′ on L_XA)·side(XBB′;A), using "left of +u_XY in H_X (seen from n_X) = positive side of H_Y" (proved: (n_X×u)·n_Y = |n_X|²|n_Y|²−(n_X·n_Y)² > 0) |
| SB reorientation | χ(0,1,k,∞)=+1 (k=2..n−1), χ(0,2,3,∞)=χ(1,2,3,∞)=+1 | the GF(2) map ε↦(those n signs) has trivial kernel (x_k=x_0+x_1 ⇒ x_0=x_1=0), so exactly one of the 2^n reorientations normalises; GP and all predicates are reorientation invariant; reorienting ∞ = reorienting all faces |
| SB mirror | χ(0,1,2,3)=+1 | χ↦−χ (mirror) composed with "flip all faces" fixes the normalisation and negates exactly the face-only quadruples |
| SYM (symmetric runs) | χ(gS)=ε(g)χ(S), ε = orientation character, + orbit-flip basis normalisation + mirror | free action ⇒ choose h_{g r}=diag(ρ(g),1)h_r; det ρ(g)=ε(g) since isometries preserve the solid; one sign per GF(2)-basis vector of orbit-parity vectors |

**Validation** (exact, `code/omsat_validate.py`, `code/omsat_geom.py`): 693 uniform configurations
(n=7: Szilassi control, 292 perturbed Szilassi with 93 embedded, 300 random; n=12: 100 random) —
0 mismatches in 2.5 M predicate evaluations (IN 180,318; REFLEX 76,212; turns 38,106; E 256,530;
orders 1.69 M; sides 281,020); triples ⇔ direct embeddedness on 693/693; CNF/Tseitin literals equal
the Eval values on 17 χ-fixed instances; χ-fixed instance SAT iff embedded (17/17). Cross-check with
Track 4's independent checker: 149 configs, 22,872 IN values, 0 mismatches, embeddedness 149/149.
Szilassi (perturbed) control: all families satisfied; reflex corners per face [1,1,1,1,2,0,2] (one
convex face). n=7 free χ: SAT (<0.1 s) under every option set.

**Symmetric 12-face cases (independent reproduction of the claims of Hashirama1337s/szilassi-12):**
[computed] Lutz #54 under T: UNSAT (1.3 s; also kissat, glucose; also without normalisation);
#3 under D3: UNSAT (9.3 s); #48 under D3: UNSAT (10.6 s); #48 under C2 (half-turn) with F4+F6: UNSAT (298 s; the plain encoding gave no result in 320 s and was stopped). Agreement with their results for these four
cases. Our encoding differs from theirs (Lemma 5.1 triple form, 176 clauses, vs their S+X form).
DRAT proof for #54 T saved (`experiments/omsat/sym_54_T.drat`); not checked with drat-trim (build
refused in this sandbox); own forward RUP checker `code/rup_check.py`: 1034 lemmas, all RUP, empty clause derived — VERIFIED (weaker than drat-trim: self-written checker).
Not done: asymmetric full instances (known to stall per the prior work; not attempted per PI),
realisation attempts (no SAT χ for n=12 arose).

## Track 4: geometry-first SAT

Pipeline: exact integer planes -> SAT over 220 triangle variables (all 59 types x all labelings at once) -> direct exact embedding check of every model.
Validation: IN predicate (§5.2) vs exact point-in-polygon: 242,400 (face,point) comparisons (n=7 and n=12, 4 ray variants), 0 mismatches. Szilassi planes (perturbed to general
position) are SAT and the model equals Szilassi's triangulation (direct checker PASS); 25 perturbed arrangements x 120 labelled tori: encoding, Lemma 5.1, pair test F_X cap F_Y = e_XY and SAT
all agree. Szilassi robustness: SAT for 100% up to relative coefficient noise 1e-2, 97% at 3e-2, 38% at 0.1, 7% at 0.2, 1.7% at 0.3, 0% at 0.5. Random 7-plane arrangements admit a torus with
frequency ~2e-4 (4/18000; 6 distributions).
n=12: 30/30 random arrangements are UNSAT (5-28 s each, no timeouts). Upper bounds on the minimum number of violations (edge-face piercings + polygon self-crossings, B) for 24 random
asymmetric arrangements: 23-39 (median 31); a 9-minute alternating SA/CP-SAT run from a random asymmetric start went 33 -> 24. This is the same plateau (21-24) reported for the GPU numerical search of
Moki & Julio (counting rules not guaranteed identical). No solution/candidate found; this is evidence about the difficulty, not about existence.
Details: experiment-log.md "Track 4", code/planes.py, code/geomsat.py.

## PI: Gauss-map prefilter and the gauge-fixed offset SMT (2026-10-29, session 1 continued)

* [P, sketch in theory-notes.md] Necessary condition on face normals alone: some gauge sign
  vector gives a PL Gauss map of degree chi/2 = -5 whose convex corners cover the sphere.
  Controls: tetrahedron, cube, Szilassi pass with their own gauges.
* [N, exact per instance] **All 1005 HackerPoet near-miss seeds fail it**: no embedded
  realization of the seed's type has the seed's face normals (any offsets). Their own Gauss
  degrees range over -5..+4 (mostly -1..+1): the best known near-misses are not even
  immersions, i.e. topologically far from an embedding although they have only 4-5 violated
  triples. Perturbations of the 20 best seeds (sigma up to 1.0, 400 samples) and 100 random
  normal sets also fail.
* Normals passing the prefilter are easy to find by annealing (seconds; e.g. types 0 and 58).
  The prefilter is not vacuous.
* With admissible normals AND the gauge imposed (`code/fixed_normals_gauge.py`, Szilassi
  control: correct gauge SAT + exact embedding, opposite gauge UNSAT), the exact offset problem
  is decided quickly: type 0 UNSAT 59 s, type 58 UNSAT 90 s, type 5 UNSAT 19 s. Without the
  gauge, seed instances gave no answer in 300 s.
* OM-SAT with Gauss clauses (`code/omsat_gauss.py`, k abstract generic directions as rank-3
  extension elements, degree cardinality + covering): n=7 Szilassi controls SAT (free, and
  with the Szilassi chirotope fixed). Lutz #48, half-turn C2, same machine and load:
  UNSAT 91.8 s without, 99.7 s with k=2, 98.3 s with k=4 directions. **No speed-up** (negative
  result; the 298 s reported by Track 3 was a different load/configuration). The Gauss clauses
  are logically implied by embedding and apparently also easy for the solver to derive in this
  symmetric case; they are not added to the overnight `sym`/`cube` jobs.

## PI: near-misses are not immersions (2026-10-29)

* [N] `code/local_viol.py` counts LOCAL violations: pairs of crossing non-adjacent edges inside a
  face, and vertices with two or more reflex corners (two reflex corners at a degree-3 vertex make
  the two faces overlap beyond the vertex; zero local violations = polyhedral immersion).
  Szilassi: 0/0. Every one of the first 300 HackerPoet seeds has >= 7 multi-reflex vertices;
  the Razorcross family (0 crossings, 4 edge-face intersections) has 8. The triple-point count
  used by all prior searches hides most of these local overlaps.
* So the known near-misses are far from even an IMMERSION, consistent with their wrong Gauss
  degree. Whether the 12-face map admits any polyhedral immersion with planar faces is open to
  our knowledge (test Q12: OM-SAT without global clauses; Q12b: numerical annealing).

## PI: the symmetric obstruction is LOCAL (2026-10-29)

OM-SAT (our encoder, CaDiCaL) on symmetric instances WITHOUT the global forbidden-triple clauses
(`code` script in experiment-log; families: uniform GP, symmetry, orbit/mirror normalization, plus
the listed local families):

| case | simple faces only | reflex <= 1 per vertex only | orientation consistency only | simple + reflex (= immersion) | full embedding |
|---|---|---|---|---|---|
| Lutz #54, T | SAT 0.6 s | SAT 0.4 s | SAT 0.6 s | **UNSAT 2.1 s** | UNSAT 1.0 s |
| Lutz #3, D3 | **UNSAT 5.0 s** | SAT 0.5 s | SAT 1.7 s | UNSAT 5.2 s | UNSAT 4.7 s |
| Lutz #45, C3 | – | – | – | UNSAT 19.1 s (with orientation consistency) | UNSAT 23.1 s |

* For these symmetric cases no polyhedral IMMERSION with planar faces exists; for D3 the 12 face
  polygons cannot even all be simple. The global no-intersection conditions are not needed.
* Hypothesis H-IMM: the 12-face map admits no polyhedral immersion with planar faces at all
  (asymmetric case: overnight `immersion` job + local tests running). Numerical immersion search
  so far: >= 12 local violations from random starts; all known near-misses have >= 7 vertices
  with two reflex corners.

## Night 1 (user's machine, 2026-10-29) and the symmetric immersion sweep

* `sym`: **25/25 symmetric cases UNSAT-VERIFIED** (our encoder, CaDiCaL proofs checked by
  drat-trim; solve 8-147 s each, 1989 s total; proofs 959 MB in total, drat-trim 1071 s; every
  "no triple clauses" control SAT). Independent certified reproduction of the claim that no
  12-face Series-1 polyhedron has a non-trivial symmetry.
* `immersion` (asymmetric, types 0-7): all 8 TIMEOUT at 2.17 h. Asymmetric immersion instances
  are not cheaper than full embedding instances (as the fresh-eyes review predicted for #48 C2).
* PI, this container (no proofs): immersion instances (no global clauses) for ALL 25 symmetric
  classes: 21 C2 classes UNSAT (68-265 s each), 4 C3 classes UNSAT (27-39 s). **[N] No symmetric
  polyhedral immersion with planar faces exists** (stronger than the embedding statement; to be
  DRAT-certified by `run_night2.sh` phase 1).

## PI: "mad ideas" round (2026-10-29)

* [N] **No Szilassi embryo.** In every one of the 59 types, any 7 faces share at most 9 vertices
  (max induced triangles on 7 dual vertices = 9; a punctured 7-vertex torus needs 13). The 12-face
  map contains no Szilassi-like piece.
* [N] **Flat 3-torus relaxation of the closure problem** (`code/period_defect.py`,
  `torus_defect`): replace "period around each handle = 0" by "period = L phi(handle)", with phi an
  integer cohomology class (tree-cotree) and L a free 3x3 lattice matrix. Same Gauss-admissible
  normals: R^3 defect 17.6 (type 0) / 17.4 (type 58); cubic axis-aligned lattice: 15-23 (no help);
  general lattice: 0.5-8 for random phi, and **exactly 0 with a non-degenerate lattice** for type 0
  (det L = 414) and type 58 (det L = 49) within a few trials (configurations in
  `experiments/torus/`). Caveat: these closed, locally consistently labelled configurations have
  NON-SIMPLE faces (0/12 and 1/12 faces simple) — closure level only, not an immersion.
  Interpretation: at the closure level the R^3 obstruction is exactly the vanishing of the handle
  periods; whether simplicity changes this is open.
* [N] Period-defect annealing in R^3, type 0, ~1.5 h: 17.6 -> 8.5 (not 0; still slowly decreasing).

## Night 2, phase 1 (user's machine): no symmetric polyhedral IMMERSION — certified

`symimm` job (our encoder without the global triple clauses: uniform GP, symmetry, normalization,
simple faces, at most one reflex corner per vertex, orientation consistency): **25/25 classes
(21 half-turn C2, 4 three-fold C3) UNSAT-VERIFIED** with CaDiCaL DRAT proofs checked by drat-trim
(7-158 s per case). **[Theorem, computer-assisted, certified]** No polyhedral immersion in R^3 of the
12-face Series-1 map with planar faces has a non-trivial symmetry. This strengthens the symmetric
embedding statement (night 1) and, as far as we know, is new. (The soundness of the local clause
families rests on mathematical-model.md and the adversarial review; SIMPLE + REFLEX1 = immersion was
re-checked in fresh-eyes-review.md.)

* [N] Torus + simple faces (`torus_simple`, exact closure, edge signs, vertex rules, and a 4-way
  disjunction per non-adjacent edge pair): for the two zero-defect torus configurations above, the
  problem with simple faces is INFEASIBLE (type 0: 116 s, type 58: 392 s; HiGHS); the R^3 version is
  infeasible in 2-3 s. The torus success was a closure-level phenomenon; face simplicity is an
  independent strong component of the obstruction.
