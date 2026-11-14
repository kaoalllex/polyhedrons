# E-261110-02: conclusion

2026-11-13. One owner laptop launch (`launch.sh 10-02 start`), 10 shards, root `results/run/`, commit `a87286bd` (owner
amendment, no proofs) in every attempt manifest, tree clean except the untracked `results/`, `queue.json` sha256
`942b0fed...8fb6` and `no_proof: true` as pinned, Python 3.14.6, kissat 4.0.4 (`8af8e56f`). One start per shard, no
restart, no Actions run.

* **Runs**: started 2026-11-13 07:07:25 UTC; every shard `SHARD-COMPLETE`, `exit_status 0`; all ended 09:07:36 UTC, wall
  **2.0 h** of the 10 h cap. Cost: **20.03 core-h** of the 80 core-h cap (sum of `core_hours` in the ten attempt
  `manifest.json`; `manifest.txt` records only start and exit status), single-thread shards. No sleep gap: kissat process
  time 3550.8-3560.6 s per map unit at the 3600 s wall cap. Per shard: the two control (c) units, then Lutz maps k and
  k + 10.
* **Controls**: in all 10 shards the encoder controls report `CONTROLS-PASS` (eight-plane SAT models checked, hinge-warm
  geometry EMBEDDED), the (10, x) positive control (c) is SAT with `model_checked`, and the negative control (c) is
  UNSAT-SOLVER as the owner amendment expects (20/20 control units pass). The positive control is a pinned formula decided
  in < 0.1 s, so it shows the path can return SAT; it does not measure power on the unpinned (10, 3) formulas.
* **Results**: 20 of 20 maps recorded, every one **TIMEOUT** (`ended_by: solver_timeout`, 3600 s), 0 SAT, 0 UNSAT-SOLVER,
  0 UNSAT-VERIFIED. Formulas: `submap=True`, 11,167-11,178 variables, 151,153-151,189 clauses, 20 distinct formula and
  canonical-map SHA-256 (in `results/run/*/results.jsonl`); solver peak 0.44-0.64 GiB. `summary.py` verdict:
  "TIMEOUTS>20%: record, escalate". No bridge run (no SAT), no `results/CANDIDATE`.
* **Prediction vs outcome**: P1 (all 20 decided, ~50 %): **missed**, none decided. P2 (at least one SAT, ~25 %): not
  observed; with 0 decisions this says nothing about existence. P3 (median decided time < 10 min, ~60 %): not
  measurable (no decision); the pilot's 2/2 TIMEOUT at 1200 s had already put it in doubt. P4 (proofs within 48 GB):
  void, the owner amendment removed proofs. The handover's expectation "> 20 % timeouts likely" held.
* **Exact verification**: nothing to verify: no SAT, so no bridge, no `verify_candidate.py --target S6` and no
  `candidate-check`; no UNSAT used as evidence.
* **What may be claimed**: NUMERICAL, instance scope: kissat 4.0.4 with default options decides none of the 20 `submap=True`
  (10, 3) formulas of `maps/maps_10_3.json` within 3600 s on this laptop. As a cost observation only: at the same element
  count and cap, the plain (10, 4) stratum C formulas of E-261109-06 were all decided (148-2041 s); the formulas differ
  (submap, single adjacencies, no proofs in either), so no cause is implied.
* **What may NOT be claimed**: anything about the existence or non-existence of a (10, 3) S6 object, or of any single
  map's realization (a TIMEOUT is not a result, SPEC §4); that the formulas are hard in general (one solver, one
  configuration, one cap); support for H-261110-03 or its rival, or for H-261110-01 or its rival; that a longer cap
  would decide them (no growth data beyond 1200 s and 3600 s, both with 0 decisions). Not run: longer caps, other
  solvers or options, symmetry breaking, cube-and-conquer, the (11, 4) maps.
* **Verdict for the direction** (DR19 / DR8, S6 at (10, 3)): **OPEN@20.03 core-h, solver-limited** (20/20 TIMEOUT at
  3600 s, kissat, 1 configuration). No scenario move ("(10, 3) exists" stays 0.25, CONJECTURE); H-261110-03 and
  H-261110-01 stay open; S0 table unchanged.
* **Next step**: the pre-registered rule "> 20 % timeouts -> record, escalate" applies; no new ROADMAP row from this
  session. For the owner / lead: whether S6 (10, 3) gets a changed formula or solver set-up (a new PLAN amendment saying
  what is different) or yields its slot to week item 1B (Stage B) or 3. The 60 core-h left under the 80 core-h cap
  belonged to this night and are not carried over without the owner's word.
* **Rows updated**: `STATUS.md` section 3af and "As of"; `ROADMAP.md` E-261110-02 State `done`; H-261110-03 and
  H-261110-01 evidence; `experiment-log.md` (2026-11-13).
