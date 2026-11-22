---
id: E-261117-04
title: P6, the equivelar slice by plain per-map formulas - (8, 3) rung with an enrichment control, (9, 4) census and plain pass
date: 2026-11-17
status: running
direction: [DR19]
origin: [I-261101-15, E-261103-01]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned: the nine-face main line since the owner-approved final lead review 2026-11-22
> (`reviews/strategy-review-2026-11-22-final.md` §3; `ROADMAP.md` week items 1, 3, 4), explore. Scores T D F G R:
> 2 2 2 1 2. Stage A (the (8, 3) rung and the enrichment control on the 790 free-C2 (8, 3) maps) <= 1 core-h, lab-run;
> stage B (the (9, 4) census) price ~4, cap 12 core-h; stage C (the (9, 4) plain pass) price 5-31 core-h, one owner
> night <= 80 core-h, only after A and B pass. Before any compute: `PLAN.md` (skill `experiment-start`). No proofs.

## Goal

`reviews/dialogue-2026-11-16-strategy.md` §2 row 6, Appendix A6. What does the equivelar slice (E = F (F + 1) / 2; at nine faces the eight 2-regular
extra-edge patterns) cost per stage? Stage A at (8, 3): maps enumerated, formulas decided, models sampled, maps
realized, completion flags. It cannot show that Roest-Vigh and Mizhaev are alone.

## Next

Stage A is pre-registered in `PLAN.md` (2026-11-22): `p6.py census`, `p6.py build`, then `run.sh` on 10 shards after the
owner's one-line permission. Stages B and C come as PLAN amendments (week items 3, 4). Coverage: the 2-regular extra-edge multigraphs are disjoint cycles
(a 2-cycle is a pair of multiplicity 3), one input per partition of F into parts >= 2: seven at (8, 3), eight at (9, 4),
fed to `enum_multi.c` directly (not `extra_graphs`, not symcensus with the trivial group). (9, 4) needs the guards
`census.py:154` and `enum_multi.c:186` raised to 9 and a re-read of the coverage argument. Session checks of the
reviews (not ledger): (8, 3) 97 classes, 51 admissible, both known maps in patterns 8 and 4+4; 45 of the 790 free-C2
(8, 3) maps and 111 symmetric (9, 4) codes are equivelar; the plain (9, 4) formula took 1.4-23.4 s on 10 of them
(all UNSAT-SOLVER). Kill: control map absent or pinned control UNSAT after one repair; an unaided recovery timeout is
a bridge diagnosis.
