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
> current stage: conditional failed-level grid registered; startup passes, full grid awaits owner authorization.
> The completed geometric pilot remains UNDERPOWERED. See CONCLUSION / STATUS 3l-3m.
> The night requires a separate committed amendment. What is different from the parked DR1 runs: a new target with
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
stays running. The dated dart-preserving surgery amendment in `PLAN.md` and the
subsequent implementation pass the bounded combinatorial gate. See CONCLUSION.
The saved audit directories are immutable attempts; the runner refuses to overwrite
an existing output directory. A new audit requires a stated reason and a fresh OUT.

## Bounded surgery stage

The surgery amendment was pre-registered in `5725a38`. With the research environment
activated, execute the new stage from the repository root with

```bash
STAGE=surgery bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

The default output is `results/surgery-audit`. The registered controls precede focus
maps. The manifest records the implementation commit and source/input hashes. Saved
chains retain labelled dart data, inverse surgery records and canonical top-map checks.
The original invocation without `STAGE` still selects the legacy representation audit.

## Surgery stage concluded

The registered controls and focus-map scope pass the surgery gate, with claims at
PROVED-1. CONCLUSION and STATUS 3k own the counts, resources and interpretation.
Saved chains and their original manifest are in `results/surgery-audit/`.
`audit.json.gz` losslessly retains the original output. The manifest's `audit.json`
hash applies to its decompressed bytes. Use `audit.py --check-saved PATH` to check
either plain or compressed evidence. The next section records recovery registration.

## Bounded recovery pilot concluded

The geometric amendment was registered in `871d8cc`, implemented in `5643bc5`, and
corrected for reflected reference alignment in `70347ad`. Both attempts remain in
`results/recovery-pilot*`. CONCLUSION / STATUS 3l own outcomes, scope and resources.
The independent checker and report are in `results/recovery-review/`.

With the research environment activated, the actual recovery entry point is

```bash
STAGE=recovery bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

This command refuses to overwrite its existing attempt. It is recorded for
provenance. A repeat requires a committed amendment, a stated reason and a fresh
OUT. The completed pilot leaves the full eight-face recovery gate closed.
The conditional grid is now registered and startup-checked; see the next section.
Focus geometry and a night remain gated.

## Conditional failed-level grid ready (2026-11-04)

PLAN's conditional calibration amendment was committed in `b851f8c`, implementation
in `3f3aeda`. The actual `STARTUP_ONLY=1 STAGE=calibration .../run.sh 0` returned
STARTUP-PASS without optimization. CONCLUSION / STATUS 3m record verification.

The full grid awaits explicit owner authorization under the project's long-run
rule. Once authorized, run from the repository root in the activated research
environment, on AC power with the lid open:

```bash
STAGE=calibration caffeinate -dimsu nice -n 10 bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0
```

Default OUT is `results/recovery-grid`. Existing output is never overwritten.
This bounded calibration is not a night or a focus search. Both conditional PASS
and UNDERPOWERED require conclusion before any new ascent or budget expansion.
