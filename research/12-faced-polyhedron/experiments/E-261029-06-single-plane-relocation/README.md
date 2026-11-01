---
id: E-261029-06
title: Exact single-plane relocation from the best near-miss
date: 2026-10-29
status: done
direction: [DR5]
origin: [I-261029-30, E-261029-02]
tests: []
produces: []
verdict: LOW-YIELD@40 min
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Are the best asymmetric near-misses local minima for moving ONE plane anywhere?

## Method

`code/relocate.py`, `code/reloc_descent.py`: the count is constant on cells of a 220-hyperplane arrangement in plane space; probe cells around sampled vertices.

## Results

From HackerPoet topology 33 (5 violations): 33 relocation steps, only count-5 cells; no improvement.

## Conclusions

NUMERICAL: the near-miss is a plateau for single-plane moves.

## Next

Superseded by the Gauss prefilter finding (E-261029-08).
