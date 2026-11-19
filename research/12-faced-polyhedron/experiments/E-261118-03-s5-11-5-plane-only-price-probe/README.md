---
id: E-261118-03
title: (11, 5) plane-only price probe - the moved-chart C2 formula on two Aut+ = 2 maps against the 12-element median
date: 2026-11-18
status: done
concluded: 2026-11-19
verdict: "Gate NIGHT; proper half-turn slice UNSAT-SOLVER@1.0 core-h: all 20 Aut+ = 2 maps x 4 kissat seeds; (11, 5) closed for the laptop"
direction: [DR19]
origin: [I-261117-02, I-261116-04, E-261117-02, E-261116-01]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Done 2026-11-19 (`CONCLUSION.md`; STATUS 3bc): maps 3634 and 4096 drawn, medians about 41 s (gate NIGHT); the
> follow-up ran the other 18 maps in the session; 80 of 80 units UNSAT-SOLVER, no candidate. Planned, week item 4 (`reviews/strategy-review-2026-11-18.md` §1, owner-approved 2026-11-18), explore, jump 2.
> Scores T D F G R: 1 2 2 1 2 | budget: one session, <= 4 core-h, 8 shards. Before any compute: `PLAN.md` (skill
> `experiment-start`). No proofs.

## Goal

Two of the 20 (11, 5) maps with Aut+ = 2 (the PLAN lists their fixed faces; more than one fixed face is out of
scope): `omsat.build(sym_planes_only=True)` in a moved chart, 4 seeds per map, cap 1800 s, against the 12-element
median of E-261116-01 (>= 3597 s). Kill: the N2 Szilassi control chain fails through the runner.

## Next

Gate: both maps decided with median <= 360 s -> the 20 maps in one owner night (<= 80 core-h); SAT -> bridge,
`--target S5`, `candidate-check`. Otherwise (11, 5) closes for the laptop: no further (11, 5) item. Lab: Opus, medium /
Codex gpt-6.1-sol, high (SAT conclusion: Opus, high / gpt-6-astra, high).
