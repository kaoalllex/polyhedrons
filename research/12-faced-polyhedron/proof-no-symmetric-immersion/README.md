# Task: proof that no symmetric polyhedral immersion exists

Separate work item. Goal: turn the computer result of 2026-10-29 into a checked, written,
reviewable proof and share it with experts.

## Statement

**Theorem (computer-assisted).** Let M be the dual map of any of the 59 neighborly orientable
genus-6 triangulations with 12 vertices (12 faces, every two sharing exactly one edge, 3 faces per
vertex). There is no polyhedral IMMERSION of M in R^3 with planar faces — faces are simple planar
polygons and every vertex star is embedded — that is invariant under a non-trivial isometry of R^3
(acting on M by a combinatorial automorphism).

Corollary (already claimed by Moki & Julio 2026, independently reproduced here): no
12-face Series-1 polyhedron (embedded) has a non-trivial symmetry.

## Current status

| Part | Status | Where |
|---|---|---|
| Reduction to face planes; open realization space; WLOG general position | written; adversarially reviewed (ACCEPT, minor fixes applied) | `../mathematical-model.md` §1-§5, `../verification/foundations-report.md` |
| Symmetry reduction: a non-trivial symmetry group contains a half-turn (C2) or a 3-fold rotation (C3); no fixed faces; no mirrors / point reflections; 25 conjugacy classes (21 C2, 4 C3) | proved in Track 6 notes, matches the prior work's section 2; class list computed by our code | `../theory-notes.md` (Q2), `../results.md` (Track 2), `../code/omsat_sym.py` |
| Symmetric configurations can be perturbed symmetrically into general position | checked per representation (random symmetric configurations are uniform) | `../code/omsat_sym.py` (`find_reps`, uniformity check) |
| Clause families: uniform 3-term GP; symmetry chi(gS) = eps(g) chi(S); orbit-flip + mirror normalization; SIMPLE (non-adjacent edges of a face do not cross); REFLEX1 (at most one reflex corner per vertex = embedded vertex star); POC (orientation consistency) | encoded in `../code/omsat.py`; predicates validated against exact geometry (0 mismatches, ~2.5 M evaluations); SIMPLE + REFLEX1 = immersion re-checked by the fresh-eyes review | `../results.md` (Track 3), `../fresh-eyes-review.md` |
| SAT results | all 25 classes UNSAT; DRAT proofs checked by drat-trim on the user's machine (night 2, phase 1, 7-158 s per case) | `../overnight/results/symimm/results.jsonl` (pushed after night 2), console log in `../results.md` |
| Embedding version | 25/25 UNSAT-VERIFIED (night 1) and agrees with the independent third-party encoding | `../overnight/results/sym/results.jsonl` |

## What remains (in order)

1. **Second, independent encoding of the local families** (SIMPLE, REFLEX1, POC, symmetry action),
   written from the geometric definitions without reading `omsat.py`; it must give UNSAT on all 25
   classes and SAT on the controls (Szilassi n=7; symmetric instances without SIMPLE, e.g. #48 C2
   without SIMPLE is SAT). Only one encoder exists for the immersion version today.
2. **Written soundness proofs** for each clause family, in one document: REFLEX1 (two reflex corners
   at a degree-3 vertex force two faces to overlap along their common line), POC, the SIMPLE
   predicate via the E-predicate, the symmetry relation with the orientation character eps, and the
   normalizations (orbit flips, mirror). Most arguments exist in scattered notes; collect and tighten.
3. **Proof hygiene**: record CNF SHA-256 hashes and proof sizes for all 25 cases (already in the
   results JSONL); optionally re-check with LRAT (cake_lpr) for a formally verified checker.
4. **Optional insight**: minimal unsatisfiable cores; for D3 (Lutz #3) simplicity alone is UNSAT —
   extract a human-readable lemma if the core is small.
5. **Write-up** (4-6 pages): statement, reduction, clause families with proofs, table of the 25
   cases (map, group, class, vars, clauses, time, proof size, verdict), reproduction instructions,
   relation to prior work (Bokowski–Kevin H. 2025; Moki & Julio 2026; Schewe 2010).
6. **Human review and contacts**: J. Bokowski (TU Darmstadt), Kevin H. (CodeParade), the
   `szilassi-12` repository authors (independent confirmation of their Part B). Possibly arXiv
   (math.CO/math.MG) after positive feedback.

7. **Free strengthening (projective symmetries)**: a finite group of projective maps preserving the bounded
   polyhedron P maps no point of P to infinity, so each map keeps P (connected) in one half-space and
   preserves conv(P); lifting to a sharp cone in R^4 and averaging in the dual cone gives an invariant
   hyperplane missing conv(P); in that affine chart the group acts affinely (then isometrically after
   averaging an inner product), and the chart change keeps P a bounded planar-faced embedding/immersion.
   Hence the theorem also excludes projective symmetries. Write out and check (`../cross-field-ideas.md`, Y9).

Also worth including in the write-up as context (separate, numerical): every known near-miss fails
the Gauss-degree condition and is not an immersion (`../theory-notes.md`, `../results.md`).

## Reproduce

```bash
cd research/12-faced-polyhedron/overnight
python3 run_overnight.py sym --sym-immersion --hours 1 --workers 7 --git   # needs cadical + drat-trim
python3 run_overnight.py sym --hours 1 --workers 7 --git                    # embedding version
```
