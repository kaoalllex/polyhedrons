---
id: E-261029-13
title: Certify: no symmetric embedding (25 classes, DRAT)
date: 2026-10-29
status: done
direction: [DR8]
origin: [E-261029-04, I-261029-44, L:mokijulio2026]
tests: []
produces: [FD5, C:symmetric_drat]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Certified, independent reproduction of "no 12-face Szilassi-type polyhedron has a non-trivial symmetry".

## Method

Laptop night 1, job `sym` of `overnight/run_overnight.py`: all 25 classes (21 C2, 4 C3), our encoder, CaDiCaL proofs checked by drat-trim; control without triples SAT for every class.

## Results

25/25 UNSAT-VERIFIED (solve 8-147 s each; proofs 959 MB). Records with CNF and proof hashes: `results/sym/results.jsonl`. Proofs regenerated bit-identically and published (E-261101-01).

## Conclusions

CERTIFIED (FD5); its encoding soundness rests on FD2 (PROVED-1). Reproduces Moki & Julio 2026.

## Next

Immersion version (E-261029-15).
