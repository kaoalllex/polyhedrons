---
id: I-261101-10
title: Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances
date: 2026-11-01
status: open
direction: [DR10, DR11]
origin: [I-261101-02, E-261029-13, E-261029-15]
---

## Idea

The 25 + 25 symmetric UNSAT instances are the only certified obstructions the project owns. Mine them: keep
GP, SYM and the normalisations as hard background; make the local clause families of each face (TRIPLE, SIMPLE,
REFLEX1, POC clauses that mention the face) one soft group per face; extract a minimal unsatisfiable set of face
groups by deletion with CaDiCaL assumptions (shrink the formula first with `drat-trim -c core.cnf`). Output per
instance: the minimal face sets F, their sizes, and the sub-map they induce.

## Why it might help

A core on k <= 6 faces that recurs across classes is the shape a lemma "kills many types at once" would have
(H-261101-02). It also gives a cheap asymmetric probe: the same face set's local clauses *without* symmetry, as a
sub-instance for every type containing that sub-map; an UNSAT there excludes a type with a tiny formula. Cross-field:
MUS/MCS extraction (Liffiton-Sakallah), proof mining in computer-assisted mathematics.

## Cheapest test

Lutz #54 under T (solves in about 1 s): a group-MUS in minutes. Then #3 D3 (simplicity alone is UNSAT there).

## Source

Strategy review 2026-11-01, direction 5; `proof-no-symmetric-immersion/README.md` item 4.
