---
id: E-261030-06
title: Gauss gate: degree and k_tau of every realization and next handle
date: 2026-10-30
status: done
direction: [DR3]
origin: [I-261030-26, I-261030-27, E-261030-04, E-261030-05]
tests: [H-261030-01, H-261030-05]
produces: [FD7]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Explain the genus-4 plateau by the Gauss class; test whether failed levels are out of class (test 2.2).

## Method

`code/gauss_gate.py` (own degree, turning numbers, all gauges, k_tau, hemisphere margin; covering confirmed on 1000 directions), `code/gate_vs_glad.py`; job `gate` (first 47 realizations on 2026-10-30, extended in night 4).

## Results

Type 0 genus 3: all arms k_tau = 0 (degree -2, need -3), no admissible gauge. 352 of 378 failed night-3 levels (93 %) are out of class. k_tau at the seed does not predict the event-energy search. Degree 1 - g on all 232 gated realizations (night 4). Records: `results/gate/`.

## Conclusions

EXACT: the type-0 plateau is a Gauss-class obstruction (H-261030-01 supported); the class is a FOUNDATION filter.

## Next

Normals first and k-drift (E-261030-08).
