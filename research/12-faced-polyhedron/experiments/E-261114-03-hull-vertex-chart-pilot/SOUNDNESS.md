# Hull-vertex chart normalization (PROVED-1, unreviewed)

Scope: bounded embedded cubic polyhedra with a uniform face-plane chirotope, subject to
the existing ALL_OPTS geometric soundness assumptions. This is geometric completeness,
not equivalence on arbitrary abstract oriented matroids or a geometric exclusion.

Let v be a vertex of the convex hull of the polyhedron's vertices. A strictly exposing
linear functional exists. The three incident edges have independent directions because
the three incident plane normals are independent. The three polygon corners are convex:
a reflex planar sector would contain a direction on the forbidden side of the exposing
plane. The local solid is the trihedral cone on these three edges (the bounded solid
cannot occupy the complementary cone outside its convex hull). Orient each incident
plane h_a, h_b, h_c positively at the neighbour on the edge opposite it. These are the
inward plane orientations. The strictly exposing functional, zero at v and positive at
all other vertices, is h_0 = lambda_a h_a + lambda_b h_b + lambda_c h_c with each lambda
positive: evaluation on the three edge directions gives the coefficients' signs.

Write e=(0,0,0,1). Set h=h_0+epsilon e, epsilon>0 sufficiently small. This plane is
strictly positive on the entire convex hull, including v. Sending h to infinity is
therefore a projective homeomorphism on the polyhedron and its convex hull: faces remain
simple planar polygons and incidence/intersections are preserved. The image is bounded.
The sketch's unperturbed equality would put v at infinity and is not used.

For any ordered face triple I other than abc, omit repeated-row determinants from
{det(H_I,h_a),det(H_I,h_b),det(H_I,h_c)}. If the remaining signs agree, their positive
weighted sum is nonzero and has that sign. For sufficiently small epsilon, det(H_I,h)
has the same sign. There are finitely many triples, so one epsilon works for all. If a
sum is zero, the old-INF determinant is nonzero by uniformity; its epsilon term makes
the new bracket nonzero. All other nonzero sums retain their signs for small epsilon.
The triple abc has three zero summands and imposes no sign implication. Brackets of four
faces stay nonzero under the invertible projective transformation.

The inward orientation remains identifiable after this positive-denominator change:
use the sign of h_a at the opposite edge neighbour P_bcd, where d is the other endpoint
partner of bc. In encoder notation this sign is chi(b,c,d,a) chi(b,c,d,INF). Thus the
negative bit of the oriented determinant against a is chi_neg(I,a) xor sd(b,c,d,a).
For each triple, encode "all positive implies INF positive" and "all negative implies
INF negative"; add the three nonreflex corner requirements. Reorientation of any face
multiplies every term and the conclusion by the same factor (the factor for a cancels
against its side sign). A mirror reverses every determinant, hence exchanges the two
implications. The existing SB_REORIENT/SB_MIRROR gauge can consequently be attained
without losing these constraints, by E-261114-01/SOUNDNESS.md.

Every eligible realization has at least one such hull vertex and admits its corresponding
chart. The union of one selected-vertex formula per combinatorial vertex therefore covers
realizations, up to these transformations. These formulas need not cover every OM model,
need not be disjoint, and their UNSAT-SOLVER outcomes are not geometric negative results.
