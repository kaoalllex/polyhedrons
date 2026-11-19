---
id: I-261116-04
title: Symmetric (11, 5) slice - the 24 admissible maps with Aut+ 2 or 3 by symmetric formulas
date: 2026-11-16
status: tried
direction: [DR19]
origin: [I-261114-03, E-261113-01, E-261116-01]
---

## Idea

The (11, 5) census (session check of 2026-11-16) has 24 admissible maps with Aut+ = 2 (20) or 3 (4). Solve their
uniform symmetric formulas as in E-261113-01 (part b): minutes in total.

## Why / cheapest test

The only (11, 5) slice affordable if a full sweep is priced above four nights; a symmetric S5 object would be a
result. Cheapest test: 24 formulas, about one shard-hour. A follow-up of E-261116-01 only. Untested proposal.

Source: `reviews/strategy-review-2026-11-16.md` §5 (N3).

## 2026-11-16 gate

E-261116-01 concludes NO-SWEEP-SYMMETRIC-SLICE (CONCLUSION / STATUS 3aq): this registered follow-up
is eligible. No symmetric formula has been run here; preparation still needs a scored ROADMAP row and
committed PLAN. Week item 2 is next; no new full-sweep budget is implied.

## 2026-11-16b decision

Owner-approved week item 1 (`reviews/strategy-review-2026-11-16b.md`): experiment E-261116-06. Only maps with a free
action are run; a fixed-face involution is outside uniform formulas and is recorded as not decidable here.

## 2026-11-17 dialogue

E-261116-06 withdrawn 2026-11-17: eleven faces admit no free C2 or C3 action (PROVED-1, astra #2), so the registered free-action domain is empty. The four Aut+ = 3 maps have no C3 realization: a face fixed by a rotation lies in a plane perpendicular to the axis, so two fixed faces would be parallel (PROVED-1, `reviews/dialogue-2026-11-16-strategy.md` Appendix A7). The 20 Aut+ = 2 maps whose involution fixes exactly one face return only through N2 (I-261117-02, E-261117-02), as a new registration; no speed-up at 12 elements keeps (11, 5) priced out.

Tried 2026-11-19 (E-261118-03, STATUS 3bc): the 20 Aut+ = 2 maps by plane-only C2 formulas in a moved chart, all
UNSAT-SOLVER (4 seeds each); improper symmetries not run.
