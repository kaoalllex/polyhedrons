---
id: I-261029-19
title: Homotopy continuation with complex detours
date: 2026-10-29
status: open
direction: [DR17]
origin: [owner]
---

## Idea
Follow paths from a solvable configuration (smooth surface, torus-relaxed) to planar faces with numerical algebraic geometry (Bertini, HomotopyContinuation.jl); paths through C avoid real singularities; use boundary configurations and keep the real solutions.

## Why it might help
Path tracking instead of random search.

## Cheapest test
Boundary configurations (some inequalities made equalities), all complex solutions, keep the real ones.

## Source
ideas/cross-field-ideas.md round 2c, Z2; ideas/search-algorithms.md item 12; round 2f #3
