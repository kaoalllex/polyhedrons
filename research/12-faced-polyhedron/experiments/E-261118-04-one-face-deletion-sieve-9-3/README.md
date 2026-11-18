---
id: E-261118-04
title: (9, 3) one-face deletion sieve - each admissible map with the planarity of one face dropped, do quasi-polyhedra with one curved face exist?
date: 2026-11-18
status: done
concluded: 2026-11-18
verdict: "OPEN-LOW@1.1 core-h, 2 of 203 maps; map 29 faces 5 and 8 SAT (unrealized), concluded on the pilot (owner)"
direction: [DR19, DR11]
origin: [I-261118-04, I-261101-18, E-261103-03]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned, week item 1 (owner, 2026-11-18: "a separate first item"; `reviews/ideas-triage-2026-11-18.md` §2 Q1),
> explore, jump 0. Scores T D F G R: 1 2 2 1 2 | budget: one session, <= 1 core-h, 10 shards. Before any compute:
> `PLAN.md` (skill `experiment-start`), unit tests run in that commit. No proofs.

## Goal

For each of the 203 admissible (9, 3) maps (E-261103-01) and each of its nine faces: the S5 formula with every
condition on that face's plane removed (8 planes + infinity = 9 elements, kissat, cap 300 s; 1827 formulas up to the
map automorphisms). A model is an OM-level quasi-polyhedron: eight planar faces, the ninth face spanning a skew polygon
whose vertices lie on the lines of its neighbours. The PLAN names the code path (the k-face sub-instance mechanism of
E-261101-23 applied to the S5 encoder of E-261103-02) and its controls: the full formula without deletion reproduces
UNSAT on a few maps (STATUS 3d); the same deletion on Roest-Vigh's (8, 3) map is SAT with Roest-Vigh's own planes
minus one pinned; a deleted formula is a relaxation of the full one (monotonicity on every map).

Run formula (owner, 2026-11-18, `PLAN.md`): plane S kept, the own conditions of F_S dropped (a planar but possibly
defective face S), since deleting plane S leaves almost only GP at (9, 3); the true curved face needs a new encoder
("For the lead").

## Next

Kill: a failed control -> repair. All UNSAT-SOLVER -> the (9, 3) obstruction needs only eight planar faces; no (9, 3)
quasi-polyhedron to straighten (planning only, no checked proof). SAT -> record the models, the bridge realizes the
eight planes, then to the lead: building the skew face and checking its capping (an embedded spanning disk) is a new
step; the non-straightening of such a model is already the UNSAT-VERIFIED full formula of its map. Lab: Opus, medium /
Codex gpt-6.1-sol, medium (a SAT conclusion: Opus, high / gpt-6-astra, high).

## Results

Concluded on the pilot (owner, 2026-11-18; `CONCLUSION.md`): controls pass; map 0 all faces TIMEOUT; map 29 faces 5
and 8 SAT (bridge: unrealized), the other seven UNSAT-SOLVER; the full sieve priced at 40-150 core-h and not run.
