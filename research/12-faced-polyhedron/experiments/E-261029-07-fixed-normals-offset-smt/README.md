---
id: E-261029-07
title: Exact offset decision at fixed normals (gauge-fixed SMT)
date: 2026-10-29
status: done
direction: [DR2]
origin: [I-261029-55]
tests: []
produces: [FD8]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

With the face normals fixed, every embedding condition is linear in the offsets: decide existence exactly.

## Method

`code/fixed_normals.py`, then `code/fixed_normals_gauge.py` with the orientation gauge imposed (z3, exact integer cofactors).

## Results

A first float-cofactor version was wrong (z3 exploited rounding) and was fixed. Szilassi control: SAT and exactly embedded for small perturbations, UNSAT for large ones. With the gauge, admissible normal sets are decided in 19-90 s (types 0, 5, 58: UNSAT); without it no answer in 300 s.

## Conclusions

PROVED-1 + EXACT tool (FD8). UNSAT is scoped to its normal set, gauge and bounds.

## Next

Basis of normals-first (E-261030-08, E-261030-11).
