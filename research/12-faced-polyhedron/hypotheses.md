# Hypotheses

Each entry: statement, status ([C] conjecture / [N] numerical / [P] proved / refuted), evidence,
test that would change our belief.

## H1. Realization space is open (no equalities) — [P]
See mathematical-model.md §2. Consequence: any realization can be taken with integer plane
coefficients and rational vertices.

## H2. All embedding conditions are oriented-matroid conditions — [P] (pending adversarial check)
mathematical-model.md §4–§5. Consequence: Schewe-style SAT nonexistence proofs are possible
per combinatorial type.

## H3. Geometry-first search covers all 59 types simultaneously — [P] (by construction)
For fixed planes, the SAT variables are the 220 potential triangles; every labeled neighborly
triangulation is a candidate assignment.

## Track 6 (mathematical-researcher, 2026-10-29; details in theory-notes.md)

- **H-T6-1 [C]** In OM-SAT (formulation A), replacing χ-fixing reorientation breaking by the gauge
  `W ≡ +1` (+ mirror fixes `λ`) and adding the edge-type rule (F4), the reflex-parity link (F5) and
  the global constraints DEG_W, COV_W, CNT (F7–F9) shortens solve times on the symmetric
  certificate cases (C3/D3/T) by ≥ 3x. Test: rerun those instances with/without the families.
  Refuted if no speed-up or slow-down (as for the parity-only redundant encodings).
- **H-T6-2 [C]** The Gauss-degree condition is very restrictive: for random normal configurations
  and each of the 59 types, the fraction with degree −5, ≥ 13 saddles and a feasible κ pattern is
  below 1e-3. Test: experiment E3. If it is large, F7–F9 are weak and should be dropped.
- **H-T6-3 [C]** The chamber formulation (theory-notes §3.2, 165 variables, no parity) solves
  fixed-arrangement instances at least an order of magnitude faster than formulation B.
  Test: same arrangements, both encodings, Szilassi as control.
- **H-T6-4 [C]** For fixed normals, `min_d #violations` (exact, E1) is a smoother objective than
  the joint continuous violation count; local search on normals with this objective gets below
  the 21–24 asymmetric plateau. Test: E1 + E4 from symmetric near-misses.
- **H-T6-5 [C]** (low confidence) In every realization (if any) no face is convex and the number of
  saddle vertices is well above the proven bound 13. Test: record `s` and convex faces in every
  near-miss with ≤ 4 violations.
- **H-T6-6 [N→C]** Szilassi: exactly one convex face, it is the C2-fixed face, two faces lie in
  supporting planes, solid = 8 chambers. Conjecture: the "fixed central face" is essential to
  Szilassi's embeddability mechanism, and has no F=12 analogue because no face can be fixed.
