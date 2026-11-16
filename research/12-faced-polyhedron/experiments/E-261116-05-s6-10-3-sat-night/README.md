---
id: E-261116-05
title: Normalised S6 (10,3) SAT-oriented owner night
date: 2026-11-16
status: running
direction: [DR19, DR8]
origin: [E-261116-02, E-261114-01]
tests: [H-261110-03]
produces: []
preregistered: true
---

Week item 2 follow-up. READY; owner night pending. No production units run.
Use the existing normalised runner with monolithic `kissat --sat`; reuse the pilot decisions.
Budget, controls, exact scope and follow-up: [PLAN.md](PLAN.md). No proofs.


## Preparation

PLAN pre-registered in `da9a862a`; [CONCLUSION.md](CONCLUSION.md) records gates and limitations.
Frozen queue and reused pilot decisions: `queue.json`, `reused.json`; controls and bounded
launcher stop/resume PASS. Shared runner and launcher fixes are covered by focused checks
and the integrated quick PASS in `results/`. No proof or geometry replay.

On AC with lid open: `bash research/12-faced-polyhedron/overnight/launch.sh 16-05 start`.
Use the same command with `status` or `stop`; restart skips completed maps.
First SAT saves its checked model and stops coverage before the subsequent thirty-model bridge.
