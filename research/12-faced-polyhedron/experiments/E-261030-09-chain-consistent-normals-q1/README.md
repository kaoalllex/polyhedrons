---
id: E-261030-09
title: Q1: one normal set in class for a whole handle chain
date: 2026-10-30
status: done
direction: [DR14]
origin: [I-261030-13]
tests: [H-261030-02]
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Find one set of 12 normals that is in the right Gauss class on all 7 levels of a chain, then decide offsets level by level.

## Method

`code/chain_normals.py` (sum of class energies over the 7 levels), exact class check, exact offsets at fixed normals.

## Results

Type 58, chain seed 3: chain-consistent normals found (`results/type58_chain_seed3_consistent_normals.json`), but the sphere level is already UNSAT at these normals (z3, 33 s).

## Conclusions

EXACT on one instance: the Gauss class is not sufficient (H-261030-02 refuted on that instance).

## Next

UNSAT-core mining on this instance (planned E-261101-05).
