---
id: I-261103-04
title: Ninth-plane sweep - add one plane to the Roest-Vigh or Mizhaev arrangement and let the exact inner solver re-select the solid
date: 2026-11-03
status: open
direction: [DR7, DR19]
origin: [E-261030-01, I-261029-27, L:roestvigh2026, L:mizhaev2026]
---

## Idea

The eight planes of each known (8, 3) object already carry a face-neighbourly solid. Add one plane (3 parameters) and ask
the CP-SAT inner solver, extended to 1-3 edge runs per pair (E-261103-05), for a 9-face all-adjacent solid of genus 3 on the
9 planes: the solver re-selects cells, so the 8 doubled pairs of the old object may be traded for the 3 of a (9, 3) map.
Sweep the 3-parameter family on a grid or at random (a minute per position, thousands per night).

## Why it might help

It is a lifting move from a known object, which the 2026-11-01 review said the toolkit lacked for 8 -> 12 faces; for 8 -> 9
faces it exists and is cheap. The arrangement is already structured (D2 or C4 symmetric), which the Wendel estimate
(`reviews/fresh-eyes-review.md` 2.3) says random arrangements are not. CONJECTURE.

## Cheapest test

1,000 random ninth planes on each of the two arrangements, 60 s of CP-SAT each, maximal adjacency recorded: anything above
36 pairs (all adjacent on 9 planes) goes to `candidate-check`; a histogram stuck at <= 28 + (a few) parks the idea with the
numbers.

## Source

Strategy review 2026-11-03 (`reviews/strategy-review-2026-11-03.md` section 4, idea 3).
