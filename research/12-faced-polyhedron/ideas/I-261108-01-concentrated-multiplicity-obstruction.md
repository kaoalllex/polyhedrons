---
id: I-261108-01
title: Concentrated-multiplicity obstruction - a local cause for the fast UNSAT of (9, 3) maps whose extra segments meet at one face
date: 2026-11-08
status: open
direction: [DR19, DR10]
origin: [E-261103-03, H-261101-02]
---

## Idea

In E-261103-03, (9, 3) maps on which the extra edge segments meet at one face (a tripled pair beside a doubled pair, one
face in three doubled pairs, a triangle of doubled pairs) have plain formulas that are UNSAT within 22-76 s (13 of 14
attempted). Maps with spread-out doubled pairs time out (`reviews/strategy-review-2026-11-08.md` §3.1, NUMERICAL).
Look for a local cause on a few faces. One candidate: on the line h_a ∩ h_b of a multiple pair, the endpoints of the
shared segments are vertices (a, b, c) whose c is fixed by the map. So the order of these points along the line is a
rank-2 restriction of the chirotope, and several multiple pairs that share a face constrain each other.

## Why it might help

A human-readable lemma in place of 13 machine refutations. It could prune the 1117 admissible (10, 4) maps (109 have a
tripled pair) before any SAT run. It is the S5 form of H-261101-02 (a short structural obstruction). Untested; the
line-order condition may be implied by weaker clauses and prune nothing new.

## Cheapest test

Face-grouped minimal unsatisfiable cores of the saved plain formulas of the fast maps (ROADMAP week item 3): at most
1 session + 1 core-h. Pass: a core on <= 6 of the 9 faces recurring in >= 3 maps. Then a brute-force line-order check
(7! orders per line) on all 203 maps, which the two (8, 3) maps must pass.

## Source

Strategy review 2026-11-08, §7.1.
