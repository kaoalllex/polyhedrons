---
id: I-261108-08
title: Independent census of the (8, 2) and (9, 3) candidate maps - a second enumerator that shares no code with E-261103-01
date: 2026-11-08
status: open
direction: [DR19]
origin: [E-261103-01]
---

## Idea

Enumerate the candidate maps as genus-g rotation systems of K_F plus the extra edges (CP-SAT with canonical-form
deduplication, or Lutz-style lexicographic surface enumeration), with admissibility, and compare classes and canonical
hashes with E-261103-01: 2 classes at (8, 2), 240 classes / 203 admissible at (9, 3).

## Why it might help

The (8, 2) / (9, 3) negative result rests on census coverage. FD3 had two enumerators for the 59 types; the S5 census
has one for the full list (its independent algorithm covered only the free-C3 sub-list). Untested.

## Cheapest test

(8, 2) first (minutes), then (9, 3). A missing map goes to the plain-formula queue.

## Source

Lead review 2026-11-08d, §6 idea N5 and audit A2; week item 3.
