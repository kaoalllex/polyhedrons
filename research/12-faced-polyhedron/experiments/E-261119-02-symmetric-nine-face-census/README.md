---
id: E-261119-02
title: Symmetric nine-face census - C3 3+3+3 and C2 4 x 2 + 1 maps by lifting the C3 exact cover, then per-map symmetric formulas
date: 2026-11-19
status: planned
direction: [DR19, DR18]
origin: [I-261030-18, I-261119-01, I-261118-02, E-261103-01, E-261118-03]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, week item 2, the main investment (`reviews/strategy-review-2026-11-19.md` §1, owner-approved 2026-11-19),
> explore, jump 2. Scores T D F G R: 2 2 1 2 2 | budget: stage A one session, <= 1 core-h; stage B <= 10 core-h owner
> run, 10 shards. Before any compute: `PLAN.md` (skill `experiment-start`) with its unit tests run in that commit. No proofs.

## Goal

Stage A: generalise `E-261103-01/c3_crosscheck.py` to (9, 4) (three pair orbits, 0, 3 or 6 fixed triangles, any
multiplicity; the code asserts <= 2 now), plus a C2 analogue with one fixed face. Controls: (9, 3) gives exactly the
census's 8 admissible free-C3 classes and its fixed-face involution classes; (7, 1) gives Szilassi's map; free C2 at
(8, 3) gives both known maps. Gate: both (9, 4) lists complete within 1 core-h. Stage B: kissat, cap 600 s; C3 by
omsat's C3 clauses in the standard chart (as for the 8 C3 (9, 3) maps), C2 4 x 2 + 1 plane-only in a moved chart (the
E-261118-03 runner). Rung: both known maps SAT on the free-C2 (8, 3) list, every (9, 3) symmetric formula UNSAT (agrees
with 3d); E-261119-01's U1 and this rung agree map by map.

## Next

SAT -> bridge, `--all-pairs` nine faces, `candidate-check`, escalate. All UNSAT-SOLVER -> genus 5 (E = 51), priced the
same way. Census gate failed -> E-261117-04 (P6). A control failure -> repair. Lab: Opus, high / Codex gpt-6-astra, high.
