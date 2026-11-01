---
id: E-261030-08
title: Pilot: normals first and k-targeted drift on type 0
date: 2026-10-30
status: done
direction: [DR2]
origin: [I-261030-24, I-261030-25, E-261030-06, E-261030-07]
tests: [H-261029-09, H-261101-04]
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Move the normals into the next Gauss class, then decide the offsets exactly; or drift the embedded polyhedron until k_tau = -1.

## Method

`code/normals_first.py`, `code/kdrift.py`, positive control `code/nf_control.py`.

## Results

Admissible genus-4 normals reached in under a minute, all offset problems UNSAT; k-drift reached the class for one handle on realizations A and C, always on the class wall (hemisphere margin 0); class seeds in `results/`. Control: the realized map's own offsets are SAT only at radius 0.05, UNSAT at >= 0.1.

## Conclusions

EXACT UNSATs, scoped to their normal sets; the control shows the realization region in normal space is narrow, so UNSATs at larger radii are weak evidence.

## Next

Laptop nights 4-5 (E-261030-11).
