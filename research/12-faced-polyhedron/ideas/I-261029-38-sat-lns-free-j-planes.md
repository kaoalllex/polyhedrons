---
id: I-261029-38
title: Large neighbourhood search with an exact solver (SAT-LNS)
date: 2026-10-29
status: tried
direction: [DR6]
origin: []
---

## Idea
Free j planes, fix the chirotope on all quadruples avoiding them from a near-miss, and let SAT/CP-SAT decide any extension; j = 1 is exact relocation; UNSAT certifies local optimality; SAT feeds a CEGAR loop.

## Why it might help
Measures how far local structure determines the global problem.

## Cheapest test
j = 1 cross-checks E-PI-1; growth of solve time with j.

## Source
ideas/search-algorithms.md item 9; archive/next-steps.md Cycle 2 #1; STATUS DR6 (LNS, LOW-YIELD)
