---
id: E-261103-03
title: Exact decision per candidate map - OM-SAT for the 2 (8, 2) maps, then the symmetric and all admissible (9, 3) maps
date: 2026-11-03
status: planned
direction: [DR19, DR8]
origin: [E-261103-01, E-261103-02, I-261030-31, I-261029-45, I-261029-57, H-261101-07]
tests: [H-261103-03, H-261103-02, H-261101-07]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: hours for (8, 2); one laptop night (10 cores) for (9, 3). Before any
> compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`). Blocked by E-261103-01 (the maps) and
> E-261103-02 (the encoder). Third item of the queue (`reviews/strategy-review-2026-11-03.md` section 2.2 item 1 and 3.3).

## Goal

Decide the focus and warm-up cases exactly, map by map. Order: (a) the 2 (8, 2) maps (9 elements, 126 bases), plain and
with the C2 clauses; (b) the 8 admissible (9, 3) maps with a free order-3 automorphism (10 elements, 210 bases) with C3
clauses, the 2 of them with |Aut+| = 6 also with D3 clauses; (c) the 24 maps with an involution, with C2 clauses; (d) all
203 admissible (9, 3) maps without symmetry. Every SAT model goes to the two realizers (hinge and two-stage, at F planes)
and, if unrealized, to the final-polynomial LP (120-s limit, certificate stored, independent checker in
`verification/certificates/final_polynomial/`). Every UNSAT keeps CNF and DRAT (drat-trim). A realized model is a CANDIDATE
until `verify_candidate.py --target S5` passes and `candidate-check` is run.

## Starting point

* The (8, 2) decision alone is a result either way: an object is the first genus-2 face-neighbourly polyhedron; two
  UNSAT-VERIFIED instances are the first non-existence theorem for a face-neighbourly case (CERTIFIED after the soundness
  write-up of the encoder, PROVED-1 until then).
* Positive control inside the run: the Roest-Vigh and Mizhaev instances (their maps, 8 planes) are SAT and their models
  realize (the realizer at 8 planes must recover an embedded object from a model; this is the k-face realizer control the
  S0 runs never had). Negative control: the 37 non-admissible (9, 3) maps are rejected before solving or are UNSAT.
* Counter calibration: the only counters are SAT / UNSAT-VERIFIED / realized (exact) / NONREALIZABLE-EXACT / LP-TIMEOUT /
  TIMEOUT; no float verdict.
* Power statement to write in the PLAN: the per-map SAT time at 10 elements on the symmetric instances first; if the median
  exceeds about an hour, (d) does not run as one night and the row is re-planned (cube-and-conquer on the rank-3 signs, or
  the symmetric subset only).

## Next

Stop rule: every map in (a)-(d) decided (UNSAT-VERIFIED, realized, NONREALIZABLE-EXACT, or a listed timeout), or the
median SAT time bound above. Outcomes: a realized (9, 3) model -> `candidate-check`, the focus result; a realized (8, 2)
model -> same, and (9, 3) continues; all (8, 2) UNSAT -> H-261103-03 supported; all 203 (9, 3) maps UNSAT or
NONREALIZABLE-EXACT -> the non-existence note, focus moves to (10, 4) with E-261103-07; many SAT models that neither
realize nor certify -> build the realizability stage (I-261029-57) before more SAT. Scenario move (S5 table of
`ROADMAP.md`): (8, 2) decided moves its row to 1 / 0 / 0 or 0 / 1 / 0; each decided (9, 3) sub-case moves A or B by the
fraction of maps decided, "cannot tell" by the fraction left undecided.
