---
id: E-261102-04
title: The genus-ladder search (the engine of the 94 archived genus-3 realizations) scored on the benchmark ladder
date: 2026-11-02
status: done
concluded: 2026-11-03
verdict: "frontier at R4: 0/14 at 40 / 120 min (LOW-YIELD@17.8 core-h for full genus-3 maps from random planes); R5 5/10 at 6 min, 3/5 at 40 min; R1 20/20"
direction: [DR1, DR6]
origin: [E-261101-26, E-261030-10, I-261101-22]
tests: [H-261101-10]
produces: []
preregistered: true
---

> Done 2026-11-03 (night 7, `CONCLUSION.md`; score in `STATUS.md` section 3b). The genus-ladder search realizes
> Szilassi 20/20 and the type-15 genus-3 map from its genus-2 parents in about half the seeds (5/10 at 6 min, 3/5 at
> 40 min, every success within 3 min), and neither full genus-3 map from random planes (0/14). It wins R5 against
> chirotope-first; R4 is now a rung where both scored engines fail.
>
> Planned 2026-11-02 from `../E-261101-26-engine-benchmark-ladder/CONCLUSION.md`; pre-registered in `PLAN.md` (pilot in its Amendments). Scores
> T D F G R: 1 2 2 1 2.

## Goal

A second row of the engine-score table (`STATUS.md` 3b), so the ladder compares engines instead of describing
one. `code/genus_ladder.search` (annealing + CMA-ES on the pair energy, every float zero re-checked exactly) is
the inner search of `archive_climb`, which produced the 94 archived genus-3 realizations from genus-2 parents,
the setting of rung R5. Chirotope-first scored 0/8 on R5 and 0/8 on each R4 map.

## Next

`experiment-start`: an engine option in `ladder.py` (`--engine genus-ladder` calls `genus_ladder.search(links, n,
minutes, rng, seed_planes)`, judged by the same exact judge). Tasks R1, R4 (both maps) and R5 at the E-261101-26
budgets; R6k only if the search accepts a sub-map, stated in the PLAN. A day pilot under the new pilot gate.
The night can be shared with E-261102-03 (cores split between the two through `launch.sh`). Decision: if this
engine beats chirotope-first on R4 / R5, the constructive queue goes through it (with the Gauss gate), and
chirotope-first stays a k-face tool.
