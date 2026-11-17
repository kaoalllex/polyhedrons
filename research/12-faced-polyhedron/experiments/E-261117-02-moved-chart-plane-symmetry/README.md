---
id: E-261117-02
title: Plane-only symmetry in a moved chart - Szilassi control chain, then the seven-plane C2 3 x 2 + 1 rung
date: 2026-11-17
status: running
direction: [DR18, DR12]
origin: [I-261117-02, I-261113-04, E-261103-02]
tests: []
produces: []
preregistered: true
---

> Planned, explore, jump 0 (a gate of the C2 4 x 2 + 1 arm). Scores T D F G R: 2 2 2 2 2 | budget: one session,
> <= 1 core-h. Before any compute: `PLAN.md` (skill `experiment-start`). No proofs.

## Goal

Week item 2 (`ROADMAP.md`; `reviews/dialogue-2026-11-16-strategy.md` §2 row 2, Appendix A4). Does a generic rational chart disjoint from the solid make
the fixed-face half-turn family uniform, and do plane-only symmetry clauses recover Szilassi?

## Next

Controls in order: exact plane-only determinants of Szilassi; a rational chart missing the whole solid; exact
transformed signs and embedding; the pinned SAT control with the correct gauge (`symbreak` normalises against
infinity: check). Then the seven-plane rung 3 x 2 + 1 on the frozen engine with a far plane as infinity, planted and
unaided recovery apart. A control failure is told apart (zero in the input, clause or gauge, solver). Pass -> the
C2 4 x 2 + 1 arm of week item 5. No speed-up at 12 elements: (11, 5) stays priced out.
