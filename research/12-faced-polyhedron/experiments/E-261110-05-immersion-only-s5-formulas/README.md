---
id: E-261110-05
title: Immersion-only and segment-free formulas on the two (8, 2) maps and six (9, 3) maps - which clause family refutes
date: 2026-11-10
status: running
direction: [DR19, DR11]
origin: [I-261110-04, E-261103-03, E-261109-03]
tests: [H-261110-01]
produces: []
preregistered: true
---

> Running (pre-registered in `PLAN.md`: kissat, no proofs, cap 900 s), explore. Scores T D F G R: 2 2 2 2 2 |
> budget: <= 3 core-h day run, 10 shards.

## Goal

Test (ii) of H-261110-01 on maps whose plain formula is UNSAT-VERIFIED: the two (8, 2) maps and the six (9, 3) maps
of E-261109-03 (40, 43, 10, 30, 48, 5). Two relaxed variants per map (I-261110-04):

* V1 immersion-only: `triples` off, `reflex` / `reflexconsist` / `poc` on (`omsat_sym` / `build`, the S2 option set
  of FD6);
* V2 plain without `SEGMENT_DISJOINT` (a default-off encoder option; default formulas and their CNF hashes must not
  change, checked by the hash tests of `verify_all.py --quick`).

Cap 1800 s per unit; DRAT checked for the (8, 2) units.

## Next

Stop rule: 16 units ended or 3 core-h. Controls: the plain formula of each map rebuilds to its recorded CNF hash; the
pinned positives of E-261103-02 stay SAT under V1 and V2 (both are relaxations).

Reading (decided now): a SAT answer is about the relaxed formula only, never a geometric object. V2 SAT -> the segment
clauses are necessary for the refutation, H-261110-01 supported. V1 UNSAT -> the obstruction is local: one session of
core mining on the (8, 2) formulas (tools of I-261101-02 / E-261101-05). V1 SAT and V2 UNSAT -> the global triples
carry it, H-261110-01 weakened. Follow-up tree: week plan item 5 (`ROADMAP.md`).
