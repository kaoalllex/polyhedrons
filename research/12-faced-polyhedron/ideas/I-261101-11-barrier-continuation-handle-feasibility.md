---
id: I-261101-11
title: Barrier continuation inside a genus-3 realization space towards an in-class handle
date: 2026-11-01
status: open
direction: [DR17, DR3]
origin: [I-261031-05, I-261101-03, E-261030-11, E-261101-07]
---

## Idea

Redo the k-drift with a correct objective and an exact feasibility set. State: 12 planes. Feasible set: the base
genus-3 map M stays exactly EMBEDDED (`ladder_exact.verify` at every accepted step). Objective for a chosen arm
(handle tau with six faces): push the six gauge normals past every open hemisphere, measured by the cosine of the
smallest enclosing spherical cap of the six unit normals (negative once they are not in a hemisphere; computable
exactly from pairs and triples). `gauss_gate.hemisphere_margin` cannot be used: it returns 0 for every
non-hemispheric set (`reviews/strategy-review-2026-11-01.md` 5.1). Keep going until `k_tau = -1`, then decide the
offsets of M + tau exactly at the reached normals and in a small neighbourhood (FD8). Inner loop as in
intersection-free simulation: a log barrier on the float margins of M's forbidden-triple conditions, a line search
that never leaves the feasible set, exact acceptance (Li et al. 2020, IPC).

## Why it might help

The nights-4/5 drift asked `hemisphere_margin` for -0.05, a value it cannot return, so whether in-class normals are
reachable *inside* the realization space of the base object is untested. That question decides H-261101-10: if no
path exists for any of the 40 type-0 and type-53 realizations, handle ladders at a fixed plane set are blocked by
geometry, not by budget; if paths exist, the ladder is alive with the right objective.

## Cheapest test

One type-0 genus-3 realization, arm (0,5,8)-(2,6,7), 1 core-hour; report the margin trajectory and the final
`k_tau`.

## Source

Strategy review 2026-11-01, section 1.3; replaces E-261101-07.
