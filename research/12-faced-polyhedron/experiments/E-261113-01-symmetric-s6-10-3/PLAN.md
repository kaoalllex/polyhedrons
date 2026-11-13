# E-261113-01: symmetric S6 (10, 3) - the tetrahedral family of Lutz #15 and ten symmetric formulas

Pre-registration, 2026-11-13 (lab session, week item 1 of the owner-approved plan). No compute before this commit.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (T + D = 4), exploit, jump 2. Origin I-261113-01.
* **Question**: does a (10, 3) S6 polyhedron exist among symmetric realizations: (a) Lutz #15 with its rotation
  group T, (b) the C3 (one fixed face) and free C2 ansatzes on the screened maps?
* **Hypotheses moved**: H-261110-03 (any `--target S6` PASS proves its (10, 3) part; negatives here are scoped to
  symmetric realizations and do not refute it).
* **H1 / H0**: H1: some unit of (a) is EMBEDDED, or some formula of (b) is SAT with a model the bridge realizes.
  H0: (a) has no EMBEDDED unit and (b) has no realized SAT.
* **Why**: the 20 asymmetric formulas all timed out at 3600 s (STATUS 3af); the S0 symmetric formulas were decided
  where the asymmetric ones were not (FD5, FD6). Screening `reviews/strategy-review-2026-11-13-symmetry.py` (EXACT).
* **Method (a), exact, no solver** (`tetra.py`). Change from the row: the map is fixed, so given the planes the
  polyhedron is determined (vertex XYZ = the point of planes X, Y, Z); each unit is decided by the exact verifier
  `ladder_exact.verify`, not by the solid engine (`solid_first` / `solid_cpsat` are float-based and assume a simple
  arrangement; this one has forced quadruple points; recorded, not adapted). Coorientations do not enter the check.
  * Reduction (PROVED-1, this session, not reviewed): a realization of #15 symmetric under rotations acting as
    Aut+(#15) = T is, after a similarity, the planes `x, y, z = +-1` and `n . p = t` for the even tetrahedron normals
    n (odd normals = t -> -t), faces labelled by a T-equivariant bijection map faces -> planes (the C2 axes are the
    normals of the three fixed non-adjacent pairs; the C3 axes those of the fixed enneagons). Coplanar opposite
    faces (scale 0) are not polyhedra here and are excluded.
  * List: all bijections octagons -> cube planes, enneagons -> tetrahedron planes, kept iff they conjugate Aut+ onto
    the 12 rotations of T acting on the planes (predicted 48). Critical t: roots of the 4 x 4 determinants, linear
    in t, over all 4-subsets; units: two rational points inside each open interval, two beyond each end, and every
    root (walls); planes scaled to integers, so the verifier's 1e-9 rounding is exact.
  * Interval constancy (PROVED-1 argument: the verifier's outcome depends only on the signs of these determinants,
    constant between roots) is also checked: the two interior points of an interval give the same report per bijection.
* **Method (b)**: E-261103-03 `tranche.py` imported-map mode on an experiment maps file of ten formula records
  (`make_queue.py`); `submap_formula` gains an optional generator: `omsat_sym.build_sym` (SYM with det rho = +1,
  orbit-flip and mirror normalisation) on the `submap=True` triangulation with `ALL_OPTS`. C3 on Lutz #1, 2, 4, 8,
  14, 15 (one class each), free C2 on #6, #12 and both involutions of #20. kissat rel-4.0.4, no proofs (`NO_PROOF=1`),
  cap 3600 s, one formula per shard after the two per-shard convex f10 controls; every SAT model through
  `tranche.bridge` and `verify_candidate.py --target S6`. Counters (SPEC §4): SAT / UNSAT-SOLVER / TIMEOUT, seconds.
* **Controls (b)**, prep (`prep_controls.py`), all must pass before launch:
  (c1) the 25 FD5 symmetric S0 CNFs rebuilt (`run_overnight.sym_build`) hash as recorded (encoder regression);
  (c2) the (10, 2) witness, trivial group through `build_sym` (normalisations, non-adjacent pairs), its normalised
  chirotope pinned: SAT; (c3) Roest-Vigh with its free C2 (rotation about z), `submap=True`, pinned normalised: SAT;
  (c4) negative: the same with det sign -1 for the involution: UNSAT; (c5) Roest-Vigh unpinned symmetric formula SAT
  and the model realized by `tranche.bridge`, saved file `verify_candidate.py --all-pairs` PASS at (24, 36, 8, -4);
  (c6) per formula: no forced-zero quadruple, a random rho-symmetric integer configuration uniform, its normalised
  chirotope SAT on the gp-only symmetric formula. Shards: convex f10 positive SAT, negative UNSAT-SOLVER.
* **Controls (a)**: positive: the same code on the map of the convex cube cut at four alternate corners (6 hexagons,
  4 triangles; map built from the hull at t = 2, not by the code under test) must be EMBEDDED for t in (1, 3) for
  some bijection; negative: it must fail at t = 4 and t = -2, and every non-equivariant bijection tried at t = 2 fails.
* **Pilot (b)**: `prep/pilot`, 2 shards: shard controls, then #1 (C3) and #6 (C2) at a 300 s cap; logs the limit
  per unit. **Gate**: binding limit = the 3600 s cap; the day run starts if every control passes. If both pilot
  formulas time out, the run still needs the owner's word (STRATEGY: a pilot can stop a night).
* **Predictions**: (P1, ~70 %) (a) has no EMBEDDED unit; (P2, ~50 %) at least 8 of 10 formulas decided in 3600 s;
  (P3, ~15 %) a SAT formula; (P4, ~60 %) c5 passes (the bridge on a doubled-adjacency map is untested).
* **Grid**: one setting; solver and cap from E-261110-02. **Budget**: (a) seconds in the session; (b) <= 10 core-h,
  10 shards, about 1 h wall, laptop on AC, launched by the owner; prep in this session.
* **Power**: (a) is exhaustive for T-symmetric #15 (no sampling). (b) detects a SAT formula kissat finds in 3600 s;
  a TIMEOUT says nothing; UNSAT-SOLVER may rank a map, never a negative claim.
* **Proofs**: none (owner, 2026-11-13). **Calibration**: no float diagnostic enters any verdict (exact verifier,
  exact signs); 3 of 10 timeouts escalates, 2 do not (`summary.py --selftest`).
* **Scenario move** ("(10, 3) exists", 0.25, CONJECTURE): verified S6 -> 1; (a) negative and (b) all UNSAT-SOLVER
  -> no numeric move (symmetric scope only); timeouts -> none. S0 table: no move.
* **Outcomes**:
  * (a) EMBEDDED unit: CANDIDATE, `verify_candidate.py FILE --target S6`, `candidate-check`, escalate.
    No EMBEDDED unit: "no realization of Lutz #15 with rotation group T", EXACT computation, reduction PROVED-1.
  * (b) SAT: CANDIDATE only; an OM model alone is not a result. UNSAT-SOLVER: scoped to its formula, ranks the map,
    no exclusion row. TIMEOUT: no information. Near-miss: not applicable to (b); in (a) recorded, not a result.
* **Follow-up tree**: SAT -> at least 6 models by seed, bridge each, `--target S6`, `candidate-check`, escalate;
  all UNSAT-SOLVER -> scoped search outcome, a replay with proofs only on the owner's word; > 20 % timeouts ->
  escalate. A failed control stops (b) for review.
* **Stop rule**: (a) all units; (b) all units recorded, a failed control (stop the shard, escalate) or the cap.
* **STATUS / ROADMAP**: a STATUS 3 section with the (a) verdict and the per-formula table; ROADMAP row to done;
  H-261110-03 evidence line; a SAT or EMBEDDED unit goes through `candidate-check` before any wording.

## Amendments
