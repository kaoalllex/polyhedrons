# Mathematical model

Status legend: **[P]** proved here (argument given), **[K]** known result from the literature
(citation in `literature-review.md`), **[C]** conjecture, **[N]** numerical observation.

## 1. Target (Series 1, F = 12)

A closed, connected polyhedral surface `S` embedded in R^3 (hence orientable) with

| Property | Value |
|---|---:|
| Faces F | 12 |
| Edges E | 66 |
| Vertices V | 44 |
| Sides per face | 11 |
| Faces per vertex | 3 |
| Euler characteristic | -10 |
| Genus | 6 |

Every face is a planar simple polygon (closed disk), every edge lies in exactly two faces, every
pair of distinct faces shares exactly one complete edge, and distinct faces meet only along their
common edge.

### 1.1 Consistency of the parameters [P]

Let every pair of faces share exactly one edge and every edge lie in exactly two faces.
Then edges are in bijection with pairs of faces, `E = C(F,2) = 66`, and each face has `F-1 = 11`
sides. If every vertex is in exactly 3 faces (equivalently, has degree 3 — see 1.2), then
`3V = 2E`, `V = 44`, and `chi = V - E + F = 44 - 66 + 12 = -10 = 2 - 2g`, so `g = 6`.
In general `V = F(F-1)/3`, `chi = F(7-F)/6`, `g = (F-3)(F-4)/12`; this is an integer only for
`F = 0,3,4,7 (mod 12)`, giving `F = 4, 7, 12, 15, 16, ...` as in the repository README.

Remark. The README's Series-1 text says "three faces meet at every vertex" as a consequence;
it is in fact a consequence of the definition only after one more argument (1.2).

### 1.2 Degree 3 is part of the definition; consequences [P]

The pairwise-one-edge condition alone does not force degree 3: it gives `E = 66`,
`sum_v deg(v) = 2E = 132`, and with `deg >= 3`, `V <= 44`, with equality iff every vertex has
degree 3; `V - 66 + 12 = 2 - 2g` then gives `g >= 6`, with `g = 6` iff all degrees are 3.
The README and the mission both fix "three faces at every vertex", so this is part of the
definition. (Vertices of degree `>= 4` mean four or more face planes through one point; that
relaxed family is logged in `open-questions.md` and not pursued.)

At a degree-3 vertex `v` with edges `e1, e2, e3` the three corners belong to pairwise distinct
faces: if two consecutive corners belonged to the same face `A`, the edge between them would
have `A` on both sides, but edges correspond bijectively to pairs of *distinct* faces.
Two distinct vertices cannot lie in the same three faces `{A,B,C}`: the unique edges `AB`,
`BC`, `CA` would all join the same two points, impossible for three distinct straight
segments.

### 1.3 Combinatorial reduction to neighborly triangulations [P] + [K]

Taking the dual map: faces -> vertices, edges -> edges, vertices -> triangles. The dual is a
triangulation of the orientable genus-6 surface with 12 vertices whose edge graph is `K_12`
(every pair of faces adjacent) and which is a simplicial complex (1.2). Conversely, every such
triangulation gives a cubic map with the Series-1 combinatorics. The vertex link of face `A`
in the triangulation is an 11-cycle `(B_1 ... B_11)` through all other faces: it is the cyclic
order of neighbours around face `A`.

[K] Altshuler, Bokowski and Schuchert (1996) proved that there are exactly **59** combinatorial
types of orientable neighborly triangulations of the genus-6 surface with 12 vertices. So the
combinatorial question (research question 1) is settled: there are exactly 59 candidate
combinatorial types. (To be independently re-verified in Track 2.)

## 2. The face-plane formulation (key reduction) [P]

Let face `X` lie in the plane `H_X = { p : n_X . p = d_X }`, with homogeneous vector
`h_X = (n_X, -d_X) in R^4`. For a triangle `{X,Y,Z}` of the dual triangulation, the vertex is
`v_XYZ = H_X ∩ H_Y ∩ H_Z` (the three planes must be independent; otherwise the three edges at the
vertex would be collinear and overlap). The edge between faces `X` and `Y` is the segment
`e_XY = [v_XYC, v_XYD]` on the line `L_XY = H_X ∩ H_Y`, where `XYC`, `XYD` are the two triangles
containing the edge `XY`.

**Consequence.** Given a combinatorial type, a candidate polyhedron is determined by 12 planes
(36 real parameters; 24 after quotienting by the 12-dimensional affine group). All face
polygons are planar *by construction*. **There are no equality constraints at all.** Every
remaining requirement (simple polygons, no self-intersection, nondegeneracy) is a strict
inequality. Hence:

* the realization space of a fixed type is an open semialgebraic subset of `R^36`;
* if any realization exists, an open set exists, so a realization with **rational** (even
  integer) plane coefficients exists, and vertices are then rational: an exact certificate is
  automatically available;
* WLOG the 12 planes, together with the plane at infinity, are in general position.

This is the exact analogue of the vertex formulation of the dual (Császár-type) problem, where
12 points are free and planarity of triangles is automatic.

## 3. Embedding conditions via triple points [P]

For any three faces `X,Y,Z` (not only triangles of the triangulation) let
`P_XYZ = H_X ∩ H_Y ∩ H_Z`. There are `C(12,3) = 220` triple points; 44 of them are vertices.

The intersection of the edge line `L_XY` with the plane `H_Z` is exactly `P_XYZ`.
Therefore an edge `e_XY` can meet a face `Z` (not containing it) only at `P_XYZ`.

**Lemma 3.1.** Assume general position (no four of the 13 planes, including the plane at
infinity, through a point). Then the realization is an embedding iff for every one of the
`220 - 44 = 176` non-triangle triples `{X,Y,Z}` and each of its three splittings into an edge
line and a face:

`NOT ( P_XYZ ∈ relint e_XY  AND  P_XYZ ∈ F_Z )`        (528 conditions)

where `F_Z` is the closed region bounded by the polygon of face `Z`, and in addition each face
polygon is simple. (Simplicity is itself the special case where `P_XYZ` lies on two edges
`e_XY`, `e_XZ` of face `X`; it is listed separately because `F_Z` is only defined for simple
polygons.)

Sketch. A face is a closed disk; the realization map is injective iff every edge meets every
face only in the combinatorially prescribed set (a vertex, the edge itself, or nothing). The
only possible meeting point of `e_XY` and `F_Z` is `P_XYZ`; if `{X,Y,Z}` is a triangle, that
point is the shared vertex. Two faces `F_X`, `F_Y` meet inside `L_XY`; every component of
`F_X ∩ F_Y` is an interval whose endpoints lie on `∂F_X ∪ ∂F_Y`, i.e. at some `P_XYW`;
if `F_X ∩ F_Y ≠ e_XY` some such endpoint is a forbidden point of the type above. Vertices in
face interiors are endpoints of edges, so they are covered too. (To be checked line by line by
the adversarial verifier.)

## 4. Oriented-matroid reduction [P]

Put `h_∞ = (0,0,0,1)` (the plane at infinity) and let `χ(A,B,C,D) = sign det(h_A,h_B,h_C,h_D)`
for `A,B,C,D` in the 13-element set `{1..12, ∞}`. Then:

* `sign` of `P_XYZ` with respect to plane `W` equals `χ(X,Y,Z,W) · χ(X,Y,Z,∞)` (up to the fixed
  sign convention of `h_W`);
* the affine order of the 10 triple points `P_XYZ` (Z ≠ X,Y) along `L_XY` is given by
  `sign(t_W - t_Z) = σ_XY · χ(XYZW) χ(XYZ∞) χ(XYW∞)` with a line-dependent global sign `σ_XY`
  that cancels in every betweenness statement;
* whether `P_XYZ` lies in the open edge `e_XY` is a betweenness statement on `L_XY`;
* whether `P_XYZ ∈ F_Z` can be decided by a parity count of boundary crossings along the line
  `L_ZX` (or `L_ZY`) from `P_XYZ` to infinity, all of whose ingredients are betweenness and
  side-of-plane statements.

Hence **every condition of Lemma 3.1 is a function of the uniform chirotope `χ` of a rank-4
oriented matroid on 13 elements.** A realization of a given combinatorial type yields a uniform
rank-4 chirotope on 13 elements (satisfying the 3-term Grassmann–Plücker relations) that
satisfies all embedding predicates. If, for a combinatorial type, no such chirotope exists
(a SAT problem), that type has no realization. This is the face-plane analogue of Schewe's
method (2010) for the vertex version. Unlike the vertex version, the embedding predicates here
involve up to ~13 elements (parity of up to 9 crossings), not 5.

Symmetries available for symmetry breaking: reorientation of the 12 face elements (fixing
`χ(1,2,k,∞)`, `χ(1,3,4,∞)`, `χ(2,3,4,∞)` removes it), reorientation of `∞` (all predicates are
invariant), global sign (mirror image), and the automorphism group of the triangulation.

## 5. Symmetric form of the embedding condition and explicit predicates [P]

**Lemma 5.1 (symmetric form).** Under general position, with each face region `F_X` taken as the
closed set "boundary curve ∪ points of odd crossing parity" (this agrees with the closed disk when
the polygon is simple), the realization is an embedding iff for each of the 176 non-triangle
triples `{X,Y,Z}`:

`NOT ( P_XYZ ∈ F_X  AND  P_XYZ ∈ F_Y  AND  P_XYZ ∈ F_Z )`.

Proof. (⇒) A point in three faces of an embedded surface is a vertex, i.e. a triangle point.
(⇐) A self-crossing of polygon `X` (edges `e_XW1`, `e_XW2`) happens at `P_XW1W2`, which then lies
on `∂F_X`, on `e_XW1 ⊂ ∂F_W1` and on `e_XW2 ⊂ ∂F_W2`, and `XW1W2` is not a triangle; so all
polygons are simple. Let `I` be a component of `F_X ∩ F_Y ⊂ L_XY`. Each endpoint `p` of `I` lies
on `∂F_X ∪ ∂F_Y`, say on the edge `e_XW` of `X`. If `W = Y`, `p ∈ e_XY`. Otherwise
`p = P_XYW ∈ F_X ∩ F_Y ∩ F_W` (as `e_XW ⊂ F_W`), so `XYW` is a triangle and `p` is an endpoint of
`e_XY`. Hence `I ⊂ e_XY`, i.e. `F_X ∩ F_Y = e_XY` for every pair; with simple polygons this makes
the realization map injective, hence an embedding. (Corners of `X` on `L_XY` other than the ends
of `e_XY` would need four concurrent planes, excluded by general position.) ∎

### 5.1 Side bits and line orders

With `h_X = (n_X, -d_X)` and `χ` as in §4 (fixed vertex ordering convention for the sign of a
permutation):

* `side(abc; d) := sign( n_d · P_abc - d_d ) = χ(a,b,c,d) · χ(a,b,c,∞)`.
* Along `L_XY`, parametrized in the direction of the spatial part of `*(h_X ∧ h_Y ∧ h_∞)`,
  `sign(t_W - t_Z) = χ(X,Y,Z,W) · χ(X,Y,Z,∞) · χ(X,Y,W,∞)`.
* `P_XWV ∈ relint e_XW` (where `e_XW = [P_XWA, P_XWB]`, `A, B` = the two triangle partners of
  `XW`) iff `side(XWA; V) = - side(XWB; V)` (the edge segment crosses the plane `H_V`).

### 5.2 In-face predicate `IN[X; Y, Z]` = "`R = P_XYZ ∈ F_X`" (ray along `L_XY`)

Let `C, D` be the two partners of `XY` (neighbours of `Y` in the link of `X`), and `C'` (resp.
`D'`) the partner of `XC` other than `Y` (resp. of `XD` other than `Y`). Let
`Plus(Z) = { W : t_W > t_Z on L_XY }`.

* boundary terms: `R ∈ relint e_XY` (i.e. `Z` between `C` and `D` on `L_XY`) or
  `R ∈ relint e_XZ` (i.e. `side(XZA; Y) = -side(XZB; Y)` for the partners `A, B` of `XZ`)
  ⇒ `IN = 1`;
* otherwise `IN = parity` of
  * transversal crossings: `#{ W ∈ Plus(Z), W ∉ {C, D} : P_XYW ∈ relint e_XW }`, plus
  * the run `e_XY`, counted once iff `C, D ∈ Plus(Z)` **and** the boundary crosses `L_XY` there,
    i.e. `side(XCC'; Y) ≠ side(XDD'; Y)` (the edges `e_XC`, `e_XD` leave `L_XY` to opposite sides).

## 6. Two complementary SAT formulations

**(A) Fixed combinatorial type, unknown geometry ("OM-SAT", Track 3).** Variables: the 715 signs
`χ` (uniform). Constraints: 3-term Grassmann–Plücker relations; the 176 forbidden-triple clauses
with `IN` expressed through §5.1–5.2 (XOR/parity constraints via auxiliary variables).
UNSAT ⇒ the type is not realizable (sound if every clause is valid for every realization).
SAT ⇒ an oriented matroid candidate; realizability must then be tested separately.

**(B) Fixed geometry, unknown combinatorial type ("geometry-first SAT", Track 4).** Fix 12 planes
in general position. All side bits and line orders are constants. Variables: `t_XYZ` for the 220
triples ("`XYZ` is a triangle"). Constraints:

* every pair `{X,Y}` lies in exactly two triangles;
* every vertex link is a single 11-cycle (lazy cuts forbidding sub-cycles);
* `E[{X,W}; V] := ¬t_XWV ∧ XOR_{A : t_A < t_V on L_XW} t_XWA` ("`P_XWV ∈ relint e_XW`";
  given exactly two partners, an odd number of partners before `V` means `V` lies between them);
* `IN[X; Y, Z]` from §5.2, where `C, D, C', D'` are now encoded through the `t` variables;
* for every triple: `t_XYZ ∨ ¬(IN[X;Y,Z] ∧ IN[Y;Z,X] ∧ IN[Z;X,Y])`.

A model is an embedded Series-1 polyhedron with exactly these face planes (all 59 combinatorial
types and all labelings are searched at once). The instance has only 220 primary variables, so
it can be solved for many arrangements; MaxSAT (soft forbidden-triple clauses) gives a graded
"distance to a solution" for arrangement-level local search. Validation: Szilassi's 7 planes must
give SAT for F = 7.

## 7. Open points in the model

* Exact SAT encoding of the in-polygon predicate (run along the edge `e_ZX` lying on the test
  line must be handled; see `experiment-log.md`).
* Whether the realization space, when non-empty, can be reached from simple starting
  configurations (numerical Track 4).
