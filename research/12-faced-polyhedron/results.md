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
