---
id: H-261103-03
title: Both (8, 2) candidate maps are UNSAT at the oriented-matroid level - no 8-face genus-2 face-neighbourly polyhedron
date: 2026-11-03
status: supported
origin: [owner, H-261101-07, E-261029-19, L:review2026-11-03]
---

## Statement

The two candidate maps of (8, 2) (8 faces, 20 vertices, 30 edges, one with a tripled pair and face sizes 7^6 9^2, one with
two disjoint doubled pairs and face sizes 7^4 8^4; both chiral with a half-turn automorphism) have no realizable chirotope:
the OM-SAT instances on 9 elements are UNSAT, or every model has a biquadratic final polynomial.

## Rival

One of the two maps realizes: the first face-neighbourly polyhedron of genus 2, with only two extra adjacencies.

## Evidence so far

Black-box engines plateaued at 1-2 violations on n = 8 maps at session budgets (E-261029-19, underpowered: no symmetric
ansatz, no exact decision). The two known 8-face objects needed genus 3 and 8 extra adjacencies, which weakly suggests that
8 faces do not close with 2. Map counts from the review's sampler (H-261103-01).

## What would move it

E-261103-03 (a): two UNSAT-VERIFIED instances support it (PROVED-1 / CERTIFIED after the encoder's soundness write-up); a
realized model refutes it and gives the first genus-2 object.

## 2026-11-04 update

E-261103-03 (8,2) pilot: both plain formulas UNSAT-VERIFIED, retained CNF/DRAT,
checked by drat-trim and replayed in verify_all (EXACT). Conditional geometric exclusion
is PROVED-1, relying on census coverage and encoding/general-position soundness without
human review. See the experiment CONCLUSION. No CERTIFIED theorem or novelty claim.

## 2026-11-04 new-map tranche

E-261103-03 completed its registered bounded coverage tranche (STATUS 3i / CONCLUSION).
EXACT decisions concern saved formulas only; geometric interpretation remains conditional
PROVED-1. No target SAT or geometric candidate. This hypothesis retains its preceding status;
partial coverage and timeouts do not decide existence.

## 2026-11-08 item 5a

E-261103-03 concluded with item 5a, a (9,3) run; the (8,2) evidence is unchanged and this hypothesis is not moved.
