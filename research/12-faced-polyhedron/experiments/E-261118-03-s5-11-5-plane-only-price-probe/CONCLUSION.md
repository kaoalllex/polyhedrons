# E-261118-03: conclusion

**Gate NIGHT, then the plane-only C2 slice of (11, 5) is UNSAT-SOLVER on all 20 Aut+ = 2 maps @ 1.0 core-h**: the
plane-only C2 formula in a moved chart decided every unit (80 of 80 UNSAT-SOLVER, map medians 17-90 s over four
kissat seeds) where the plain normalised formulas of E-261116-01 were censored at 3600 s. No SAT model, no candidate.
Planning only: no checked proof, no geometric negative.

* **Runs**: pre-registration `b74fcbe8`; amendment 1 (pilot, added control, run in session) `c537cafe`; amendment 2
  (the registered NIGHT follow-up on the other 18 maps) `85166c3b`. All runs on the laptop by `overnight/launch.sh
  18-03 start`, 10 shards, every shard `SHARD-COMPLETE`, `exit_status: 0`, no stop file:
  * control chain `prep/control` (10 shards, about 10 s each) and pilot `prep/pilot` (2 shards, 0.023 core-h);
  * probe `results/run`, 2026-11-19 05:59 UTC, maps 3634, 4096 x seeds 0-3: 0.125 core-h shard wall (61 s max);
  * follow-up `results/rest`, 06:02 UTC, the other 18 maps x seeds 0-3 (72 units): 0.838 core-h (358 s max).
  * Total about 1.0 core-h (shard wall sums from the attempt manifests; solver time 0.094 + 0.798 core-h) against
    4 core-h for the probe and 80 for the night. No sleep gap possible at these lengths (minutes).
* **Controls** (all PASS): N2 Szilassi chain through the runner: plane-only seeds 0-3 SAT, every model realized,
  `--target S5` PASS ((14, 21, 7, 0), the known Szilassi type); the standard chart (INF fixed, forced zeros) seeds
  0-5 UNSAT-SOLVER. Shard controls on every shard of both runs: convex f11 pinned SAT, wrong map UNSAT-SOLVER.
  Added in amendment 1 (fast UNSATs of a new encoding are suspect): `controls_12.py` on all 20 maps
  (`results/controls_12_all.json`): 5 random integer plane sets symmetric under the map's own involution, moved
  chart, `build_sym` gauge, pinned into the map's GP + symmetry + gauge formula: 100 of 100 SAT; every unpinned
  formula SAT. So the symmetry and gauge clauses admit genuine symmetric configurations at 12 elements; the UNSATs
  come from the embedding clauses together with the symmetry. `make_queue.py` recomputed the orientation-preserving
  automorphisms from the links: each of the 20 maps has exactly one involution with exactly one fixed face (and
  Szilassi's map Aut+ 42 with its half-turn: the function's control).
* **Prediction vs outcome**: P1 (CLOSED at the probe, ~75 %) failed: both medians about 41 s, gate NIGHT. P2 (a unit
  decides within 1800 s, ~35 %) held, all 80 did. P3 (control chain passes, ~85 %) held.
* **Exact verification**: no candidate; `verify_candidate.py` only on the control models (Szilassi, PASS). Every
  UNSAT record keeps its formula and CNF SHA-256 (`results.jsonl`); no proofs (owner, 2026-11-13).
* **What may be claimed**: for each of the 20 admissible (11, 5) maps with Aut+ = 2, the plane-only C2 formula of
  its involution (`omsat` `ALL_OPTS`, `build_sym` orbit-flip and mirror gauge, INF a generic plane) is
  UNSAT-SOLVER for kissat seeds 0-3 (SPEC §4, formula scope). Read for planning: no (11, 5) S5 object whose map
  automorphism group contains a proper half-turn, within this encoder, is expected. The speed (two orders of
  magnitude below the plain 12-element median) is NUMERICAL, these 20 formulas.
* **What may NOT be claimed**: any (11, 5) non-existence, even symmetric (no checked proof; mirror gauge soundness
  inherited from `omsat_sym`, not re-proved; no positive control with a fixed-face involution on a map with
  doubled pairs exists); anything about the 3962 asymmetric admissible maps (still priced out, STATUS 3aq);
  anything about improper symmetries (a mirror plane, inversion or rotoreflection: not run; the census Aut+ counts
  only rotations) or the four Aut+ = 3 maps (no C3 realization, PROVED-1, dialogue A7); that the speed transfers to
  other cases.
* **Hypotheses**: H-261101-07 (the (11, 5) part) unchanged, status open; evidence line added.
* **Verdict**: (11, 5) proper half-turn slice UNSAT-SOLVER@1.0 core-h, 20 of 20 maps x 4 seeds. The registered
  route ends: (11, 5) closes for the laptop (no further (11, 5) item without the lead).
* **Next step**: week item 5 (E-261116-08, S6 (10, 3) replay pricing) or the lead review. For the lead: (1) the
  plane-only fixed-face formulas decide 12-element S5 formulas in under 90 s; idea I-261119-01 (the same slice where a
  map census has involutions fixing faces: S6 (11, 4), (12, 5), nine-face S1 maps; not S0, whose half-turns fix no
  face, FD5). (2) Improper symmetries of (11, 5) maps are the
  only symmetric (11, 5) slice not run.
* **Rows updated**: `STATUS.md` 3bc and header, `ROADMAP.md` (row done, week item 4), `experiment-log.md`,
  `paper/OUTLINE.md` (B6 and change log), README, H-261101-07, idea I-261119-01, handover.
