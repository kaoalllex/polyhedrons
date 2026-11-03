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

## Hand-over (2026-11-02, evening, before night 7)

* **Branch.** Still `experiment/E-261101-25-chirotope-first` (on top of `claude/strategy-review-2026-11-01`); all
  work committed there. Owner: one PR of the stack into `main` when convenient (`verify` green).
* **Done this session**: E-261102-03 and E-261102-04 pre-registered with their pilots (`PLAN.md` Amendments of each;
  `experiment-log.md`). `ladder.py` (E-261101-26 harness) gained `run --alt`, `--timeout`, `--engine genus-ladder`, a
  budget in each unit's key (a task can run at several budgets), and `score --cutoffs` with per-unit binding limit,
  budget fraction, alternations, highest k realized, best energy.
* **In flight (night 7, owner launches ~21:00 from `research/12-faced-polyhedron/`)**:
  * `bash overnight/launch.sh start experiments/E-261102-03-chirotope-alt-cap-or-wall 10` (20 units x 120 min,
    ~45 core-h, ~4.5 h);
  * `bash overnight/launch.sh start experiments/E-261102-04-genus-ladder-engine-score 4` (~20 core-h, ~5.2 h).
  * Collect: `launch.sh status DIR`; results in `DIR/results/<shard>/results.jsonl`; score over all shards with
    `cd experiments/E-261101-26-engine-benchmark-ladder && python ladder.py score ../E-261102-0N-.../results/[0-9]*
    --to ../E-261102-0N-.../results/scores.json` (`--cutoffs 40 120` for -03).
* **Next session, in order**:
  1. `experiment-conclude` E-261102-03 and E-261102-04 (any R4 / R5 success: `candidate-check` first). Then the
     decision on E-261102-02 written in -03's PLAN (amend / kill full-map form / engine-change row), and the STATUS 3b
     engine-score table gets both rows.
  2. By day: E-261101-06 (rank-3 SAT per type), the exact side; an independent checker of the three stored
     final-polynomial certificates (types 0 k = 9, 53 k = 9, 57 k = 8).
* **E-261102-02** stays blocked until E-261102-03 is concluded.
* **Open owner actions:** launch night 7 (above); merge the branches; send the first external e-mail (E-261101-11
  README "Why and whom"); Zenodo DOI (Phase 0 TODO).
* **Do not** use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (floors at 0, E-261101-07).
