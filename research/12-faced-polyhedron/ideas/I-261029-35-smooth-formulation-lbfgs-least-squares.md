---
id: I-261029-35
title: Smooth formulation with L-BFGS / Levenberg-Marquardt
date: 2026-10-29
status: open
origin: [owner]
---

## Idea
Variables = vertices + planes, equations = vertices on their three planes (smooth), inequalities as smooth penalties or barriers, LM / L-BFGS from many starts; for fixed normals closure is linear (period_defect.py).

## Why it might help
The current energy is piecewise constant, so gradients need a smooth model.

## Cheapest test
not stated

## Source
ideas/search-algorithms.md To try later, item 4
