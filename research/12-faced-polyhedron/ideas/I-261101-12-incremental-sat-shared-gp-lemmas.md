---
id: I-261101-12
title: One incremental SAT session for all types - shared Grassmann-Pluecker lemmas, selector literals per type
date: 2026-11-01
status: open
direction: [DR8]
origin: [I-261031-02, L:pirozhkov2026]
---

## Idea

The 59 asymmetric instances (and the 25 + 25 symmetric ones) share the 411,840 GP clauses; only the link-dependent
families (TRIPLE, SIMPLE, REFLEX1, POC) and SYM differ. Put them in one formula with a selector literal s_t per
type (every type-specific clause gets the literal not-s_t), and solve sequentially under the assumption s_t with
one incremental CaDiCaL. Learned clauses about GP alone persist across types; a refutation under s_t is a DRAT
proof of not-s_t, so certificates stay valid.

## Why it might help

GP reasoning is most of the solver's work. A 2-5x saving over the sum of separate runs changes the campaign's
budget (H-261101-06) and the shape of cube-and-conquer (shared cubes on the rank-3 variables).

## Cheapest test

The 25 symmetric embedding instances in one session versus the recorded separate times (`results/sym/results.jsonl`,
sum 1,989 s); minutes to an hour.

## Source

Strategy review 2026-11-01, section 2 (cube-and-conquer specifics).
