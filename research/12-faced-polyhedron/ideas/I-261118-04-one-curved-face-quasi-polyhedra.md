---
id: I-261118-04
title: One curved face - quasi-polyhedra with F - 1 planar faces and one skew face, straightened or shown unstraightenable
date: 2026-11-18
status: parked
direction: [DR19, DR11]
origin: [owner, I-261101-18]
---

## Idea

Owner (2026-11-18): allow one non-planar face. Such quasi-polyhedra are not solutions, but they may lead to one by
straightening the curved face, or show that no straightening exists. Reading: F - 1 planar polygons plus one face
spanning a skew polygon whose vertices lie on the lines X ∩ Y, so the neighbours stay polygons. A solution is a
quasi-polyhedron with a planar S, so "none can be straightened" equals "no solution"; the idea helps where the
quasi-objects of a case form a small list (straightening one with the other planes fixed is a single-plane cell
question). Knot theory enters only through the capping condition: S's boundary must bound an embedded disk that
misses the other faces.

## Why it might help

At OM level the quasi-objects of a map are the models of its formula with one face deleted, the face ladder of
I-261101-18 with the deleted face as a geometric object. Session check (`reviews/ideas-triage-2026-11-18-strip.py`):
no nine-face quasi-polyhedron arises by local surgery on Roest-Vigh's or Mizhaev's object (a legal tree of
doubled-pair edges touches at most 6 of 8 faces). Untested proposal.

## Cheapest test

E-261118-04, the (9, 3) one-face deletion sieve (<= 1 core-h). A straightening rung with a known answer (bend one face
of Roest-Vigh's object, repair with the planes free) only after a SAT there.

Source: `reviews/ideas-triage-2026-11-18.md` §2 (owner-approved as week item 1, 2026-11-18).

Parked 2026-11-19 (lead review 2026-11-19 §2, owner-approved): the pilot E-261118-04 tested the planar-defect reading
(STATUS 3az); the curved-face reading is untested. Neither a curved-face encoder nor a final-polynomial test of the two
map-29 models changes a decision: straightening is the full formula, UNSAT-VERIFIED for all 203 (9, 3) maps (STATUS 3d),
and nine faces at genus >= 4 has no census to sieve. The owner may reopen it.
