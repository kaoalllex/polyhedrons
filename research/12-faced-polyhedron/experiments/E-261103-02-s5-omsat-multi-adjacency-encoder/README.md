---
id: E-261103-02
title: OM-SAT encoder for multiple adjacencies and F != 12, validated on the two 8-face objects
date: 2026-11-03
status: done
direction: [DR19, DR8]
origin: [E-261030-01, I-261030-31, L:roestvigh2026, L:mizhaev2026]
tests: []
produces: []
verdict: FOUNDATION
preregistered: true
---

> Completed, 2026-11-03. Controls and scope: `CONCLUSION.md`; predicate argument and symmetry limitation: `SOUNDNESS.md`.
> Pre-registration: `5dc2caa`. The first (8,2) formula is built, not solved.

## Goal

Close the one infrastructure gap between the project and an exact S5 decision: `STATUS.md` 3b records that the 8-face
objects (doubled adjacencies) are not expressible in the OM-SAT encoder (`code/omsat.py`). Extend the encoder to F planes
plus the plane at infinity for any F, and to pairs of faces sharing m >= 1 collinear edge segments: in Lemma 5.1
(`theory/mathematical-model.md` section 5) "F_X cap F_Y = e_XY" becomes "F_X cap F_Y = the union of the m shared segments",
the m segments on L_XY disjoint and ordered, with endpoints at the 2m triple points of the partner faces; the IN / E /
REFLEX / RTURN predicates keep their form with the partners read from the map's `links`. Add the symmetric clauses of
`omsat_sym.py` for an automorphism of the map realised by an isometry (C3 free on faces, C2 with fixed faces allowed).

## Starting point

* Positive controls (all must pass before any target instance): the chirotopes of the Roest-Vigh and Mizhaev planes (8 planes
  + infinity, `code/control_rost_vigh.py`, `literature/mizhaev2026-planes.json`) satisfy their own maps' formulas under the
  `Eval` backend; 0 mismatches between `Eval` and exact geometry on 1,000 random perturbations of each object and of
  Szilassi (the FD2 protocol, `code/omsat_validate.py`); a CNF built for each object is SAT and its model is the object's
  chirotope when the chirotope is asserted.
* Negative controls: the Roest-Vigh planes against Mizhaev's map fail; a map whose parallel edges are paired differently
  (the two copies swapped at one end) is rejected by the encoder's consistency check or gives UNSAT on the true planes.
* Guard the exact verifier first: `code/ladder_exact.verify` must return `EMBEDDED: False` (not raise) on a map with a
  repeated corner triple (review finding 6; the 37 non-admissible (9, 3) maps are the test set).
* Soundness note: the extended predicates are PROVED-1 at best (an AI session writes them); E-261101-09 step 1 (predicate
  equality with a second encoder) is the cheap external check and should be run on the shared single-adjacency predicates.

## Next

Stop rule: the three controls pass and the first (8, 2) instance is built, or a written obstruction (a predicate that cannot
be expressed in the chirotope, which would take the exact route out for S5 and leave the heuristic engines). Outcomes feed
E-261103-03 directly. Scenario move: none.

## Outcome

The bounded controls pass (EXACT); S0 circuit baselines are unchanged. The extension's soundness is
PROVED-1 only. Free C2/C3 have positive uniform controls; fixed-face C2 and the tested D3 action
force zeros, so uniform symmetry-only UNSATs must not be used as geometric exclusions.
See `CONCLUSION.md` for counts, resources, evidence and what remains untested.
