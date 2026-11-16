---
id: E-261116-06
title: S5 (11, 5) symmetric slice - free-C2 and free-C3 uniform formulas of the 24 symmetric admissible maps
date: 2026-11-16
status: planned
direction: [DR19]
origin: [I-261116-04, E-261116-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, exploit, jump 2. Scores T D F G R: 1 2 2 1 2 | budget: one session + <= 2 core-h, 10 shards.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs.

## Goal

Week item 1 (`ROADMAP.md`). Is a symmetric (11, 5) formula SAT? The PLAN lists which of the 24 maps (Aut+ 2 or 3,
E-261116-01 census) have a free action; fixed-face involutions are out of scope for uniform formulas.

## Next

Free C2 / C3 positive controls of E-261103-02 through the same runner; cap 3600 s. SAT -> 30 models and the bridge,
`--target S5`, `candidate-check`, escalate. Otherwise (11, 5) closes at laptop scale for this encoder.
