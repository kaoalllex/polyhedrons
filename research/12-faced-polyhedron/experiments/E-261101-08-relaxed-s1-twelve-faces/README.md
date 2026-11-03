---
id: E-261101-08
title: Relaxed S1 target: 12 faces with doubled pairs, symmetric ansatz
date: 2026-11-01
status: planned
direction: [DR12]
origin: [I-261030-06, I-261030-07, E-261030-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: 2 nights max, <= 25 % of compute. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

A new 12-face object with all pairs adjacent and a few doubled pairs: the smallest case has three doubled pairs and
genus 7 (d = 6g - 36), so one C3 orbit of doubled pairs is the natural ansatz. It is a goal in itself (the first
12-face polyhedron with every pair of faces adjacent), not a route to S0: removing doubled edges is a surgery that
changes the genus, not a continuous move (I-261030-09 parked for that reason).

## Next

Stop rule: calibration on Roest-Vigh fails -> fix the engine, do not run n = 12

## Starting point (2026-11-01)

* `code/solid_cpsat.best_solid` requires at most one edge run per pair of planes, so today it cannot represent any
  S1 object: it would not find Roest-Vigh's or Mizhaev's polyhedron even from their own planes. First task: an
  option allowing two runs per pair (and counting a doubled pair once in the adjacency objective).
* Calibration, in this order, before any 12-face run: (1) `best_solid` with two runs allowed on the 8 Roest-Vigh
  planes (`code/control_rost_vigh.py`) must return all 28 pairs with the 8 doubled ones; (2) the same on Mizhaev's
  planes (`literature/mizhaev2026-planes.json`); (3) the outer search with a D2 two-orbit ansatz from random starts
  must rediscover an 8-face object (Roest-Vigh report that their method did).
* Then n = 12 with a C3 orbit of three doubled pairs (genus 7), starting from a spiky tetrahedral core (I-261101-20).
