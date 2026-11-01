---
id: I-261030-01
title: Spine-seeded solids (thickened graphs of cycle rank 6)
date: 2026-10-30
status: open
direction: [DR14]
origin: [owner]
---

## Idea
Start the solid-first search from a thickened spatial graph of cycle rank 6 (K5, K3,4, cube with diagonal pair, theta-chain, knotted versions) instead of random cells.

## Why it might help
Twisted, branching or knotted tunnels are allowed by the problem but never aimed at.

## Cheapest test
Choose 12 planes approximating the thickened graph, take cells near it as the solid, then CP-SAT + annealing.

## Source
ideas/cross-field-ideas.md round 2e, T1; STATUS DR14
