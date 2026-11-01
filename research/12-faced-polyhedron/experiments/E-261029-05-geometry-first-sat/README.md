---
id: E-261029-05
title: Geometry-first SAT: fixed planes, all maps at once
date: 2026-10-29
status: done
origin: [owner]
tests: []
produces: []
verdict: LOW-YIELD@1 session
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

For fixed planes, decide with SAT whether any labelled map of any type embeds (Track 4).

## Method

`code/planes.py` (exact geometry and a direct checker), `code/geomsat.py` (SAT / MaxSAT / CP-SAT), `code/exp_n7.py`, `code/exp_n12.py`, `code/anneal.py`.

## Results

IN predicate vs exact point-in-polygon: 242,400 comparisons, 0 mismatches. Szilassi (perturbed) SAT; random 7-plane arrangements admit a torus with frequency about 2e-4. n = 12: 30/30 random arrangements UNSAT; best upper bounds 23-39 violations; a 9-minute annealing run 33 -> 24 (`results/track4_anneal_sphere_unif_1.json`).

## Conclusions

EXACT validation of the predicates; for n = 12 the random-plane approach is far from solutions (same 21-24 plateau as earlier GPU searches).

## Next

The Track-4 checker became the independent cross-check of the OM-SAT encoder.
