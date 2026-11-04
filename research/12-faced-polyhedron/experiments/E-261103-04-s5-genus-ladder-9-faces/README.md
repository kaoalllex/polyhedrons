---
id: E-261103-04
title: Genus ladder on 9 faces - the admissible (9, 3) maps from their sphere down and up again (explore)
date: 2026-11-03
status: running
direction: [DR1, DR19]
origin: [E-261103-01, E-261102-04, I-261030-10, H-261101-07]
tests: [H-261101-07, H-261103-02]
produces: []
preregistered: true
---

> Representation audit pre-registered, **explore** (counts towards the one-in-two exploration share of `STRATEGY.md`). Scores T D F G R: 1 2 2 1 2 |
> current stage: the dart-preserving surgery amendment in `PLAN.md`; implementation and its bounded audit are next.
> The geometric pilot and night require a committed amendment. What is different from the parked DR1 runs: a new target with
> genus 3 (below the S0 "ravine" at 3 -> 4), 9 faces (12 free parameters instead of 21), and all pairs adjacent.

## Goal

The cheapest geometric contact with the focus target. For every admissible (9, 3) map: remove handles with `code/tubes.py`
down to a 9-vertex sphere, check that it is a simple triangulation before invoking convex realizability, then climb M0 -> M1 -> M2 -> M3 with
`genus_ladder.search` (the `archive_climb` floor, the engine of E-261102-04) and the exact verifier at every level;
`verify_candidate.py --target S5` on every genus-3 float zero. The engine passes R1 (Szilassi) and R5 (a genus-3 map from
its genus-2 parents, 5/10 at 6 min) and its per-seed outcome is decided in about 3 minutes, so one night covers hundreds of
(map, seed) units; many seeds, short budgets (E-261102-04's lesson).

## Starting point

* Why the S0 evidence does not forbid it: `STRATEGY.md` prefers jumps because of the genus-3 -> 4 ravine; (9, 3) is
  genus 3, and the ladder reaches genus 3 from parents on 12-face maps (`STATUS.md` 3b). R4 (from random planes) is not
  needed: the parents are built by the ladder itself.
* Controls: R1 at the start of the night (20 seeds, must be 20/20); the (8, 3) maps of Roest-Vigh and Mizhaev through the
  same ladder (sphere -> genus 3 with 8 faces, 8 extra adjacencies: do their known realizations get rediscovered? a
  positive control at the target genus with the doubled-adjacency machinery of `ladder_exact.verify`).
* Counters: exact EMBEDDED per level; `pair_energy` is diagnostics only.
* Grid: the budget per level (3 and 10 min) x the seed count, not one setting with many seeds.

## Next

Stop rule: the night, or the first `--target S5` PASS (then `candidate-check`). Outcomes: a PASS is the focus result;
none -> the per-level failure statistics (which level fails, how often the genus-2 parents are reached, whether the (8, 3)
control passes) decide whether the ladder keeps a place on the S5 side (passes the (8, 3) control: one more night with the
other seed kind; fails it: parked for S5 with the failure mode written). Scenario move: a PASS sets the (9, 3) row to
exists; a failed night moves nothing (search failure).

## Activated stage (2026-11-04)

The owner requested continuing on the current local branch, without creating another branch.
`PLAN.md` activates the representation gate only. Run with the research environment activated:

```bash
bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

The original ladder proposal above is subject to this gate. Its triangle-only helpers must
preserve parallel-edge identities before any recovery search. Source inspection suggests
they cannot do so. The audit records the exact scope on the frozen census and controls.

## Representation gate concluded

See `CONCLUSION.md` and `STATUS.md` section 3j for the completed audit, resources,
failed initial attempt and control-orientation correction. The legacy conversion
loses parallel-edge identities (PROVED-1 implementation limitation). The experiment
stays running. The dated dart-preserving surgery amendment in `PLAN.md` specifies
the next implementation and bounded combinatorial audit before geometric work.
The saved audit directories are immutable attempts; the runner refuses to overwrite
an existing output directory. A new audit requires a stated reason and a fresh OUT.
