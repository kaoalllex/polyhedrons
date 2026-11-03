---
id: H-261101-16
title: Guided by the Farkas certificate, the normals reach offset-feasible configurations that annealing never found
date: 2026-11-01
status: open
origin: [I-261101-19, E-261030-11, H-261101-09]
---

## Statement

Starting from Gauss-admissible normals whose offset problem is UNSAT, the exact certificate gradient reaches
offset-SAT normals for the sphere level of a chain and for the own level of the 80 radius-0 seeds in a few hundred
steps, where random sampling at radii up to 0.2 found none in 12,202 decisions.

## Rival

The infeasibility landscape over the normals is flat or chaotic (H-261101-09's thinness); the gradient oscillates
between cells and never reaches SAT.

## Evidence so far

None. The period-defect annealing of night 2 decreased a float defect slowly (17.6 -> 8.5 in 1.5 h) but never to 0.

## What would move it

E-261101-24: a monotone decrease with SATs on the positive control and on some seeds supports it; oscillation
without SAT on the control means the engine is wrong, on the seeds alone it weakens the hypothesis.
