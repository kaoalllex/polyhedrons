---
id: I-261103-01
title: Embedded first, planar later - flatten the faces of an embedded genus-6 surface with the target adjacency, never leaving embedding
date: 2026-11-03
status: open
direction: [DR17]
origin: [owner, H-261101-10, E-261102-03, E-261102-04]
---

## Idea

Every engine so far keeps the faces planar (12 planes) and fights for embedding; all of them stall at genus 3-4. Do
the reverse. Topologically, an embedded closed surface of genus 6 split into 12 hexagonal-type regions with the
target adjacency (a target map) always exists. Build one as a triangulated mesh (each face a patch of many small
triangles, no self-intersection), then deform it continuously to make every patch planar: minimise a planarity
energy (distance of each patch's vertices to a best-fit plane) under a hard non-intersection barrier (an incremental
potential or a continuous collision check), so the surface stays embedded at every step. At zero planarity energy
the patches are planar polygons and the result is an S0 candidate (then `candidate-check`).

## Why it might help

H-261101-10 and the Gauss gate say that the handle ladder needs a jump in the class of the normals that no
continuous move at nearly fixed planes makes (21 of 21 type-0 arms). This method has no ladder: it starts at genus 6
with the right combinatorics and moves through embedded surfaces, a space where the jump is not forbidden. It is the
standard pipeline of planar-quad meshing and architectural geometry (PQ meshes, planarization with collision
handling), not used on this problem as far as we know (to be checked).

## Cheapest test

Positive controls on the benchmark ladder before the target (PROTOCOL 8a): R1 (Szilassi map, genus 1, 7 faces) from
a smooth embedded torus split into the 7 regions; then R4 (a genus-3 map with a known realization) from a smooth
surface, the rung no engine passes. One session for the prototype on R1. If R1 converges to an exactly verified
Szilassi and R4 converges at least once, the target gets a pre-registered run; if R1 fails, the idea is parked with
the failure mode recorded. What would kill it fast: the planarity energy plateaus above 0 on R1 with the barrier
active (the same wall seen from the other side).

## Source

Owner, 2026-11-03 (session after night 7: "we need creative and risky methods"); suggested in the discussion of the
ravine between genus 3 and 4.
