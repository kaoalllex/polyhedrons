---
id: E-261110-06
title: Normalised S5 (10,4) strata A and B
date: 2026-11-10
status: running
direction: [DR19]
origin: [E-261109-06, E-261108-03, I-261031-02]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Running, exploit, jump 2 (reopened by the owner on 2026-11-14 as week item 2, the second target of `STRATEGY.md`).
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

The superseded cube rule is retained in the git history. The current stop and follow-up rules are in `PLAN.md`.

## Preparation

READY for the owner night; see `CONCLUSION.md` and `results/validation.json`. The experiment remains running pending that night.

Owner entry point (AC power; launch.sh supplies caffeinate):

```sh
bash research/12-faced-polyhedron/overnight/launch.sh 10-06 start
```

Use `status` or `stop` in place of `start`; restart resumes recorded work.
