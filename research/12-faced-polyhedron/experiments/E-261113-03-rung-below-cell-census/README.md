---
id: E-261113-03
title: Rung-below cell census - all eighth-plane cells over seven planes of Roest-Vigh, the gate of Stage B
date: 2026-11-13
status: running
direction: [DR7, DR18, DR12]
origin: [I-261113-03, E-261112-01]
tests: [H-261112-01]
produces: []
preregistered: true
---

> Running (pre-registered 2026-11-13, `PLAN.md`; pilot passed, amendment 1; owner day run pending), explore, control. Scores T D F G R: 2 2 2 1 2 | budget: one prep session, then an owner day run of
> <= 20 core-h, 10 shards.

## Goal

Week item 5 (`ROADMAP.md`), prep only this week. Delete one plane of Roest-Vigh (one per symmetry class of the
planes); enumerate every generic cell of the eighth plane over the remaining seven with distinct exact rational
representatives (rank-4 enumeration, independent Zaslavsky count); decide each cell with the Stage A model at eight
faces (28 pairs, edge runs >= 30, genus free). Time 50 cells and price the run before it is proposed. The
enumerator must reach the known object unaided; SOLID cells are classed by canonical dual map and genus.

## Next

Kill: a count mismatch, or the planted cell is not found (a defect of the enumerator, not a result). Stop rule: all
cells recorded or the cap. Reading (decided now): a SOLID cell whose map differs from the source's -> exact
`verify_candidate.py --all-pairs` at eight faces, `candidate-check`, escalate, and Stage B (E-261112-02) is
proposed to the owner; the source map only -> Stage B is parked at this budget. UNSAT-SOLVER verdicts are never a
family negative. The enumerator is the one Stage B and the thin-wedge replay need.
