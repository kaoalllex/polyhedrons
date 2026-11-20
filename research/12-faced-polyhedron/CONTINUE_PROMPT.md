# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-01 concluded; E-261119-02 stage A pre-registered, owner launch pending)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* E-261119-01 (week item 1) done, STATUS 3bd: discovery PASS (free C2 (8, 36) returned both known maps, realized), then
  UNKNOWN at 1.5 h; (8, 30) and C3 (9, 39) UNKNOWN at 1 h (no refutation power); symmetric (8, 3) slice OPEN.
* 2026-11-20: the first stage-A launch ran no unit (bash `SECONDS` gave a 0 s cap); repaired to `BUDGET` (PLAN amendment 1).
* Next (item 2): the owner re-runs `bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start` (10 x 360 s,
  <= 1 core-h; the unit tests run in shard 0); then `python3 symcensus.py summary results/stageA`: per-family gate (C3,
  C2), lists, strata; pricing one map per multiplicity stratum and the stage-B amendment follow.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a first launch stopped and killed with no record, 8.5
  core-h discarded); the normaliser rule under-blocks (amendment 1), so E-261119-02's per-map blocking uses invariant copies.
