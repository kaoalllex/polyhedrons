---
id: E-261029-20
title: Solid-first search: Szilassi found without a prescribed map
date: 2026-10-29
status: done
direction: [DR7]
origin: [I-261029-27]
tests: []
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Search over planes plus a set of arrangement cells, so that the solid is always embedded and the map is not fixed.

## Method

`code/solid_first.py`, `code/solid_search.py`; topology macro-moves (tunnel drilling, handle attaching).

## Results

Without macro-moves every run stops at 4 (sphere-like trap); with them all runs reach genus 1 and one of four found a Szilassi-type polyhedron without any prescribed map, exactly EMBEDDED (`results/szilassi_found_without_map.json`, a positive control in `verify_all`).

## Conclusions

EXACT positive control: the solid-first representation can find embedded objects with an unknown map.

## Next

Exact inner step at n = 12 (E-261030-02).
