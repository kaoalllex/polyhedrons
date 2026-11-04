# E-261103-05: adversarial review of one auxiliary candidate

PROVED-1: **ACCEPT for the auxiliary S1 object (8 faces, genus 3), instance scope only.**
Reviewer: adversarial-verifier AI agent, separate from the construction author. This is an
implementation filter, not independent human review. The standalone exact computation below
does not receive the SPEC label EXACT until reproduced through `verification/verify_all.py`.

## Claim and evidence

CLAIMED (received claim): "Expected V,E,F,chi=24,36,8,-4; 28 adjacent pairs and eight excess
edges, embedded." The claim concerns only
`results/recheck/d2_seed4_15.candidate.json`. Its SHA-256 is
`c8abb190c1b2b5cd8998b9df5595e63a7907378e3be85620e42f7330ce00fc78`.

PROVED-1: The candidate consists of eight integer face planes and cyclic neighbour lists.
The reimplementation reads these data directly. It imports only Python standard-library
modules, uses `fractions.Fraction` for geometry, and imports no construction or project
geometry/verification helpers.

CLAIMED (received project-verifier logs, not rerun by this reviewer): these commands were
recorded in `results/recheck/d2_seed4_15.all-pairs.log` and `d2_seed4_15.S5.log` respectively,
from `research/12-faced-polyhedron/`:

```sh
python3 verification/verify_candidate.py experiments/E-261103-05-s5-symmetric-solid-first/results/recheck/d2_seed4_15.candidate.json --all-pairs
python3 verification/verify_candidate.py experiments/E-261103-05-s5-symmetric-solid-first/results/recheck/d2_seed4_15.candidate.json --target S5
```

```text
0 {"all_pairs_adjacent": true, "V_E_F_chi": [24, 36, 8, -4], "points_distinct": true, "simple_faces": 8, "nonsimple_faces": [], "edges_consistent": true, "bad_pairs": [], "EMBEDDED": true, "single_adjacency": false, "target": "all-pairs", "PASS": true}
1 record(s), target all-pairs: 1 PASS, 0 fail
0 {"all_pairs_adjacent": true, "V_E_F_chi": [24, 36, 8, -4], "points_distinct": true, "simple_faces": 8, "nonsimple_faces": [], "edges_consistent": true, "bad_pairs": [], "EMBEDDED": true, "single_adjacency": false, "target": "S5", "PASS": false}
1 record(s), target S5: 0 PASS, 1 fail
```

## Checks reimplemented and run

PROVED-1: The following command exited 0 and returned `verdict: ACCEPT`:

```sh
python3 experiments/E-261103-05-s5-symmetric-solid-first/verify_independent.py experiments/E-261103-05-s5-symmetric-solid-first/results/recheck/d2_seed4_15.candidate.json
```

PROVED-1: `verify_independent.py` reconstructs all triple points by Cramer's rule. A face with
link `L` has successive vertices `{f,L[k-1],L[k]}` and its next edge lies in plane `L[k]`.
Matching edges by both endpoint triples preserves the pairing of repeated neighbour labels;
the checker does not collapse the map to its triangle set.

PROVED-1: All eight face cycles are planar simple 9-gons. The checker rejects repeated
vertices, zero-length edges, collinear consecutive edges, zero signed area, and intersections
of nonadjacent boundary segments, using an injective coordinate projection of each face.

PROVED-1: Each of the 36 edges has exactly two incident faces, with reciprocal neighbour
labels and the correct supporting plane pair. Every one of the 24 vertices belongs to
exactly its three named faces and has three distinct graph neighbours; its face link is a
triangle. The primal graph and face graph are connected. Propagating orientation signs
across every edge gives a coherent orientation. The resulting counts are
`(V,E,F,chi)=(24,36,8,-4)`, hence genus 3.

PROVED-1: For each of all 28 plane pairs the checker independently computes the closed
section of each filled face polygon along their intersection line. It collects exact line
crossings and collinear boundary endpoints, tests midpoint membership by winding number,
and retains isolated contacts. The intersection of the two interval unions equals exactly
the union of the paired shared edges, including endpoints. This checks all face pairs and
detects additional isolated contacts, boundary crossings, interior overlaps, and intersections
in gaps between shared edge segments.

PROVED-1: All 28 face pairs are adjacent: 20 have one edge and eight have two edges, accounting
for all 36 edges. The doubled pairs are
`(0,4), (0,7), (1,5), (1,6), (2,5), (2,6), (3,4), (3,7)`.

## Degeneracies and exact margins

PROVED-1: All 56 normal-triple determinants and all 70 four-plane determinants are nonzero,
with minimum absolute values 12 and 56 respectively. All 56 arrangement triple points are
finite and pairwise distinct. No four planes concur, and no selected vertex lies on an
additional plane. The minimum absolute nonincident plane evaluation over all arrangement
triple points is `1/6`.

PROVED-1: The minimum squared selected-edge length and the minimum squared distance between
distinct selected vertices are both `2695/110976`. The plane-evaluation and determinant values
use the supplied integer coefficient scale; they are not normalized Euclidean clearances.
Integer input is unchanged by rationalization at either `1e-9` or `1e-12`; no floating-point
rounding choice enters this reimplementation.

## Scope, objections, and remaining uncertainty

PROVED-1: **Reject the interpretation as S5 or as a focus result.** At genus 3 the defining
inequality permits nine faces (`36 <= 39`) but not ten (`45 > 42`), so `F_max(3)=9`; this
candidate has eight. No S0 or S5 existence question is answered by this auxiliary object.

PROVED-1: No failing geometric or combinatorial item was found for this one integer
configuration. No other candidate, control fixture, search, solver, map isomorphism, novelty
comparison, symmetry verification, encoding soundness proof, or full suite was run by this
reviewer. The owner of the parent task retains the project-suite and integration work.

PROVED-1: The main remaining uncertainty is correctness of these two software implementations
and their geometric arguments. A counterexample to the interval-section or topology checks,
or a failing recheck of the pinned input, would change this ACCEPT. Reproduction in
`verify_all.py` is required for EXACT; a human mathematical review outside the agent chain is
required for a reviewed proof. This AI review does not confer PROVED or CERTIFIED status.
