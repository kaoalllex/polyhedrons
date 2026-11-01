---
id: E-261029-04
title: Reproduce the symmetric impossibility on four instances
date: 2026-10-29
status: done
direction: [DR8]
origin: [L:mokijulio2026, E-261029-03]
tests: []
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Reproduce independently the published claim that symmetric realizations are impossible, on a few cases.

## Method

Own automorphism computation, symmetric OM-SAT instances (`code/omsat_sym.py`) with controls (free action, no forced zeros, explicit symmetric chirotope SAT, instance without triples SAT); CaDiCaL via PySAT.

## Results

Lutz #54 under T UNSAT (1.3 s), #3 under D3 UNSAT (9.3 s), #48 under D3 UNSAT (10.6 s), #48 under C2 with REFLEX1 + POC UNSAT (298 s). A DRAT proof for #54 T was checked by the own RUP checker (`code/rup_check.py`). Files: `results/sym_*.log`, `results/sym_54_T.cnf.gz`, `results/sym_54_T.rupcheck.log`.

## Conclusions

EXACT agreement with the prior work on four cases; the full sweep followed on the laptop (E-261029-13).

## Next

All 25 classes with drat-trim (E-261029-13).
