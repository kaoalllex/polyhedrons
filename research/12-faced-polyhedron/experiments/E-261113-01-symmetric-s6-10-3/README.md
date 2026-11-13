---
id: E-261113-01
title: Symmetric S6 (10, 3) - the tetrahedral family of Lutz #15 and ten symmetric formulas
date: 2026-11-13
status: done
direction: [DR19, DR8, DR18]
origin: [I-261113-01, E-261110-02, E-261103-02]
tests: [H-261110-03]
produces: []
preregistered: true
verdict: OPEN@0.034 core-h ((a) 0 EMBEDDED of 816 units; (b) 10/10 UNSAT-SOLVER, 0 SAT, 0 TIMEOUT; no proofs)
concluded: 2026-11-13
---

> Done (2026-11-13): (a) Lutz #15 with rotation group T, 0 EMBEDDED over every equivariant labelling and interval
> of `t` (family scope, reduction PROVED-1); (b) one owner launch, 10 shards, 0.034 core-h: all ten symmetric formulas
> UNSAT-SOLVER in seconds, controls pass. OPEN; no negative claim from (b) (`CONCLUSION.md`). Scores T D F G R:
> 2 2 2 2 2, jump 2.

## Goal

Week item 1 (`ROADMAP.md`). (a) Lutz #15 with the rotation group T: planes `|x| = |y| = |z| = 1` and four planes
`n_i . p = t`; every interval of `t` and every coorientation choice decided by exact arrangement cells and the solid
engine with 42 single adjacencies (the arrangement is not simple; if the engine cannot take it, record that and go
to (b)). (b) `omsat.build(..., sym=...)` with `submap=True`: C3 on Lutz #1, 2, 4, 8, 14, 15 and free C2 on #6, 12,
20 (two involutions), ten formulas, kissat, cap 3600 s. Screening and its scope: I-261113-01.

## Next

None from this experiment: a replay of (b) with proofs only on the owner's word. Week item 2 (E-261113-02) next;
fixed-face C2 (I-261113-04) and improper symmetries are not run. Evidence: `CONCLUSION.md`, `results/a/tetra.json`,
`results/run/` (summary: `python3 summary.py`), prep records in `prep/`, inputs in `maps/` and `queue.json`.
