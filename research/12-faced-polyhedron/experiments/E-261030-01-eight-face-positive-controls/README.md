---
id: E-261030-01
title: Positive controls: the 8-face Mizhaev and Roest-Vigh polyhedra
date: 2026-10-30
status: done
direction: [DR12]
origin: [L:mizhaev2026, L:roestvigh2026, I-261030-11]
tests: [H-261029-07]
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Check our exact verifier and Gauss tools on the known 8-face genus-3 objects with doubled adjacencies.

## Method

Published planes and face cycles; `code/ladder_exact.py` with doubled links; `code/control_rost_vigh.py` (in `verify_all`).

## Results

Mizhaev's planes EMBEDDED (pair energy 0); Roest-Vigh EMBEDDED, all pairs adjacent, own Gauss degree -2 = 1 - g.

## Conclusions

EXACT: doubled adjacencies can be embedded (H-261029-07 proved); our tools agree with both papers.

## Next

Relaxed 12-face target (planned E-261101-08); negative control of the S0 check (`verify_all`).
