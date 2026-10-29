# Theory notes, Track 6 (necessary conditions, symmetry, construction)

Author: mathematical-researcher, 2026-10-29. Labels: **[P]** proved here (proof given), **[K]** known
(cited), **[C]** conjecture, **[N]** numerical observation. Notation as in `mathematical-model.md`
(planes `H_X`, `h_X = (n_X, -d_X)`, `χ`, `P_XYZ`, `L_XY`, `e_XY`, link of `X` = cyclic order of
neighbours = boundary order of polygon `F_X`). General position (GP) of the 13 planes is assumed
throughout, as in the model.

## 0. Clause families: summary and soundness status

| # | Family | Statement (sketch) | Status | Implied by Lemma 5.1 in OM-SAT? |
|---|---|---|---|---|
| F1 | at most one reflex corner per vertex | 3 binary clauses per vertex on reflex literals | [P] sound | yes, but only by a long-range argument (1.1); helpful in practice (Moki–Julio "orient": 2.7–10x) |
| F2 | gauge `W ≡ +1`, `λ` fixed | each face plane oriented so its link order is CCW about `n_X` | [P] valid symmetry breaking (replaces the χ-fixing reorientation breaking; do not combine with it) | n/a (symmetry breaking) |
| F3 | vertex type = one sign | in gauge: `v_XYZ` saddle ⟺ `χ(X,Y,Z,∞) = -1` for the positively oriented triangle `(X,Y,Z)` | [P] sound | no (needs F2 + reflex-parity link F5) |
| F4 | edge-type rule | in gauge, at every vertex: the 3 edges have equal dihedral type ⟺ corner vertex | [P] sound; equivalent to F1 given F3 | as F1 |
| F5 | reflex-parity link | reflex literal (local χ-product) = parity of boundary crossings on the ray beyond the corner | [P] sound | it is the bridge between local signs and the parity predicates |
| F6 | face turning rule | per face, the 11 vectors `κ_i p_i` wind exactly once (+1) about 0 | [P] sound | probably implied (rank-3 Umlaufsatz), not checked |
| F7 | Gauss degree `DEG_W` | for each `W`: Σ over oriented triangles `t ∌ W` with `-n_W ∈ cone(t)` of `χ(t,∞)` equals `χ(S)/2 = -5` | [P] sound | **not known to be implied** (uses Hopf / Morse theory) |
| F8 | covering `COV_W` | for each `W`: some positively oriented triangle has `-n_W` in its cone; hence `q_W ≥ 6` | [P] sound | **not known to be implied** (uses existence of a global maximum) |
| F9 | saddle count | `#{saddle vertices} ≥ 13` (generally `≥ 2g+1`) | [P] sound | **not known to be implied** (metric: area argument) |
| F10 | offset-line parity / orientation alternation | along lines offset from `L_XY` into each quadrant, the crossings of `S` are even in number and alternate entering/leaving, the direction being fixed by the gauge normal | [P] sound | parity part implied in realizable case; Moki–Julio report the parity part slowed the solver; the alternation part is new and untested |
| F11 | per-face convex corners | `≥ 3` convex corners per face (`r_X ≤ 8`) | [P] sound | implied by F6 |
| — | "no face on the convex hull" | **false** as a necessary condition: two Szilassi faces lie in supporting planes [N] | refuted (for F=7 analogue; no reason to expect it for F=12) | — |
| — | new local "linking" clause at a non-triangle point `P_XYZ` | none found beyond "at most one of `e_XY, e_YZ, e_XZ` contains `P_XYZ`" (implied) | Lemma 5.1 is complete; no further local clause exists that is not a consequence of it in realizations | — |

All "sound" families are valid for every embedded realization in GP; they can be added to
formulation A (OM-SAT) without losing solutions. F7–F9 are the only *global* ones and the only ones
for which I see no derivation inside the abstract encoding; they constrain only the rank-3
contraction `χ(·,·,·,∞)` (the configuration of the 12 normals) once the gauge F2 is imposed.

## 1. Local structure at vertices and edges

### 1.1 At most one reflex corner per vertex [P]

Let `v = v_XYZ`. The three edges leave `v` along linearly independent directions `u_XY, u_XZ,
u_YZ` (independence of the three planes). Apply the affine map sending `v ↦ 0`, `u_XY ↦ e1`,
`u_XZ ↦ e2`, `u_YZ ↦ e3`; convexity of corners and all incidences are affine invariants. Then
`H_X = {c=0}`, `H_Y = {b=0}`, `H_Z = {a=0}` (coordinates `a e1 + b e2 + c e3`), and near `v` the
face `F_X` is either the convex quadrant `{a,b ≥ 0}` or the reflex sector `{a ≤ 0 or b ≤ 0}`
(angle exactly `π` is impossible since `u_XY, u_XZ` are not collinear), similarly for `F_Y`, `F_Z`.
If `F_X` and `F_Y` are both reflex, both contain the segment `{-t e1 : 0 ≤ t < ε}` of `L_XY`, which
is not in `e_XY` (`e_XY` leaves `v` along `+e1`): the faces overlap outside their common edge,
contradiction. ∎
Local types: **corner** (all three convex; surface = boundary of the octant `O`; solid = `O`
("convex vertex") or its complement ("concave vertex")) and **saddle** (exactly one reflex, say
`X`; surface = boundary of `{c ≤ 0} ∪ O`; solid = that set or its complement).

*Implied by Lemma 5.1, but not locally* [P]: if `X` and `Y` are both reflex at `v`, walk along
`L_XY` from `v` away from `e_XY` to the first triple point `p = P_XYW` where the parity of `F_X`
or of `F_Y` changes. Then `p` lies in `F_X`, in `F_Y`, and on `e_XW` or `e_YW ⊂ F_W`; `XYW` is not a
triangle (`p ≠ v` and the other end of `e_XY` lies on the other side). So the forbidden-triple
clause of `XYW` fails. The chain involves the order of up to 10 points on `L_XY`, which explains
why the explicit clause helps a CDCL solver.

### 1.2 Turn signs, the gauge and the vertex type [P]

For a corner `v = v_{X B_i B_{i+1}}` of `F_X` let `μ_X(B)` be the sign of the direction in which
`F_X`'s boundary (link order) traverses `e_XB`, relative to `n_X × n_B`. Then the turn of `F_X` at
`v` (sign of `det(n_X, d_in, d_out)`) is
`τ_X(v) = μ_X(B_i) μ_X(B_{i+1}) χ(X,B_i,B_{i+1},∞)`,
using `det(n_X, n_X×n_Y, n_X×n_Z) = |n_X|² det(n_X,n_Y,n_Z)` and `χ(X,Y,Z,∞) = sign det(n_X,n_Y,n_Z)`.
`μ_X(B)` is a line-order sign of the two endpoints of `e_XB` (three χ-signs, §5.1 of the model).
Adjacent faces traverse a common edge in opposite directions and `n_Y×n_X = -(n_X×n_Y)`, hence
`μ_X(Y) = μ_Y(X) =: μ_XY`. Let `W_X = ±1` be the winding of `F_X` (link order) about `n_X`; a
corner is reflex iff `τ_X(v) ≠ W_X`. For the positively oriented triangle `(X,Y,Z)` (in `X`'s link
`Y` is followed by `Z`), the three turns multiply to `χ(X,Y,Z,∞)` (every `μ` appears twice), so

`(-1)^{#reflex corners at v} = χ(X,Y,Z,∞) · W_X W_Y W_Z`.

With F1 (#reflex ∈ {0,1}) the vertex type is determined by this sign.
**Gauge F2.** Replacing `h_X` by `-h_X` flips `n_X`, `W_X` and every `χ` containing `X`, and leaves
all predicates unchanged; so WLOG `W_X = +1` for all `X` (all 12 normals "link-CCW"). In this gauge:
saddle ⟺ `χ(X,Y,Z,∞) = -1`, reflex `X` at `v` ⟺ `τ_X(v) = -1`. Geometrically: with gauge normals
`N_X`, a vertex is a corner iff `det(N_X,N_Y,N_Z) > 0` (cube corner: `det(e1,e2,e3) = 1`).
Szilassi check [N]: holds at all 14 vertices; all 7 gauge normals are outward for the consistent
orientation, 8 saddles.

### 1.3 Edge types [P]

Let `κ_XY = +1` if the solid near `relint e_XY` is the convex wedge between `F_X` and `F_Y`
(dihedral angle `< π`), `-1` otherwise. Writing `s_X(Y)` for the side of `H_Y` on which `F_X` lies
near `e_XY` and `o_X` for the side of `H_X` on which the solid lies, one has `s_X(Y) = -μ_XY W_X`,
`κ_XY = o_X s_Y(X)` and `o_X = λ W_X` with one global `λ = ±1`; hence
`κ_XY = -λ μ_XY W_X W_Y`, i.e. **in the gauge, the dihedral type of every edge is one line-order
sign** (`κ_XY = -λ μ_XY`). Combining with 1.2: `τ_X(v) = κ_XY κ_XZ χ(X,Y,Z,∞)` (gauge), so F1
becomes the **edge-type rule F4**: at a corner vertex all three edges have the same type, at a
saddle they do not (exactly one pair agrees: the two edges of the reflex face). As SAT: with
auxiliary `κ_e` (66, each an XOR of 3 χ-signs) and `σ_v = χ(v,∞)` (44), 8 clauses of length 4 per
vertex. Szilassi [N]: 16 convex, 5 reflex edges; rule holds at all 14 vertices.
Consequences [P]: extreme vertices of `conv(S)` are convex vertices (all three edges convex);
vertices on a 3-fold symmetry axis are corners (1.1: the three congruent corners cannot all be reflex).

### 1.4 Face turning rule F6 [P]

Let `p_B` be the orthogonal projection of `n_B` to `H_X`. Then `n_X × n_B` is `p_B` turned by
`+90°` in `H_X`, so the edge directions of `F_X` are `-λ κ_{XB_i} R_90 p_{B_i}`. A simple polygon
traversed CCW has turning number `+1` with every exterior angle in `(-π,π)`, so (gauge) the closed
sequence `κ_1 p_{B_1}, …, κ_11 p_{B_11}`, consecutive vectors joined by the rotation of angle `< π`,
winds exactly once about `0`, the `i`-th turn being positive iff the corner is convex. All 2-D
orientations needed are `κ_i κ_j χ(X,B_i,B_j,∞)`: the rule involves only the rank-3 contraction and
the `κ`'s (a table constraint over 11 bits per face).

## 2. Global conditions

### 2.1 Gauss map degree, covering, and `s ≥ 13` [P]

Gauge normals `N_X`; map the dual triangulation `T` to `S²` by `X ↦ N_X/|N_X|`, each triangle to the
geodesic triangle (a proper triangle by GP). Rounding edges and vertices gives a smooth surface
whose Gauss map is homotopic to this map, so by Hopf **`deg = χ(S)/2 = 1-g = -5`** (for F=7: 0).
The value does not depend on `λ` (flipping all normals and the orientation of `T` both reverse the
degree). For a regular value `m`, `deg = p(m) - q(m)` where `p, q` count positively / negatively
oriented triangles whose cone contains `m`. **Covering:** for every generic `m` the maximum of
`x ↦ m·x` on `S` is attained at a vertex which (1.1, 1.3) is a convex vertex with `m` in its outward
normal cone, so `p(m) ≥ 1` (in gauge terms `p(±m) ≥ 1`, sign of `λ` irrelevant). Hence
`q(m) ≥ 6` for all regular `m`. The negatively oriented triangles are exactly the saddles; each has
spherical area `|δ(v)| < 2π` (a simplicial cone lies in an open half-space). So
`Σ_saddles area ≥ ∫ q ≥ 24π` and **`s ≥ 13`** (general F: `s ≥ 2g+1`; GB alone gives `s ≥ 11`,
the Morse count `#index(-1) = #index(+1) + 10 ≥ 12`). Szilassi [N]: `s = 8 ≥ 3`.
**Clause forms.** Only `m = -N_W` is chirotope-expressible without new elements (`m = +N_W` is a
vertex of the image; line directions need inner products). `-N_W` is regular in GP and lies in no
triangle containing `W`. `-N_W ∈ cone(N_X,N_Y,N_Z)` ⟺ `χ(W,Y,Z,∞) = χ(X,W,Z,∞) = χ(X,Y,W,∞) =
-χ(X,Y,Z,∞)`. So:
* `DEG_W`: `Σ_{t ∌ W, -N_W ∈ cone t} χ(t,∞) = -5` (cardinality constraint over ≤ 33 triangles);
* `COV_W`: `∃ t ∌ W` with `χ(t,∞) = +1` and `-N_W ∈ cone t`;
* `CNT`: `#{t : χ(t,∞) = -1} ≥ 13`.
Szilassi [N]: degree 0 at random directions; at `-N_W` the symmetric model is degenerate (below,
§4.3), after a `1e-7` perturbation the degree is 0 for all 7 `W`.

### 2.2 Other global facts

* [P] Every non-facial 3-cycle `XYZ` of `T` is non-separating (a separating 3-cycle would leave
  vertices on both sides or a genus ≥ 1 side triangulated by 3 vertices; both contradict
  neighbourliness). So the loop through `F_X, F_Z, F_Y` is essential in `H_1(S; Z/2)`.
* [P] For a non-triangle triple at most one of `e_XY, e_XZ, e_YZ` contains `P_XYZ` (two on one face
  = self-crossing, two on different faces = triple point in three faces). Implied by Lemma 5.1.
* [P] Each reflex corner of `F_X` forces two distinct transversal crossings `P_XBW ∈ relint e_XW`
  (the two side lines continue into the polygon and must exit), hence `C_X ≥ 2 r_X`; each such
  crossing forces `P_XBW ∉ F_B`.
* [N] "Faces avoid the convex hull" is not a valid clause: Szilassi faces 5 and 7 (1-based, a
  C2-swapped pair, each with 2 reflex corners) lie in supporting planes.
* Linking. I found no chirotope-local analogue of Schewe-type linking conditions that is not a
  consequence of Lemma 5.1; the honest statement is that Lemma 5.1 is complete for realizations,
  and the only conditions I can prove that are plausibly *not* derivable inside OM-SAT are the
  metric/topological ones F7–F9 (Hopf, existence of maxima, angle areas) and the orientation
  alternation F10.

## 3. Structural reductions for the asymmetric case

### 3.1 Fixed normals make everything linear [P]

Fix `n_1..n_12`. Then `P_XYZ = M_XYZ^{-1}(d_X,d_Y,d_Z)` is linear in `d ∈ R^12`, every side bit and
every `det(h_X,h_Y,h_Z,h_W)` (expand along the `d` column) is the sign of a linear form in `d`, and
the `χ(·,·,·,∞)` are constants. Hence for fixed normals and fixed type the set of embedding offsets
`d` is a **union of open cells of a central arrangement of ≤ 495 hyperplanes in R^12** (lineality
= 3 translations). The inner problem "∃ d" is exact SMT(LRA) / MILP with 12 real unknowns and the
Lemma 5.1 Boolean structure. Moreover, given the normals, vertex types (F3), the edge-type rule (F4)
and the face turning rule (F6) form a CSP on the 66 bits `κ_e` alone (44 four-literal rules, 12
tables over 11 bits): a fast exact *prefilter* on normal configurations; given `κ`, all edge-endpoint
orders `μ` are fixed linear constraints on `d`. Search space: normals mod GL(3) = 15 dims (outer),
`d` = 8 dims (inner, exact).

### 3.2 Chamber formulation for fixed planes [P]

If `S` is embedded with faces in the 12 planes, its solid `U` is a union of closed bounded chambers
of the arrangement (each open chamber misses `S`). Conversely a set `U` of bounded chambers gives a
Series-1 polyhedron iff (i) at each of the 220 triple points the 8 surrounding chambers form one of
the patterns: empty/full, half-space (point inside one face), quadrant or its complement (edge),
octant or complement (corner vertex), 3 or 5 octants around a vertex of the octahedron (saddle,
the reflex face is the plane containing the 3/5-set's "axis"); (ii) no segment of a line has the
"two opposite quadrants" pattern; (iii) each line carries exactly one maximal edge run; (iv) each
plane's selected region is a disk (connectivity by lazy cuts, as in formulation B). All other
octant patterns are non-manifold or put a point twice on a face. There are **no parity
constraints**: inside/outside is a primary variable. 165 Boolean variables (bounded chambers of 12
planes in GP). Szilassi [N]: its solid is the union of **8 chambers** of its 7-plane arrangement
(20000 random samples, every sampled chamber entirely in or out).

### 3.3 Polar view [P]

`h_X = (n_X,-d_X)` is also the homogeneous point `p_X = n_X/d_X`; `h_∞` is the origin. So a
face-version configuration is a 13-point configuration in RP³ (12 points + a centre `O`) modulo
PGL(4) (39 − 15 = 24 dims): the face problem is "the vertex (Császár) problem's 12 points plus a
free centre, with different predicates". Construction ansatz E5 below uses this.

## 4. Q2: check of the Moki–Julio symmetry reduction (README §2)

Independent geometric proofs (no use of the 59 automorphism groups):
1. [P] An isometry fixing all 12 faces fixes all 44 vertices, which span R³, so it is the
   identity; `G ↪ Aut(T)`. An isometry maps the bounded component of `R³∖S` to itself, so it
   preserves the outward normal; hence it is orientation preserving on `S` iff it is a rotation.
2. [P] **No non-trivial isometry fixes a face.** `g(F_X)=F_X` ⇒ `g|H_X` is a symmetry of an
   11-gon: identity (⇒ `g` = reflection in `H_X`, forcing all other planes ⊥ `H_X`, contradicting
   independence at the 33 vertices off `X`), rotation (order divides 11; no corner can be the
   centre), or a line reflection (⇒ `g` = half-turn about a line in `H_X`, impossible since it
   reverses the outward normal of the fixed face, or a mirror ⊥ `H_X`).
3. [P] **No mirror.** For a mirror `Π`, a fixed face has exactly one fixed neighbour (reflection of
   an 11-cycle), all faces are neighbours, so 0 or 2 faces are fixed. Each swapped pair `{Y,σY}`
   has `σ`-invariant edge `e_{YσY}`; reversal is impossible (points of `F_Y ∩ Π` near the midpoint
   would lie in `F_{σY}`); pointwise fixing needs both third vertices fixed, i.e. triangles
   `X Y σY` and `B Y σY` with `X,B` the fixed faces, and the reflection of `X`'s link swaps only one
   consecutive pair. 5 or 6 swapped pairs, at most 1 realizable: contradiction.
4. [P] **No inversion**: the 6 invariant edges `e_{X,iX}` would all have midpoint the centre.
5. [P] **Rotations have order 1, 2, 3**: a rotation of order 4, 6 or 12 contains a half-turn with the
   same axis, whose axis passes through the midpoints of the 6 reversed edges `e_{X,hX}`; the
   rotation fixes those points, forcing it to preserve a 2-set of faces, so its square fixes a face.
   Prime orders ≥ 5 do not divide 12. Improper elements: square has order ≤ 3 and no mirror /
   inversion ⇒ only S4 rotoreflections.
6. Admissible groups: C1, C2, C3, D2, S4, D3, T, all acting freely on faces. A half-turn meets `S`
   in exactly 6 points (edge midpoints, quotient genus 2); a 3-fold axis meets `S` in exactly 2
   vertices (Riemann–Hurwitz `r = 8 - 3g'`, `r ≤ 4`), both **convex corners**, segment between them
   inside `U`; for D2, S4, T the centre lies in `U`. Parameter counts (plane configurations modulo
   the normalizer): **24, 12, 8, 6, 6, 4, 2**.

Assessment of their §2: the reduction is correct, and steps that they establish by computation
(free action on faces, no orientation-reversing involution, element orders) follow from 2–5 for
every map, so they cannot hide a gap. Remarks: (a) "orientation preserving ⇒ rotation" needs fact 1
(not stated by them, true). (b) Rotations by ±120° are conjugate in SO(3) (half-turn ⊥ axis), so one
3-fold case per conjugacy class suffices, irrespective of the "mirror image" argument. (c) The GP
perturbation argument is sound: each of the 715 determinants is a polynomial on the linear space of
G-symmetric configurations; one random point with all non-zero shows none vanishes identically,
so GP is generic within the symmetric space and the realization set is open there. (Caution: this
fails for groups with a fixed face — Szilassi's own C2 model has 3 triple points at infinity,
`(W, gW, fixed face)` — but no face is fixed for F=12.) (d) The real trust point is the encoder
(do the CNFs encode the predicates?); DRAT certifies the CNF only. Their 0-mismatch tests against
exact geometry are evidence, not proof; independent re-encoding of at least the T, D3 and C3 cases
(small, fast) is advisable. The work is unrefereed and AI-assisted.

## 5. Q3: Szilassi in the face-plane picture [N] (`index.html` coordinates; reproduce with `python3 -I code/szilassi_faceplane_check.py`, float arithmetic)

* Faces need consistent re-orientation (two of the published walks are reversed).
* Reflex corners per face (1-based faces 1..7): `1,1,1,1,2,0,2`; total 8 = number of saddles
  (6 corner vertices). Exactly one convex face (face 6), as in Grünbaum–Szilassi [K].
* The C2 axis is the z-axis; face permutation `(1 2)(3 4)(5 7)`, face 6 fixed, axis ⊥ face 6 through
  its centre (allowed for hexagons: `g|H_X` is a point reflection; impossible for 11-gons, §4 item 2).
  The fixed face is the convex one.
* 16 convex / 5 reflex edges; edge-type rule and vertex-type rule hold everywhere.
* Faces 5 and 7 (swapped pair) lie in supporting planes.
* Gauss degree 0 = χ/2; solid = union of 8 chambers.
* Mechanism (interpretation, [C]): one central C2-invariant convex face with three swapped pairs
  wrapped around it; the "central symmetric face" ingredient cannot exist for F=12 (odd polygons,
  free action), consistent with the claimed non-existence of symmetric F=12 realizations. The
  21-line order table was not produced in this session (time).

## 6. Construction ansatzes (precise experiments)

* **E1 (bilevel, exact inner).** Outer: normal configurations (15 dims); prefilter by DEG/COV/CNT
  (F7–F9) and the κ-CSP of §3.1 for each of the 59 types. Inner: SMT(LRA) or MILP over `d` with the
  Lemma 5.1 structure; MaxSMT gives `f(normals) = min_d #violations` exactly. Validation: Szilassi
  normals (perturbed) must give SAT for F=7. Belief change: if prefilter-feasible normals are rare
  or always inner-UNSAT, that is evidence for non-existence and suggests a proof via normals alone.
* **E2 (chamber MaxSAT for fixed planes).** 165 variables, local octant tables; compare speed with
  formulation B on the same arrangements; then local search over planes using the MaxSAT optimum
  as objective. Validation: Szilassi planes ⇒ the 8-chamber solution.
* **E3 (Gauss-map-first).** For each type `T`, search normal configurations whose Gauss map has
  degree −5 with ≥ 13 saddles and a feasible κ pattern (cheap, rank 3 only); feed survivors to E1.
  Measures how restrictive the degree condition is (H-T6-2).
* **E4 (symmetry breaking of near-misses).** Start from symmetric near-misses (e.g. the reported S4
  configurations with 4 violations), apply E1's exact inner solver at their normals and along
  asymmetric perturbation paths; question: does breaking symmetry ever lower the exact
  `min_d` violation count below the symmetric value?
* **E5 (polar start).** Take 12-point near-embeddings of the vertex version (Bokowski–Guedes de
  Oliveira type) and optimize the free centre `O` (3 dims) for the face predicates.
