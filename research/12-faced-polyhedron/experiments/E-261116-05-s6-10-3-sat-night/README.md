---
id: E-261116-05
title: Normalised S6 (10,3) SAT-oriented owner night
date: 2026-11-16
status: done
concluded: 2026-11-16
verdict: ALL-20-DECIDED-UNSAT-SOLVER
direction: [DR19, DR8]
origin: [E-261116-02, E-261114-01]
tests: [H-261110-03]
produces: []
preregistered: true
---

> Concluded: all twenty normalised Lutz (10,3) formulas UNSAT-SOLVER (18 fresh, #1/#2 reused);
> no candidate, no checked proof, no geometric negative. Evidence: [CONCLUSION.md](CONCLUSION.md).

## Result and next step

One owner launch, ten shards, well inside the budget; every map decided inside its cap.
Fresh CNF-hash, log, provenance and budget audit PASS (`results/run-audit.json`). Planning only:
S6 (10,3) by these formulas is exhausted at solver level; a checked replay is idea I-261116-05,
on the owner's word. H-261110-03 and credences unchanged. Week item 5 next.

Week item 2 follow-up; budget, controls, exact scope and follow-up: [PLAN.md](PLAN.md). No proofs.


## Preparation

PLAN pre-registered in `da9a862a`; [CONCLUSION.md](CONCLUSION.md) records gates and limitations.
Frozen queue and reused pilot decisions: `queue.json`, `reused.json`; controls and bounded
launcher stop/resume PASS. Shared runner and launcher fixes are covered by focused checks
and the integrated quick PASS in `results/`. No proof or geometry replay.

On AC with lid open: `bash research/12-faced-polyhedron/overnight/launch.sh 16-05 start`.
Use the same command with `status` or `stop`; restart skips completed maps.
First SAT saves its checked model and stops coverage before the subsequent thirty-model bridge.
