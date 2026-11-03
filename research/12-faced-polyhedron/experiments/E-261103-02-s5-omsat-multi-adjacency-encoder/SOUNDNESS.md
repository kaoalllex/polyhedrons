# Multi-adjacency predicates and symmetry scope

Evidence label: **PROVED-1**. This is a single-author argument, without independent human review.
Predicate agreement is an exact computational control, not a proof for all chirotopes.

## Input and segment pairing

Let the oriented face boundary of X have cyclic neighbour word L_X. An occurrence of Y at position i
represents the edge on L_XY with endpoint partners L_X[i-1] and L_X[i+1]. The unordered endpoint pair
must occur at Y as well. Every unordered corner triple occurs exactly once in each of its three faces.
Consequently the 2m partners of a pair with m edges are distinct, and a corner XYZ identifies exactly
one incident edge of XY. A triangle set alone loses the pairing when m > 1; links are mandatory then.
`Triangulation` checks these invariants before constructing any formula. It preserves the original
single-edge partner ordering and circuit path.

## Segment predicates

The side and line-order identities are unchanged from `theory/mathematical-model.md` sections 4-5.
For one segment [P_XYA,P_XYC], the open-membership predicate is the XOR of side(XYA;V) and side(XYC;V),
with FALSE for V equal to an endpoint partner. E(X,Y;V) is the OR of these predicates over the shared
segments, i.e. membership in their open union. Every two shared segments must be disjoint: none of
either segment's endpoints may lie inside the other. Distinct partners and uniformity exclude equal
endpoints. Four such nonmembership clauses suffice even for nested intervals. These clauses are
part of the embedding (`triples`) family, tagged SEGMENT_DISJOINT; they are not added to symmetry-only
controls or when embedding constraints are deliberately disabled.

## Ray parity

The boundary contribution is closed segment-union membership on XY or XZ. Outside that boundary,
IN(X;Y,Z) counts the crossings of a ray along L_XY. A transverse boundary edge is counted individually
when its intersection lies in the edge interior and ahead of the query. Counting individual segments,
rather than OR-ing them before XOR, retains even-odd parity for defective self-crossing polygons.

For each boundary run on L_XY with endpoint partners C,D, the off-line boundary edges at its ends
leave L_XY to sides side(XCC';Y), side(XDD';Y); C',D' are obtained from the unique incident segments.
The run contributes one crossing precisely when both endpoints are ahead and these sides differ.
When the query lies on a run, boundary membership already gives TRUE. Uniformity prevents any other
boundary corner from lying on L_XY. These cases exhaust the polygon boundary.

At a declared corner XYZ, REFLEX uses the same crossing count on the ray opposite the other partner
of the incident XY segment, omitting the starting run. Closed membership in another run is retained
for defective configurations with overlapping collinear edges. On simple polygons this gives the
usual reflex bit. RTURN keeps the existing determinant formula with the incident partners read
from the paired segments. The old single-adjacency formulas remain unchanged.

## Extended Lemma 5.1

Assume a valid input map, uniform planes (including infinity), the segment-disjoint clauses, and all
forbidden non-corner triples. If two nonincident edges of a face X cross, on lines XW and XZ, their
intersection is P_XWZ. If XWZ is not a corner, it lies in all three closed faces, contrary to the
forbidden-triple clause. If it is a corner, its unique incident edges on XW and XZ meet there. A
different edge copy on either line containing this point would overlap its incident segment,
contrary to segment disjointness. Collinear edges on the same line are also disjoint. Thus each
face boundary is simple.

Now inspect F_X intersect F_Y on L_XY. Its interval endpoints lie on boundary edges. An endpoint on
an edge XW with W != Y is a triple point in F_X,F_Y,F_W, so XYW must be a declared corner. Such a
corner is already an endpoint of a prescribed XY segment. Segment disjointness and simplicity imply
that at each such endpoint the other face's incident boundary edge leaves L_XY transversely, so the
intersection cannot extend past that endpoint into a gap between prescribed segments. There are
no additional endpoints or isolated contacts at non-corner triples. Hence the intersection is
exactly the union of the prescribed shared segments. Conversely an embedding satisfies all these
clauses. This extends the original symmetric condition without assuming m = 1.

## Isometry clauses and a limitation of uniformity

`build_sym` now uses T.n and the existing orbit reorientation basis. Each supplied permutation must
preserve corner triples and segment pairings. Proper cooriented isometries use
chi(g(S)) = chi(S); improper ones have the existing determinant sign -1. Infinity is fixed.
Free C2 and free C3 have exact uniform symmetry-only positive controls. These have no embedding
constraints and are not realizations of their census maps.

For a proper C2 permutation fixing X and exchanging A,B, the set {X,A,B,infinity} is invariant and
the induced permutation is odd. The cooriented symmetry relation requires its chirotope value to
equal its negative, hence zero. This can describe valid symmetric arrangements, but not uniform ones.
The controlled D3 action contains such C2 elements and has the same limitation. Its symmetry-only
UNSAT and the C2-fixed UNSAT exclude only those uniform cooriented formulas. They do not exclude
symmetric embedded surfaces. A nonuniform oriented-matroid encoder would be required to decide such
symmetry families without perturbing away their symmetry. The asymmetric uniform encoder remains
available: perturbation removes symmetry, which is allowed by S5.

No claim here changes S0, supplies a new S5 witness, or decides a census map.
