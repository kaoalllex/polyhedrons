# Portrait of the hypothetical solution ("work backwards")

Assume an embedded Series-1 12-face polyhedron S exists. Everything below is a proved or claimed
necessary property; together they are a specification for searches.

| # | Property | Status / source |
|---|---|---|
| 1 | Combinatorial type: the dual of one of the 59 neighborly genus-6 triangulations | [K] ABS 1996; [N] re-enumerated here |
| 2 | No non-trivial isometric symmetry | claimed (Moki & Julio 2026, DRAT); 4 cases reproduced here; mirror/point symmetry excluded here by Aut data |
| 3 | Planes can be taken with integer coefficients (realization space is open) | [P] model §2 |
| 4 | At most one reflex corner at every vertex; >= 3 convex corners per face | [P] |
| 5 | Gauss map of degree chi/2 = -5 in the gauge; every direction covered by a convex corner | [P] theory-notes PI addendum |
| 6 | Hence >= 13 saddle vertices (>= 13 reflex corners in total), at most 31 convex vertices | [P] (Track 6 F9) |
| 7 | Its normals lie in the Gauss-admissible region, which contains NONE of the 1005 known near-misses' normals | [N] exact per instance |
| 8 | It is a polyhedral immersion (simple faces, embedded vertex stars) of its map | [P]; whether ANY immersion exists is test Q12 |
| 9 | At every convex vertex all three edges have the same dihedral type; at a saddle two do, opposite the reflex corner | [P] (Track 6 F4) |

Consequence for search strategy: improve nothing from the known near-misses (they are in the wrong
topological class, Gauss degree mostly -1..+1); search inside the class defined by rows 4-8.
