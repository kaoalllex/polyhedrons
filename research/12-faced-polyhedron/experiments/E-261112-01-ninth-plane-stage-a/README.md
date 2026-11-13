---
id: E-261112-01
title: Ninth-plane Stage A - exact near-copy cells over both eight-plane sources
date: 2026-11-12
status: done
direction: [DR7, DR18, DR12]
origin: [owner, I-261112-01, I-261103-04, I-261110-03, E-261108-01]
tests: [H-261112-01]
produces: []
preregistered: true
verdict: OPEN@8.01 core-h (Stage A list exhausted, 2,004/2,004 UNSAT-SOLVER, 0 SAT, 0 open; discovery power unmeasured)
concluded: 2026-11-13
---

> Scores T D F G R: 2 2 2 1 2. Preparation plus <= 12 core-h (amendment 2), 10 shards, laptop run.
> Owner-approved dialogue, filed 2026-11-12. Prep amendments 1-2 on 2026-11-12; one launch 2026-11-12/13.

> Concluded 2026-11-13: controls pass in every shard; all 2,004 near-copy cells INFEASIBLE (UNSAT-SOLVER), 0 SOLID,
> 0 open, 8.01 core-h. Instance scope only, no family negative; H-261112-01 stays open ([CONCLUSION.md](CONCLUSION.md)).

## Goal / origin

Test the exact near-copy subset of ninth-plane cells for S1 with nine faces and free genus. The approved
[dialogue](../../reviews/dialogue-2026-11-10-strategy.md) supplies the predictions, not registered results.
The new finite list and E >= 39 replace the random fixed-E sweeps; no LOW-YIELD inference is inherited.

## Next

None in this experiment; see [CONCLUSION.md](CONCLUSION.md). Stage B stays a separately gated queue item.

## Environment (checked 2026-11-12, no solver call)

From the repository root: `source ~/.venvs/polyhedra/bin/activate`.
Python 3.14.6, macOS arm64; all eight installed versions match `../../requirements.txt`, including
`ortools==9.15.6755`; `python3 -m pip check` reports no broken requirements. OR-Tools native imports,
CpModel constraint construction and CpSolver construction pass;
no `Solve` call, recovery, reinsertion control or target computation was run. The default Homebrew Python has
no OR-Tools. Use this activated environment for preparation and record `pip freeze` in every run manifest.
