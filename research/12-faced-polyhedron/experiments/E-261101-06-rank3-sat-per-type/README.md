---
id: E-261101-06
title: Rank-3 (normals-only) SAT per type
date: 2026-11-01
status: planned
direction: [DR9]
origin: [I-261030-29, I-261031-01]
tests: [H-261101-02, H-261101-03]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: 1 day coding, minutes per type. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

A short human-checkable exclusion of a type, or model counts and a split basis for cube-and-conquer.

## Next

Stop rule: per type UNSAT or a model count estimate; stop after 3 types if every one is SAT with no pruning

## Starting point (moved from ROADMAP.md)

Variables: the 220 signs chi(X, Y, Z, inf) in the gauge, kappa bits, vertex-type bits. Clauses: rank-3 GP,
degree -5 at sampled directions, covering, >= 13 saddles, vertex rule F3/F4, face turning F6, face-winding
identity. Controls: Szilassi normals (n = 7) SAT; the 94 genus-3 realizations' normals SAT for their sub-maps;
random normals mostly UNSAT. Outcome: UNSAT for a type = a short human-checkable exclusion (unlikely, decisive);
SAT = model counts and a split basis for E-261101-15.
