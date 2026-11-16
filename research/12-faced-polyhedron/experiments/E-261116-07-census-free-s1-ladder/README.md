---
id: E-261116-07
title: Census-free S1 formula - one OM-SAT instance per (F, g) with tope variables for the solid, ladder pilot
date: 2026-11-16
status: planned
direction: [DR19, DR7, DR18]
origin: [I-261103-02]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, explore, jump 2 via its follow-up. Scores T D F G R: 2 2 1 2 2 | budget: 1-2 sessions + <= 1 core-h;
> a passed ladder earns a <= 20 core-h day run. Before any compute: `PLAN.md` (skill `experiment-start`). No proofs.

## Goal

Week item 2 (`ROADMAP.md`). Can one formula without a given map decide (F, g) at 8 planes in minutes? Ladder: (7, 1)
SAT with Szilassi's chirotope accepted; (8, 3) accepts the Roest-Vigh and Mizhaev chirotopes pinned, then solves
unpinned; (8, 2) UNSAT-SOLVER.

## Next

Kill and follow-up rules in `ROADMAP.md` week item 2. A pass -> (9, 4) and (9, 5), a 10-configuration portfolio on 10
shards; SAT -> bridge, `--all-pairs` with nine faces, `candidate-check`.
