---
id: I-261110-04
title: Immersion-only and segment-free variants of the decided S5 formulas - is multiplicity what the solver refutes
date: 2026-11-10
status: open
direction: [DR19, DR11, DR10]
origin: [I-261108-01, E-261103-03, I-261029-54]
---

## Idea

Every admissible (8, 2) and (9, 3) plain formula is UNSAT-VERIFIED (STATUS 3d). Which clause family carries the
refutation? Re-solve a few decided maps with clause families removed. Each variant is a relaxation of the plain
formula, so SAT in a variant is a statement about that formula only, never a geometric object.

* **V1, immersion-only** (the S2 encoding of FD6): `triples` off, `reflex` / `reflexconsist` / `poc` on.
* **V2, plain without `SEGMENT_DISJOINT`**: the global forbidden triples stay, the clauses that keep the boundary runs
  of a multiple pair disjoint on their common line go.

Reading of the encoder (EXACT, `code/omsat.py` lines 562-568): `SEGMENT_DISJOINT` is emitted only under
`triples`, so V1 drops both the global triples and the segment clauses and cannot separate them. V2 needs a
default-off encoder option; the default formulas and their recorded CNF hashes must not change.

## Why it might help

It decides between two readings of the negative ladder (H-261110-01). If V2 is SAT where plain is UNSAT, the
multiple-adjacency constraints are necessary for the refutation, and the ladder says little about S0, which has
none. If V1 is already UNSAT, the obstruction is local, and a lemma may be readable from the cores of the two
(8, 2) formulas, which solve in seconds (STATUS 3d; core tools of I-261101-02 / E-261101-05). It extends I-261108-01
(a local cause on the faces of concentrated patterns) from "which faces" to "which clause family".

## Cheapest test

E-261110-05: the two (8, 2) maps and six (9, 3) maps, V1 and V2, cap 1800 s, DRAT for (8, 2); <= 3 core-h.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §4 I-D, §5 H-A); V2 added
by the lead session of 2026-11-10 after reading where the encoder emits `SEGMENT_DISJOINT`.
