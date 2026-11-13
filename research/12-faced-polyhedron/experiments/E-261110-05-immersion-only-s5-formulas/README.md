---
id: E-261110-05
title: Immersion-only and segment-free formulas on the two (8, 2) maps and six (9, 3) maps - which clause family refutes
date: 2026-11-10
status: done
direction: [DR19, DR11]
origin: [I-261110-04, E-261103-03, E-261109-03]
tests: [H-261110-01]
produces: []
preregistered: true
verdict: DONE@0.44 core-h (V2 8/8 UNSAT-SOLVER; V1 (8,2) 2/2 UNSAT-SOLVER, (9,3) 5 SAT + 1 TIMEOUT; no proofs)
concluded: 2026-11-13
---

> Done (2026-11-13): V2 UNSAT-SOLVER on all eight maps; V1 UNSAT-SOLVER at (8, 2), SAT on five (9, 3) maps:
> H-261110-01 weakened; LOCAL at (8, 2) -> core mining (`CONCLUSION.md`, STATUS 3ai).
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
