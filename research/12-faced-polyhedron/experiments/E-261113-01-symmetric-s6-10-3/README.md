---
id: E-261113-01
title: Symmetric S6 (10, 3) - the tetrahedral family of Lutz #15 and ten symmetric formulas
date: 2026-11-13
status: planned
direction: [DR19, DR8, DR18]
origin: [I-261113-01, E-261110-02, E-261103-02]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, exploit, jump 2. Scores T D F G R: 2 2 2 2 2 | budget: one prep session + <= 10 core-h day run, 10
> shards. Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). No proofs (owner,
> 2026-11-13): every UNSAT is UNSAT-SOLVER.

## Goal

Week item 1 (`ROADMAP.md`). (a) Lutz #15 with the rotation group T: planes `|x| = |y| = |z| = 1` and four planes
`n_i . p = t`; every interval of `t` and every coorientation choice decided by exact arrangement cells and the solid
engine with 42 single adjacencies (the arrangement is not simple; if the engine cannot take it, record that and go
to (b)). (b) `omsat.build(..., sym=...)` with `submap=True`: C3 on Lutz #1, 2, 4, 8, 14, 15 and free C2 on #6, 12,
20 (two involutions), ten formulas, kissat, cap 3600 s. Screening and its scope: I-261113-01.

## Next

Controls: the free-C2 formula of an eight-face source SAT unpinned and realized by the bridge; S0 symmetric CNF
hashes unchanged; a wrong determinant sign UNSAT. Stop rule: all units recorded, a failed control or the cap.
Reading (decided now): SAT -> at least 6 models by seed, bridge, `verify_candidate.py --target S6` at (10, 3),
`candidate-check`, escalate; an OM model alone is not a result. All UNSAT-SOLVER -> a scoped search outcome that
ranks the maps, no exclusion row; a replay with proofs only on the owner's word. More than 20 % timeouts -> escalate.
