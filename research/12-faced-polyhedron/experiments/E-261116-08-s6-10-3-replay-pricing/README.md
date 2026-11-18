---
id: E-261116-08
title: S6 (10, 3) replay pricing - proof size, check time and memory on two of the twenty normalised CNFs
date: 2026-11-16
status: planned
direction: [DR19, DR8]
origin: [I-261116-05, E-261116-05]
tests: [H-261110-03]
produces: []
preregistered: false
---

> Planned, audit, jump 0. Scores T D F G R: 1 2 2 1 2 | budget: one session, <= 2 core-h.
> Owner-approved proofs (2026-11-16b) for the named claim: paper item D3, formula-scope exclusion of the twenty formulas.

## Goal

Week item 4 (`ROADMAP.md`). Rebuild the fastest and slowest CNF by hash; kissat DRAT + drat-trim and CaDiCaL LRAT + a
linear checker; record proof size, check time and peak memory; extrapolate to the twenty.

## Next

<= 1 night and <= 200 GB transient -> an owner replay night (proofs checked during the run and deleted, SHA-256 and
checker transcripts kept); above -> lead.
