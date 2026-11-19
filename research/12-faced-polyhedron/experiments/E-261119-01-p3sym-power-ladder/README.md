---
id: E-261119-01
title: P3-sym power ladder - discovery and refutation on known answers at the nine-face orbit size, and the symmetric (8, 3) slice by map blocking
date: 2026-11-19
status: planned
direction: [DR19]
origin: [I-261119-02, E-261118-02, I-261118-01]
tests: [H-261101-07]
produces: []
preregistered: false
---

> Planned, week item 1 (`reviews/strategy-review-2026-11-19.md` §1, owner-approved 2026-11-19), explore, jump 0 (its
> pass branch earns a jump-2 night). Scores T D F G R: 2 2 2 1 2 | budget: 1 session + <= 20 core-h, one owner evening.
> Before any compute: `PLAN.md` (skill `experiment-start`) with its unit tests run in that commit. No proofs. What differs
> from E-261118-02: known-answer units at the target's orbit size (the parked-methods rule; a longer cap alone scores D = 0).

## Goal

P3-sym (E-261118-02) unpinned, 5 workers, one seed. U1 free C2 4 x 2 at (8, 36), cap 1.5 h: 66 quad orbits, both known
objects inside; on each model decode, census code, bridge, `--all-pairs`, then block that map (a clause over the
variables that fix its dual map, with all images under the normaliser of the action) and continue. U2 free C2 at
(8, 30), cap 1 h, expected INFEASIBLE ((8, 2) negative, STATUS 3d). U3 C3 3+3+3 at (9, 39), cap 1 h, expected
INFEASIBLE ((9, 3) negative, 3d). U4 D2 and S4 at (8, 36) with blocking, 15 min each, first. Controls: those of
E-261118-02, both known objects pinned under free C2 (orbit-size-2 gauge reachable); blocking control: with
Roest-Vigh's map blocked U1 still returns Mizhaev's, and the reverse.

## Next

A failed control -> repair. U2 or U3 SAT -> stop, bridge: a PASS contradicts 3d (`candidate-check`, escalate), no PASS
means P3 and omsat disagree (lead). U1 model and U2, U3 INFEASIBLE within their caps -> one owner night: C3 3+3+3 at
E = 45, 51, 57, cap max(4 h, 10 x the slowest of these times), <= 60 core-h. U1 model, U3 UNKNOWN -> no C3 night, C3 to
E-261119-02. U1 UNKNOWN -> P3-sym parked for nine faces. A new (8, 3) map realized, `--all-pairs` PASS ->
`candidate-check`, escalate (meets E-261112-02's reopening condition). Blocking ends INFEASIBLE -> "the symmetric
uniform (8, 3) solids have only the known maps", UNSAT-SOLVER (planning). Lab: Opus, high / Codex gpt-6-astra, high.
