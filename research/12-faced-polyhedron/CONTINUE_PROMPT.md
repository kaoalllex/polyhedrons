# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-02 stage B: rung and pricing pass; amendment 3 (pass 1) registered, owner launch pending)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2 stage A done, STATUS 3be. Stage B amendment 2 run: rung held, pricing 33 of
  33 UNSAT-SOLVER in <= 0.29 s; `controls_b.py` (generic symmetric planes pinned SAT, wrong action UNSAT) PASS (README).
* In flight: owner launch `bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start` = pass 1, 12562
  records at 30 s, `BUDGET` 10 core-h, projected ~1.8 core-h, ~11 min. `maps/pass1.json` is untracked: if missing,
  `python stageb.py` first. Then: replication of the 33 pricing records, per-family reading per the amendment-3 tree,
  `move_raw.py`, STATUS line; UNKNOWNs -> pass 2 (owner).
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
