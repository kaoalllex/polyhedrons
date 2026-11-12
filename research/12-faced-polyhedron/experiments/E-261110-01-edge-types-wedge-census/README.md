---
id: E-261110-01
title: Edge-type tool and wedge census with its null model - exact edge convexity, dihedral angles, wedge covariate
date: 2026-11-10
status: planned
direction: [DR12, DR18]
origin: [I-261110-01, I-261110-07, I-261101-20]
tests: []
produces: []
preregistered: true
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: 1 session, < 0.1 core-h. `PLAN.md` is committed; the run is batched
> with a future approved prep if needed. Deferred 2026-11-12: random-family scoring is replaced by exact cells;
> the tool is optional support for the thin-wedge gate (week item 3), not an active run.

## Goal

A committed tool, `code/edge_types.py`, that computes from (planes, links): exact edge convexity, vertex types,
dihedral angles and the wedge covariate (the largest k with k disjoint pairs under an angle threshold). With it,
re-run the 2026-11-10 session's observation and its null model from committed code
(`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §2). It is the counter calibration of E-261110-03, not a result: a
diagnostic is checked on controls before any phenomenon is named.

## Next

`PLAN.md`. Stop rule: every input and every null-model row computed, or a failed control (then E-261110-03 does not
start). Tests no hypothesis; it checks the two statements of I-261110-07 on data.
