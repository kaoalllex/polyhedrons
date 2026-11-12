---
id: H-261101-11
title: The symmetric obstructions have cores on at most six faces that recur across classes
date: 2026-11-01
status: open
origin: [I-261101-10, H-261101-02]
---

## Statement

Every certified symmetric UNSAT has a minimal unsatisfiable core whose local clauses involve at most six faces
(with the GP axioms and the symmetry as background), and the same face pattern recurs across the 25 classes.

## Rival

Cores need ten or more faces; the obstruction is global.

## Evidence so far

None. The D3 case (#3) is UNSAT with face simplicity alone (`results.md`), a hint that few families suffice, not
that few faces do.

2026-11-09 (S5, (9, 3), not S0): no one-face contraction core (E-261109-05) and no face-indexed core on <= 7
faces (E-261108-02); the (9, 3) UNSATs look global. Status unchanged.

## What would move it

E-261101-18. A recurring small core also yields the asymmetric sub-instance test described there.
