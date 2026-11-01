---
id: I-261029-59
title: Continuous violation depth instead of a violation count
date: 2026-10-29
status: tried
direction: [DR6]
origin: []
---

## Idea

Sum over violated triples of the smallest distance to a face boundary; zero iff embedded in general position.

## Why it might help

Replaces flat count plateaus with a landscape.

## Cheapest test

CMA-ES / Nelder-Mead, 10 min.

## Source

reviews/fresh-eyes-review.md section 3 #6; tried 2026-10-30 as a depth weight in the ladder energy: no gain (experiment-log).
