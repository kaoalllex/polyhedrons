---
id: E-261101-08
title: Relaxed S1 target: 12 faces with doubled pairs, symmetric ansatz
date: 2026-11-01
status: planned
direction: [DR12]
origin: [I-261030-06, I-261030-07, E-261030-01, I-261110-03, I-261110-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2, jump 2 (re-scored 2026-11-10, was 1 2 2 1 2) | budget: one night per family.
> **Gated**: after E-261110-03 or E-261110-04 gives a witness. Before any compute: `PLAN.md` from
> `experiments/_template/` (skill `experiment-start`).

## Goal

A new 12-face object with all pairs adjacent and a few multiple pairs: the smallest case has **six** extra segments
and genus 7 (d = 6g - 36; corrected 2026-11-10, this line said "three doubled pairs"), e.g. six doubled pairs as one
D3 orbit or two C3 orbits, or three tripled pairs as one C3 orbit. It is a goal in itself (the first
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
* Then n = 12 with six extra segments (genus 7; corrected 2026-11-10), starting from a spiky tetrahedral core (I-261101-20).

## 2026-11-10: target T1 of I-261110-03 (relaxed Szilassi-12), families and gate

* The first two starting-point items are done: E-261103-05 extended the inner solver to 1-3 runs per pair and
  recovered both (8, 3) objects from their planes and one from random D2 planes (STATUS 3g).
* Genus free (>= 7): E in {72, 78}, not fixed in advance. FD5 covers the 59 single-adjacency maps only, so symmetric
  realizations are allowed here. A witness is S1 at 12 faces; it is never S0.
* Families, one night each: the T-orbit of one plane (12 congruent faces, 2 parameters: an exhaustive exact chamber
  walk instead of sampling); D2 with three 4-orbits (8 parameters); 6 wedges with C3 or D3 symmetry (I-261110-01),
  the last only if E-261110-03 does not park wedge seeding.
* Gate: no 12-plane run before a family has a witness or a measured rate at 8, 9 or 10 planes (E-261110-03, -04).
