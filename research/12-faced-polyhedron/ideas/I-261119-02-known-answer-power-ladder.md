---
id: I-261119-02
title: Known-answer power ladder - decided negatives as refutation rungs and the free-C2 eight-face formula as the discovery rung of P3-sym
date: 2026-11-19
status: tried
direction: [DR19]
origin: [I-261118-01, E-261118-02, E-261103-03]
---

## Idea

Every rung so far timed only the finding of a known object; no rung timed a refutation at the target's size. Use the
decided negatives as refutation rungs of the same orbit size: P3-sym with a free C2 at (8, 30) (66 quad orbits; the
(8, 2) negative) and with C3 3+3+3 at (9, 39) (72 orbits, the nine-face C3 size; the (9, 3) negative), both expected
INFEASIBLE (STATUS 3d). Use the free-C2 formula at (8, 36) (66 orbits, both known objects inside) as the discovery rung.

Lemma (PROVED-1 sketch, lead review 2026-11-19 §2, owner 5): a uniform symmetry group of an eight-face solid contains a
free half-turn (order 3 needs two fixed faces; orders >= 5 make planes concurrent; a mirror or inversion forces zero
signs; a rotoreflection of order 4 squares to a free half-turn). So the free-C2 (8, 36) formula holds every symmetric
uniform (8, 3) solid, D2 and S4 included; blocking found maps under the normaliser enumerates that slice.

## Why it might help

It separates the three readings of the nine-face UNKNOWN of E-261118-02 (formula size, refutation cost, no C3 object)
and answers the owner's question 5 (unknown symmetric (8, 3) objects). Orbit counts 36 / 34 / 66 / 72 are EXACT
(`reviews/strategy-review-2026-11-19-orbits.py`). Untested proposal.

## Cheapest test

E-261119-01 (week item 1): one owner evening, <= 20 core-h.

Source: `reviews/strategy-review-2026-11-19.md` §5 N1 (owner-approved 2026-11-19).

## 2026-11-20 E-261119-01

Discovery rung passed: free C2 at (8, 36) returned Mizhaev's and Roest-Vigh's maps in 59 s and 81 s, realized; then
UNKNOWN at 1.5 h (no third map found or excluded). Refutation rungs undecided: (8, 30) and C3 (9, 39) UNKNOWN at 1 h on
5 workers, so P3-sym's nine-face UNKNOWN is not read as evidence (STATUS 3bd).
