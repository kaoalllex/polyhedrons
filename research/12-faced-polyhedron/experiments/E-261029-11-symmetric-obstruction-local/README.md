---
id: E-261029-11
title: Is the symmetric obstruction local (immersion level)?
date: 2026-10-29
status: done
direction: [DR11]
origin: [H-261029-08, I-261029-56, E-261029-04]
tests: [H-261029-08, H-261029-10]
produces: []
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Drop the global no-intersection clauses and see whether symmetric instances stay UNSAT.

## Method

OM-SAT with only local families (simple faces, at most one reflex corner per vertex, orientation consistency).

## Results

#54 T, #3 D3, #45 C3 UNSAT without global clauses (D3: simple faces alone suffice); all 21 C2 and 4 C3 classes UNSAT as immersion instances in the session (68-265 s; no proofs); #48 C2 without simplicity SAT.

## Conclusions

NUMERICAL (no proofs yet): no symmetric polyhedral immersion. Certified on the laptop in E-261029-15.

## Next

DRAT certification (E-261029-15); write-up (planned E-261101-10).
