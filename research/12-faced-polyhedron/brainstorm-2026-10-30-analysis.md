# Analysis of the owner's brainstorm "Research Mission" (2026-10-30) against the project state

## 1. Corrections of facts in the brainstorm

* **Our target is not the 8-face object.** Strict target (README Series 1): 12 faces, every two share EXACTLY
  one edge, three faces per vertex, embedded in R^3 -> V = 44, E = 66, genus 6, faces 11-gons. The 8-face
  genus-3 polyhedra (Mizhaev; Röst-Vígh) are a RELAXED class (8 pairs share two collinear edges).
* **pd37_0 is not a polyhedron candidate.** It is a 12-face NORMAL set (type 37) with zero period/closure
  defect from night 2; it was shown to be a FALSE POSITIVE (exact closure needs >= 11 of 12 faces
  non-simple; simple-defect MILP). It has 12 faces, so it cannot be combinatorially equivalent to any
  8-face construction; the requested equivalence check is not applicable.
* **Map generation for the strict target is finished.** The maps are exactly the duals of the neighborly
  genus-6 triangulations on 12 vertices: 59 isomorphism classes, enumerated twice independently, matched to
  HackerPoet's and Lutz's lists, with automorphism groups (`data/k12_triangulations.json`, Track 2). So
  Stages B-E of the brainstorm (coordinate-free representation, generation, screening, isomorphism) are
  done for the strict target; the open problem is purely Stage F/G (realization). Generators are useful
  only for RELAXED targets (doubled pairs, other face counts).
* Exact verification (Stage G) exists (`ladder_exact.py`, rational; positive controls Szilassi and
  Röst-Vígh; `verify_solid.py`, `planes.check_embedding`).

## 2. What is already used (brainstorm item -> our tool)

| Brainstorm item | Project |
|---|---|
| rotation systems, darts, canonical forms, automorphisms | `k12_tools.py`, `check_triangulations.py`, `k12_invariants.py` |
| map enumeration | Track 2 (59 types), `enum_k12.c`, `enum2_k12.c` |
| group actions / symmetric search | certified UNSAT for every symmetric case (25 classes, DRAT) |
| algebraic topology / Euler, genus, degree | Gauss-degree gate (`gauss_gate.py`), turning numbers |
| computational geometry, exact predicates | OM-SAT encoder (`omsat.py`, sub-maps), `ladder_exact.py` |
| CMA-ES, DE, annealing, NGOpt, GA, basin hopping | `search-algorithms.md` (all tried; review stop list: no new black-box engines) |
| discrete differential geometry (angle defect) | covering + saddle bound s >= 2g+1 (theory-notes F7-F9) |
| quality-diversity / archive | `archive_climb.py` (MAP-Elites-style archive) |

## 3. New ideas taken from the brainstorm (added to the plan)

| # | Idea | Concrete experiment | Value |
|---|---|---|---|
| B1 | **SPEC.md**: one strict specification + the relaxed variants (doubled pairs d = 6/12 at genus 7/8; other face counts) with formulas; novelty = new combinatorial map class (canonical form), not new coordinates | write it (1 h) | removes confusions like the pd37_0 one |
| B2 | **Voltage-graph lifting for SYMMETRIC RELAXED maps**: 12 faces = orbits of a free group of order 4 or 6; enumerate base maps with voltages, derive face-neighbourly cubic maps with collinear doubled pairs (genus 7 or 8) | generate all such maps for D2, C4, Z6 and count them; each one feeds L2 (symmetric plane search) | the combinatorial generator the relaxed targets L1/L2 need |
| B3 | **Canonical comparison of the 8-face objects**: Mizhaev vs Röst-Vígh vs our n = 8 ladder maps (with doubled adjacencies), map canonical form | reproduce "not combinatorially equivalent" from the papers' data | validates our canonical forms on doubled maps; needed before claiming any relaxed object new |
| B4 | **Uniform (Thomson / spherical-design) starts for normal annealers** | A/B test in Q1 and normals_first: random vs Riesz-energy-minimal 12 directions | cheap; may speed up the class search |
| B5 | **Realization-space size (rigidity view)**: at fixed normals all conditions are linear in the offsets; the volume/width of the offset polytope of known realizations (genus-3 type 0, Röst-Vígh) measures how narrow the target region is | LP width per realization | calibrates radii for normals_first (control: SAT only at r = 0.05) |

## 4. Not adopted (reason)

Spectral / Ramanujan / expander filters, critical group, delta-matroids, partial duality, graphons, quantum
automorphisms, Graph Embedding Tensor, cosmic web / persistent homology: their role would be fingerprints
or generators of maps, but the strict map space is finite and already classified with exact canonical
forms. Fullerenes, MOF, zeolites, capsids, diatoms, cellular automata, swarms, origami, tensegrity,
quasicrystals, orbital resonances, protein landscapes: analogies without a concrete experiment that
changes the realization question (the brainstorm's own Tier-3 rule). Revisit only for relaxed targets
(B2 covers that need).

## 5. Updated work plan (after night 4)

0. Night-4 analysis (`analyze_n5.py`, arch log): realized genus per type, n5 SAT/UNSAT statistics,
   kdrift class crossings on genus-2 arms with k_tau = -1.
1. L6 engine calibration on Röst-Vígh's polyhedron + L2 symmetric rediscovery (agreed first).
2. Q1 next steps (a)-(c) (`METHODS_PROTOCOL.md`).
3. B1 SPEC.md; B3 canonical comparison of the 8-face objects (with Mizhaev's coordinates as the second
   control); then B2 voltage generator -> L1 relaxed 12-face search.
4. P1 projective ladder test; Q3 flip through degeneration; n = 8 links-based gate; B4, B5 as cheap side tests.
