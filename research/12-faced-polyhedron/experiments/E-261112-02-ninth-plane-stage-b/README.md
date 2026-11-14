---
id: E-261112-02
title: Ninth-plane Stage B - full generic cell lists, Roest-Vigh first
date: 2026-11-12
status: parked
direction: [DR7, DR18, DR12]
origin: [owner, I-261112-01, E-261112-01]
tests: [H-261112-01]
produces: []
preregistered: false
---

> Parked (2026-11-14): the gate E-261113-03 found only the source map (STATUS 3ak); reopened only by a lead decision.
> Scores T D F G R: 2 1 1 1 2 (D down, lead review 2026-11-13: a miss changes nothing). Gated by the rung-below
> census E-261113-03 (owner, 2026-11-13): proposed only if it finds a second map. PLAN and runner are not prepared.
> One prep session, then one owner night per source, Roest-Vigh first, <= 80 core-h per night, 10 shards.

## Goal / gates

Cover all generic open ninth-plane cells of each fixed eight-plane source with the Stage A hard S1 model and
controls. Before a timing run, commit a PLAN: rank-4 enumeration with distinct exact rational representatives,
independent Zaslavsky count, verified symmetry actions and measured orbit sizes. The approved dialogue's full
counts and cost estimates are predictions to reproduce, not a coverage certificate or a night budget.

Time 50 cells under that PLAN and price remaining work, controls and overhead by source. A Stage A miss alone
does not earn Stage B. Require agreement of counts and passing recovery/reinsertion controls. Reuse Stage A
units only by exact representative/formula/provenance match; unfinished orbits carry over by manifest.

## Next / stop

Owner launches each night after these gates; a projected source cost above one night requires an explicit
owner budget decision. Stop on a failed gate, first candidate, completed source or night's cap. No automatic
second night or source. SAT -> exact `--all-pairs` PASS with nine faces and `candidate-check`; UNSAT-SOLVER
never yields a family negative, timeout leaves the unit open. Cell walls and varying the base planes are outside scope.
