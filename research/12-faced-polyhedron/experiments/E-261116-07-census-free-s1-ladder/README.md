---
id: E-261116-07
title: Census-free S1 formula v2 - one OM-SAT instance per (F, E) with validity-gated cells, eager connectivity, ladder L0-L3 and a bridge gate
date: 2026-11-16
status: planned
direction: [DR19, DR7, DR18]
origin: [I-261103-02]
tests: [H-261101-07]
produces: []
preregistered: false
---

> **Amended 2026-11-17 to specification v2** (owner; `reviews/dialogue-2026-11-16-strategy.md` §2 row 3, §4, Appendix A1), week item 3, the main
> investment. Planned, explore, jump 2 via its tree. Scores T D F G R: 2 2 1 2 2 | budget: 2 sessions, <= 6 core-h
> (L0 0.5, L1-L2 3 of which 2 for (9, 39), L3 2.5). It does not wait for week items 1-2. Before any compute: `PLAN.md`
> (skill `experiment-start`). No proofs; every UNSAT is UNSAT-SOLVER.

## Goal

Can one formula without a given map produce an eight-face all-pairs model that realizes to exact coordinates? v2
replaces the 16b ladder: no tope-circuit block; cells at finite vertices with validity bits; unbounded cells blocked
in both directions at infinity; gauge on chi alone; facet, segment, vertex (`solid_cpsat.ALLOWED` plus no-pinch and
no-diagonal), run and end bits; per-plane Euler disk count and eager connectivity (no lazy cuts). Scope: uniform,
cubic, one disk face per plane.

## Next

Unit tests first (pinch pattern, annulus, disk + annulus; every passing `ALLOWED` pattern has 0 or 3 ends; face-cycle
extraction). Ladder: L0 regression against the frozen engine on K13's archived verdicts, Roest-Vigh, Mizhaev and the
saved uniform perturbation of Szilassi (raw Szilassi rejected as out of domain); L1 (7, 21) SAT; L2 (8, 30) and
(9, 39) UNSAT-SOLVER ((9, 39) undecided in 2 core-h is a budget stop); L3 (8, 36) unpinned, at most 30 distinct
signed chirotopes in the gauge, each through the bridge. Gate: one unpinned model realized to exact coordinates
passing `--all-pairs` at eight faces inside the cap. Decision tree (review §2): topology or control failure -> repair
or park; gate passed -> the nine-face run (E = 45, 51, 57: plain, C3, N2 cube, N3) needs a new budget line from the
lead; models but no bridge and P4 recovers a control -> one capped coupled recovery test at eight faces. SAT at nine
faces -> bridge, `--all-pairs`, `candidate-check`, escalate. Proof obligations: E-261116-09.

> Superseded 16b plan (not run): ladder (7, 1), (8, 3) pinned then unpinned, (8, 2) UNSAT-SOLVER, <= 1 core-h; a pass
> earned a <= 20 core-h day run at (9, 4), (9, 5).
