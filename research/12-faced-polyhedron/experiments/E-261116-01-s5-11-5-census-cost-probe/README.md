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
> Pre-registered in `PLAN.md`; preparation in progress. No proofs.

## Goal

Week item 1 (`ROADMAP.md`). What does an (11, 5) S5 formula cost with the normalised encoder, and what does that
predict for a sweep of the admissible maps and for S0 (I-261116-03)?

## Next

Census: rerun `E-261103-01/census.py 11 5` with its manifest (the lead's session check: 4099 classes, 3986 admissible,
44 s, `reviews/strategy-review-2026-11-16-census-11-5.json`); Euler and admissibility checks, S0 control unchanged.
Controls: the E-261114-01 positive / negative sets plus convex f11 pinned and unpinned. Probe: 10 admissible maps by a
frozen seed, stratified by doubled-pair pattern ([1,1,1,1] 5, [1,1,2] 4, [2,2] 1), kissat, cap 3600 s; bridge and 30
models on any SAT. Output: censored price of the 3986 maps; median time against element count 9-12. Follow-up: price
<= 1 night -> owner night, fastest pattern first; 1-4 nights -> lead; > 4 nights or >= 5 / 10 TIMEOUT -> no sweep, only
I-261116-04. SAT -> 30 models, `--target S5`, `candidate-check`, escalate. Median <= 20 min -> E-261116-03.
Kill: census differs on rerun, a failed control.
