---
id: E-261119-01
title: P3-sym power ladder - discovery and refutation on known answers at the nine-face orbit size, and the symmetric (8, 3) slice by map blocking
date: 2026-11-19
status: running
direction: [DR19]
origin: [I-261119-02, E-261118-02, I-261118-01]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned, week item 1 (`reviews/strategy-review-2026-11-19.md` §1, owner-approved 2026-11-19; reconciled with the
> Codex second opinion, `reviews/strategy-review-2026-11-19-reconcile.md`, owner-approved the same day), explore,
> jump 0. Scores T D F G R: 2 1 2 1 2 | budget: 1 session + hard <= 20 core-h incl. controls and bridges, one owner evening.
> Before any compute: `PLAN.md` (skill `experiment-start`) with its unit tests run in that commit. No proofs. What differs
> from E-261118-02: known-answer units at the target's orbit size (the parked-methods rule; a longer cap alone scores D = 0).

## Goal

P3-sym (E-261118-02) unpinned, 5 workers, one seed. U1 free C2 4 x 2 at (8, 36), cap 1.5 h: 66 quad orbits, both known
objects inside; on each model decode, census code, bridge, `--all-pairs`, then block that map by its complete paired
runs (one predicate per run on line ij with end triples ijk, ijl; the negated conjunction of its E runs and every image
under the normaliser of the action, 384 for free C2) and continue; a map whose bridge fails stays open. U2 free C2 at
(8, 30), cap 1 h, predicted INFEASIBLE ((8, 2) negative, STATUS 3d). U3 C3 3+3+3 at (9, 39), cap 1 h, predicted
INFEASIBLE ((9, 3) negative, 3d); 3d's checked proofs are for the map CNFs, not for P3. U4 D2 and S4 at (8, 36) with
blocking, 15 min each, first. Controls: those of E-261118-02, both known objects pinned under free C2 (orbit-size-2
gauge reachable); blocking controls: a synthetic unit test (same end triples, different pairing); each known object
pinned with its own map blocked INFEASIBLE, with the other map blocked SAT; unpinned, with Roest-Vigh's map blocked U1
still returns Mizhaev's, and the reverse.

## Next

A failed control -> repair. U2 or U3 SAT -> stop: decode, GP, Euler, darts, census code, action; transport chi into the
3d map CNF and evaluate its clause families; bridge; a PASS -> `--target S5`, `candidate-check`, escalate. U1 UNKNOWN ->
P3-sym parked for nine faces. Otherwise record each unit and go to E-261119-02 (C3 at nine faces per map there). No C3
night from this experiment: one needs a changed nine-plane discovery test (e.g. the planted control of the Codex review
§5) and the owner's word. A new (8, 3) map realized, `--all-pairs` PASS -> `candidate-check`, escalate (meets
E-261112-02's reopening condition). Blocking ends INFEASIBLE -> "this P3-sym free-C2 formula with these blocks is
INFEASIBLE", UNSAT-SOLVER (planning); no claim on maps whose bridge failed. Lab: Opus, high / Codex gpt-6-astra, high.
