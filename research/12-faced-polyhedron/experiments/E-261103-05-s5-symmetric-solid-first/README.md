---
id: E-261103-05
title: Symmetric solid-first for S5 - disk-aware R2/R3 explore pilot (the Roest-Vigh route)
date: 2026-11-03
status: done
direction: [DR7, DR18, DR19]
origin: [I-261030-07, I-261101-08, I-261101-20, E-261101-16, L:roestvigh2026]
tests: [H-261103-02, H-261101-07]
produces: []
preregistered: true
verdict: BENCHMARK-PASS
concluded: 2026-11-04
---

> Completed registered R2/R3 **explore pilot**. See CONCLUSION.md and STATUS section 3g.
> Both known-plane controls and random D2 recovery pass. No nine-plane run or night was activated;
> any target pilot needs a new committed plan. Results/pilot is immutable. No process is active.

## Goal

Reproduce the method that found both 8-face objects, on 9 planes: sample symmetric arrangements (C3: one axis, three
orbits of three planes, about 7 free parameters; D3: an orbit of six and an orbit of three; C2: four pairs and one fixed
plane), decide each with the CP-SAT inner solver `code/solid_cpsat.best_solid` extended from "at most one edge run per pair"
to 1-3 runs per pair with E = 39 in total and every pair adjacent, and verify every solid exactly (`code/verify_solid.py`,
`verify_candidate.py --target S5`).

## Starting point

* **R2 (must pass first):** the Roest-Vigh planes give their polyhedron (28 pairs, 8 doubled) and Mizhaev's planes give his,
  through the extended inner solver alone (the "construction procedure from the planes" of Roest-Vigh section 4).
* **R3 (the gate of the night):** rediscover one of the (8, 3) objects from random D2 or S4 two-orbit planes within one
  session; failure parks the row with the failure mode (how close the maximal adjacency got).
* Catalogue weights (I-261101-20): tetrahedral hulls and long spikes (four far vertices), as in both known objects; the C3
  family gridded densely, D3 and C2 sampled; filters before the solver: no two normals antipodal, normals not in an open
  hemisphere, general position (perturb by 1e-6).
* The decision version of the inner solver must encode the disk condition exactly (E-261101-16's note), so that INFEASIBLE
  is a verdict per arrangement; UNKNOWN is a timeout.
* Pilot negative: the tetrahedron arrangement cannot supply seven edge runs. Random nine-plane draws
  are not known negatives and are not used as such; the bounded pilot is R2/R3 only.

## Next

Stop rule: R2 and R3, then the night, or the first solid with 36 pairs on 9 planes (then `candidate-check`). Outcomes: an S5
PASS at (9,3) is the focus result; geometric symmetry must be checked on the actual solid, not inferred from the plane arrangement, and novelty requires separate review; R3 fails -> parked
with a power statement; the night ends at < 36 pairs everywhere -> the histogram of maximal adjacency per family goes to
`CONCLUSION.md`, and the exact route (E-261103-03) is the only remaining one for the symmetric maps. Scenario move: a PASS
sets the (9, 3) row to exists; a failed night moves nothing.
