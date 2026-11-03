---
id: H-261101-12
title: Some types are SAT at the oriented-matroid level with only non-realizable models
date: 2026-11-01
status: open
origin: [I-261029-57, L:pirozhkov2026, L:schewe2010]
---

## Statement

For at least one of the 59 types the full asymmetric OM-SAT instance is satisfiable, and every model is a
non-realizable chirotope (a final polynomial exists). A certified campaign then needs a realizability stage.

## Rival

All 59 types are UNSAT at the OM level, as in the vertex version (Schewe 2010).

## Evidence so far

Relaxed instances are SAT (C2 #48 without SIMPLE, `reviews/fresh-eyes-review.md` 2.4); two full instances were
refuted by a third party (CLAIMED, `literature/README.md`). Before 2026-11-03 nothing was known on the realizability of any model.

Independent check (2026-11-03): the three exact final polynomials (k-face SAT models of types 0 k = 9, 53 k = 9, 57 k = 8) pass a standard-library checker in `verify_all` (`verification/certificates/final_polynomial/`): three OM-SAT models that are not realizable, EXACT. Each is one model of a sub-instance; nothing says every model of a type is non-realizable.

## What would move it

E-261101-15 on two types; the realizability audit of I-261029-57 on the relaxed models.
