---
id: E-261029-19
title: Smaller analogues n = 7, 8 with black-box engines
date: 2026-10-29
status: done
direction: [DR6, DR15]
origin: [I-261029-07, I-261029-29, I-261029-31, I-261029-32, I-261029-33, I-261029-34]
tests: [H-261029-07]
produces: []
verdict: LOW-YIELD@sessions 2-5
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Calibrate the pipeline on n = 7 (Szilassi) and test engines on n = 8 (genus 2, doubled adjacencies or 4-valent vertices).

## Method

`code/ladder.py` (maps by annealing over rotation systems), exact verifier `code/ladder_exact.py`; engines: annealing, exact single-plane relocation, ILS, GA (island model), CMA-ES, NGOpt / DE; rung 8b with 4-valent vertices (`code/ladder4.py`); "beauty" polishing (`code/beauty.py`).

## Results

n = 7: Szilassi-type polyhedra from random planes in seconds by every engine (exactly EMBEDDED). n = 8: plateau at 1-2 violations on every map and engine (not degenerate limits). The exact verifier caught four optimizer exploits (merged collinear edges, a gap overlap, scale collapse, an edge through a 4-valent point).

## Conclusions

NUMERICAL: black-box engines solve n = 7 and stall at n = 8; the exact verifier is essential (FD10).

## Next

Structured searches (solid-first E-261029-20, genus ladder E-261030-03).
