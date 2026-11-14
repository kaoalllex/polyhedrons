---
id: E-261113-03
title: Rung-below cell census - all eighth-plane cells over seven planes of Roest-Vigh, the gate of Stage B
date: 2026-11-13
status: done
direction: [DR7, DR18, DR12]
origin: [I-261113-03, E-261112-01]
tests: [H-261112-01]
produces: []
preregistered: true
verdict: OPEN@15.97 core-h (25,531 cells, 4 SOLID, all with Roest-Vigh's map; 0 open; Stage B parked)
concluded: 2026-11-14
---

> Done (2026-11-14): all 25,531 cells recorded, 25,527 UNSAT-SOLVER, 4 SOLID (both planted cells and one more per
> deletion), every SOLID with Roest-Vigh's map; controls pass; 15.97 core-h. H0 holds: Stage B parked at this budget
> (`CONCLUSION.md`, STATUS 3ak). Scores T D F G R: 2 2 2 1 2.

## Goal

Week item 5 (`ROADMAP.md`), prep only this week. Delete one plane of Roest-Vigh (one per symmetry class of the
planes); enumerate every generic cell of the eighth plane over the remaining seven with distinct exact rational
representatives (rank-4 enumeration, independent Zaslavsky count); decide each cell with the Stage A model at eight
faces (28 pairs, edge runs >= 30, genus free). Time 50 cells and price the run before it is proposed. The
enumerator must reach the known object unaided; SOLID cells are classed by canonical dual map and genus.

## Results / conclusions

Controls 80/80 pass; the planted cells P0, P4 give Roest-Vigh's object unaided. 25,531 / 25,531 cells recorded, mean
2.24 s per cell: 25,527 INFEASIBLE (UNSAT-SOLVER), 4 SOLID (`d0_c08712`, `d0_c03925`, `d4_c04592`, `d4_c09730`), all
with Roest-Vigh's map (genus 3, all 28 pairs), each verified exactly in the worker. No second map: by the registered
reading Stage B (E-261112-02) is parked at this budget. Instance scope; no family negative (`CONCLUSION.md`).

## Next

None in this experiment. The enumerator is kept for the thin-wedge replay and any later Stage B; the lead review
decides the next item.
