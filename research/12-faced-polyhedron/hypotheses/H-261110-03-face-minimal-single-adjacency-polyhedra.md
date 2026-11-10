---
id: H-261110-03
title: Face-minimal cubic polyhedra with single adjacencies exist at (10, 3) and (11, 4) and fail at (12, 5) or (12, 6)
date: 2026-11-10
status: open
origin: [I-261110-02, H-261101-07, L:schewe2010, L:hlz2010]
---

## Statement

Some dual of a vertex-minimal triangulation of the orientable surface of genus 3 (10 faces, 42 of 45 pairs adjacent)
and of genus 4 (11 faces, 51 of 55) is realizable as an embedded polyhedron with planar simple faces (proposed
target S6); at genus 5 or genus 6 (12 faces; genus 6 is S0) none is. This is the face analogue of the picture in
print for the vertex version (CLAIMED: realizable through genus 4, mixed at genus 5, none at genus 6).

## Rival

The face version fails earlier than the vertex version: already the 20 maps at (10, 3) have no realization. The
vertex result does not transfer by duality, so the analogy carries no weight on its own.

## Evidence so far

None for the face version (nothing found in print, CLAIMED, one web search 2026-11-10; nothing run here). Planning
weight of the 2026-11-10 session for "(10, 3) exists": 0.25 (CONJECTURE).

## What would move it

E-261110-02: a SAT model that realizes and passes the exact verifier with 42 single adjacencies -> the (10, 3) part
is proved by a witness; 20 UNSAT-VERIFIED -> the (10, 3) part is refuted at formula scope (geometric reading
PROVED-1, conditional on the census, which is CLAIMED until re-enumerated, on encoder soundness and on general
position; cubic class only); timeouts move nothing. (11, 4) is proposed only if the (10, 3) median time is below 10
minutes.
