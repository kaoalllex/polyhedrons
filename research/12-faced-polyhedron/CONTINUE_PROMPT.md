# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-02 stage A done; pricing and the stage-B amendment next)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2 stage A done, STATUS 3be: both families complete, every control exact
  (C3 3+3+3 (9, 4) 118 classes, C2 4 x 2 + 1 (9, 4) 12444; 0.24 core-h). No run in flight.
* Next (item 2): price one map per multiplicity stratum (four C3, seven C2; README "Stage A results") with the stage-B
  formulas (C3 omsat C3 clauses, standard chart; C2 plane-only moved chart, `build_sym` gauge), then the stage-B
  amendment to `PLAN.md` with its rung and controls; the owner launches stage B (<= 10 core-h, 10 shards).
* Maps per stratum: `symcensus.py summary results/stageA` rebuilds the full `summary.json` (codes, actions) from the
  committed `results.jsonl` (run it with `~/.venvs/polyhedra/bin/python`).
* For the lead: 12444 C2 maps leave < 3 s per map in stage B's 10 core-h against a 600 s cap; after pricing, either a
  C2 subset rule or a larger budget is needed (owner decision).
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
