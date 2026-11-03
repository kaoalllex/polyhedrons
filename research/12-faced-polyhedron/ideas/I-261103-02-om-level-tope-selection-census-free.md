---
id: I-261103-02
title: Census-free exact search - select the solid's topes inside the oriented matroid, chirotope and cell set in one SAT instance
date: 2026-11-03
status: open
direction: [DR19, DR7, DR8]
origin: [I-261029-27, I-261101-08, L:roestvigh2026]
---

## Idea

Solid-first (`code/solid_first.py`, `solid_cpsat.py`) selects bounded cells of a *fixed* arrangement with CP-SAT; the
arrangement is coordinates. Do it one level up: variables for the rank-4 chirotope on F + 1 elements (210 signs at F = 9)
*and* for the set of bounded topes (cells) that form the solid, with the face-structure conditions written on cocircuits and
topes: one disk face per plane, 1-3 edge runs per pair, every pair adjacent, cubic vertices, orientability. One SAT instance
then asks "does any (9, 3) polyhedron exist, with any map", without a map census; a model gives a chirotope to realize (the
existing realizers), and UNSAT with DRAT is a theorem for the whole case at once.

## Why it might help

It is the exact form of the Roest-Vigh "construction procedure from the planes alone" (their section 4) and the only
formulation that quantifies over maps and chirotopes together; it also attacks S0's one loophole (a symmetric arrangement
with an asymmetric solid) without a catalogue. Risk: the tope set of a rank-4 oriented matroid is implicit in the chirotope,
so the encoding may be large or the solver slow. CONJECTURE.

## Cheapest test

7 planes (8 elements): the instance must be SAT with Szilassi's chirotope among its models and realize; then 8 planes
against the two known (8, 3) objects (their chirotopes must be models). If the 7-plane instance does not solve in minutes,
park.

## Source

Strategy review 2026-11-03 (`reviews/strategy-review-2026-11-03.md` section 4, idea 1).
