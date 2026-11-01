---
id: E-261101-20
title: One incremental SAT session for the symmetric instances - do shared GP lemmas cut the total time?
date: 2026-11-01
status: planned
direction: [DR8]
origin: [I-261101-12, E-261029-13, E-261029-15]
tests: [H-261101-06]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: a few core-hours in a session. Before any compute: `PLAN.md`
> (skill `experiment-start`).

## Goal

Total solving time of the 25 symmetric embedding instances in one incremental CaDiCaL session with a selector
literal per class, against the recorded sum of separate runs (1,989 s, `E-261029-13/results/sym/results.jsonl`).

## Next

Stop rule: one pass in each of two orders (easy first, hard first). A speed-up below 1.5x closes the idea; above
2x it becomes the default for E-261101-15 and the campaign.

## Starting point

* Build with `omsat.build` once for GP (shared), then add each class's SYM, SB and type-specific clauses with the
  literal not-s_k appended; solve under assumptions [s_k]; pysat `Solver(name='cadical195')` keeps learned clauses.
* Check soundness of the trick on the controls: with all selectors false the formula must be SAT; each UNSAT under
  s_k must be reproduced by the stand-alone instance (same verdict).
* Report: time per class in both orders, total, and the fraction of learned clauses that mention only GP variables.
