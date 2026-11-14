---
id: E-261114-01
title: Normalised S6 (10, 3) - the twenty sub-map formulas with the reorientation and mirror units
date: 2026-11-14
status: planned
direction: [DR19, DR8]
origin: [I-261114-01, E-261110-02]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, exploit, jump 2. Scores T D F G R: 2 2 2 2 2 | budget: one prep session + <= 20 core-h day run, 10 shards.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 1 (`ROADMAP.md`). Are the twenty `submap=True` formulas of Lutz's (10, 3) maps decided within 3600 s once
`symbreak` and `mirror` are on (E-261110-02 left 20 / 20 at TIMEOUT without them)?

## Next

Prep: (a) exact invariance test of every `ALL_OPTS` clause family under one-element reorientation and under the
mirror on random uniform chirotopes (`omsat.Eval`), with one PROVED-1 paragraph; (b) re-gauged positive controls
pinned SAT (Roest-Vigh, Mizhaev, Szilassi, convex f9 / f10, grooved box, the 16 realized (10, 2) objects) and the 50
(10, 2) maps unpinned SAT; (c) the 2 (8, 2) and 203 (9, 3) formulas with units all UNSAT-SOLVER, ratios on (10, 4)
maps 845, 96, 85; (d) pilot Lutz #1, #2 at 1200 s. Gate: a failed positive control -> one retry with reorientation
units only, then escalate; both pilot units TIMEOUT -> no day run, E-261114-03 first. Run: 20 maps, cap 3600 s,
bridge on every SAT. Follow-up: SAT -> at least 30 models by seed, bridge, `--target S6`, `candidate-check`,
escalate; all UNSAT-SOLVER -> a planning reading, the lead proposes a proof replay; > 20 % TIMEOUT -> E-261114-03.
