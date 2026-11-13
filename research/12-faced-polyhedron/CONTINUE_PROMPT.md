# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, E-261112-01 concluded; no candidate)

* Branch `lab/2026-11-09`; prep and conclusion committed there, not pushed.
* E-261112-01 done: controls pass, 2,004/2,004 near-copy cells UNSAT-SOLVER, 0 SAT, 8.01 core-h; OPEN, instance scope
  (`CONCLUSION.md`, STATUS 3ae). H-261112-01 open. No runs in flight; no raw files to move (`raw/` empty).
* NEXT (owner decision): week item 1B, Stage B prep (E-261112-02: PLAN, independent rank-4 count, orbits, 50-cell
  timing; no compute before its gates, night only on the owner's budget), or week item 2 (E-261110-02 prep).
* Checks: run integrity verified at conclusion (unit set = list hash, commit/env identical in all shards, 50/50
  controls); trace.py 0 errors. verify_all --quick last ALL PASS before amendment 2 (gate code: test_stage_a,
  startup check 3); the conclusion changes no code.
* For the lead (unchanged): crease lemma proof/five outside chords; pencil planar lemma vs implemented clauses.
