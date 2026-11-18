---
id: E-261117-01
title: Cayley census - face-transitive cubic maps, order-8 rung at (8, 3), then Z9 and Z3 x Z3 at (9, 4), each map decided
date: 2026-11-17
status: done
concluded: 2026-11-17
verdict: NO-ADMISSIBLE-CAYLEY-9-4
direction: [DR19]
origin: [I-261117-01, I-261030-18, E-261103-01]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Concluded: no face-transitive cubic (9, 4) map is admissible (two valid classes, both with repeated vertex
> triples); six classes at (8, 3), Roest-Vigh's among them. Stage B had no input. EXACT, coverage PROVED-1;
> 0.017 core-h. Evidence: [CONCLUSION.md](CONCLUSION.md).

## Goal

Week item 1 (`ROADMAP.md`; `reviews/dialogue-2026-11-16-strategy.md` §2 row 1, Appendix A3). Which face-transitive cubic (9, 4) maps exist (Cayley maps of
Z9 and Z3 x Z3), and is any of them SAT by the plain formula at 10 elements or the free-C3 uniform formula?

## Next

Rung below first: the five groups of order 8, valency 9; Roest-Vigh's map must appear, else bug. Report raw
rotations, valid maps, distinct maps and cost per stage. Empty list or all UNSAT-SOLVER: this slice closed for
planning. SAT -> the bridge, `--all-pairs` with nine faces, `candidate-check`, escalate.
