---
id: I-261029-09
title: Rare-event level sampling (subset simulation, Wang-Landau, population annealing)
date: 2026-10-29
status: open
origin: []
---

## Idea
Sample the level sets E <= 20, 15, ..., 0 for a fixed type and labeling with a population (subset simulation, Wang-Landau, parallel tempering, nested sampling).

## Why it might help
Estimates the size of the needle; the level sampler is itself a search.

## Cheapest test
Levels E <= 20, 15, ..., 0 with fastviol.

## Source
ideas/cross-field-ideas.md Y3; ideas/search-algorithms.md item 8
