---
id: H-261101-17
title: Core-guided SAT under rank-3 assumptions reaches embedding models of the full 12-face instance in minutes
date: 2026-11-01
status: open
origin: [I-261101-21, H-261101-12, H-261101-01]
---

## Statement

For a type with trivial automorphism group, the full OM-SAT instance under the rank-3 assumptions of a Gauss-admissible
seed is decided in seconds to minutes, the cores are small (tens of literals), and after a bounded number of releases
the solver returns a model; some of these models are realizable, giving an S0 polyhedron, or none is, which points at
non-realizable chirotopes (H-261101-12).

## Rival

Under assumptions the instance is as hard as without them (timeouts), or every core is large (the assumptions carry no
information), so the loop degenerates to the unassumed instance.

## Evidence so far

Control at n = 7 passed (E-261101-25 pilot: random planes -> EMBEDDED). Night run 1 (k = 7 sub-instances only,
UNDERPOWERED): cores of tens of literals solved in under a second and small minimal correction sets, in line with the
"small cores" part; most seeds used up the 12-round budget, and no model realized (`CONCLUSION.md` of E-261101-25).
Nothing yet on the full 12-face instance.

## What would move it

E-261101-25 pilot: per-call solve times, core sizes, number of releases to the first model, realization success.
