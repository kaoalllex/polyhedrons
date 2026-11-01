---
id: E-261029-17
title: Structure of near-miss defects (winding number, defect positions)
date: 2026-10-29
status: done
direction: [DR5]
origin: [I-261029-16, I-261029-13, E-261029-02]
tests: []
produces: []
verdict: LOW-YIELD@minutes
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Do near-misses bound a solid, and do their defects sit at fixed combinatorial positions?

## Method

`code/q17_winding.py` (exact octant winding test at 220 triple points), `code/q18_gwas.py` (canonical relabelling, automorphism orbits, 12 types with >= 25 seeds).

## Results

45 of 1005 seeds bound a solid (w in {0,1}); no universal defect position (hotspots only in symmetric types).

## Conclusions

NUMERICAL: no exploitable structure.

## Next

-
