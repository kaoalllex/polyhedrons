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
Nothing yet on the full 12-face instance of a target type. Benchmark ladder (E-261101-26, 2026-11-02, E-261102-02
settings, `--alt 20`): on two full 12-face genus-3 maps with known realizations, 0/10 seeds each from random planes and
0/10 from genus-2 parents reached an embedding within 40 min. The face ladder realized at most k = 9, and every
failure was cut by the alternation cap, with the SAT calls always fast and SAT. The first 7 / 8 / 9 faces of the
type-15 map: 5/10, 1/10, 1/10. Weakens the "full instance in minutes" part for this configuration; the "small cores" part
holds (`CONCLUSION.md` of E-261101-26).

## What would move it

E-261101-25 pilot: per-call solve times, core sizes, number of releases to the first model, realization success.
