---
id: E-261116-01
title: (11, 5) census and cost probe - the last S5 rung below S0, ten normalised formulas at 12 elements
date: 2026-11-16
status: done
concluded: 2026-11-16
verdict: NO-SWEEP-SYMMETRIC-SLICE
direction: [DR19, DR8]
origin: [I-261114-03, E-261103-01, E-261110-06]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Completed, exploit, jump 2. Scores T D F G R: 2 2 2 2 2 | budget: one prep session + <= 10 core-h day run, 10 shards.
> Pre-registered in `PLAN.md`; owner run concluded in `CONCLUSION.md`. No proofs or geometric negative.

## Goal

Week item 1 (`ROADMAP.md`). What does an (11, 5) S5 formula cost with the normalised encoder, and what does that
predict for a sweep of the admissible maps and for S0 (I-261116-03)?

## Preparation

PASS; census reproduction, inherited control provenance, new-size controls and actual-launcher
resume check: `CONCLUSION.md`. The bounded startup fixture is not a price sample.

## Results and next step

The owner run is complete: NO-SWEEP-SYMMETRIC-SLICE, with no SAT or candidate. Cost observations are
NUMERICAL, sampled-formula scope; see `CONCLUSION.md`, `results/run/verdict.json` and `results/run-audit.json`.
The full sweep does not pass the registered gate; only I-261116-04 remains for this target.
E-261116-03 stays parked because its median gate was not met. Week item 2 is next.
