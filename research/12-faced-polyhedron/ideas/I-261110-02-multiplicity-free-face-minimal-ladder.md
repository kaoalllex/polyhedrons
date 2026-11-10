---
id: I-261110-02
title: Multiplicity-free face-minimal ladder - duals of the vertex-minimal triangulations, single adjacencies at every rung
date: 2026-11-10
status: open
direction: [DR19, DR8]
origin: [owner, I-261101-07, L:schewe2010, L:hlz2010]
---

## Idea

The S5 ladder (I-261101-07) needs multiple adjacencies at every rung below S0 (2, 3, 3, 2 extra segments at (8, 2),
(9, 3), (10, 4), (11, 5)); S0 has none. A second ladder has S0's zero slack at every rung: the duals of the
**vertex-minimal triangulations** of the orientable surfaces. Such a dual is a cubic map whose faces are simple
polygons, every adjacency is single, and **not** every pair of faces is adjacent. Proposed target id S6
(`reviews/strategy-review-2026-11-10.md` §3; not in `SPEC.md` until the owner approves; S0 is not weakened).

| (F, g) | maps | adjacent pairs | Label of the count |
|---|---:|---|---|
| (10, 2) | 865 | 36 of 45 | CLAIMED (Lutz; web check 2026-11-10) |
| (10, 3) | 20 | 42 of 45 | CLAIMED (Lutz; web check 2026-11-10) |
| (11, 4) | 821 | 51 of 55 | CLAIMED, from the handoff session's memory; **not confirmed** by the 2026-11-10 web check |
| (12, 5) | 751,593 | 60 of 66 | same: not confirmed |
| (12, 6) | 59 | 66 of 66 = S0 | EXACT (FD3) |

Pair counts are E = 3 (F + 2g - 2) (elementary). The map counts must be read from the primary tables (Lutz
math/0506316; Sulanke-Lutz math/0610022) before any of them enters `STATUS.md`.

Scope of "face-minimal" (elementary counting, PROVED-1): among **cubic** polyhedra with pairwise single adjacencies
(dual a simplicial complex), genus g needs F (F - 1) / 2 >= 3 (F + 2g - 2) faces, so F >= 10 at genus 3. Polyhedra
with vertices of degree >= 4 or with multiple adjacencies are outside this class (Roest-Vigh has 8 faces at genus 3).

## Why it might help

* The vertex version is decided in print through genus 4 (CLAIMED, abstracts only): every vertex-minimal
  triangulation of genus 2, 3 and 4 is realizable (Bokowski-Lutz; Hougardy-Lutz-Zelke), genus 5 has realized
  examples and non-realizable ones, genus 6 has none (Schewe). Realizability does not transfer to the face version by
  duality, and nothing on the face version was found in print (CLAIMED, one web search, 2026-11-10).
* (10, 3) is small: 20 maps, 11 elements as at (10, 4), fewer constraints (no multiple segments). A SAT model that
  realizes is a new polyhedron; 20 UNSAT-VERIFIED formulas are a conditional face-minimality statement for genus 3
  and the first negative on a ladder with S0's slack.
* It tests H-261110-01 from the other side: SAT models at (10, 3) and none at (10, 4) support "multiplicity is the
  obstruction".

## Cheapest test

Build the (10, 3) formulas with `Triangulation(..., submap=True)` (`code/omsat.py`), run two of them for 20 minutes.
Then E-261110-02 (all 20 maps, one night with DRAT). The maps are not on disk (`literature/` holds only the genus-6
lists); the prep fetches Lutz's list as untrusted data, checks it and converts it to dual `links`.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §3 T2, §4 I-B).
