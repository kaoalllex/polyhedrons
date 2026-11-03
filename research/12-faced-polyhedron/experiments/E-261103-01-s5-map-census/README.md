---
id: E-261103-01
title: Census of face-neighbourly triangular maps for (7, 1), (8, 2), (9, 3), (10, 4) - the candidate maps of the S5 targets
date: 2026-11-03
status: running
direction: [DR19]
origin: [I-261101-07, E-261101-12, L:review2026-11-03]
tests: [H-261103-01, H-261101-07]
produces: []
preregistered: true
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: 2 sessions, minutes to hours of CPU (laptop, daytime). Before any
> compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). **First item of the queue since the strategy
> review of 2026-11-03** (`reviews/strategy-review-2026-11-03.md` section 2.1 and 3.3).

## Goal

The complete list, up to isomorphism and mirror, of the dual maps of S5 candidates at (F, g) = (7, 1), (8, 2), (9, 3) and
(10, 4): oriented triangular maps with F vertices, E = 3(F + 2g - 2) edges, loopless, whose underlying simple graph is K_F
(the E - C(F, 2) extra edges are parallel copies; a pair may have multiplicity 2 or more). For every map: the `links`
(cyclic neighbour list per face, repeats = multiple adjacencies, the format of `ladder_exact.verify`), the face sizes, the
multi-edge pattern, |Aut+|, reflexibility, the fixed-point data (fixed faces, edges, vertices) of every non-trivial
automorphism, and the **admissibility flag**: every corner triple distinct (two polyhedron vertices on the same three
planes would coincide, so a map with a repeated triple has no realization).

## Starting point

* The flip-walk sampler of the review (`reviews/strategy-review-2026-11-03-flipwalk.py`) and its output
  (`reviews/strategy-review-2026-11-03-maps.json`): 240 classes at (9, 3), 203 admissible, 8 with a free order-3
  automorphism (2 of them with |Aut+| = 6); 2 classes at (8, 2); >= 113 at (10, 4). The sampler is a lower bound with
  saturation evidence, not a census; the census must contain every sampled class (a hard control) and may contain more.
* Enumerator design: `code/enum_k12.c` generalised to multiple edges. State = (phi, alpha) on 2E darts (phi = the fixed
  partition into oriented triangles, alpha = the edge involution) or vertex rotations as cyclic words with repeated
  letters; backtracking over unpaired darts with the K_F constraint as pruning (every vertex must see every other); isomorph
  rejection by the canonical code of the sampler (lexicographic minimum of the BFS code over all 2E roots and both
  orientations) or by canonical augmentation. Python first; C if (10, 4) does not finish in hours.
* **Controls (pre-register all):** (7, 1) gives exactly 1 class, |Aut+| = 42, chiral (the Csaszar-Mobius torus); (12, 6)
  with zero extra edges gives the 59 types of FD3 with their automorphism orders (if too slow in Python, run the C version or
  state that this control was not run); the (9, 3) and (8, 2) censuses contain every class of the review's JSON; the (8, 3)
  census, if it finishes (the sampler saw 22,666 classes in 150 s, so it may not), contains the Roest-Vigh and Mizhaev dual
  maps (`control83` mode of the sampler builds them from the published data).
* Cross-check of the symmetric sub-list: construct the C3 (9, 3) maps as Z_3 voltage lifts of torus maps with 3 vertices,
  13 edges, 8 triangles and 2 branch points (I-261030-18); the lift list must equal the census' list of maps with a free
  order-3 automorphism.
* Output: `results/maps_F_g.json` per case with the fields above; a summary table in `CONCLUSION.md`; the admissible
  symmetric maps listed first (they are the input of E-261103-03 and E-261103-05).

## Next

Stop rule: the four censuses with every control passed, or a written reason why a case does not finish (then the
sampled set stands in for it, labelled as such). Outcomes: 240 / 203 / 8 and 2 / 2 confirmed -> H-261103-01 supported, the
geometric queue runs as planned; more maps -> re-plan E-261103-03 with the new count; fewer -> the sampler has a bug, fix and
re-run before anything geometric. Scenario move: none (combinatorics only; the credences of the S5 table move only through
geometric decisions).
