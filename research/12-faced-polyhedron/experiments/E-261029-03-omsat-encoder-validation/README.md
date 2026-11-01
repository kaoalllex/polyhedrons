---
id: E-261029-03
title: Validate the OM-SAT encoder against exact geometry
date: 2026-10-29
status: done
direction: [DR8]
origin: [I-261029-42, L:schewe2010]
tests: []
produces: [FD2, FD4]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Check that every predicate and clause family of the oriented-matroid encoder matches exact geometry.

## Method

`code/omsat.py` (CNF and Eval backends), `code/omsat_geom.py` (exact geometry), `code/omsat_validate.py`, `code/omsat_crosscheck_track4.py` (cross-check with the independent Track-4 checker).

## Results

693 configurations, 2.5 M predicate evaluations, 0 mismatches; triples <-> direct embeddedness 693/693; CNF literals equal Eval values on 17 instances; cross-check with Track 4: 149 configurations, 0 mismatches. Files: `results/validation.json`, `results/validation.log`, `results/crosscheck_track4.json`; the Lutz-to-our-id map moved to `data/lutz_to_ourid.json`.

## Conclusions

EXACT tests of the encoder (FD4); Lemma 5.1 re-derived (FD2, PROVED-1). Single encoder: a second one is still needed for theorem-level claims.

## Next

Symmetric instances (E-261029-04).
