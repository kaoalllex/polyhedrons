---
id: E-261118-01
title: N1b - the five unrealized face-transitive (8, 3) classes of E-261117-01 by the plain and normalised formulas
date: 2026-11-18
status: planned
direction: [DR19]
origin: [E-261117-01, I-261117-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, week item 1 (`reviews/strategy-review-2026-11-18.md` §1, owner-approved 2026-11-18), exploit, jump 0.
> Scores T D F G R: 2 1 2 1 2 | budget: <= 0.2 core-h, 10 shards. Before any compute: `PLAN.md` (skill
> `experiment-start`). No proofs.

## Goal

E-261117-01 found six face-transitive (8, 3) classes; class 0 is Roest-Vigh's. Is any of the other five SAT at formula
level (9 elements, plain and normalised, kissat, cap 600 s) and realized by the bridge? Controls: Roest-Vigh's class
SAT, Roest-Vigh's planes on another class UNSAT-SOLVER.

## Next

Kill: Roest-Vigh's class not SAT -> stop and repair. SAT, realized, `verify_candidate.py --all-pairs` (eight faces) PASS
-> `candidate-check`, escalate (a third eight-face object, a rung control for E-261118-02). All UNSAT-SOLVER -> no
follow-up. Lab: Opus, medium / Codex gpt-6.1-sol, medium (SAT conclusion: Opus, high / gpt-6-astra, high).
