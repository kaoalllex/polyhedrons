---
id: I-261108-09
title: Perturbation lemma - vertices of degree >= 4 resolve into cubic vertices, so the cubic (8, 2) / (9, 3) negative would cover non-cubic objects
date: 2026-11-08
status: open
direction: [DR19]
origin: [owner, E-261103-03]
---

## Idea

Conjecture: let P be an embedded polyhedral surface with planar simple faces, every two faces adjacent, and some
vertices of degree >= 4. A small generic perturbation of the face planes, with the surface near each such vertex
redefined as the boundary of the cells of the perturbed arrangement that inherit membership from the original cones
(the small bounded cells in or out), gives an embedded cubic surface with the same faces (still simple), the same
genus and every adjacency kept, possibly with new segments. At (8, 2) and (9, 3) the result is cubic with all pairs
adjacent, so E = 30 or 39: an S5 object, which the census and the plain UNSATs exclude (conditional, `STATUS.md` 3d).
The non-cubic objects of the `STATUS.md` §4 scope entry (e.g. (9, 3) with V = 23, E = 36, three 4-valent vertices)
would then be excluded at the same level plus this lemma.

Local picture: k planes through a vertex p, otherwise in general position; k <= 6 at (9, 3) (degree excess <= 3) and
k <= 5 at (8, 2). After the perturbation the unbounded cells near p keep the membership of the cones with the same
sign vector; only the bounded cells are free. A 4-valent vertex with faces A, B, C, D in cyclic order should split
along A ∩ C or B ∩ D, depending on the sign of the perturbation: true for a convex vertex, unchecked for saddles.

## Why it might help

It would remove the word "cubic" from the (8, 2) / (9, 3) note, which is the first question a referee would ask,
without a solver run. Untested: for some saddle vertex no choice of sign and bounded cells may give a manifold vertex
with every face connected; then the gap stays and needs its own formulas (chirotope zeros at the concurrent
quadruples).

## Cheapest test

An exact finite check of the **universal** local statement: for every perturbation type of the k planes through p,
some choice of the bounded cells gives a valid patch. Only the universal form makes the global step free: one small
generic perturbation of all planes is then covered at every exceptional vertex, and the patch choices sit in disjoint
small balls, so they impose no further conditions on the planes (review 08e Follow-up Q4 accepts this). An
existential local result (some perturbation works) does not suffice, because one plane passes through several
vertices. A valid patch must:

* keep the boundary trace of the continued original surface on a small sphere around p;
* keep every labelled face a disk sector attached along its prescribed boundary arc (face connectivity alone does not
  exclude a hole);
* have positive-length outgoing edges and no extra component.

For k = 4, a generic central arrangement of 4 planes is unique up to reorientation: take every union of its 14 cones
whose boundary is a manifold 4-valent vertex with all four planes as faces, perturb with both signs, put the bounded
cell in and out, and test the three conditions and the adjacency bookkeeping. Then k = 5, 6 (finitely many
perturbation types). Also cover the nongeneric central stars the lemma allows: k <= 6 incident planes need not have
every triple of normals independent. Seconds of CPU in one session, then a written argument for the global step
(compact separation away from the vertices); PROVED-1 at best. A failed universal type kills this sufficient lemma,
not the weaker existential one; the fallback is I-261108-10.

## Source

Owner's question of 2026-11-08 on non-cubic (9, 3) objects (`STATUS.md` §4 scope entry); the lead's sketch in that
session; question 3 of `reviews/REVIEW_PROMPT_2026-11-08.md`. Planned for the note package, after week items 1, 3, 4.
