---
id: E-261030-02
title: Solid-first with an exact CP-SAT inner step at n = 12
date: 2026-10-30
status: done
direction: [DR7]
origin: [E-261029-20]
tests: [H-261030-03]
produces: [W:lab_solid_genus3]
verdict: OPEN-LOW: dead-end maps
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Reach as many adjacent pairs as possible with 12 planes, no map prescribed.

## Method

`code/solid_cpsat.py` (for fixed planes CP-SAT picks the best solid), `code/solid_exact_search.py` (annealing over planes), dead-end analysis with `code/handle_add.py` (`reach`).

## Results

Genus 3 (48 of 66 pairs) and genus 2 (42 pairs), exactly verified (`results/genus3_12faces_48pairs*.json`, `results/genus2_12faces_42pairs.json`); plateau at 48. Every map found is a dead end: handles reach at most 54 (or 60).

## Conclusions

EXACT witnesses (S3); the free search drifts into maps that cannot be completed.

## Next

Keep extendability by construction: genus ladder (E-261030-03).
