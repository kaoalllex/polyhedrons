---
id: E-261110-06
title: (10, 4) strata A and B remainder - laptop nights only under the cube rule, otherwise one explore night
date: 2026-11-10
status: planned
direction: [DR19]
origin: [E-261109-06, E-261108-03, I-261031-02]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, exploit, jump 2 (reopened by the owner on 2026-11-14 as week item 2, the second target of `STRATEGY.md`).
> Scores T D F G R: 2 2 2 2 2 (lead review 2026-11-14) | budget: one prep session + one owner night <= 80 core-h,
> 10 shards. Before any compute: `PLAN.md` (skill `experiment-start`) and the owner's approval of the night.

## Goal

The 757 admissible (10, 4) maps not yet attempted: strata A (520, pattern `(1^4,2)`) and B (237, pattern `1^6`),
priced at 485 core-h = 6.06 laptop nights by E-261109-06 (STATUS 3ad). Compute is laptop-only (owner, 2026-11-10), so
the Actions branch of the E-261109-06 follow-up tree no longer exists.

## Next

Since 2026-11-14 (`reviews/strategy-review-2026-11-14.md` §2 item 2): the formulas carry the reorientation and mirror
units of E-261114-01, after its soundness controls pass. Prep: the 10 maps of E-261103-07 (10 / 10 TIMEOUT without the
units), cap 1800 s, price the 757 maps. Projected <= 80 core-h -> one owner night, cap 3600 s, bridge on every SAT, no
first-SAT stop; above -> the fastest patterns first inside one night, the rest to the lead. Follow-up: SAT -> 30
models, bridge, `--target S5`, `candidate-check`, escalate; all UNSAT-SOLVER -> the lead proposes a proof replay and the
(11, 5) probe (I-261114-03).

History, the rule of 2026-11-10 (replaced "Actions after item 2"; its gate E-261113-04 ended PARK):

* Gate: the cube-and-conquer pilot on maps 96 and 85 (week plan item 4; registered by the lab session that runs it).
* The pilot prices A + B at <= 3 laptop nights -> A + B are proposed to the owner as nights of the E-261109-06 design
  with cubes, fastest maps first, first-SAT stop.
* Otherwise -> A + B become one explore night (fastest stratum A maps first, same design, <= 80 core-h), scheduled
  after E-261110-02 and E-261110-04; no further (10, 4) night without a new lead decision.

UNSAT-SOLVER answers stay what they are: they skip a map, they are not a negative result. Stop rule: the first SAT
(then the follow-up tree of E-261109-06), the night's cap, or a failed control.
