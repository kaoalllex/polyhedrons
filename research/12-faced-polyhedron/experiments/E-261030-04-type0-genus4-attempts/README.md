---
id: E-261030-04
title: Type 0: attempts at genus 4
date: 2026-10-30
status: done
direction: [DR1]
origin: [E-261030-03, I-261030-03, I-261030-05, I-261029-38]
tests: [H-261030-04]
produces: []
verdict: LOW-YIELD@1 session
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Add a fourth handle to the type-0 genus-3 realizations.

## Method

Branching ladder (`code/beam_ladder.py`), LNS on the handle planes, level skipping (`code/seed_search.py`), drift inside the genus-3 realization space (`code/drift_search.py`), repair search, degeneracy floor (`ladder.degeneracy`), depth-weighted energy, singularity (flip) analysis.

## Results

Best honest attempt 4 violations (`results/type0_genus4_attempt_4viol.json`); "2 violations" was a degenerate limit (`results/type0_genus4_attempt_degenerate.json`, a negative control in `verify_all`); the degenerate attractor approaches faces 1 and 6 meeting twice (an invalid flip).

## Conclusions

NUMERICAL plateau; explained afterwards by the Gauss class (E-261030-06): every arm has k_tau = 0.

## Next

Gauss gate (E-261030-06), normals first (E-261030-08).
