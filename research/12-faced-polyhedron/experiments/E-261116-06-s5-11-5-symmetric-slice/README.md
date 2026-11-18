---
id: E-261116-06
title: S5 (11, 5) symmetric slice - free-C2 and free-C3 uniform formulas of the 24 symmetric admissible maps
date: 2026-11-16
status: parked
direction: [DR19]
origin: [I-261116-04, E-261116-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> **Withdrawn 2026-11-17: registered free-action domain empty** (owner; `reviews/dialogue-2026-11-16-strategy.md` §4). Eleven faces admit no
> free C2 or C3 action (PROVED-1, astra #2); the four Aut+ = 3 maps have no C3 realization (two fixed faces would
> be parallel, A7). The Aut+ = 2 maps return only through N2 (E-261117-02), as a new registration. Not run.

> Was: planned, exploit, jump 2. Scores T D F G R: 1 2 2 1 2 | budget: one session + <= 2 core-h, 10 shards.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 1 (`ROADMAP.md`). Is a symmetric (11, 5) formula SAT? The PLAN lists which of the 24 maps (Aut+ 2 or 3,
E-261116-01 census) have a free action; fixed-face involutions are out of scope for uniform formulas.

## Next

Free C2 / C3 positive controls of E-261103-02 through the same runner; cap 3600 s. SAT -> 30 models and the bridge,
`--target S5`, `candidate-check`, escalate. Otherwise (11, 5) closes at laptop scale for this encoder.
