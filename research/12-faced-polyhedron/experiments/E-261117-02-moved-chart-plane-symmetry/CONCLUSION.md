# E-261117-02: conclusion

**GATE PASSED (N2-MOVED-CHART-C2)**: a far rational plane as infinity makes Szilassi's fixed-face half-turn family
uniform for the encoder and for the frozen engine; the control chain passed, the correct gauge is `build_sym`'s
orbit gauge (not `symbreak`), and the C2 3 x 2 + 1 sampler recovers the Szilassi type unaided at 37 / 13495 draws,
about 12 times the asymmetric baseline of the same engine and chart rule. The C2 4 x 2 + 1 arm of item 5 is open.

* **Runs**: pre-registration `eb2c2feb`, amendment `5ebe4512` (N 5000 -> 15000 per arm after the pilot). Stage A in
  the session, `bash run.sh stage_a` -> `results/controls/` (under 2 s). Pilot `results/pilot/0/` (61 s, one core,
  288 units per arm). Stage B on the laptop (AC), `overnight/launch.sh 17-02 start`, 10 shards, 14:05:07-14:10:39
  UTC (332 s wall each; the 330 s shard deadline bound, not N: 13495 c2 and 13490 asym units, indices up to about
  13500 of 15000). Total about 0.94 core-h (stage B 10 x 332 s = 0.92, pilot 0.017, stage A < 0.001) within the
  1 core-h cap. All manifests present; `dirty_files: 1` is the output directory. No sleep gap, no UNKNOWN, no
  engine rejection after the chart move.
* **Controls** (`results/controls/controls.json`, all PASS; reproduced by `test_n2.py` in `verify_all`):
  * K1: Szilassi's 35 plane-only determinants nonzero; the half-turn (x, y, z) -> (-x, -y, z) maps every plane vector
    exactly onto its partner (face 5, z = 1/5, fixed); chi(gS) = sgn chi(S) on all 35. Standard-chart zeros exactly
    chi(0,1,5,inf), chi(2,3,5,inf), chi(4,5,6,inf), the forced zeros of SOUNDNESS.md.
  * K2: far plane H' = (-2, -3, -5, 11): all 14 vertices strictly positive (minimum 13/5), all 35 triples with H'
    nonzero.
  * K3: moved planes, 70 signs uniform, plane-only signs unchanged, moved vertices incident exactly, EMBEDDED,
    (14, 21, 7, 0), `verify_candidate.py --all-pairs` PASS.
  * K4 (Szilassi's map, ALL_OPTS, plane-only clauses): pinned without gauge SAT; `build_sym` gauge (orbits
    {0,1}, {2,3}, {4,6}, {5}; flips {2,3,5}) pinned SAT and unpinned SAT. **Gauge check**: the `symbreak` normal
    form is not reachable by any of the 32 equivariant gauges (orbit flips x mirror), and the unpinned `symbreak` +
    plane-only formula is UNSAT-SOLVER: combining `symbreak` with symmetry clauses would exclude Szilassi. `build_sym`
    already switches `symbreak` off; this run confirms that is required, also with a moved infinity.
  * Negatives, all failed as required: the standard-chart formula with g fixing INF UNSAT-SOLVER (the forced zero);
    the pinned moved chirotope with another of the seven involutions of the K7 map (Aut 42) UNSAT-SOLVER; the engine
    rejects Szilassi's standard planes (`nonuniform triple of normals`); tetrahedron at E = 7 INFEASIBLE.
  * K5 planted: the frozen engine on the moved Szilassi planes, OPTIMAL in 0.2 s, 20 bounded cells, EMBEDDED,
    Szilassi's own links, `verify_candidate` PASS.
* **Stage B** (`results/summary.json`; Wilson 95 %):

| Arm | Units | Hits (EMBEDDED, all pairs, E = 21) | Rate | Wilson 95 % | INFEASIBLE | Redraws | Median s |
|---|---:|---:|---:|---|---:|---:|---:|
| c2 (C2 3 x 2 + 1) | 13495 | 37 | 2.7e-3 | 2.0e-3 - 3.8e-3 | 13458 | 2641 | 0.124 |
| asym (seven planes) | 13490 | 3 | 2.2e-4 | 0.8e-4 - 6.5e-4 | 13487 | 481 | 0.115 |

  Every hit has (V, E, F, chi) = (14, 21, 7, 0) and passes `verify_candidate.py --all-pairs` (40 of 40) and the
  standalone checker of E-261103-05 with only the face count and topology constants changed to (7; 14, 21, 7, 0)
  (session check: 41 of 41 ACCEPT including the moved Szilassi; a link with two entries swapped is rejected).
  Descriptive (`hit_charts.py`, `results/hit_charts.json`, not in the verdict): 39 of 40 hits have every vertex in
  the standard affine chart (so the chart move only removed the engine's uniformity-at-infinity rejection); one
  asym hit (unit 10768) crosses the old plane at infinity (12 of 14 vertices) and exists only in the moved chart;
  all 37 c2 hits have links invariant under the draw's half-turn (necessary for a symmetric solid; not checked
  on cells).
* **Prediction vs outcome**: P1 (c2 >= 1 verified hit, ~60 %) held -> the gate passes. P2 (c2 rate above asym with
  disjoint intervals, ~40 %) held. P3 (asym >= 1 hit, ~40 %) held.
* **What may be claimed** (labels `SPEC.md` §5): the moved-chart algebra (coorientations kept, plane-only signs
  unchanged, infinity signs those of {h_i, H'}) PROVED-1, checked on Szilassi (EXACT). The control chain and the
  gauge finding EXACT for Szilassi's map, formula scope; the K4 UNSATs are UNSAT-SOLVER. The 40 hits are exact
  recoveries of the known Szilassi type (EXACT per object), not new objects. The rates are NUMERICAL, for this box
  ([-8, 8] without 0), this cap (10 s, never binding), this normal list and E = 21 only.
* **What may NOT be claimed**: anything at nine or more planes; that the 12x ratio transfers to C2 4 x 2 + 1 at nine
  planes; that a plane-only SAT model carries a projective half-turn (the equivariant perturbation step is
  unproved, E-261116-09); the speed of plane-only formulas at 12 elements (not measured; (11, 5) stays priced
  out); any comparison with the Gaussian 6.4e-4 of C6 (another engine).
* **Hypotheses**: none in `tests`. I-261117-02 and I-261113-04: tested, passed at the seven-plane rung.
* **Verdict**: GATE PASSED at 0.94 core-h (one box, one cap); the C2 4 x 2 + 1 arm with a far plane as infinity may
  join E-261110-04 (item 5), whose PLAN must state its own power (the seven-plane rate is a rung-below
  number, not a nine-plane forecast).
* **Next step**: week item 3 (P3 v2, E-261116-07). Item 5's PLAN takes the C2 4 x 2 + 1 arm (`n2.draw` /
  `n2.chart` extended to nine planes). Plane-only formulas for the (9, 4) maps with a one-face involution (not enumerated) and
  the 20 (11, 5) Aut+ = 2 maps: a new
  registration through the lead only.
* **Rows updated**: `STATUS.md` 3av and header, `ROADMAP.md` (row done, week items 2 and 5), `experiment-log.md`,
  `paper/OUTLINE.md` change log (D2 note), README, idea notes I-261117-02 and I-261113-04, `verify_all.py` line.
