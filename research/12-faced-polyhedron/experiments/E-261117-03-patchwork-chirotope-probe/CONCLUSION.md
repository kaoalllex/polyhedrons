# E-261117-03: conclusion

2026-11-17. Session runs on the laptop, eight processes, one CP-SAT worker per unit (ortools 9.15).

* **Runs**: step 0 (`d4191846`): the 16 S6 (10, 2) files passed `candidate-check` (`witnesses/README.md`). Pilot
  `results/pilot/` at `ebd16a51`, with the C0 name-clash fix uncommitted (dirty `p4.py`, committed in `96e6a008`;
  a first attempt crashed in C0, no output kept): wall 109 s, 0.21 core-h. Development probes on the planted controls
  after the pilot: about 0.09 core-h (not in a manifest; times in the PLAN amendment). Amended run
  `results/amended/` at `f9361470` (clean but for its own output): wall 356 s, 0.57 core-h (1991 s of unit time plus
  C0). Total **about 0.87 core-h** of the 1 core-h budget. The registered `session` mode was not run (amendment).
* **Controls**: C0 PASS in both runs: 18,934 uniquely optimal and 55,602 tied 4 x 4 matrices (all 65,536 at K = 1;
  random and planted ties at K = 2, 3, 8), 0 disagreements with brute force over the 24 costs, embedded
  [[0, 0], [0, 1]] case certified. Planted tropical Vandermonde control n = 8 (K 21) found at K = 32 in 62.7 s
  (pilot cap 3 s: UNKNOWN). GP-flip negative: UNKNOWN at 90 s, not SAT (passes as registered; no UNSAT-SOLVER).
  Capacity at K = 32: n = 8 OPTIMAL in 2.3 s, n = 9 OPTIMAL in 7.1 s, so the box is not empty at nine elements.
  Every model (planted, Szilassi C1, C2) passed the exact side: unique minima by brute force, combinatorial and exact
  determinant signs equal the target, charted chi equal.
* **C1** (K = 32, cap 90 s, n <= 9): **perturbed Szilassi's chirotope is patchwork** (OPTIMAL in 49.9 s, max weight
  32, signs reproduced already at q = 3); its charted integer planes on Szilassi's map pass `--target S5`.
  Roest-Vigh, Mizhaev and all 17 K13 solids: UNKNOWN at 90 s. Coverage 1 of 20 at K <= 32.
* **C2** (Szilassi's map formula, omsat `ALL_OPTS`, AND P4, K = 32, cap 120 s): **OPTIMAL in 68.6 s**; the model's
  patchwork matrix, at q = 3 and charted to integers, passes `--target S5` on Szilassi's map: a polyhedron of the
  Szilassi type realized by construction, with no bridge.
* **Prediction vs outcome**: P1 (C0 passes, ~90 %) held. P2 (Szilassi patchwork, ~40 %) held. P3 (at least half the
  controls covered, ~30 %) failed: 1 of 20. P4 (C2 model passing S5, ~40 %) held. P5 (capacity at K = 2) not tested
  after the amendment (the pilot's 3 s n = 8, K = 2 capacity was UNKNOWN).
* **Exact verification**: `verify_candidate.py --target S5` on `results/amended/c1_szilassi_patchwork.json` and
  `results/amended/c2_szilassi_map_p4.json`: PASS, V E F chi = 14 21 7 0, all pairs adjacent, single adjacencies,
  distinct points, simple faces. Integer planes (largest coordinates about 4.5e17 and 3.3e20), so every check is exact
  and there is no rounding margin. `candidate-check`: an S5 object at (7, 1), the known Szilassi map, an auxiliary
  result, not the focus target (S1, nine faces); no adversarial re-check requested (a known type).
* **What may be claimed**: EXACT (instance): the perturbed Szilassi chirotope of E-261103-02 is coherent patchwork in
  the box [0, 32]; the coupled formula (Szilassi's map AND P4) returns, in 69 s, a chirotope with a patchwork matrix
  whose exact realization passes S5. The per-minor certificate (potentials scaled by 4) agrees with brute force on
  74,536 matrices (NUMERICAL coverage, completeness argument PROVED-1).
* **What may NOT be claimed**: that Roest-Vigh, Mizhaev, the K13 solids or the (10, 2) objects are not patchwork
  (UNKNOWN at 90 s; the (10, 2) objects and n = 11 were not run); anything about K < 32; any nine-face statement;
  a new object (Szilassi's map, known type); speed beyond these caps and this host.
* **Verdict for the direction**: **OPEN** at seven faces, **UNDERPOWERED@0.87 core-h** at nine and more elements:
  realization by construction works end to end on Szilassi's map, but this CP-SAT encoding does not decide the
  nine-element controls in 90 s and cannot find a planted n = 11 control in 120 s. Not parked: C2 is SAT, so the kill
  "C2 UNSAT-SOLVER in the box" did not fire.
* **Next step**: for the lead (follow-up tree, "covers known objects"): only one control is covered and only at
  K = 32, so the sampler (<= 6 core-h) is not opened by this session. Open questions: a faster P4 host at nine
  elements (measure on Roest-Vigh and Mizhaev first: more workers, a longer cap, a sign-free first stage, or a
  stronger matching formulation), then the coupled P3 + P4 test, which now has a working P4 half. Week item 5 next.
* **Rows updated**: `STATUS.md` 3ax, `ROADMAP.md` item 4 and row (done), `experiment-log.md` (2026-11-17),
  I-261029-10 note.
