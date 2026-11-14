# E-261113-04: cube-and-conquer pilot on (10, 4) maps 96 and 85

Pre-registration, 2026-11-13 (lab session, week item 4 of the owner-approved plan). No solver run on these units before
this commit (the c1/c2 hash and literal checks ran without a solver).

* **ROADMAP row / scores**: week item 4, T 1 D 2 F 2 G 2 R 2 (T + D = 3), explore. Origin I-261031-02 (cube-and-conquer),
  E-261108-03 (the monolithic times), E-261110-06 (the rule this pilot gates).
* **Question**: do segment-order cubes reduce the summed kissat core-seconds on (10, 4) maps 96 and 85?
* **Hypotheses moved**: H-261101-06 (the cost of an exact per-map decision), only as a planning price; no
  decision-point credence moves.
* **H1 / H0**: H1: the summed cube time is <= 0.5x the monolithic time on both maps. H0: >= 0.7x on both.
* **Target and scope**: S5 at (10, 4), the plain uniform formula of the E-261103-02 encoder (`pilot.from_links`,
  `ALL_OPTS`), exactly the formula of E-261108-03 (control c1). Every UNSAT is UNSAT-SOLVER. The question is about
  solver cost, not about the maps.
* **Cube generator**: march_cu was the first choice; it could not be built in this session (building downloaded
  third-party code was refused by the session's permission system), so the row's fallback applies, with no other
  substitution: the segment-order cubes of the doubled pairs. For each of the three doubled pairs `(X, Y)`, `X < Y`,
  with segments `(A, C), (D, E)` as `Triangulation.segments` lists them: `lt(X,Y,A,C)`, `lt(X,Y,D,E)`,
  `lt(X,Y,A,D)` (orientation of each segment on `L_XY`, and which comes first; with SEGMENT_DISJOINT these fix the
  order of the four endpoints). Nine literals, all existing variables of the plain formula (no new definition);
  512 cubes per map, every sign vector, so the cubes cover the formula by construction. A cube = the plain CNF plus
  nine unit clauses. Map 96 pairs (0,3), (1,2), (3,5); map 85 pairs (2,4), (3,6), (8,9).
* **Units** (`cubes.py` through `run.sh`, 10 shards, unit j on shard j % 10): unit 0 the monolithic map 845 (speed
  calibration), then the 512 cubes of 96, then the 512 of 85. Solver kissat rel-4.0.4 (SHA-256 `4bc06993...`, as in
  E-261108-03), no options, `NO_PROOF=1`.
* **Caps**: cube cap 0.1x the arm's monolithic time (107.3 s for 96, 274.9 s for 85); arm cap: a cube is not started
  (recorded `SKIPPED-ARM-CAP`) once the arm's recorded solver seconds reach 0.7x monolithic; calibration cap 600 s.
* **Counters** (SPEC §4): per arm, cubes SAT / UNSAT-SOLVER / TIMEOUT / SKIPPED-ARM-CAP, summed solver seconds, the
  largest cube, r = summed seconds / recorded monolithic seconds (E-261108-03, 1073.49 s and 2748.86 s, 10
  simultaneous shards, the same load as here). CNF writing in Python is not solver time; shard core-h are reported too.
* **Controls** (every shard, before any unit; a failure stops the shard): c1 the plain CNFs of 96, 85 and 845 rebuild
  to their recorded SHA-256; c2 the nine literals of each arm are distinct unfixed variables of the formula and the 512
  cubes are all their sign vectors; c3 positive and negative: the pinned Roest-Vigh chirotope (E-261103-02) with the
  eight cubes of its first doubled pair: exactly one SAT, equal to the cube read off the pinned model, seven
  UNSAT-SOLVER; that cube on the unpinned Roest-Vigh formula SAT (the unpinned formula without a cube is recorded, no
  expectation). Calibration (not a stop): map 845 monolithic / 188.38 s outside [0.75, 1.33] marks the reading
  UNCALIBRATED and the lead decides.
* **Calibration of diagnostics**: r is a ratio of solver seconds with a fixed threshold; `summary.py --selftest`
  checks every reading on synthetic inputs on both sides of 0.5 and 0.7, with timeouts and skips as lower bounds.
* **Power**: two maps, one cube design, one solver. A PARK says these cubes do not pay on these maps; it says nothing
  of march_cu cubes, other cube variables or other maps. A CUBES-WIN on two maps prices, it does not prove.
* **Proofs**: none (owner rule 2026-11-13); no outcome here is a negative claim.
* **Readings** (`summary.py`, decided now): any SAT cube -> CONTRADICTION (kissat called the formula UNSAT; check the
  model, escalate); r >= 0.7 on both arms, lower bounds included -> PARK (cube-and-conquer parked at this budget);
  both arms complete (512 decided) with r <= 0.5 -> CUBES-WIN: propose the eight (10, 3) maps without symmetry (Lutz
  #3, 5, 7, 9, 10, 11, 13, 18) with cubes to the owner; A + B are then priced at r_max x 6.06 nights (f = 7.16) and
  x 4.18 (the 96 / 85 ratios, E-261109-06) and stay behind the (10, 3) proposal under the rule of E-261110-06;
  anything else -> BETWEEN (record, no change). TIMEOUT cube: no answer for that cube; the arm's r is a lower bound.
* **Predictions**: (P1, ~50 %) r <= 0.5 on map 85; (P2, ~35 %) CUBES-WIN; (P3, ~25 %) PARK; (P4, ~70 %) at least one
  cube of each arm is refuted in under 1 s (the order bits conflict with other clauses).
* **Budget**: worst case per arm 0.7x + 10 in-flight cubes x 0.1x = 1.7x monolithic, so <= 1.7 x 3822 s + 600 s
  = 1.97 core-h of solver time plus CNF writing (about 1 s per cube, <= 0.3 core-h): <= 3 core-h; about 15-30 min wall
  on 10 shards. Pilot in this session: controls plus a few cubes of 96 on one shard.
* **Stop rule**: all units recorded, a failed control, or the caps above.
* **STATUS / ROADMAP**: a STATUS 3 section with the two-arm table and the reading; E-261110-06 row updated by the rule;
  week item 4 marked done.

## Amendments

### 2026-11-13: amendment 1, pilot (no plan change)

`OUT_DIR=results/pilot LIMIT=4 SHARDS=10 bash run.sh 1` (one shard alone, 0.006 core-h, 20 s wall): controls pass
(c1 the three plain hashes equal the records; c2 nine distinct unfixed literals and 512 cubes on both arms; c3 the
pinned Roest-Vigh chirotope with the eight cubes of pair (0, 5): cube 2 SAT, the cube read off the pinned model, the
other seven UNSAT-SOLVER; cube 2 on the unpinned formula SAT; the unpinned formula without a cube SAT). Units:
map 96 cubes 0, 10, 20, 30 UNSAT-SOLVER in 0.2, 10.6, 7.3, 0.1 s (each solver log ends `s UNSATISFIABLE`). Not a
reading: four cubes on an unloaded machine; their mean (4.5 s) times 512 is about 2.2x the monolithic time of 96, so
PARK is the likelier outcome, but the cube times are far from uniform. Gate met (controls pass, no cube at its cap):
the run starts unchanged by the owner (`launch.sh 13-04 start`). The calibration unit 845 and shard 0 were not
exercised in the pilot (same code path as the cubes, `pilot.solve` without units).
