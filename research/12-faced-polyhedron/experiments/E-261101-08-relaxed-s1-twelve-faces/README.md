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
