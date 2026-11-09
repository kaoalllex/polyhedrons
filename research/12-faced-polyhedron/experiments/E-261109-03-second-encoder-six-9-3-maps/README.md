---
id: E-261109-03
title: Second, independently written S5 encoder on six (9, 3) maps and the pinned controls (week item 4, I-261031-03)
date: 2026-11-09
status: running
direction: [DR8, DR19]
origin: [I-261031-03, E-261103-02, E-261103-03]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Audit. Pre-registered in `PLAN.md`. The encoder (`enc2.py`) is written from `theory/mathematical-model.md` section 5
> (Lemma 5.1, side bits, line orders) and the S5 definition, without reading `omsat.py` or `pilot.build`.

## Goal

Do two independently written encoders agree (SAT/UNSAT) on six (9, 3) maps and on the pinned controls? A disagreement
suspends the (9, 3) claim.

## Next

`PLAN.md`: write `enc2.py`, differential test against exact geometry, pilot on map 40, then the six maps in 8 shards.
