---
id: E-261103-07
title: Census and symmetric sub-list of the (10, 4) candidate maps - preparation of the stretch target
date: 2026-11-03
status: planned
direction: [DR19]
origin: [E-261103-01, I-261101-07]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 2 2 | budget: minutes to hours of CPU with the enumerator of E-261103-01; no geometry.
> Runs after or alongside E-261103-01; no geometric (10, 4) run before (9, 3) is decided (`STRATEGY.md` section 1).

## Goal

The complete list of (10, 4) candidate maps (10 vertices, 48 edges, 32 triangles, 3 extra edges) with admissibility and
automorphism data, and the sub-list with a geometrically realizable symmetry (a free C2, or C5 with fixed triangles; the
sampler saw 113 classes in 3 minutes, Chao1 estimate about 460, four with an involution, none with an order-3 or order-5
automorphism).

## Starting point

* The enumerator and controls of E-261103-01; the sampled (10, 4) classes of the review as a containment control.
* Riemann-Hurwitz bookkeeping for the symmetric sub-list: a free C2 on 10 faces (5 orbits) or a C2 with fixed faces; a C5
  needs 4 fixed polyhedron vertices on the axis.

## Next

Stop rule: the census, or a written reason why it does not finish (then the sampled set, labelled as such). Outcome: the
count and the symmetric sub-list set the (10, 4) row of the S5 table ("cannot tell" falls if the maps are few) and the plan
for the stretch. Scenario move: none.
