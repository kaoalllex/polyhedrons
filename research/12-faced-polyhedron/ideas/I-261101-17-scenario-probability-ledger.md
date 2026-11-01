---
id: I-261101-17
title: An explicit three-scenario credence ledger for the decision point
date: 2026-11-01
status: open
direction: []
origin: []
---

## Idea

Keep three scenarios with current credences in `ROADMAP.md`: (A) a realization exists; (B) all 59 types are
UNSAT at the oriented-matroid level, as in the vertex version; (C) some types are OM-SAT but every model is
non-realizable. Every `PLAN.md` states, before the run, how each outcome moves the three credences (a likelihood
ratio or a sentence); `experiment-conclude` updates the table.

## Why it might help

The decision point (campaign / change the ansatz / stop) is qualitative today. With explicit credences, a cheaper
model can apply the stop rules mechanically, and sunk cost stops driving the queue.

## Cheapest test

Fill the table once from the present evidence (reviewer's starting values: A 0.2, B 0.55, C 0.25, all CONJECTURE)
and update it after E-261101-06 and E-261101-16.

## Source

Strategy review 2026-11-01, section 2 (estimate) and section 6.
