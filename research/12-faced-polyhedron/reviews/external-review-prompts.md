# Self-contained prompts for an independent AI reviewer (copy one block into another chat)

An independent model is useful as a second pair of eyes on PROOFS and ARGUMENTS (it makes
different mistakes). It is not useful for our heavy computations. Paste its answer back to Claude.

## Prompt 1: check the Gauss-map degree argument

```
I want a careful, skeptical check of the following argument. Point out any gap.

Setting: S is a closed orientable polyhedral surface embedded in R^3, genus 6 (Euler char -10),
with 12 planar simple polygonal faces, every vertex in exactly 3 faces. Let K be the dual
triangulation (12 vertices = faces, 44 triangles = vertices of S), coherently oriented. For each
face X let g_X be a unit normal chosen so that the polygon of X, traversed in the cyclic order of
its neighbours given by the orientation of K, is counter-clockwise about g_X.
Claim (i): for every generic unit vector u, sum over triangles T=(X,Y,Z) of K of
sign det(g_X,g_Y,g_Z) * [u lies in the cone spanned by g_X,g_Y,g_Z] equals chi/2 = -5.
Claim (ii): every generic u lies in the cone of some triangle with det(g_X,g_Y,g_Z) > 0.
Argument: smooth S; the Gauss map is constant on faces, sweeps the short arc between adjacent
face normals across each edge (exterior dihedral angle in (-pi,pi)), and on each vertex disk covers
the geodesic triangle of the 3 normals with multiplicity +-1 (sign = sign of the angle deficit,
|deficit| < 2pi), so the total degree is the Gauss-map degree chi/2 (Hopf). For (ii), the vertex of
S maximizing <u,x> is a convex corner and u is in its outward normal cone. Reversing the global
orientation of K turns g into inward normals and leaves the sum unchanged.
Questions: is each step correct? Is the sign convention consistent? Are there degenerate cases?
```

## Prompt 2: creative ideas

```
Open problem: does a polyhedron embedded in R^3 exist with 12 planar faces, every two faces sharing
exactly one complete edge, 3 faces per vertex (44 vertices, 66 edges, genus 6)? Known: the
combinatorial types are the duals of the 59 neighborly genus-6 triangulations with 12 vertices;
the problem reduces to choosing 12 planes (all conditions are strict sign conditions); no symmetric
solution exists (computer proof); the best numerical near-misses (4-5 intersections) are not even
immersions (they have vertices where two faces overlap locally) and their Gauss map has the wrong
degree; for symmetric configurations even a polyhedral immersion is impossible.
Propose 10 genuinely new approaches (from any field) to either construct it or prove it
impossible. For each: the precise mathematical idea, why it could work, and a concrete first test.
```
