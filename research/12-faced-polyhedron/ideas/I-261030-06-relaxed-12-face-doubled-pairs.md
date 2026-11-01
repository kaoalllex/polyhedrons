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
