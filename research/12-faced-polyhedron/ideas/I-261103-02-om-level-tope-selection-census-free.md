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

## 2026-11-16b decision

Owner-approved week item 2 (`reviews/strategy-review-2026-11-16b.md`), experiment E-261116-07. Why now: a map census is
out of reach at (8, 3) and (9, 4) (session check, >= 34,402 (8, 3) classes after 551 of 1806 patterns), while per-map
formulas at 10 elements take seconds. Ladder (7, 1), (8, 2), (8, 3) before (9, 4), (9, 5); kill rule in `ROADMAP.md`.

## 2026-11-17 dialogue

`reviews/dialogue-2026-11-16-strategy.md` §2 row 3, Appendix A1: specification v2 replaces the 16b ladder (no tope-circuit block, both directions at infinity, validity bits, no-pinch, Euler and eager connectivity, the (9, 39) pricing rung, the bridge gate); marks 2 2 3 1 / 2 1 3 1. The main investment: week item 3, E-261116-07 amended (2 sessions, <= 6 core-h, decision tree of review §2). Proof obligations go to E-261116-09.

## 2026-11-17 result

E-261116-07 (CONCLUSION / STATUS 3aw): the seven-plane cheapest test passed (Szilassi's type unpinned in 8 s, realized);
the eight-plane rung found no model in 16 cubes x 560 s, also in the cube that contains both known (8, 3) chirotopes.
Parked (ROADMAP "Parked methods"), not refuted; status stays open. A rerun must change the search and measure its time
to a model on that cube first.
