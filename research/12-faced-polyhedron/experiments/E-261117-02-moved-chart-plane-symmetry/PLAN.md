# E-261117-02: Plane-only symmetry in a moved chart - Szilassi control chain, then the seven-plane C2 3 x 2 + 1 rung

Pre-registration, 2026-11-17. Week item 2 (`ROADMAP.md`; dialogue 2026-11-16-strategy §2 row 2, Appendix A4).

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (T + D = 4). Explore, jump 0: a gate of the C2 4 x 2 + 1 arm of item 5.
* **Question**: does a generic rational far plane as infinity make Szilassi's fixed-face half-turn family uniform for
  the encoder and the frozen engine, with the correct gauge, and does a C2 3 x 2 + 1 sampler then find Szilassi solids
  unaided at seven planes?
* **Hypotheses moved**: none (`tests: []`); scores the method of I-261117-02 / I-261113-04. Pass -> the C2 4 x 2 + 1
  arm joins item 5; fail -> parked with the failing link named.
* **H1**: all controls pass and the C2 arm recovers Szilassi unaided. **H0**: a control fails, or no C2 unit
  within the budget yields a verified seven-face all-pairs solid.
* **Why**: a half-turn g fixing face X (plane orthogonal to the axis) and swapping A, B forces chi(X, A, B, inf) = 0 in
  the standard chart (`E-261103-02/SOUNDNESS.md`): the uniform encoder and the engine's `arrangement` (`nonuniform
  triple of normals`) reject such arrangements. A far plane H' = (-n, R), R > n . p for every finite triple point,
  is not g-invariant; the chart X' = (x, R - n . x) keeps every coorientation (det M = R > 0), keeps all plane-only
  signs, and its infinity signs are those of {h_i, H'} (PROVED-1, in `n2.py`'s docstring; checked on K3).
* **Method**: `n2.py` (new), `omsat.build` with the new opt-in `sym_planes_only` (symmetry clauses only on
  quadruples of planes; default unchanged). Stage A `controls`, Szilassi from `index.html`, g = (1 0)(3 2)(6 4):
  * K1 exact plane-only determinants: 35 nonzero, g maps plane vectors exactly, chi(gS) = sgn chi(S); standard-chart
    zeros exactly the triples (0,1,5), (2,3,5), (4,5,6);
  * K2 a rational H' (first of a fixed normal list) with all 14 vertices strictly on its positive side and all 35
    triple determinants with H' nonzero;
  * K3 moved planes: 70 signs uniform, plane-only signs unchanged, moved vertices incident exactly, `ladder_exact.verify`
    EMBEDDED all pairs and `verify_candidate.py --all-pairs` PASS;
  * K4 encoder (Szilassi's map, ALL_OPTS, cadical195, 60 s): pinned moved chirotope + plane-only g, no gauge, SAT;
    the `build_sym` gauge (orbit flips on the orbfix quads, mirror) applied to the pinned signs, SAT; the same gauge
    unpinned, SAT. Gauge check, reported, not a pass condition: whether `symbreak` is reachable by an equivariant
    gauge, and the unpinned `symbreak` + plane-only formula;
  * K5 planted: the frozen engine of E-261103-05 (`pilot.arrangement`, `Tables`, `best_solid`, hard disk model,
    E = 21, max_runs 3, cap 20 s), unchanged, on the moved Szilassi planes: EMBEDDED, all pairs, verify_candidate PASS.
  Stage B `sample`: two arms per unit i, interleaved; integer box [-8, 8] without 0, seeded by (arm, i). c2: plane
  (0, 0, +-1, d) and three pairs (a, b, c, d), (-a, -b, c, d); asym: seven independent planes (same engine, same chart
  rule: the baseline). Draws with a zero plane-only determinant or no uniform chart are redrawn (counted). Engine as
  K5, cap 10 s, E = 21. Unaided: the engine gets the planes and E only. Target S1 at seven faces (the Szilassi type);
  a hit is a recovery, not a new object. Counters: engine statuses OPTIMAL / FEASIBLE / INFEASIBLE /
  UNKNOWN per unit, hits = EMBEDDED all-pairs, each re-checked by `verify_candidate.py --all-pairs` in `summary`.
* **Controls**: positive K1-K5 (must pass). Negative (must fail): the standard-chart formula with g fixing INF
  (UNSAT); the pinned moved chirotope with another involution of the K7 map (UNSAT); the engine on Szilassi's standard
  planes (rejected, `nonuniform triple of normals`); the engine on a tetrahedron at E = 7 (INFEASIBLE). Stage A was run
  in development before this commit (all PASS, symbreak not reachable, its formula UNSAT); it is rerun into
  `results/controls/` after the commit and that run is the record.
* **Pilot**: shard 0, DEADLINE 60 s into `results/pilot/0/`: unit cost per arm, UNKNOWN share, redraws.
* **Pilot gate**: the binding limit is the shard deadline (330 s), not the unit cap. If more than 10 % of pilot units
  end UNKNOWN, amend the cap before stage B; if the projected units per arm are below 1000, say so in the amendment.
* **Predictions**: (P1) the C2 arm has >= 1 verified hit (~60 %); decision: the gate of item 5's C2 arm. (P2) the C2
  hit rate exceeds the asym rate with disjoint 95 % Wilson intervals (~40 %); decision: none, reported as the
  rung-below rate the dialogue lacked (§6). (P3) asym has >= 1 hit (~40 %).
* **Grid**: one box, one cap, one normal list; the rate depends on all three and is reported for this setting only.
* **Budget**: <= 1 core-h: stage A < 0.01, pilot 60 s, stage B 10 shards x 330 s (0.92 core-h), N <= 5000 per arm;
  laptop on AC under caffeinate via `launch.sh 17-02` (minutes of wall, no night). No proofs.
* **Power statement**: with N units of an arm and no hit, p >= 3/N is rejected at 95 % for this box, cap and chart
  rule only. The Gaussian 6.4e-4 (C6) used another engine and is not a baseline; asym is. Not measured: plane-only
  formulas at nine or more elements, their speed at 12 elements (the 165 infinity signs at eleven planes lose their
  symmetry), the equivariant perturbation step (E-261116-09).
* **Proofs**: none; every UNSAT is UNSAT-SOLVER (no named negative claim).
* **Counter calibration**: no float diagnostic enters the verdict (exact signs, exact geometry, solver statuses).
* **Scenario move**: none for S0 / S5 (seven faces, a known type). A pass only adds an arm to item 5.
* **Outcomes and their meaning**:
  * hit: a recovery of Szilassi's type from a C2 (or asym) draw in a moved chart, exactly verified; method evidence.
  * INFEASIBLE: that arrangement, chart and E = 21 only.
  * UNKNOWN / not run: no information; counted, never a negative.
  * K4 SAT: an OM relaxation with plane-only symmetry, not a symmetric realization (perturbation step unproved).
* **Follow-up tree**: all controls pass and P1 holds -> the C2 4 x 2 + 1 arm (far plane as infinity) is added to
  E-261110-04's PLAN (item 5). A control fails -> park, naming input zero (K1-K2), clause or gauge (K4), solver or
  engine (K4-K5). Controls pass, no C2 hit -> no C2 arm in item 5; the C2 rung stays open with its power bound.
  Plane-only formulas for (9, 4) maps with a one-face involution and the 20 (11, 5) maps with Aut+ = 2: a new
  registration through the lead in any case.
* **Stop rule**: a failed control (stage A stops before stage B); the stage-B deadline or N per arm; 1 core-h cap.
  No first-hit stop: the rate is the second output.
* **STATUS.md / ROADMAP.md**: a STATUS line with the control chain, the gauge finding and the two rates; ROADMAP
  State concluded; item 5's C2 arm marked open or not by the gate.

## Amendments
