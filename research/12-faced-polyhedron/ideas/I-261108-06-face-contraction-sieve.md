---
id: I-261108-06
title: Face-contraction sieve - is a plain S5 formula already UNSAT on the clauses of the rank-3 contraction at one face?
date: 2026-11-08
status: parked
direction: [DR19, DR9]
origin: [E-261101-06, E-261108-02]
---

## Idea

The clauses whose chirotope variables all contain one face X describe the rank-3 contraction at X: the line
arrangement in the plane of X with X's polygon on it. They form a clause subset of the plain formula, so an UNSAT is an
exact exclusion of the whole map, and each sub-formula is small.

## Why it might help

A cheap pre-filter for the 1117 (10, 4) maps. The core study E-261108-02 grouped clauses by constraint faces, not by
contraction, so it does not answer this. Untested.

## Cheapest test

Power first: the 203 known-UNSAT (9, 3) maps x 9 faces at 20 s, 10 shards (<= 1 core-h). Kill: 0 of 203 -> park;
>= 20 of 203 -> run on the (10, 4) maps.

## Source

Lead review 2026-11-08d, §6 idea N3; week item 5.

## 2026-11-09 result

E-261109-05: 0 of 203 (9, 3) maps killed by a one-face contraction (cap 20 s, controls pass). Parked; the contraction
never contains TRIPLE or REFLEX1 (three-face clauses), which is where the (9, 3) obstructions live.
