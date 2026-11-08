---
id: E-261103-06
title: Embedded first, planar later - pilot on Szilassi from a torus, then an 8-face object from a smooth genus-3 surface
date: 2026-11-03
status: parked
direction: [DR17, DR19]
origin: [I-261103-01, I-261103-05, E-261101-26]
tests: [H-261101-07]
produces: []
preregistered: true
verdict: UNDERPOWERED
concluded: 2026-11-07
---

> Planned, **explore**. Scores T D F G R: 1 2 2 2 1 | budget: one session for the prototype and R1; a second session for the
> (8, 3) rung only if R1 converges. Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`).

> Concluded: R1 pilot, all 4 valid starts blocked by the barrier at energy 84-118; UNDERPOWERED, parked (CONCLUSION).

## Goal

The pilot that I-261103-01 asks for, with S5 rungs: start from an embedded triangulated surface carrying the target map
(each face a patch of many small triangles), minimise a planarity energy per patch under a hard non-intersection barrier
(incremental potential or continuous collision check), and stop when every patch is planar; then read off the planes and
run `verify_candidate.py`. The method has no ladder and never leaves embedding.

## Starting point

* R1: the Szilassi map on a smooth torus; the output must be an exactly verified Szilassi (`--target S5` PASS at (7, 1)).
* R2': the Roest-Vigh (or Mizhaev) map on a smooth genus-3 surface (a Lawson-type or any embedded genus-3 mesh split into 8
  regions with the map's adjacency, doubled pairs as two boundary arcs); the output must be an exactly verified 8-face
  object (not necessarily theirs: any S1 embedding on that map, `--all-pairs`).
* Starting surfaces: I-261103-05 (a spectral drawing of the cubic 1-skeleton with planar face cycles as constraints) if
  available; otherwise a hand-built embedded mesh.
* Kill criterion (from the idea file): the planarity energy plateaus above zero on R1 with the barrier active.
* Counters: the planarity energy is a float diagnostic; the verdict is the exact verifier only.

## Next

Stop rule: R1 converges to an exact Szilassi and R2' converges at least once (then a pre-registered (9, 3) night on the
admissible maps, symmetric ones first), or R1 fails (idea parked with its failure mode). Scenario move: none until a
target run.
