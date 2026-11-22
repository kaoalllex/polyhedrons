# Paper plan: face-neighbourly polyhedra, computer-assisted results

A living plan, not a draft (owner, 2026-11-16). It lists what the paper would contain, where the evidence lives, the
evidence level of each claim (`SPEC.md` §5) and what is missing before a claim may be written as a theorem. Numbers
stay in `STATUS.md`; this file points to them. Writing the paper itself stays deferred (`STRATEGY.md`, side track).

**Update rule.** `experiment-conclude` updates this file when a conclusion adds, strengthens, weakens or removes an
item below (one line in the item and one in the change log). The lead review checks it once a week. Nothing here
is a claim on its own: a line may state only what its source says at its label.

## 1. Working title and shape

* "Face-neighbourly polyhedra: symmetric obstructions, small cases and exact constructions" (working title).
* One paper with three parts (negative results, small cases, constructions); a split into a short theorem paper
  (part A) and a computational paper (parts B, C) stays possible if the referees' expectations differ.
* Venue candidates: arXiv math.CO / math.MG first, then Experimental Mathematics or Discrete & Computational Geometry.
* Every computer-assisted statement is stated at formula scope with its conditions; no "does not exist" without them.

## 2. Contributions and their state

| # | Item | Level now | Source | Missing before the paper |
|---|---|---|---|---|
| A1 | No polyhedral immersion of a 12-face neighbourly map with a non-trivial rotational symmetry (25 classes) | EXACT, DRAT-checked; CERTIFIED after E-261101-10 | FD6; `proof-no-symmetric-immersion/` | second encoder for SIMPLE / REFLEX1 / POC; written soundness proofs; archived CNF + proofs |
| A2 | Same for mirrors and point reflections | PROVED-1 (Lemma A) | I-261101-16 | human review of Lemma A, or state A1 for rotations only |
| A3 | Projective symmetries are covered too | PROVED-1 sketch | I-261029-15; `proof-no-symmetric-immersion/README.md` item 7 | written proof |
| A4 | No symmetric embedding (reproduces Moki & Julio 2026) | CERTIFIED | FD5 | overlap statement with `L:mokijulio2026` |
| B1 | Census of candidate maps for cubic maximal face-neighbourly polyhedra: (7,1) 1, (8,2) 2, (9,3) 240 / 203 admissible, (10,4) 1183 / 1117; (11,5) reproduced (STATUS 3aq) | EXACT; coverage PROVED-1 | STATUS 3c; E-261103-01, E-261109-02 (second enumerator to (9,3)), E-261116-01 | written coverage argument; second enumerator at (10,4) and (11,5) |
| B2 | No cubic maximal face-neighbourly polyhedron with (F, g) = (8, 2) | UNSAT-VERIFIED (EXACT, formula scope); geometric reading PROVED-1 | STATUS 3d; E-261103-03, E-261109-01..03 | archived proofs; encoder soundness write-up; human review |
| B3 | Same at (9, 3), all 203 admissible maps | as B2; second encoder agrees on six maps | STATUS 3d, 3aa | as B2; second encoder on more maps |
| B4 | Same at (10, 4), all 1117 admissible maps | UNSAT-SOLVER (no checked proof) | STATUS 3ad, 3ao | checked replay (I-261116-02, parked by the owner); normalisation soundness write-up (E-261114-01 `SOUNDNESS.md`) |
| B5 | Scope: cubic, extended to vertices of degree <= 4 by the perturbation lemma at k = 4; degree 5-6 not covered at (8, 2), (9, 3); uniformity is no loss for cubic objects | PROVED-1 (L1, L6; local check EXACT) | STATUS §4, 3bi; I-261108-09, E-261116-09 | L6 at k = 5, 6; human review |
| B7 | Face-transitive cubic maps: (8, 3) six classes (Roest-Vigh's among them; the other five UNSAT-SOLVER at formula scope, plain and normalised, both orientations); (9, 4) none admissible (two classes with repeated vertex triples); (9, 7) none admissible | EXACT; coverage PROVED-1; formulas UNSAT-SOLVER (no proof) | STATUS 3au, 3ba, 3bj; E-261117-01, E-261118-01, E-261119-03 | written Sylow / parametrisation argument; human review |
| B8 | Symmetric cubic maps at nine faces: C3 3+3+3 and C2 4 x 2 + 1 lists at (9, 4), free C2 at (8, 3) holding both known maps; no C3 3+3+3 map at (9, 5); the C2 4 x 2 + 1 (9, 5) list (978228 classes) | EXACT; coverage PROVED-1; every per-map uniform symmetric formula UNSAT-SOLVER (planning only); the two families cover every symmetric nine-face object but Cs (L3, PROVED-1); parity Lemma P excludes 3 priced (9, 5) maps and 17 (map, action) pairs exactly | STATUS 3be, 3bf, 3bg, 3bh, 3bi; E-261119-02, E-261116-09 | written coverage argument; stage B formulas; second enumerator or a cross-check against a full (9, 4) census |
| B6 | (11, 5): sampled cost probe complete, no SAT or candidate; full sweep gate closed; the 20 proper half-turn maps' plane-only C2 formulas UNSAT-SOLVER | NUMERICAL, instance scope; UNSAT-SOLVER only, no geometric negative | STATUS 3aq, 3bc; E-261116-01, E-261118-03 CONCLUSION | improper symmetries and asymmetric maps not run; existence open |
| C1 | A 10-face genus-2 polyhedron with single adjacencies (36 of 45 pairs), exact coordinates | EXACT witness | `witnesses/` `lab_s6_10_genus2`; FD10 | literature novelty check; minimality statement only if proved |
| C2 | Realized (10, 2) face-minimal objects from the SAT-to-coordinates bridge (16 objects, then 5 more maps) | EXACT per object | E-261113-02, E-261114-02 | decide whether a dataset table belongs in the paper |
| C3 | 12-face genus-3 objects with 48 of 66 pairs adjacent; one map completable to a target map by 3 handles | EXACT witnesses + certificate | `witnesses/` `lab_type0_genus3`, `lab_solid_genus3`; E-261101-03 | dossier (I-261031-04): second verifier, canonical map form, novelty search |
| C4 | Any S6 (10, 3), S5 (11, 5) or nine-face object found later | - | E-261116-02, -04, -01 | `candidate-check`; would become the headline |
| D1 | Known numerical near-misses fail the Gauss class and are not immersions (1005 seeds) | EXACT per instance | FD11, FD7 | short section or appendix |
| D2 | Normalisation of the OM-SAT formulas (reorientation, mirror) and its effect (13-45x on three known UNSAT (10, 4) maps) | PROVED-1 + NUMERICAL | E-261114-01; `reviews/strategy-review-2026-11-14.md` | methods section; keep the speed-up as an observation |
| D3 | The (10, 3) S6 status: all 20 normalised Lutz formulas UNSAT-SOLVER; symmetric formulas UNSAT-SOLVER; the T family of Lutz #15 empty | UNSAT-SOLVER / EXACT family scope | STATUS 3af, 3ag, 3am, 3ar, 3as | an open-problem paragraph; checked replay of the 20 CNFs (I-261116-05) for a formula-scope exclusion |

## 3. Section skeleton

1. Introduction: Szilassi, Csaszar, the 12-face question; prior work (`L:abs1996`, `L:bokowski2025`,
   `L:mokijulio2026`, `L:pirozhkov2026`, `L:roestvigh2026`, `L:mizhaev2026`, `L:schewe2010`, `L:hlz2010`).
2. Definitions: face-plane formulation, embedding and immersion, S0 / S5 / S6 classes, cubic, admissible map
   (`SPEC.md`, `theory/mathematical-model.md`).
3. The encoding: chirotope variables, Lemma 5.1 triple conditions, multiple adjacencies, normalisations; soundness
   proofs; validation against exact geometry (FD2, FD4).
4. Symmetric obstructions: A1-A4, table of the 25 classes, certificates.
5. Small cases: census B1, decisions B2-B4, scope B5, controls (positive controls, second encoder, second census).
6. Constructions: C1-C3 with coordinates in an appendix or a data release.
7. Diagnostics: D1, the Gauss-class filter.
8. Open problems: S0, (10, 3), (11, 5), nine faces; what the computations do not exclude.
9. Reproducibility: code release, CNF hashes, proof archive (Zenodo), exact verifiers, `verify_all.py`.

## 4. Before any submission (all items, not per claim)

* Human review: none so far; the owner declined the letters (E-261101-11, parked). The paper must say so until one
  happens.
* Proof archive: proofs for A1, B2, B3 (and B4 if replayed) on Zenodo or a release, not git (owner, 2026-11-08).
* Novelty: a literature check per item (C1 and B2-B4 especially); STATUS §6 has the 2026-11-08 check for S5.
* Statements reviewed by an adversarial pass against overclaiming (`candidate-check` style), then by a human.

## 5. Change log

* 2026-11-16: created at the owner's request from STATUS §1-§5, the witnesses list and
  `proof-no-symmetric-immersion/`; B4 added as UNSAT-SOLVER, its replay parked (I-261116-02).
* 2026-11-16: E-261116-01 concludes the owner probe; B1 includes the reproduced (11,5) census,
  B6 records sampled/censored cost evidence only. No new geometric negative or construction.

* 2026-11-16: E-261116-02 updates D3 with two solver-level decisions; no geometric
  exclusion or construction. The registered owner-night follow-up gate passes.
* 2026-11-16: E-261116-05 updates D3: all twenty normalised (10, 3) formulas UNSAT-SOLVER;
  no checked proof, geometric exclusion or construction (replay idea I-261116-05).
* 2026-11-17: E-261117-01 adds B7 (face-transitive census at (8, 3), (9, 4)); no formula, construction or
  geometric negative.
* 2026-11-17: E-261117-02 adds a caveat to D2: with symmetry clauses the `symbreak` normal form is not equivariantly
  reachable (Szilassi, UNSAT-SOLVER); the orbit gauge of `build_sym` is the valid one. No new item.
* 2026-11-18: E-261118-01 strengthens B7: the five non-Roest-Vigh (8, 3) classes are UNSAT-SOLVER (planning only; a
  claim in the note needs a checked proof replay of those 16 formulas).
* 2026-11-19: E-261118-03 extends B6: the plane-only C2 slice of the 20 (11, 5) Aut+ = 2 maps UNSAT-SOLVER; no proof,
  no geometric exclusion or construction.
* 2026-11-20: E-261119-02 stage A adds B8 (symmetric nine-face map lists); maps only, no formula, construction or
  geometric negative.
* 2026-11-20: E-261119-02 stage B pass 1 extends B8: the uniform symmetric formulas of all 12562 (9, 4) records
  UNSAT-SOLVER; no proof, no geometric exclusion or construction.
* 2026-11-20: E-261119-02 amendment 4 extends B8: the C3 3+3+3 (9, 5) list is empty (EXACT, coverage PROVED-1).
* 2026-11-22: E-261119-02 amendment 4 extends B8: the C2 4 x 2 + 1 (9, 5) list is complete (EXACT, coverage PROVED-1).
* 2026-11-22: E-261116-09 updates B5 (degree <= 4 by L6, PROVED-1) and B8 (coverage lemma L3, parity Lemma P).
* 2026-11-22: E-261119-03 extends B7 to genus 7: no admissible face-transitive (9, 7) map (EXACT, coverage PROVED-1).
