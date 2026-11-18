---
id: E-261117-04
title: Equivelar price pilot - stage A at (8, 3) over the seven extra-edge patterns, costs per stage
date: 2026-11-17
status: planned
direction: [DR19]
origin: [I-261101-15, E-261103-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned (queue, not this week), explore. Scores T D F G R: 1 2 1 1 2 | budget: one session, 1 core-h; stage B
> has no night before a price. Before any compute: `PLAN.md` (skill `experiment-start`). No proofs.

## Goal

`reviews/dialogue-2026-11-16-strategy.md` §2 row 6, Appendix A6. What does the equivelar slice (E = F (F + 1) / 2; at nine faces the eight 2-regular
extra-edge patterns) cost per stage? Stage A at (8, 3): maps enumerated, formulas decided, models sampled, maps
realized, completion flags. It cannot show that Roest-Vigh and Mizhaev are alone.

## Next

Before ranking: the census caps extra edges at 8 (`census.py:154`, `enum_multi.c:186`), (9, 4) needs 9 and a re-read
of the coverage argument. Kill: control map absent or pinned control UNSAT; an unaided recovery timeout is a bridge
diagnosis. Stage B: census inside the joint cap, partial coverage per pattern.
