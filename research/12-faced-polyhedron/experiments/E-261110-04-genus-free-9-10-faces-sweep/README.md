---
id: E-261110-04
title: Genus-free sweep at 9 and 10 planes - every pair adjacent, multiple adjacencies allowed, E free
date: 2026-11-10
status: planned
direction: [DR7, DR18, DR12]
origin: [I-261110-03, I-261110-01, E-261107-01, E-261108-01, E-261110-03]
tests: [H-261110-02]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 1 2, jump 2 | budget: one owner night. **Gated**: only after E-261110-03 names a
> family with a measured rate at 8 planes. Before any compute: `PLAN.md` (skill `experiment-start`).

## Goal

Target T3 of I-261110-03: nine (then ten) mutually adjacent faces at any genus; nothing is in print for nine
(CLAIMED, web search 2026-11-10). The two (9, 3) solid-first sweeps fixed E = 39; this run frees the genus:
E in {45, 51} at nine planes (genus 4, 5), E = 54 at ten (genus 5), by the parity rule E = 3F mod 6.

Families: the E-261110-03 winner carried to 9 and 10 planes; candidates are C3 / D3 with three orbits, 4 wedges + 1
plane, 5 wedges. Inner solver and exact verification as in E-261110-03; first-witness stop.

What is different from the parked (9, 3) arrangement-first runs (E-261107-01, E-261108-01; `ROADMAP.md` parked
methods): E is free instead of 39, and the family arrives with a measured hit rate from the 8-plane rung.

## Next

Stop rule: the night, or the first exact all-pairs solid (`verify_candidate.py --all-pairs`, then `candidate-check`).
A witness is an S1 object at 9 or 10 faces with its genus and multiplicities reported; never S5 unless its genus is
the minimal one, never S0. No witness -> LOW-YIELD at the budget for that family, with the 8-plane rate as the power
statement.
