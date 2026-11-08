---
id: E-261103-07
title: Census and symmetric sub-list of the (10, 4) candidate maps - preparation of the stretch target
date: 2026-11-03
status: running
direction: [DR19]
origin: [E-261103-01, I-261101-07]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned. Scores T D F G R: 1 2 2 2 2 | budget: minutes to hours of CPU with the enumerator of E-261103-01; no geometry.
> Runs after or alongside E-261103-01; no geometric (10, 4) run before (9, 3) is decided (`STRATEGY.md` section 1).

## Goal

The complete list of (10, 4) candidate maps (10 vertices, 48 edges, 32 triangles, 3 extra edges) with admissibility and
automorphism data, and the sub-list with a geometrically realizable symmetry (a free C2, or C5 with fixed triangles; the
sampler saw 113 classes in 3 minutes, Chao1 estimate about 460, four with an involution, none with an order-3 or order-5
automorphism).

## Starting point

The census part was completed by E-261103-01 later on 2026-11-03 (counts and evidence in
`STATUS.md` section 3c). Reuse its `results/maps_10_4.json`; do not repeat enumeration.
This item remains planned for the geometric compatibility analysis of its symmetry actions.


* The enumerator and controls of E-261103-01; the sampled (10, 4) classes of the review as a containment control.
* Riemann-Hurwitz bookkeeping for the symmetric sub-list: a free C2 on 10 faces (5 orbits) or a C2 with fixed faces; a C5
  needs 4 fixed polyhedron vertices on the axis.

## Next

Stop rule (revised 2026-11-08, `reviews/strategy-review-2026-11-08.md` L3): the census is complete (E-261103-01); what remains is a (10, 4) cost probe, 10 maps of mixed patterns (design and caps amended by the owner on 2026-11-08, see `PLAN.md`), run only as the follow-up of ROADMAP week item 5a. Outcome: the
count and the symmetric sub-list set the (10, 4) row of the S5 table ("cannot tell" falls if the maps are few) and the plan
for the stretch. Scenario move: none.

## Pattern census (2026-11-08, review 2026-11-08c §7 idea 2; no solving)

`python3 experiments/E-261103-07-s5-10-4-census-symmetry/pattern_census.py` counts `maps_10_4.json` by multiple-adjacency
pattern (definition in the script; it reproduces every pattern label of E-261103-03's `queue_item5a.json`). EXACT
counting on the E-261103-01 census (coverage PROVED-1). 1183 classes, 1117 admissible:

| Pattern | Admissible | All | Aut+ of the admissible maps | (9,3) cadical at 1800 s: n, min / median / max |
|---|---|---|---|---|
| `(1^4,2)/(2,2,2)` | 520 | 553 | 1: 520 | 94, 77 / 213 / 841 s |
| `1^6/(2,2,2)` | 237 | 237 | 1: 183, 2: 45, 3: 7, 4: 2 | 33, 81 / 497 / 1239 s |
| `(1,1,2,2)/(2,2,2)` | 186 | 200 | 1: 171, 2: 15 | 36, 31 / 93 / 288 s |
| `(1,1,2,2)/(2,3)` | 70 | 70 | 1: 56, 2: 14 | 7, 70 / 89 / 136 s |
| `(1,1,1,3)/(2,2,2)` | 58 | 63 | 1: 48, 2: 8, 3: 2 | 5, 69 / 122 / 215 s |
| `(1,2,3)/(2,3)` | 38 | 52 | 1: 38 | none at 1800 s (60-s units: 22-76 s) |
| `(2,2,2)/(2,2,2)` | 7 | 7 | 1: 5, 3: 2 | none at 1800 s (60-s units: 22-76 s) |
| `(3,3)/(4)` | 1 | 1 | 2: 1 | no (9,3) analogue (a quadrupled pair) |

The (9,3) times are from E-261103-03 items 1(b) and 5a (`solver.log`), NUMERICAL. The two slow patterns hold 757 of the
1117 maps (68 %); at (9,3) they were 128 of 203 (63 %). Cost model (untested): (9,3) medians times (10,4) counts give
about 73 core-h of solver time, about 125 core-h with the checker, before the unknown growth factor from 10 to 11 elements
that the cost probe measures.
