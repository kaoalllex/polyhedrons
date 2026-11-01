---
id: E-261029-12
title: Does any type admit an asymmetric polyhedral immersion?
date: 2026-10-29
status: done
direction: [DR8, DR11]
origin: [I-261029-54, H-261029-06]
tests: [H-261029-06]
produces: []
verdict: OPEN: 8/8 timeouts
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Decide immersion (local conditions only) for asymmetric instances.

## Method

OM-SAT without global clauses, types 0 and 41 in the session; night-1 laptop job `immersion` on types 0-7 (2.2 h each); numerical immersion annealing on types 56-58.

## Results

Simple faces only: SAT (527 s). Simple + reflex: no answer in 25 min; night 1: 8/8 TIMEOUT at 2.17 h (`results/immersion/results.jsonl`). Numerical: >= 12 local violations, always even - explained by the parity theorem (`reviews/fresh-eyes-review.md` 2.2).

## Conclusions

A timeout is no information. Asymmetric immersion instances are not cheaper than embedding instances.

## Next

Needs cube-and-conquer (planned E-261101-15).
