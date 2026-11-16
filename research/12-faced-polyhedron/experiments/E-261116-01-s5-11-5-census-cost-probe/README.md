---
id: E-261116-01
title: (11, 5) census and cost probe - the last S5 rung below S0, ten normalised formulas at 12 elements
date: 2026-11-16
status: running
direction: [DR19, DR8]
origin: [I-261114-03, E-261103-01, E-261110-06]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned, exploit, jump 2. Scores T D F G R: 2 2 2 2 2 | budget: one prep session + <= 10 core-h day run, 10 shards.
> Pre-registered in `PLAN.md`; preparation passed; ready for owner day run. No proofs.

## Goal

Week item 1 (`ROADMAP.md`). What does an (11, 5) S5 formula cost with the normalised encoder, and what does that
predict for a sweep of the admissible maps and for S0 (I-261116-03)?

## Preparation

PASS; census reproduction, inherited control provenance, new-size controls and actual-launcher
resume check: `CONCLUSION.md`. The bounded startup fixture is not a price sample. No owner run yet.

## Owner run

On AC power, from the repository root (the launcher supplies caffeinate and ten shards):

```sh
bash research/12-faced-polyhedron/overnight/launch.sh 16-01 start
```

Use the same command with `status` or `stop`. After the workers finish, the next lab session runs
`summary.py` and concludes the day stage under the registered follow-up tree. No proofs.
