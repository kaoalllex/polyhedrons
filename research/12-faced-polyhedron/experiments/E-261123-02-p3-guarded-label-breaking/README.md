---
id: E-261123-02
title: P3 with guarded face-label symmetry breaking - refutation rungs on the known negatives (8, 30) and (9, 39)
date: 2026-11-23
status: planned
direction: [DR19]
origin: [E-261116-07, I-261123-01]
tests: []
produces: []
preregistered: true
---

> Planned: week item 2 of the owner-approved final lead review 2026-11-23 (`reviews/strategy-review-2026-11-23-final.md`
> §2; `ROADMAP.md` week plan). Explore, J 2 through the tree. Scores T D F G R: 1 2 2 2 2. One prep session + <= 3.0
> core-h. What is different from E-261116-07 (its parked rule): a changed search, static face-label symmetry breaking
> (I-261123-01), measured first on known negatives. Before any compute: `PLAN.md` (skill `experiment-start`).

## Goal

Does guarded label breaking give the census-free formula refutation power: (8, 30) and (9, 39) INFEASIBLE on every one
of their 16 cubes at 225 / 450 s, where E-261116-07 left all of them UNKNOWN (STATUS 3aw)? A pass earns a separately
priced (8, 36) unaided-recovery test, and only after that a (9, 45) price; any UNKNOWN parks this configuration.

## Starting point

* `experiments/E-261116-07-census-free-s1-ladder/p3.py` (CP-SAT; sign gauge and mirror fix, 16 cubes per rung,
  `Formula.block` removes one signed chirotope) and its results as the baseline (reused, not rerun).
* The rule and its soundness argument: `ideas/I-261123-01-guarded-label-symmetry-breaking.md`; regression fixture:
  E-261117-04 `maps/stageA.json` record 51 (unguarded swaps keep none of its 96 size-sorted labellings).
* Cross-review 2026-11-23 check C: two labellings of Roest-Vigh's map share a cube and survive each other's chirotope
  block, so discovery and "nothing else" tests need a whole-map-class blocker with controls.

## Next

The PLAN (lab session, Opus high / Codex gpt-6-astra high), after week item 1 or between its runs.
