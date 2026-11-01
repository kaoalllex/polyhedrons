---
id: H-261029-03
title: At fixed normals, min over offsets of the violation count is a smoother objective; local search on normals with it gets below the 21-24 plateau
date: 2026-10-29
status: open
origin: [owner]
---

## Statement

At fixed normals, min over offsets of the violation count is a smoother objective; local search on normals with it gets below the 21-24 plateau.

## Rival

It plateaus like the joint objective.

## Evidence so far

Joint normals + offsets annealing inside the admissible class reached 22 (sprint board Q1); the exact min-over-offsets objective itself was not tried.

## What would move it

Local search on normals with the exact fixed-normal objective from symmetric near-misses.
