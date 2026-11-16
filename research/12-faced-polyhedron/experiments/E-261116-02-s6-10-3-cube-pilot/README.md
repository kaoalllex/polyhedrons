---
id: E-261116-02
title: S6 (10, 3) cube pilot - march_cu cubes and a SAT-oriented kissat configuration on Lutz #1 and #2
date: 2026-11-16
status: running
direction: [DR19, DR8]
origin: [E-261114-01, E-261113-04]
tests: [H-261110-03]
produces: []
preregistered: true
---

> Planned, exploit, jump 2. Scores T D F G R: 1 2 2 1 2 | budget: one prep session + <= 8 core-h day run, 10 shards.
> Pre-registered in `46784cbc`; preparation passed. Owner day launch pending. No proofs.

## Goal

Week item 2 (`ROADMAP.md`). Does a real lookahead cuber or a SAT-oriented configuration decide a normalised (10, 3)
formula that monolithic kissat left at TIMEOUT at 1200 s (E-261114-01)?

## Next

Lutz #1, #2 normalised: march_cu cubes (built by the owner, untried) at a depth giving 100-500 cubes, cube cap 600 s;
in the same day run `kissat --sat` on both at 3600 s. Controls: cube cover (the formula with "no cube holds" is
UNSAT-SOLVER); one SAT (10, 2) map through the same pipeline. Follow-up: a map decided -> one owner night on all 20
by that method, <= 80 core-h; SAT -> 30 models, `--target S6`, `candidate-check`. Neither decided -> park S6 (10, 3)
as solver-limited at laptop scale (OPEN, no negative); no long-cap night unless the owner asks.

## Preparation (2026-11-16)

NUMERICAL timing, SPEC section 4 instance scope; no target decision or new candidate.
`results/prep/summary.json`: positive pipeline and target cube-cover gates PASS.
Selected partitions and counts are frozen there; `results/sat-config/result.json`
checks the SAT-oriented option on the same known-SAT control.
`results/startup-check.json`: bounded launcher check, ten shards, no solver units.
`verify_all.py --quick`: ALL PASS (archive skipped); trace: zero errors.
The solver-unit resume path has not been exercised through a stop/restart.
Launch on AC: `bash research/12-faced-polyhedron/overnight/launch.sh 16-02 start`;
use the same command with `status` or `stop`. The launcher supplies caffeinate.

The runner reserves the two monolithic allocations before dispatching cube work;
unfinished killed attempts keep their reservations. A budget stop leaves unresolved
cubes OPEN. Target SAT stops dispatch and preserves its checked assignment;
the registered thirty-model bridge is a subsequent stage, before any witness claim.
