---
id: E-261110-03
title: Arrangement-family scoring at the 8-plane rung with the wedge covariate - four families, all 28 pairs, E free
date: 2026-11-10
status: parked
direction: [DR7, DR18, DR12]
origin: [I-261110-01, I-261110-03, E-261103-05, E-261110-01]
tests: [H-261110-02]
produces: []
preregistered: false
---

> Parked by the owner, 2026-11-12; not run. Replaced by E-261112-01/02 (exact ninth-plane cells).
> Historical proposal below is retained, not an active launch instruction. Recovery alone did not establish
> discovery power. No hypothesis change or negative result; future sampling needs a new power statement and PLAN.

## Goal

The benchmark-ladder rule of `PROTOCOL.md` §8a applied to samplers: score an arrangement family on a rung with known
answers before it is used on a target. Four families of 8 planes, 200 arrangements each:

1. isotropic `random_planes`;
2. D2 with two 4-orbits (the family of E-261103-05: 1 SOLID in its first 5 seeds, which is not a rate);
3. wedge-seeded isotropic: four pairs at 10-40 degrees, random mid-planes and rims;
4. wedge-seeded D2.

Inner solver: the disk-aware CP-SAT model of E-261103-05 with all 28 pairs adjacent and E free (36 or 42; E = 30 is
S5 (8, 2), excluded at formula scope). Per arrangement: `wedge_planes` (E-261110-01) and the outcome; every SOLID
goes through the exact verifier. Report the rate per family and, inside each family, the rate with and without four
disjoint pairs <= 25 degrees.

## Next

Stop rule: 800 arrangements decided or 3 core-h. Controls: the Roest-Vigh and Mizhaev planes must return their
objects (R2 of E-261103-05); a tetrahedron-type negative must be INFEASIBLE.

Kill for I-261110-01 / H-261110-02: ratio < 2 inside every family, with >= 10 positives in total. Fewer than 10
positives in total -> UNDERPOWERED, recorded, escalate. The family with the most positives per core-second seeds
E-261110-04. Follow-up tree: week plan item 3 (`ROADMAP.md`).

## Starting point (2026-11-10)

* Generic `solid` job for `overnight/run_overnight.py`: an arrangement generator plugin (random, wedges(m, angle
  range), orbit(G, params)) x `solid_cpsat.best_solid` with E free and all pairs adjacent; SAT -> exact verify ->
  CANDIDATE. Build it from the workers of E-261107-01 (`nine.py`) and E-261108-01 (`sweep.py`); do not write a new
  launcher.
* The PLAN fixes the seeds, the per-arrangement cap and the meaning of a cap hit (UNKNOWN, never INFEASIBLE).
* An (8, 3) or (8, 4) solid found here is an auxiliary S1 object and an engine calibration, not a focus witness;
  `candidate-check` still applies before any wording.
