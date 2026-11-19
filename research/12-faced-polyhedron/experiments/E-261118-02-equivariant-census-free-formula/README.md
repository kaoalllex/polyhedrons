---
id: E-261118-02
title: P3-sym - the census-free formula on symmetric quotients, D2 / S4 eight-face rung before C3 3+3+3 at nine faces
date: 2026-11-18
status: done
concluded: 2026-11-19
verdict: "Rung PASS (D2, S4 known maps unaided in seconds, realized); nine faces UNDERPOWERED@17.0 core-h: C3 3+3+3 at E = 45, 51, 57 UNKNOWN at 1 h"
direction: [DR19, DR7]
origin: [I-261118-01, I-261118-02, I-261103-02, E-261116-07]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Done 2026-11-19 (`CONCLUSION.md`), week item 3, the main investment (`reviews/strategy-review-2026-11-18.md` §1,
> owner-approved 2026-11-18), explore, jump 2. Scores T D F G R: 2 2 2 2 2 | budget: <= 6 core-h before the nine-face
> run, which is <= 17 core-h in one owner run (amendment 1). No proofs. What differs from the parked E-261116-07: an
> opt-in group action on the planes (the parked-methods rule).

## Goal

An opt-in plane action in `p3.Formula` (permutation, orientations transported along orbits, det sign on chi; cells
and all derived variables follow); the default and the stage-A regression stay unchanged. Controls: Roest-Vigh (D2)
and Mizhaev (S4, improper) pinned SAT under their groups, one orbit's signs flipped INFEASIBLE, gauge reachability;
negative: Cs 3 x 2 + 1 at (7, 21) INFEASIBLE if the census marks the (7, 1) class chiral (I-261118-03). Rung (eight
faces, E = 36): D2 2 x 4 and S4 2 x 4 unpinned, 5 workers each, cap 30 min; side unit: plain cube 5 of E-261116-07
with 8 workers, 15 min.

## Next

Kill: a failed control -> repair or park; no rung model -> park with the cause, then week item 6 (E-261117-04). A rung
model realized by the bridge with `--all-pairs` PASS -> C3 3+3+3 at nine faces, E = 45, 51, 57, cap max(3 x rung
time, 1 h), <= 40 core-h, owner run; Cs 4 x 2 + 1 only if C3 decides at all three E. SAT -> bridge, `--all-pairs` nine
faces, `candidate-check`, escalate; UNSAT-SOLVER -> slice closed for planning; UNKNOWN -> UNDERPOWERED, to the lead.
Lab: Opus, high / Codex gpt-6-astra, high.

## Results

Concluded 2026-11-19 (`CONCLUSION.md`): controls pass; the D2 / S4 rung passed in the pilot (Roest-Vigh's and
Mizhaev's maps unaided, realized, `--all-pairs` PASS; known objects). Owner run: C3 3+3+3 at nine faces, E = 45, 51,
57, all UNKNOWN at 1 h on 5 workers; the plain cube 5 UNKNOWN at 15 min on 8 workers. No nine-face model; UNDERPOWERED,
to the lead.
