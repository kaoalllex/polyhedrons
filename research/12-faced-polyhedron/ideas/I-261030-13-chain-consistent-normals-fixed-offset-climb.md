---
id: I-261030-13
title: Chain-consistent normals with offsets-only climb
date: 2026-10-30
status: tried
direction: [DR14]
origin: []
---

## Idea
Find one normal set with k_tau = -1 for every handle of a chain and the right degree at every level, then climb with normals fixed and exact SMT/LP offsets, loosening normals only when UNSAT.

## Why it might help
Removes the type-0 failure mode (k_tau = 0) by construction.

## Cheapest test
Anneal normals for types 0, 11, 24, 58 chains, then solve_gauge level by level.

## Source
ideas/cross-field-ideas.md Round 3, Q1; STATUS DR14 (normals found, sphere UNSAT; feeds DR10)
