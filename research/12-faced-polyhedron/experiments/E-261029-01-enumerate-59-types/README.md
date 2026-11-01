---
id: E-261029-01
title: Enumerate the neighbourly genus-6 triangulations with 12 vertices
date: 2026-10-29
status: done
origin: [L:abs1996, L:lutz, L:hackerpoet, L:ellingham]
tests: []
produces: [FD3]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

An independent, machine-checkable list of every map Szilassi-12 could have.

## Method

Two C enumerators (`code/enum_k12.c`, `code/enum2_k12.c`), canonical forms, an independent checker (`code/check_triangulations.py`, with negative controls), invariants (`code/k12_invariants.py`), and a bijection with two published lists (`code/compare_literature.py`).

## Results

Exactly 59 classes from both enumerators (12,144 labelled solutions, every class hit 264/|Aut| times); bijection with the HackerPoet and Lutz lists; automorphism orders agree 59/59. A checker bug and an enumerator overcount were found and fixed during the run. Data: `data/k12_triangulations.json`, `data/k12_invariants.json`, `data/k12_literature_map.json` (the shared dataset stays in `data/`).

## Conclusions

EXACT: the 59 types are reproduced (FD3). This is a replication of Altshuler-Bokowski-Schuchert 1996, not a discovery.

## Next

Every later experiment uses these maps.
