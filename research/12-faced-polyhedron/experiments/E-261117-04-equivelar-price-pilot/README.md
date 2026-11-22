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

## Stage A results (2026-11-22, PLAN.md; STATUS 3bk)

* **Census (EXACT computation, coverage PROVED-1)**: `results/census_8_3/` (`p6.py census`, 22 s): the seven
  cycle-union inputs complete, 97 classes, all equivelar, 51 admissible. Classes per pattern 8 / 6+2 / 5+3 / 4+4 /
  4+2+2 / 3+3+2 / 2+2+2+2: 43 / 13 / 8 / 21 / 6 / 0 / 6; admissible 12 / 11 / 0 / 16 / 6 / 0 / 6. Every census control
  passed: both known codes (Roest-Vigh 4+4, Mizhaev 8), the six face-transitive classes of 3au and the 45 equivelar
  free-C2 codes present; the admissible classes with a free half-turn are exactly those 45.
* **Formulas** (`maps/stageA.json`, `queue_stageA.json`, `results/stageA/`): 796 of 796 units decided within the 60 s
  cap (max 3.3 s, 367 solver-s). Equivelar: 2 SAT (the two known maps) of 51, 49 UNSAT-SOLVER (the face-transitive
  classes 1-5 among them, as in E-261118-01). Non-equivelar free-C2: 0 SAT of 745, 745 UNSAT-SOLVER. Both SAT models
  realized by the first bridge stage (hinge), `verify_candidate.py --all-pairs` PASS, (V, E, F, chi) =
  (24, 36, 8, -4): the known objects, recovered unaided. No TIMEOUT, no SAT left unrealized: no follow-up queue.
* **Controls**: the pinned Roest-Vigh pair (positive SAT, same-multigraph negative UNSAT-SOLVER) and the runner's
  convex controls passed on all 10 shards; every shard SHARD-COMPLETE.
* **Cost**: 622 core-s on 10 shards (ledger) + 22 s census = 0.18 core-h; ~2.5 min wall (pilot shard 0, then 1-9).
* **Predictions**: P1-P5 all held (P2's first-model realization, 0.5; P3, 0.6).
* **Scope**: plain sub-map formulas in the code's orientation, UNSAT-SOLVER (planning only, no proof). Not shown:
  that the two known solids are the only (8, 3) ones; anything about non-equivelar maps without a free half-turn or
  about the mirror orientation's formulas. Week item 2 has no input (no map of the 790 UNKNOWN or SAT-unrealized).

## Next

Stage A done (above). Stage B, the (9, 4) census (week item 3): PLAN amendment 1 (root-stride units, 30 per
pattern; `p6.py census-b`, `merge`). Coverage: the 2-regular extra-edge multigraphs are disjoint cycles
(a 2-cycle is a pair of multiplicity 3), one input per partition of F into parts >= 2: seven at (8, 3), eight at (9, 4),
fed to `enum_multi.c` directly (not `extra_graphs`, not symcensus with the trivial group). (9, 4) needs the guards
`census.py:154` and `enum_multi.c:186` raised to 9 and a re-read of the coverage argument. Session checks of the
reviews (not ledger): (8, 3) 97 classes, 51 admissible, both known maps in patterns 8 and 4+4; 45 of the 790 free-C2
(8, 3) maps and 111 symmetric (9, 4) codes are equivelar; the plain (9, 4) formula took 1.4-23.4 s on 10 of them
(all UNSAT-SOLVER). Kill: control map absent or pinned control UNSAT after one repair; an unaided recovery timeout is
a bridge diagnosis.
