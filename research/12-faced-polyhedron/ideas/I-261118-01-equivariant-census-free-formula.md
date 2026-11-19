---
id: I-261118-01
title: Equivariant census-free formula - a group action on the planes of P3 decides all G-symmetric solids of one (F, E) in one formula
date: 2026-11-18
status: tried
direction: [DR19, DR7]
origin: [I-261103-02, E-261116-07, I-261117-02]
---

## Idea

Add the equalities of a plane action (permutation, transported orientations, det sign on chi) to the census-free
formula of E-261116-07. The cells and every derived variable follow. One formula then decides every solid invariant
under G at that (F, E): C3 3+3+3 at nine faces; D2 and S4 2 x 4 at eight faces as the rung with known answers.

## Why it might help

P3 found the K7 map in 8 s at seven faces (70 chirotope signs) and nothing at eight in 560 s per cube. The orbit
counts (`reviews/strategy-review-2026-11-18-orbits.py`, EXACT): C3 on nine faces has 72 orbits of 210 quads, D2 and S4
on eight have 36 and 34 of 126; the cells shrink by the same factor. Both eight-face objects carry a free order-4
group, and Szilassi a half-turn. That CP-SAT presolve merges the equalities is CLAIMED. Untested proposal.

## Cheapest test

E-261118-02's rung: D2 and S4 at eight faces, E = 36, must return Roest-Vigh's and Mizhaev's types unaided in 30 min.

Source: `reviews/strategy-review-2026-11-18.md` §5 N1.

## 2026-11-19 E-261118-02

Rung passed: the D2 and S4 formulas returned Roest-Vigh's and Mizhaev's maps unaided in seconds, both realized (STATUS
3bb). Nine faces: C3 3+3+3 at E = 45, 51, 57 UNKNOWN at 1 h on 5 workers (UNDERPOWERED). The method works one rung
below; whether it reaches nine faces is open (to the lead).
