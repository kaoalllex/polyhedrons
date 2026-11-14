---
id: I-261113-03
title: Rung-below cell census - all eighth-plane cells over seven planes of a known eight-face object as the discovery-power control of the cell method
date: 2026-11-13
status: tried
direction: [DR7, DR18, DR12]
origin: [I-261112-01, E-261112-01]
---

## Idea

Run the ninth-plane method one rung below, where an answer is known: delete one plane of Roest-Vigh (one per
symmetry class), enumerate every generic cell of the eighth plane over the remaining seven, and decide each cell
with the Stage A model at eight faces (28 pairs, edge runs >= 30, genus free). The enumerator must reach the known
object unaided, not through a representative built from the deleted plane. SOLID cells are classed by canonical dual
map and genus.

## Why / cheapest test

Stage A has no positive control at nine planes, so its 2,004 UNSAT-SOLVER verdicts carry no discovery-power
statement (E-261112-01 CONCLUSION); Stage B as queued would repeat that for two nights. The census gives the number
of cells and of distinct maps that the method finds where one object exists. Only the source map -> the family is
rigid and Stage B is parked at this budget; another map -> a new eight-face all-pairs object (a candidate, to
`candidate-check`) and a reason for Stage B. Cheapest test: E-261113-03 (prep, 50 timed cells, then an owner day
run). Untested proposal.

Source: `reviews/strategy-review-2026-11-13.md` §6 (N3); approved by the owner on 2026-11-13.
