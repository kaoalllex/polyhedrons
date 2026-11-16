---
id: E-261116-02
title: S6 (10, 3) cube pilot - march_cu cubes and a SAT-oriented kissat configuration on Lutz #1 and #2
date: 2026-11-16
status: planned
direction: [DR19, DR8]
origin: [E-261114-01, E-261113-04]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, exploit, jump 2. Scores T D F G R: 1 2 2 1 2 | budget: one prep session + <= 8 core-h day run, 10 shards.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 2 (`ROADMAP.md`). Does a real lookahead cuber or a SAT-oriented configuration decide a normalised (10, 3)
formula that monolithic kissat left at TIMEOUT at 1200 s (E-261114-01)?

## Next

Lutz #1, #2 normalised: march_cu cubes (built by the owner, untried) at a depth giving 100-500 cubes, cube cap 600 s;
in the same day run `kissat --sat` on both at 3600 s. Controls: cube cover (the formula with "no cube holds" is
UNSAT-SOLVER); one SAT (10, 2) map through the same pipeline. Follow-up: a map decided -> one owner night on all 20
by that method, <= 80 core-h; SAT -> 30 models, `--target S6`, `candidate-check`. Neither decided -> park S6 (10, 3)
as solver-limited at laptop scale (OPEN, no negative); no long-cap night unless the owner asks.
