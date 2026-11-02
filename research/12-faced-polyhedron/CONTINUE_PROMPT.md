# Prompt to continue this research in a new session

The standing rules are in the root `CLAUDE.md`, which loads automatically. This file holds only the hand-over:
what was in flight when the last session ended. The `session-handover` skill rewrites the block below. Paste the
part under the line into a new Claude Code session on `kaoalllex/polyhedrons`.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

1. Read `STATUS.md` and `ROADMAP.md`.
2. Read the hand-over below.
3. Unless the owner names another task, work on the top `open` row of `ROADMAP.md`, using the `experiment-start`
   skill.

## Hand-over (2026-11-02, daytime)

* **Branch.** Still `experiment/E-261101-25-chirotope-first` (on top of `claude/strategy-review-2026-11-01`); all
  night-6 follow-ups are committed there. Owner: one PR of the stack into `main` when convenient (`verify` green).
* **Night 6 concluded**: E-261101-23 and E-261101-25 UNDERPOWERED (a final-polynomial LP without a time limit hung
  9 of 10 shards); their `CONCLUSION.md` files and `reports/NIGHT_REPORT_2026-11-02.md`. Fixed: LP time limits
  (`LP-TIMEOUT`), the seed cap holds inside a step (TIME-CAP), exact final polynomials store their certificates,
  drat-trim overruns become `CHECK-TIMEOUT`, E-23 logs a start line per unit.
* **Launcher** `overnight/launch.sh start|status|stop EXPERIMENT_DIR [SHARDS]` replaces `run_night6.sh`: unknown
  commands print usage, a second start is refused, `status` flags a running shard silent for 60 minutes.
* **Running (daytime, owner's laptop)**: E-261102-01, the 32 types night 6 did not reach at k = 8, 9, 8 shards
  (`PLAN.md` pre-registered with predictions P1-P5). Expected wall time ~1.5 h.
* **Evening session**: (1) `experiment-conclude` for E-261102-01 (core-hours from the manifests, P1-P5,
  `candidate-check` on any realized model, keep every UNSAT's CNF / proof / hashes); (2) write an independent
  checker for the stored final-polynomial certificates (re-derive each three-term Grassmann-Pluecker relation and its
  sign pattern from the bracket indices, check the multipliers' identity in exact arithmetic) and run it on the
  type 0 k = 9 certificate; (3) set E-261102-02 to `running` in ROADMAP and its README when the owner launches it.
* **Night 7**: E-261102-02 (chirotope-first night run 2: `--rounds 40`, `--seed-minutes 40`, all 10 seed slices),
  pre-registered; it runs before the benchmark ladder E-261101-26 at the owner's request (PROTOCOL 8a gate and its
  consequences in its `PLAN.md`).
* **Open owner actions:** merge the branches; send the first external e-mail (E-261101-11 README "Why and whom");
  Zenodo DOI (Phase 0 TODO).
* **Next ROADMAP items:** E-261101-26 (benchmark ladder), E-261101-06 (rank-3), E-261101-21, E-261101-22,
  E-261101-18, E-261101-09, E-261101-11, E-261101-16.
* **Do not** use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (floors at 0, E-261101-07).
