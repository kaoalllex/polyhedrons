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

> Scores T D F G R: 2 2 2 1 2. Preparation plus <= 7.3 core-h, 10 shards, laptop day run.
> Owner-approved dialogue, filed 2026-11-12. Planned, not running; the owner explicitly requested no compute.

## Goal / origin

Test the exact near-copy subset of ninth-plane cells for S1 with nine faces and free genus. The approved
[dialogue](../../reviews/dialogue-2026-11-10-strategy.md) supplies the predictions, not registered results.
The new finite list and E >= 39 replace the random fixed-E sweeps; no LOW-YIELD inference is inherited.

## Next

Implement and freeze the list, coverage/orbit checks and runner under [PLAN.md](PLAN.md); then commit the prep
amendment before any pilot. No `run.sh` or launch command is provided until that entry point exists and passes
its bounded startup check. Stage B has a separate gated queue row and is not pre-registered for execution.

## Environment (checked 2026-11-12, no solver call)

From the repository root: `source ~/.venvs/polyhedra/bin/activate`.
Python 3.14.6, macOS arm64; all eight installed versions match `../../requirements.txt`, including
`ortools==9.15.6755`; `python3 -m pip check` reports no broken requirements. OR-Tools native imports,
CpModel constraint construction and CpSolver construction pass;
no `Solve` call, recovery, reinsertion control or target computation was run. The default Homebrew Python has
no OR-Tools. Use this activated environment for preparation and record `pip freeze` in every run manifest.
