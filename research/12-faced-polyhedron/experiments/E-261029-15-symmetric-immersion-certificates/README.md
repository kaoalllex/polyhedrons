---
id: E-261029-15
title: Certify: no symmetric polyhedral immersion (25 classes, DRAT)
date: 2026-10-29
status: done
direction: [DR11]
origin: [E-261029-11]
tests: [H-261029-08, H-261029-10]
produces: [FD6, C:symmetric_drat]
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Certify the session result of E-261029-11.

## Method

Laptop night 2, job `sym --sym-immersion`: local clause families only, CaDiCaL + drat-trim.

## Results

25/25 UNSAT-VERIFIED (7-158 s per case). Records: `results/symimm/results.jsonl`; proofs regenerated and published (E-261101-01).

## Conclusions

EXACT (DRAT-checked); CERTIFIED after the write-up with soundness proofs (planned E-261101-10). As far as we know stronger than the published embedding statement.

## Next

Write-up (planned E-261101-10); human review (planned E-261101-11).
