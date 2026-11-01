---
id: H-261101-06
title: An exact per-type decision costs about 300 core-hours and its proofs can be checked on the fly in 6-hour shards
date: 2026-11-01
status: open
origin: [L:pirozhkov2026]
---

## Statement

An exact per-type decision costs about 300 core-hours (the only data point, CLAIMED: 2 formulas in 648.5 core-h) and
its LRAT proofs can be checked on the fly with a verified checker inside 6-hour Actions shards, keeping only cube
lists, verdicts and hashes. Restated 2026-11-01: the earlier threshold of 2,000 core-h was already met by that data
point; the binding constraints are encoding agreement and proof handling.

## Rival

Cost or proof size is an order of magnitude worse than the pilot suggests, or the two encoders disagree on a
predicate.

## Evidence so far

Third-party pilot: 648.5 core-h for 2 maps (CLAIMED).

## What would move it

E-261101-09 (predicate equality of the two encoders); E-261101-15 (one type on an Actions matrix); E-261101-20
(shared GP lemmas).
