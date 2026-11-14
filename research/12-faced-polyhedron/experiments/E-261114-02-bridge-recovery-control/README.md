---
id: E-261114-02
title: Bridge recovery control - exact chirotopes of the 16 realized (10, 2) objects and 30 seeds on five unrealized maps
date: 2026-11-14
status: planned
direction: [DR19]
origin: [I-261114-02, E-261113-02]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, explore, control. Scores T D F G R: 1 2 2 2 2 | budget: < 1 core-h, chained with the prep of E-261114-01.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 3 (`ROADMAP.md`). Does `tranche.bridge` recover a chirotope that is known to be realizable, and how many
models does a map need before one realizes?

## Next

The exact chirotopes of the 16 realized (10, 2) objects of E-261113-02 through the frozen bridge with three
optimizer seeds; 30 solver seeds on five drawn maps that were never realized. Reading (decided now): recovery >= 0.8
-> the bridge is adequate and every target SAT takes at least 30 models; recovery <= 0.3 -> one session on the
realizer before any target SAT is judged; between -> record. Realized objects are controls, never headlines.
