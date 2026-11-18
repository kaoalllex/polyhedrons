---
id: E-261117-02
title: Plane-only symmetry in a moved chart - Szilassi control chain, then the seven-plane C2 3 x 2 + 1 rung
date: 2026-11-17
status: done
concluded: 2026-11-17
verdict: GATE-PASSED
direction: [DR18, DR12]
origin: [I-261117-02, I-261113-04, E-261103-02]
tests: []
produces: []
preregistered: true
---

> Concluded: gate passed. A far plane as infinity makes Szilassi's fixed-face half-turn family uniform; control
> chain and negatives passed; `build_sym`'s orbit gauge is correct, `symbreak` is not (with symmetry clauses). The
> C2 3 x 2 + 1 sampler recovers the Szilassi type unaided, well above the asymmetric baseline; the C2 4 x 2 + 1 arm
> of item 5 is open. 0.94 core-h. Evidence: [CONCLUSION.md](CONCLUSION.md).

## Goal

Week item 2 (`ROADMAP.md`; `reviews/dialogue-2026-11-16-strategy.md` §2 row 2, Appendix A4). Does a generic rational chart disjoint from the solid make
the fixed-face half-turn family uniform, and do plane-only symmetry clauses recover Szilassi?

## Next

Controls in order: exact plane-only determinants of Szilassi; a rational chart missing the whole solid; exact
transformed signs and embedding; the pinned SAT control with the correct gauge (`symbreak` normalises against
infinity: check). Then the seven-plane rung 3 x 2 + 1 on the frozen engine with a far plane as infinity, planted and
unaided recovery apart. A control failure is told apart (zero in the input, clause or gauge, solver). Pass -> the
C2 4 x 2 + 1 arm of week item 5. No speed-up at 12 elements: (11, 5) stays priced out.
