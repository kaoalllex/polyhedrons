---
id: E-261029-08
title: Gauss-map prefilter on all known near-misses
date: 2026-10-29
status: done
direction: [DR3, DR5]
origin: [L:hackerpoet, L:banchoff1967, E-261029-02]
tests: []
produces: [FD7, FD11]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Do the near-misses have the topology a solution needs (Gauss degree -5 with covering)?

## Method

Exact prefilter on normals only (signs of 3x3 determinants, all gauges); local violation counter (`code/local_viol.py`): multi-reflex vertices and in-face crossings.

## Results

All 1005 near-miss seeds fail the prefilter (own degrees -5..+4, mostly -1..+1); perturbations and 100 random normal sets fail too; admissible normals are easy to find by annealing. Every one of 300 seeds has >= 7 vertices with two reflex corners: not even immersions.

## Conclusions

EXACT per instance (FD11); the prefilter is a polyhedral form of a classical degree statement (FD7, PROVED-1).

## Next

Search inside the admissible class instead of repairing near-misses (E-261029-07, E-261029-10).
