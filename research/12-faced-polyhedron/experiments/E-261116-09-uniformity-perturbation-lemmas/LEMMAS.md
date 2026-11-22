# E-261116-09 part A: lemmas L0-L6

Single author (an AI session), unreviewed: every proof here is at most **PROVED-1** (`SPEC.md` §5). Exact checks:
`checks.py` -> `results/checks.json` (PASS). Inputs: the Codex review §4 (`reviews/strategy-review-2026-11-19-codex.md`),
the lead review §2 (`reviews/strategy-review-2026-11-19.md`), I-261116-07, I-261108-09, I-261118-02.

## Conventions

An **object** is a closed orientable polyhedral surface P embedded in R^3, every face a planar simple polygon, distinct
faces on distinct planes, every corner strict (angle neither 0 nor pi), every edge in exactly two faces. **Cubic**: every
vertex in exactly three faces. **S1**: every two faces adjacent (multiple collinear edge segments allowed). Face X has the
covector h_X = (n_X, d_X), n_X its outward normal, plane n_X . x + d_X = 0; chi(S) = sign det(h_S) on 4-sets of covectors,
with INF = (0, 0, 0, 1) in the standard chart or a chart covector c in a moved chart (E-261117-02). **Uniform**: chi != 0 on
every 4-set of the planes and the chart covector. A **symmetry** is an isometry phi(x) = A x + t with phi(P) = P; it acts on
covectors by phi . (n, d) = (A n, d - (A n) . t). An **equivariant configuration** for a group H of isometries is a covector
tuple with h_{phi X} = phi . h_X for all phi in H (positive transport). A **forced zero** of H is a 4-set whose chi vanishes on
every equivariant configuration. The **uniform formulas** are the encoder's (E-261103-02 `SOUNDNESS.md`: "uniform planes,
including infinity"); the symmetric ones are `omsat_sym.build_sym` (standard chart) and its plane-only variant (moved chart).

## L0 Basic facts (PROVED-1)

(a) A symmetry maps the bounded component of R^3 \ P to itself, so h_{phi X} = phi . h_X: transport is positive, and a
face fixed by phi has phi . h_X = h_X. (b) The face action is faithful: phi fixing every face fixes every vertex (the
intersection of its fixed planes), the vertices span R^3 affinely, so phi = id. Hence G = Sym(P) is finite and has a
fixed point; put it at 0, so t = 0. (c) Proper phi induce orientation-preserving map automorphisms (outward normal and
ambient orientation are kept), improper phi orientation-reversing ones. (d) In an S1 object no two face planes are
parallel: distinct parallel planes are disjoint, and adjacent faces must meet. (e) A rotation r != id fixing a face X has
A n_X = n_X, so n_X is on the axis; two fixed faces would be parallel, so r fixes at most one face of an S1 object, and a
face not fixed by r has a free <r>-orbit (any r^j fixing it fixes its normal, hence fixes it under all of <r>).
(f) Inversion (A = -I) sends n_X to -n_X: it fixes no face, and in an S1 object it is impossible (by (d)). A genuine
rotoreflection (A = R_theta (+) (-1), theta != 0, pi) has no fixed nonzero vector, so it fixes no face.
(g) **Mirrors force a zero on F >= 6 faces.** Let sigma be a mirror with f fixed faces and p swapped pairs, f + 2p = F.
Fixed covectors lie in the 3-space {(n, d) : n in the mirror plane}, so four fixed faces give chi = 0. For two swapped
pairs S = {A, sA, B, sB}: det(s . h_S) = det(A (+) 1) det(h_S) = -det(h_S), while s permutes S by an even permutation, so
det(h_S) = -det(h_S) = 0. F >= 6 gives p >= 2 or f >= 4. The zero is projective (four planes through a point or parallel
to a line), so it holds in every chart. (h) **Rotation orbits of size >= 4 force a zero.** For a rotation about the z
axis the covectors of one orbit are (R^j u, w, d) with u horizontal: they lie in a 3-space, so any four have chi = 0, in
every chart (Codex §4). (i) **Stabiliser test** (Codex §4): a 4-set S with g(S) = S is a forced zero exactly when
det(A_g) times the sign of g on S is -1; it must be run over every element, powers included. It finds only these
stabiliser zeros; (h) is a zero of another kind. A uniformity claim therefore needs a witness (L2), not the test alone.

## L1 Uniformity for cubic objects (I-261116-07) - PROVED-1

**Statement.** Let P be a cubic object. Every sufficiently small perturbation of its covectors (h_X) defines an object
P' with the same map (faces, cyclic orders, edges and edge multiplicities), and the perturbations whose chirotope is
uniform (INF included) are dense in that neighbourhood. So a uniform plain formula of a map loses no cubic object.

**Proof.** (1) At a vertex v the three incident normals are independent: otherwise the three planes share a line through
v, two of the three edges at v lie on it, and the face between them has a corner of angle 0 or pi. So v' = the solution
of the three perturbed plane equations moves continuously. (2) Let P' have the moved vertices in the same cyclic orders.
Choose disjoint balls B_v around the vertices and thin tubes around the open edges outside the balls. Inside B_v, P is
the boundary of a union of octants of three transversal planes; the same union of octants of the perturbed planes gives
the same local picture. Inside a tube, P is two half-planes on two transversal planes; likewise stable. Outside the balls
and tubes, P is a finite union of compact pieces of face interiors, pairwise disjoint unless in one face, at positive
distance from every non-incident feature; small motion keeps all these clearances positive and all endpoint orders on
every line strict (multi-adjacency segments included). So P' is embedded with the same map, its faces simple. (3) The
product of all 4 x 4 minors (INF included) is a nonzero polynomial on R^{4F} (generic covectors), so its zero set is
nowhere dense and meets no open set fully. **Scope.** Cubic objects only, any (F, g), standard chart; the plain uniform
formulas (E-261103-02/03, E-261114-01) with the encoder's soundness (PROVED-1, `SOUNDNESS.md`) and its gauges assumed,
not re-proved. Removes "uniform" from cubic small-case statements, never "cubic" (L6). Symmetric formulas: L2.

## L2 Equivariant uniformity of the three retained actions - PROVED-1 (witnesses EXACT)

**Statement.** Let P be a cubic object and H a group of its symmetries of one of the types (a) C3 acting freely on nine
faces (3+3+3), standard chart; (b) a half-turn fixing exactly one of nine faces (4 x 2 + 1), moved chart; (c) a half-turn
acting freely on eight faces (free C2), standard chart. Then arbitrarily close to P there is an H-equivariant uniform
configuration (a: with INF; b: with a chart covector c far from P'; c: with INF) realizing an object P' with the same
map, on which the same isometries act with the same face permutation.

**Proof.** With the axis on z, the equivariant configurations form a linear space L: one free covector per free orbit,
and the fixed face of (b) in {(0, 0, c, d)} (L0 a, e); in (b) the chart covector is a free extra factor R^4. The product
of all minors is a polynomial on L; `checks.py` gives a point of L where every minor is nonzero (a: 210 quads, min 8;
b: 210, min 44, the Codex minima reproduced; c: 126, min 20), so the polynomial is not identically zero on the
irreducible L and uniform points are dense in L. L1 (2) applies to every small perturbation, equivariant ones included;
equivariance makes phi(P') = P' with the same permutation. In (b), the standard chart has the forced zero {X, A, phi A,
INF} (`SOUNDNESS.md`), hence the moved chart, sound by E-261117-02 (plane-only symmetry, PROVED-1, gate EXACT); c is
chosen far enough that its plane misses P'. Face labels inside orbits are irrelevant: every quad is tested. **Scope.**
Exactly these three actions and charts, any genus; the witness certifies genericity, not openness at a non-cubic or
pinched object (Codex §4). It covers the stage-B formulas of E-261119-02 (C3 3+3+3, C2 4 x 2 + 1) and the free-C2
formulas of E-261119-01 / the (8, 3) rung, each up to the encoder's and gauge's soundness (not re-proved).

## L3 Symmetric nine-face objects (I-261118-02) - PROVED-1

**Statement.** Let P be a nine-face S1 cubic object of any genus and G = Sym(P). If G is neither C1 nor Cs (a single
mirror), G contains an element of order 3, acting freely (3+3+3), or a half-turn, fixing exactly one face (4 x 2 + 1).
So by L2 every symmetric nine-face S1 cubic object except the mirror-only ones has a uniform realization of the same map
in the C3 3+3+3 formula (standard chart) or the C2 4 x 2 + 1 formula (moved chart) of that action; mirror families are
outside every uniform formula (L0 g). **Proof.** Let G+ be the proper subgroup. If G+ != 1 take g in G+ of prime order
p. By L0 e the orbit sizes are p and at most one 1, so 9 = p a + f with f <= 1: p = 5, 7 and p >= 11 fail, p = 3 forces
f = 0, p = 2 forces f = 1. If G+ = 1 then G = {1, s} with s an improper involution: a mirror (Cs) or inversion,
impossible (L0 f). The C3 gauge: build_sym's orbit flips (h -> -h on whole orbits) commute with the action, so the gauge
is equivariant and reachable on every configuration (`omsat_sym.orbfix_quads`); its soundness for the map clauses is
the encoder's reorientation invariance (not re-proved here). Rotations of order >= 4 (L0 h), D2 and S4 (no fixed face,
orbits of even size on nine faces) need no separate case: a retained subgroup of order 2 or 3 suffices. **Scope.**
Nine faces, S1, cubic, any genus; covers E-261119-02's two families as the symmetric slice up to Cs; says nothing about
Cs objects or asymmetric ones (C1), which only the plain formulas see.

## L4 Eight faces: a half-turn or nothing uniform (owner 5) - PROVED-1

**Statement.** Let P be an eight-face S1 cubic object of any genus. If G = Sym(P) contains a rotation of even order or a
rotoreflection of order 4, it contains a half-turn, which acts freely on the faces, and by L2 (c) P has a uniform
free-C2 realization of the same map and action (standard chart). Otherwise G is one of C1, Cs, C7, C7v, and no uniform
formula retains any nontrivial element of G (mirrors: L0 g; the 7-orbit of C7: L0 h). **Proof.** A half-turn fixes at
most one face (L0 e) and 8 - f is even, so it is free. Prime orders in G+: 8 = p a + f, f <= 1, leaves p = 2 and p = 7
(7 + 1); p = 3 needs f = 2. If 2 does not divide |G+|, G+ is a rotation group of odd order, hence cyclic, of order 7
(orbits 1 + 7). Improper s: s^2 in G+. If s^2 = 1, s is a mirror (inversion is impossible, L0 f). If s^2 has order 7,
s has order 14 and s^7 is an improper involution commuting with C7: inversion (impossible) or the horizontal mirror,
which maps the C7-fixed face to a parallel C7-fixed face (two fixed faces, L0 e). So G+ in {1, C7} and every improper
element is a mirror: C1, Cs, C7, C7v. **Scope.** E-261119-01's symmetric (8, 3) slice: the free-C2 formulas cover every
(8, g) S1 cubic object whose group contains a half-turn (D2 and S4 included, through their half-turns); C1, Cs, C7 and
C7v objects are covered only by the plain formulas (L1).

## L5 (11, 5): the improper slice has no uniform formula (lead 4) - PROVED-1

**Statement.** Let P be an (11, 5) S5 object on one of the 3986 admissible maps (Aut+ = 1: 3962, 2: 20, 3: 4;
E-261116-01, E-261118-03). Every improper symmetry of P is a mirror, and forces a zero (L0 g, 11 faces). So no uniform
formula retains an improper symmetry; Sym(P) is C1, Cs, a half-turn group or C2v, and the half-turn cases are those of
the plane-only C2 formulas of E-261118-03. **Proof** (Codex §4). Let s be improper; s^2 is proper. If s^2 != 1 it
induces a nontrivial element of Aut+ (L0 b, c): impossible for Aut+ = 1; for Aut+ = 3 it is a rotation of order 3 on
eleven faces with at most one fixed face, but 11 = 3 a + f forces f = 2; for Aut+ = 2, s^2 is the unique involution h,
a half-turn fixing exactly one face F (11 odd, L0 e); s commutes with h, so s fixes F, but s has order 4, a genuine
rotoreflection, which fixes no face (L0 f). So s^2 = 1: a mirror or inversion, and inversion fixes no face while an
involution on eleven faces fixes one. **Scope.** These maps, S5 cubic, standard or moved chart; nothing about mirror
objects under the plain formula, nor about the 3962 asymmetric maps.

## L6 Perturbation lemma at 4-valent vertices (I-261108-09, k = 4) - PROVED-1 (local check EXACT)

**Statement.** Let P be an object whose vertices have degree 3 or 4. A small generic perturbation of the face planes,
with the surface inside a small ball around each 4-valent vertex redefined as below, gives a cubic object with the same
faces (each still a simple polygon), the same genus, every adjacency kept, and one new edge per 4-valent vertex, joining
the two faces opposite at that vertex. At (8, 2) and (9, 3) an S1 object with vertices of degree <= 4 thus becomes an S5
object (E = 30, 39) and falls under the conditional negative of `STATUS.md` 3d at its level plus this lemma.

**Local check (universal).** At a 4-valent vertex v with faces A, B, C, D in cyclic order, strict corners make every
three of the four normals independent (any three of the planes contain two consecutive ones and their middle face), so
the central arrangement is generic and, after a linear map, is x, y, z, x + y + z. Near v, P is the boundary of a union
U of its 14 cones. A small generic perturbation of A, B, C, D is, after a near-identity affine map that keeps the
identification of unbounded cells with cones, x, y, z, x + y + z = +-epsilon: two types. The perturbed solid keeps the
membership of the 14 unbounded cells and chooses the bounded tetrahedron in or out. `checks.py` enumerates all 2^14
unions U, finds 288 whose boundary is a manifold 4-valent vertex using each plane once, and for both signs tests both
choices: the boundary is a disk patch (connected, chi = 1, every edge in two boundary 2-faces), every vertex link one
cycle with 1, 2 or 3 maximal arcs on distinct planes (only cubic vertices), each labelled face a closed disk. Result:
for all 576 (U, sign) at least one choice is valid (552 exactly one, 24 both), each valid patch has exactly one new
adjacency (the opposite pair). Controls: the six convex cones are valid and keep the tetrahedron out (their solid is the
perturbed intersection of four half-spaces); opposite cones, the eight 3-faced cones and a patch with a flipped far cell
are rejected. The far trace and the four outgoing edges are kept by construction (unbounded faces inherit).

**Global step.** Choose disjoint balls B_v around the 4-valent vertices, so small that only the four incident faces
meet B_v; a non-incident plane through B_v carries no face there and does not change the surface. Away from the balls L1
(2) applies verbatim. A perturbation small against the radii puts the tetrahedron of each B_v deep inside it; the patch
choice inside each ball is independent of the others and of the planes, since the local check is universal over both
perturbation types (an existential check would not suffice: one plane passes through several vertices). Faces stay
disks (each face sector is replaced by a disk on the same arc), so faces stay simple polygons and the genus is kept.
**Scope.** Degree <= 4 only. Degree 5 and 6 (k = 5, 6: (8, 2) allows one 5-valent vertex, (9, 3) a 5- or 6-valent one)
are **not run**; for those the note keeps its scope word. The new edge joins an already adjacent pair (S1), so the
result may have a new multiple adjacency; S5 allows it.
