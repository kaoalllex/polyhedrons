---
id: E-261029-09
title: Do Gauss clauses speed up OM-SAT?
date: 2026-10-29
status: done
direction: [DR16]
origin: [I-261029-55]
tests: [H-261029-12]
produces: []
verdict: LOW-YIELD@1 instance
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Test whether degree and covering clauses shorten symmetric SAT instances.

## Method

`code/omsat_gauss.py` (k abstract directions), Lutz #48 C2 with k = 0, 2, 4.

## Results

UNSAT 91.8 s without, 99.7 s with k = 2, 98.3 s with k = 4: no speed-up.

## Conclusions

NUMERICAL timing on one instance; the clauses are not used in the certificate jobs.

## Next

-
