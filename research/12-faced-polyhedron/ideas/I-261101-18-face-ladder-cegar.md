---
id: I-261101-18
title: The face ladder is monotone, the genus ladder is not - k-face sub-instances and face-CEGAR seeds
date: 2026-11-01
status: open
direction: [DR8, DR11, DR1]
origin: [I-261029-11, I-261101-10, E-261030-03, FD2]
---

## Idea

Deleting a face Z from a solution leaves 11 planar simple 11-gons, pairwise adjacent, embedded, with one planar
boundary cycle (the old boundary of F_Z). Every solution therefore restricts to a realization of every k-face
sub-object, for every subset of k faces: the face ladder is **monotone**. The genus ladder is not (a genus-3 object
on 12 planes is not part of a genus-6 one; the handle changes which chambers form the solid everywhere), which is why
nights 3-5 measured the method, not the problem. In the OM-SAT encoding a k-face sub-instance is the instance with
the local clause families (TRIPLE with all three faces in the set, SIMPLE, REFLEX1, POC) kept only for those k
faces; GP and the normalisations stay. Two uses:

1. **Obstruction.** An UNSAT k-face sub-instance kills every type containing that sub-map, with a formula a human
   can read when k is small. Start with k = 7 face sets that span the most triangles of T (at most 9, by the
   "no Szilassi embryo" count), then k = 8, 9.
2. **Seeds in the right class (face-CEGAR).** A SAT model of a k-face sub-instance is a chirotope of a partial
   object; realize it numerically (fit the 12 planes to the 715 signs, hinge loss, then exact re-check of the k
   faces), add the clauses of the next face, re-solve with the model as phase hints, repeat. The first seeds whose
   realized faces are all simple and pairwise correct, unlike every HackerPoet near-miss (FD11).

## Why it might help

It is the only ladder along which a realization of the top rung restricts to realizations of every lower rung, so
every negative result on a rung is a theorem about the target and every positive result is a genuine partial
solution. Cross-field: CEGAR (counterexample-guided abstraction refinement) from model checking; lazy clause
generation in CP.

## Cheapest test

One type (a trivial-Aut type), all 7-face sets up to automorphism, CaDiCaL with a 10-minute limit each: the count
of UNSAT / SAT / timeout, and one realized SAT model.

## Source

Strategy review follow-up 2026-11-01 (dialogue with the owner): monotonicity argument.
