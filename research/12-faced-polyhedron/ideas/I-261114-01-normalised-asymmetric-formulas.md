---
id: I-261114-01
title: Normalised asymmetric formulas - the reorientation and mirror units on the plain S5 / S6 formulas
date: 2026-11-14
status: open
direction: [DR19, DR8]
origin: [I-261029-43, E-261110-02, E-261108-03]
---

## Idea

The plain S5 / S6 formulas are built from `omsat_validate.ALL_OPTS`, which sets neither `symbreak` nor `mirror`, so
they carry no unit on a chirotope variable; the S0 formulas have both. Switch the two existing options of
`omsat.build` on for the asymmetric target formulas: n units fix the reorientation of the n planes, one unit fixes
the mirror image.

## Why / cheapest test

Session check of the lead review 2026-11-14 (`reviews/strategy-review-2026-11-14-symbreak.py`, kissat, no proofs,
known answers only; NUMERICAL, not ledger evidence): (8, 2) #0, (9, 3) #40 and (10, 4) #845, #96, #85 are
UNSAT-SOLVER 10-89x faster with the units; Roest-Vigh, Mizhaev and Szilassi have a gauge satisfying them and stay SAT
pinned; two (10, 2) maps stay SAT. Soundness of the units on the `submap=True` and multi-adjacency clause families is
not proved: it is the first prep step of E-261114-01 (exact invariance test, PROVED-1 paragraph, positive controls).
A wrong normalisation turns UNSAT answers into non-results. Untested on any target formula.

Source: `reviews/strategy-review-2026-11-14.md` §1, §6 (N1); approved by the owner on 2026-11-14.
