---
id: I-261116-05
title: S6 (10, 3) exclusion at formula scope - a checked proof replay of the twenty normalised Lutz formulas
date: 2026-11-16
status: open
direction: [DR19, DR8]
origin: [E-261116-05, E-261116-02]
---

## Idea

All twenty normalised uniform S6 formulas of Lutz's (10, 3) list are UNSAT-SOLVER (E-261116-02 for #1, #2;
E-261116-05 for #3-#20; STATUS 3ar, 3as), with recorded CNF SHA-256. A checked replay of exactly these CNFs
would make them UNSAT-VERIFIED, the outcome that H-261110-03 names as refuting its (10, 3) part at formula
scope (conditional on the PROVED-1 normalisation soundness, encoder soundness, census coverage and general
position; cubic class only).

## Why / cheapest test

The solves are short (763-2734 s with `kissat --sat`, 7.3 worker-h for eighteen), so a replay is likely about
one owner night, unlike the parked (10, 4) replay (I-261116-02). Cheapest test: rebuild one CNF by hash, solve
it with a proof-producing configuration (LRAT first, as in I-261116-02) and record proof size, check time and
peak memory; gate on the total for twenty fitting one night and the transient disk.

## Status

Proposal only, not run. Proofs are off by default (owner, 2026-11-13): it needs the owner's word and a named
negative claim (a note or a STATUS exclusion) before any plan. Until then the twenty formulas are UNSAT-SOLVER,
planning only.

## 2026-11-16b decision

The owner approved pricing (`reviews/strategy-review-2026-11-16b.md`, approval 3): named claim, paper item D3
(formula-scope exclusion of the twenty S6 (10, 3) formulas). Experiment E-261116-08 prices two CNFs in one session;
the replay night needs its gate (<= 1 night, <= 200 GB transient) and the owner's launch.
