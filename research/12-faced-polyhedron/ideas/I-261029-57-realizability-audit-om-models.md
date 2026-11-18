---
id: I-261029-57
title: Check whether SAT oriented-matroid models of relaxed instances are realizable
date: 2026-10-29
status: open
direction: [DR8]
origin: [L:bokowski2025]
---

## Idea

Fit points or lines to the rank-3 contractions of SAT models (C2 #48 without simplicity; type 0 simple-only) by hinge loss, then the rank-4 configuration.

## Why it might help

Non-realizable models show the OM relaxation is too weak and suggest cheap contraction-realizability clauses; realizable ones give concrete configurations to study.

## Cheapest test

Seconds per contraction.

## Source

reviews/fresh-eyes-review.md section 3 #3.

## 2026-11-17 dialogue

Owner's B2-Q2 (biquadratic final polynomials for unrealized models), `reviews/dialogue-2026-11-16-strategy.md` §3: keep, conditional on a failed bridge (branch 3 of the P3 tree), marks 3 1 2 1 / 3 1 2 1. The project pipeline `verification/certificates/final_polynomial` was not read in the thread (feasibility mark open). No slot this week.
