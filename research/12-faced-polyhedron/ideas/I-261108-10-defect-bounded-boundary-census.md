---
id: I-261108-10
title: Defect-bounded boundary census - the non-cubic (8, 2) / (9, 3) maps as at most s edge contractions of cubic precursor maps
date: 2026-11-08
status: open
direction: [DR19]
origin: [I-261108-09, E-261103-01]
---

## Idea

Defect identity (review 08e §3, PROVED-1, elementary): for a closed orientable surface with simple disk faces,
distinct face planes, degrees >= 3 and every pair of faces sharing an edge, with C = F (F - 1) / 2, m = E - C and
D = sum over vertices of (deg - 3), Euler and the degree sum give D + m = 3F + 6g - 6 - C =: s. So s = 2, 3, 3, 2, 0 at
(8, 2), (9, 3), (10, 4), (11, 5), (12, 6), and s = 9 at (9, 4). A non-cubic (9, 3) object has at most three exceptional
vertices of degree at most 6; at (8, 2), at most two of degree at most 5.

Generate the non-cubic maps combinatorially: refine each non-triangular dual face by abstract diagonals (D <= s in
total), which gives a cubic precursor map on the same F faces still containing K_F; contracting the dual forests
recovers the map. So the non-cubic maps are the contractions of at most s edges of the full cubic census, inadmissible
maps included. Then decide the surviving maps directly, with the concurrences as equations and their sign
conditions, not with uniform GP clauses on forced-zero minors.

## Why it might help

It closes the non-cubic scope of `STATUS.md` §4 without the geometric perturbation lemma, if I-261108-09 fails its
universal test. Untested: the surviving list may be large, and the concurrence systems may be hard.

## Cheapest test

One session, <= 1 core-h, 8 shards: start with the two (8, 2) precursor maps; enumerate the one- and two-edge
contractions, deduplicate oriented dart maps, check simple face boundaries, vertex links and disk contractions (never
collapse a handle cycle). Coverage control: a square-pyramid map recovered by contracting a split apex. Stop at 1000
distinct maps or the cap (a cost kill, not a non-existence result); a failed round trip stops the enumeration until
coverage is repaired.

## Source

Review `reviews/strategy-review-2026-11-08e.md` §3 (defect identity) and §5; fallback of I-261108-09 (owner
2026-11-08). Not a gate of the cubic note.
