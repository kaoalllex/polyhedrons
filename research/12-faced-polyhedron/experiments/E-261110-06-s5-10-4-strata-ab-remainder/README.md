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

> Planned, conditional. Scores T D F G R: 1 2 2 1 2 (T down from 2: the lead session of 2026-11-10 judges (10, 4) a
> weak proxy for S0, `reviews/strategy-review-2026-11-10.md`) | budget: set by the rule below. Before any compute:
> `PLAN.md` (skill `experiment-start`) and the owner's approval of every night.

## Goal

The 757 admissible (10, 4) maps not yet attempted: strata A (520, pattern `(1^4,2)`) and B (237, pattern `1^6`),
priced at 485 core-h = 6.06 laptop nights by E-261109-06 (STATUS 3ad). Compute is laptop-only (owner, 2026-11-10), so
the Actions branch of the E-261109-06 follow-up tree no longer exists.

## Next

Rule (owner-approved 2026-11-10, replaces "Actions after item 2"):

* Gate: the cube-and-conquer pilot on maps 96 and 85 (week plan item 4; registered by the lab session that runs it).
* The pilot prices A + B at <= 3 laptop nights -> A + B are proposed to the owner as nights of the E-261109-06 design
  with cubes, fastest maps first, first-SAT stop.
* Otherwise -> A + B become one explore night (fastest stratum A maps first, same design, <= 80 core-h), scheduled
  after E-261110-02 and E-261110-04; no further (10, 4) night without a new lead decision.

UNSAT-SOLVER answers stay what they are: they skip a map, they are not a negative result. Stop rule: the first SAT
(then the follow-up tree of E-261109-06), the night's cap, or a failed control.
