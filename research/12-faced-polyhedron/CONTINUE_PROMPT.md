# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-02 stage A done; amendment 2 (pricing, rung) registered, owner launch pending)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2 stage A done, STATUS 3be: both families complete, every control exact
  (C3 3+3+3 (9, 4) 118 classes, C2 4 x 2 + 1 (9, 4) 12444; 0.24 core-h). No run in flight.
* In flight (item 2, amendment 2): owner launch `bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start`
  (rung (9, 3), rung (8, 3), pricing in turn per shard, <= 1.5 h); results in `results/stageB-<queue>/`. Then: rung
  check, per-stratum decided fractions by 30/60/120/600 s, the pass-1 projection, amendment 3 (two-pass, owner 2026-11-20).
* For the lead: 12444 C2 maps leave < 3 s per map in stage B's 10 core-h against a 600 s cap; after pricing, either a
  C2 subset rule or a larger budget is needed (owner decision).
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
