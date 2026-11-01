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
