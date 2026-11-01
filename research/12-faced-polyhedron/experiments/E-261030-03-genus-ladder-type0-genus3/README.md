---
id: E-261030-03
title: Genus ladder: an extendable genus-3 polyhedron of type 0
date: 2026-10-30
status: done
direction: [DR1]
origin: [E-261029-19, E-261030-02, I-261030-03]
tests: [H-261030-03]
produces: [W:lab_type0_genus3]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Climb from the sphere by handles inside one target map, so that every level can still be completed.

## Method

`code/genus_ladder.py`, `code/tubes.py` (chains M6 -> ... -> M0 by removing tubes), annealing + CMA-ES per level, exact check; diversity searches for more realizations.

## Results

Type 0 realized at genus 3 with `reach` = 66 (the first non-dead-end genus-3 polyhedron); four realizations A-D plus a polished copy (`results/type0_genus3_extendable*.json`, all in `verify_all`). The map has exactly one completion to genus 6, the type-0 map itself (certificate E-261101-02).

## Conclusions

EXACT witness (S3), our best positive object.

## Next

Climb to genus 4 (E-261030-04); dossier (planned E-261101-03).
