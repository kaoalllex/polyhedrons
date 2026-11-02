---
id: H-261101-15
title: The obstruction is local in faces - every type has an UNSAT sub-instance on at most nine faces
date: 2026-11-01
status: open
origin: [I-261101-18, H-261101-02]
---

## Statement

For every one of the 59 types there is a set of at most nine faces whose k-face sub-instance (GP, normalisations and
the local clause families of those faces only) is UNSAT; the smallest such sets recur across types as the same
sub-map.

## Rival

Every sub-instance with k <= 11 is SAT: an obstruction, if any, needs all twelve faces and is global.

## Evidence so far

None for asymmetric types. For symmetric classes, face simplicity alone is UNSAT in the D3 case (`results.md`), a
hint that few clause families suffice, not that few faces do.

E-261101-23 (night 6, UNDERPOWERED): on the greedy face set (one set per type and k), no UNSAT at k = 8 for the 27
types reached or at k = 9 for the 26 tried; k = 10 timed out everywhere; 32 types not reached (`CONCLUSION.md` of
E-261101-23). Says nothing about other face sets; the hypothesis stays open.

## What would move it

E-261101-23: UNSAT at k <= 9 for a type supports it (and excludes that type, EXACT after drat-trim); all k <= 9
sub-instances SAT on three types weakens it, and their models feed face-CEGAR.
