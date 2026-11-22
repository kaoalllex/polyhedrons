---
id: I-261119-03
title: Face-transitive nine-face maps at genus 7 - Cayley maps of Z9 and Z3 x Z3 at valence 14
date: 2026-11-19
status: tried
direction: [DR18]
origin: [owner, I-261117-01, E-261117-01, I-261117-04]
---

## Idea

The owner's idea (root TODO, 2026-11-19): number the faces and edges of known solutions and look for a pattern to
extrapolate to nine faces. Its precise form is the Cayley pattern: faces numbered by a group, every face seeing its
neighbours as the same sequence shifted by its number. Szilassi's map is a Z7 Cayley map (CLAIMED from memory) and
Roest-Vigh's an order-8 one (E-261117-01, EXACT); Mizhaev's is not (two face orbits). At nine faces a face-transitive
cubic map has face degree 2E / 9 = (42 + 12 g) / 9, an integer only at genus 4, 7, 10, ...; E-261117-01 found genus 4
empty (no admissible class). Genus 7 (valence 14, E = 63) is not enumerated.

## Why it might help

A finite, cheap slice that either closes face-transitive nine faces at genus 7 or gives classes for the plain formula
at 10 elements (and for I-261117-04's one-orbit arrangements). Untested proposal; geometric plausibility of 14-gon
faces is low.

## Cheapest test

E-261119-03 (week item 5, optional): N1's two enumerators at valence 14, the plain formula on any admissible class;
<= 1 session. Kill: no admissible class.

Source: `reviews/strategy-review-2026-11-19.md` §5 (owner's raw idea, Q1 kept; Q2 and Q3 dropped; owner-approved 2026-11-19).

## Result (2026-11-22)

Tried in E-261119-03 (STATUS 3bj): no face-transitive cubic (9, 7) map is admissible; with E-261117-01 the slice is
empty at genus 4 and 7 (EXACT, coverage PROVED-1). Genus 10 and beyond not enumerated.
