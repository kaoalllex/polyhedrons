---
id: I-261030-06
title: Relaxed 12-face target with collinear doubled pairs
date: 2026-10-30
status: open
direction: [DR12]
origin: [L:mizhaev2026, L:roestvigh2026]
---

## Idea
Every pair adjacent, d pairs doubled collinear (d = 6 gives genus 7, d = 12 genus 8); not covered by the symmetric UNSAT for the 59 simple maps.

## Why it might help
The 8-face case exists only in this relaxed form; a 12-face analogue would be new.

## Cheapest test
Solid-first CP-SAT with <= 2 collinear edge runs per pair, objective = adjacent pairs (66).

## Source
ideas/cross-field-ideas.md Round 3, L1

## 2026-11-10: count confirmed, genus left free

Cubic counting gives g = 1 + (E - 3F) / 6, so at 12 faces E = 72 (six extra segments, genus 7) is the smallest
relaxed case and E = 78 (twelve, genus 8) the next: the d = 6 and d = 12 of this file. The E-261101-08 row said "three
doubled pairs, genus 7"; that was a miscount and is corrected there. The genus-free form of this target, its 9- and
10-face relatives and the arrangement families are I-261110-03.
