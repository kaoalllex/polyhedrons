---
id: I-261110-05
title: XOR-aware solving - Gauss-Jordan on the crossing parities, or an order encoding of the triple points along each line
date: 2026-11-10
status: open
direction: [DR19, DR8]
origin: [E-261108-03, I-261031-02]
---

## Idea

The encoder's `IN` predicates are crossing parities: long XOR chains (`code/omsat.py`, `Predicates.IN`), which CDCL
solvers handle badly once they are Tseitin-encoded. Two variants:

1. CryptoMiniSat with Gauss-Jordan elimination on the XOR constraints, against kissat on the same formulas;
2. an order encoding of the triple points along each line L_XY (the "ordered beads" of
   `reviews/brainstorm-2026-11-08.md` item 19) in place of parity.

## Why it might help

E-261108-03 found no 10x among CDCL configurations (best ratio 2.35x); a different treatment of the parity structure
is a different mechanism, not another solver brand. It only matters while a long sweep stays in the plan (the
(10, 4) strata A and B, E-261110-06).

## Cheapest test

Three known (9, 3) maps with recorded kissat times, both variants, same machine. Kill: < 1.5x on all three. Low
priority: no week-plan slot; run it only if the cube-and-conquer pilot keeps strata A and B in the plan.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §4 I-E). Untested.
