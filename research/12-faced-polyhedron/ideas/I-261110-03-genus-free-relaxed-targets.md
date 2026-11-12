---
id: I-261110-03
title: Genus-free relaxed targets - every pair of faces adjacent, multiplicities and genus left to the inner solver
date: 2026-11-10
status: open
direction: [DR12, DR7, DR18]
origin: [I-261030-06, I-261030-07, E-261101-08, E-261107-01]
---

## Idea

The two (9, 3) solid-first sweeps (E-261107-01, E-261108-01) fixed E = 39, which is now excluded at formula scope
(STATUS 3d). Free the genus instead: the solid-first inner model (`code/solid_cpsat.best_solid`, the disk-aware
variant of E-261103-05) with all pairs adjacent, 1-3 edge runs per pair and **E free**.

Counting (cubic: V = 2E/3, g = 1 + (E - 3F) / 6, so E = 3F mod 6; elementary):

| F | admissible E beyond the minimal case | genus | extra segments over F (F - 1) / 2 |
|---|---|---|---|
| 8 | 36, 42 (30 is S5 (8, 2), excluded at formula scope) | 3, 4 | 8, 14 |
| 9 | 45, 51 (39 is S5 (9, 3), excluded at formula scope) | 4, 5 | 9, 15 |
| 10 | 54 (48 is S5 (10, 4), the focus sweep) | 5 | 9 |
| 12 | 72, 78 (66 is S0) | 7, 8 | 6, 12 |

So the smallest relaxed 12-face case has **six** extra segments (genus 7), not three: I-261030-06 had it right, the
E-261101-08 row was miscounted (corrected 2026-11-10). Six extra segments make a C3 or D3 orbit of doubled pairs
natural.

Targets, never reported as S0 or S5:

* **T1, relaxed Szilassi-12** (S1 at 12 faces, genus >= 7): the nearest existence result to S0 a laptop can reach.
  FD5 does not apply: it covers the 59 single-adjacency maps only, so symmetric realizations are allowed. Experiment:
  E-261101-08.
* **T3, nine or ten mutually adjacent faces at any genus** (S1 at 9 and 10 faces): nothing is in print for nine
  mutually adjacent faces (CLAIMED, web search 2026-11-10). Experiment: E-261110-04.

Arrangement families: D2 with three 4-orbits (12 planes, 8 parameters); the T-orbit of one plane (12 congruent
faces, 2 parameters, small enough for an exhaustive exact chamber walk); C3 / D3 at 9 planes; wedge-seeded families
(I-261110-01) if E-261110-03 scores them above the others.

## Why it might help

It is what Mizhaev and Roest-Vigh did at 8 faces, and the engine exists and is calibrated (E-261103-05: both (8, 3)
objects recovered from their planes, one from random D2 planes). The S5 constraint "minimal genus" is what the exact
route refuted at 8 and 9 faces; dropping it keeps "every two faces adjacent".

## Cheapest test

E-261110-03 at 8 planes with E free (36 or 42): the family and its hit rate on a rung with known answers. No run on
9, 10 or 12 planes before a family has a measured rate there (`PROTOCOL.md` §8a).

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §3 T1, T3, §4 I-C).
