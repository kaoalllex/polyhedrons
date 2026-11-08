---
id: I-261108-05
title: Certified incremental SAT across the maps of one pattern - shared OM lemmas, selector literals, incremental proofs
date: 2026-11-08
status: open
direction: [DR19, DR8]
origin: [I-261101-12, E-261103-07]
---

## Idea

All (10, 4) plain formulas share the rank-4 oriented-matroid part on 11 elements and differ in the map clauses. One
CaDiCaL session per multiple-adjacency pattern, with a selector literal per map, keeps the learned OM lemmas across maps.
Incremental proof formats with a checker (IDRUP / LIDRUP of the SAT-competition incremental track; CLAIMED, not checked
here) keep each UNSAT certifiable.

## Why it might help

The (10, 4) route needs a large speed-up (E-261103-07: 10/10 TIMEOUT). Shared lemmas may cut the total time when many
formulas share most clauses. Untested.

## Cheapest test

Six `(1^4,2)` (9, 3) maps with known UNSAT in one incremental session against separate solving; >= 2x total speed-up
makes it a variant of the (10, 4) speed-up benchmark.

## Source

Lead review 2026-11-08d, §6 idea N2. Overlaps E-261101-20 (the S0 form).
