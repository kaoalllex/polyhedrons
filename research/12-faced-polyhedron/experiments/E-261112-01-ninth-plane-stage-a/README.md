---
id: E-261112-01
title: Ninth-plane Stage A - exact near-copy cells over both eight-plane sources
date: 2026-11-12
status: planned
direction: [DR7, DR18, DR12]
origin: [owner, I-261112-01, I-261103-04, I-261110-03, E-261108-01]
tests: [H-261112-01]
produces: []
preregistered: true
---

> Scores T D F G R: 2 2 2 1 2. Preparation plus <= 12 core-h (amendment 2), 10 shards, laptop run.
> Owner-approved dialogue, filed 2026-11-12. Prep amendments 1-2 on 2026-11-12; not launched yet.

## Goal / origin

Test the exact near-copy subset of ninth-plane cells for S1 with nine faces and free genus. The approved
[dialogue](../../reviews/dialogue-2026-11-10-strategy.md) supplies the predictions, not registered results.
The new finite list and E >= 39 replace the random fixed-E sweeps; no LOW-YIELD inference is inherited.

## Next

Prep done ([PLAN.md](PLAN.md) amendments 1-2). Owner, from the research folder, one launch (pilot, automatic pilot
gate, then the rest; about 1-1.5 h on 10 cores): `bash overnight/launch.sh 261112-01 start`; `status` / `stop` as
usual. Exit 6 in a shard = pilot gate stop (owner decision); exit 5 = candidate (run `candidate-check`).
Stage B has a separate gated queue row and is not pre-registered.

## Environment (checked 2026-11-12, no solver call)

From the repository root: `source ~/.venvs/polyhedra/bin/activate`.
Python 3.14.6, macOS arm64; all eight installed versions match `../../requirements.txt`, including
`ortools==9.15.6755`; `python3 -m pip check` reports no broken requirements. OR-Tools native imports,
CpModel constraint construction and CpSolver construction pass;
no `Solve` call, recovery, reinsertion control or target computation was run. The default Homebrew Python has
no OR-Tools. Use this activated environment for preparation and record `pip freeze` in every run manifest.
