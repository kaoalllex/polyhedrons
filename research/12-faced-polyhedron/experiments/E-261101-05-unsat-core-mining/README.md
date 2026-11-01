---
id: E-261101-05
title: Proof mining: small cores of fixed-normal UNSAT instances
date: 2026-11-01
status: planned
direction: [DR10]
origin: [I-261101-02, I-261029-03, E-261030-09, E-261030-11]
tests: [H-261101-02]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: ~5 core-h + theory. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

Minimised cores with ablation of constraint families on the Q1 sphere and the r = 0 drift seeds.

## Next

Stop rule: a core family explained, or 50 cores with no pattern

## Starting point (moved from ROADMAP.md)

Instances: the Q1 sphere (type 58, `experiments/E-261030-09-chain-consistent-normals-q1/results/`) and the 80 r = 0 kdrift seeds
(`experiments/E-261030-11-normals-first-night-runs/results/n5/attempts/kd_*`, `radius: 0.0`). Save every SMT2 instance; extract minimal cores (z3
`unsat_core` with named assertions, then deletion-based minimisation); classify by which constraint families
they use (closure / periods, simplicity, reflex, orientation). **Ablation**: re-solve with each constraint
family switched off in turn (and with weaker / stronger variants) and record which families the contradiction
needs. Report per instance: the exact model, the minimised core, the ablation table, the scope of the conclusion
(`SPEC.md` §4: instance / family / theorem) and possible mathematical consequences. Keep every SMT2 file and
solver output. Outcome: a recurring small core -> state it as a lemma (PROVED-1), test it as a cheap
normal-level filter, add it to the gate; no pattern -> record and stop. The tooling lives in the experiment
folder and is reused by E-261101-04 and any later UNSAT (no generic framework before a first result).
