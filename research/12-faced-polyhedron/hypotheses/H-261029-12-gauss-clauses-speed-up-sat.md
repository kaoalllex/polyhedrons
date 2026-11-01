---
id: H-261029-12
title: Adding Gauss clauses (degree, covering) to OM-SAT speeds up the symmetric certificate instances at least 3x
date: 2026-10-29
status: weakened
origin: [owner]
---

## Statement

Adding Gauss clauses (degree, covering) to OM-SAT speeds up the symmetric certificate instances at least 3x.

## Rival

The clauses are implied and easy for the solver to derive; no speed-up.

## Evidence so far

Lutz #48 C2, same machine and load: UNSAT 91.8 s without, 99.7 s with k = 2, 98.3 s with k = 4 directions (one instance, NUMERICAL timing).

## What would move it

A speed-up on other instance families (asymmetric cubes) would revive it.
