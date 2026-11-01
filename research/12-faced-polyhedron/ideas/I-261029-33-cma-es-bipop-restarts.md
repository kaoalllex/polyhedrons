---
id: I-261029-33
title: CMA-ES with BIPOP-like restarts
date: 2026-10-29
status: tried
direction: [DR6]
origin: []
---

## Idea
CMA-ES (cma 4.0.0) with restarts; scale-collapse guard added after float false zeros.

## Why it might help
Baseline continuous global optimizer.

## Cheapest test
n = 7 exact; n = 8 best 1-2.

## Source
ideas/search-algorithms.md Tried; STATUS DR6 (LOW-YIELD)
