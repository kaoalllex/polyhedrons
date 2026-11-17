# E-261117-03: P4 patchwork chirotopes - certificate C0, control coverage C1, Szilassi's map formula with P4 C2

Pre-registration, 2026-11-17. Week item 4 (`ROADMAP.md`; dialogue 2026-11-16-strategy §2 row 4, Appendix A2).
Step 0 is done (commit `d4191846`: the 16 S6 (10, 2) files passed `candidate-check`, 13 maps,
`witnesses/s6_10_2_controls/`).

* **ROADMAP row / scores**: T 1 D 2 F 1 G 2 R 2 (T + D = 3). Explore, jump 0.
* **Question**: are the chirotopes of the known face-neighbourly objects coherent patchwork (H_ij = s_ij t^w_ij,
  integer w in [0, K], every 4 x 4 minor with a unique minimum-weight matching) at small K, and does P4 coupled to a
  map formula return a chirotope that realizes by construction?
* **Hypotheses moved**: none directly (`tests: []`); I-261029-10 gets its first exact measurement.
* **H1**: some known controls are patchwork at K <= 32, and C2 returns a model realized at t = 1/q passing
  `--target S5` on Szilassi's map. **H0**: none is patchwork in the ladder within the caps, or C2 gives no model.
* **Why**: a patchwork chirotope is realizable by construction (exact integer planes, no bridge), the bottleneck that
  E-261113-02 measured (one SAT model in ten realized) and E-261116-07 could not pass.
* **Method**: `p4.py` (new; docstring). CP-SAT 9.15, one worker per unit, eight processes. Per 4-subset: 24
  matching selectors, the induced permutation matrix, potentials u_a + v_j = 4 w on the matching and <= 4 w - 1 off
  it, u_0 = 0, bound 4 (4K + 1) (A2 wrote 3 (4K + 1); v needs 4K + 3 (4K + 1), docstring, PROVED-1); the selected
  matching's sign parity equals the target sign (enforced XOR). Normalisation: a zero weight in every row and column
  (lossless, A2). All 4n sign bits free plus one global sign. INF is an ordinary row (omsat order, last).
  Exact side, independent of CP-SAT: brute-force minima of all minors, exact integer determinants of q^K H(1/q) for
  the smallest q in 2..25 that reproduces the signs (q = 25 always does), a rational chart sending INF to (0,0,0,1)
  with det > 0, `chirotope_from_planes` of the charted integer planes, then `verify_candidate` on the control's map.
  Integer planes make `ladder_exact.verify`'s 1e-9 scaling exact, so "not verifier-conditioned" cannot arise here.
  Ladder K in {2, 4, 8, 16, 32}, ascending, stop at the first SAT (membership is monotone in K). Counters (SPEC §4):
  CP-SAT status, `EMBEDDED`, `adjacent_pairs`; per K the number of covered controls.
* **C0** (certificate): fixed 4 x 4 weights vs brute force over all 24 costs: all 65,536 matrices at K = 1, 2,000
  random each at K = 2, 3, 8, 1,000 tied each, and the embedded [[0, 0], [0, 1]] case. Pass: the certificate selects
  exactly the unique minimum (and nothing else) and is infeasible on every tie; both classes occur.
* **C1** (coverage, fixed chi from the planes as given): Szilassi (the saved uniform perturbation), Roest-Vigh,
  Mizhaev, the 17 K13 solids (OPTIMAL rows of the hashed archive), the 16 S6 (10, 2) files; cap 12 s per (control, K).
  Every model: unique minima, combinatorial and exact chi equal the target, charted chi equal, and on a known map the
  verifier target (S5 Szilassi, all-pairs RV and Mizhaev, S6 the (10, 2) files; K13 has no map: chi only).
  Capacity diagnostic: any all-unique n x 4 matrix (no signs) for n = 8, 9, 11 and each K, same cap; a control
  without SAT at a K whose capacity is not SAT says nothing about that control.
* **Controls**: positive (must succeed): planted tropical Vandermonde chirotopes w_ij = a_i b_j with random signs,
  n = 8 (K 21) and n = 11 (K 30), found in the ladder; C0 as above. Negative (must not be SAT): perturbed Szilassi's chi
  with the first sign flip that breaks three-term Grassmann-Pluecker (not a chirotope, so not patchwork), whole ladder.
* **C2**: Szilassi's map formula (omsat, `ALL_OPTS`, 8 elements) loaded into CP-SAT AND P4 on its chi variables,
  one unit per K, cap 120 s. Pass: no INFEASIBLE at a K >= Szilassi's C1 K (a contradiction = encoder bug), and every
  model realizes exactly and passes `--target S5` with Szilassi's links.
* **Pilot**: `p4.py all` with caps 3 s (C1) and 10 s (C2) on the full unit list; exposes crashes, model build time
  at n = 11, and whether the 12 s cap binds. Gate: all checks of C0 pass; build time < 25 % of the cap.
* **Predictions**: P1 C0 passes (~90 %). P2 Szilassi perturbed is patchwork in the ladder (~40 %). P3 at least half
  of the 36 controls covered at K <= 32 (~30 %). P4 C2 yields a model passing S5 (~40 %). P5 capacity at K = 2 is
  not SAT for n >= 8 within the cap (~70 %; the 60 s development probe at n = 8 was UNKNOWN).
* **Grid**: K is the only parameter (the ladder); caps fixed.
* **Budget**: <= 1 core-h, one session, eight processes on the laptop (C0 ~0.1, C1 <= 0.7 worst case, capacity
  0.05, C2 0.17). No sampler in this plan.
* **Power statement**: a SAT is exact evidence of membership at that K; UNKNOWN or INFEASIBLE in the ladder never
  refutes membership (A2: a finite K never does). 12 s per unit can miss hard members at n = 11.
* **Proofs**: none; every INFEASIBLE is UNSAT-SOLVER for its box only.
* **Counter calibration**: no float diagnostic; every sign and the verifier input are exact integers.
* **Scenario move**: none for any outcome (a method probe); A/B/C credences unchanged.
* **Outcomes and their meaning**:
  * SAT: membership of that chi at that K, exactly checked; a C2 SAT is a realization by construction on Szilassi's
    map, a method result at seven faces, never an S0/S1 claim.
  * INFEASIBLE: UNSAT-SOLVER in that box only. UNKNOWN: no information.
  * near-miss: does not arise (no numerical stage).
* **Follow-up tree**: C1 covers known objects at small K -> the lead decides on inverting the P3 / P4 build split and
  on the gated sampler (<= 6 core-h, its own amendment, fixed units, rejections counted). C1 covers none but the
  planted ones -> park P4 at K <= 32, cause recorded. C2 INFEASIBLE at every K -> park the probe at those K.
* **Stop rule**: a failed control (C0, planted, negative, any model failing its exact check) stops the run: repair or
  park with the cause. Budget cap 1 core-h.
* **What changes**: STATUS gets one line (coverage per K, C2 status); ROADMAP row done or parked with the cause;
  I-261029-10 gets the measurement.

## Amendments

### 2026-11-17, pilot (`results/pilot/`, caps 3 s / 10 s, wall 110 s, ~0.25 core-h)

* First pilot attempt crashed in C0 (a local name shadowed the tie generator; fixed in `p4.py`, no output kept).
* C0 PASS: 18,934 unique and 55,602 tied matrices, 0 disagreements, embedded 2 x 2 case certified; 8 s.
* C1: every unit UNKNOWN at 3 s, including both planted controls; the GP-flip negative was not SAT; no model, so no
  exact check was exercised. Capacity (no signs): n = 8 SAT for K >= 4 (K = 2 UNKNOWN); n = 9 and 11 UNKNOWN at
  every K. C2: UNKNOWN at every K in 10 s.
* Development probes after the pilot (planted controls alone, K = 32 box): n = 8 (K 21) OPTIMAL in 57.9 s with one
  worker (17.7 s with eight workers at K = 24); n = 11 (K 30) UNKNOWN at 120 s with one worker. About 0.09 core-h.
* Reading: the registered 12 s cap cannot pass the planted positive control even at n = 8, and n = 11 (the 16
  (10, 2) controls) is out of reach of this encoding within the session budget. The session run is not started;
  escalated to the owner (about 0.34 core-h of the 1 core-h used).
