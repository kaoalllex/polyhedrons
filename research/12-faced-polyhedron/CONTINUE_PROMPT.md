# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, E-261112-01 concluded; no candidate; next: week item 2)

* Branch `lab/2026-11-09`; prep and conclusion committed there, not pushed.
* E-261112-01 done: controls pass, 2,004/2,004 near-copy cells UNSAT-SOLVER, 0 SAT, 8.01 core-h; OPEN, instance scope
  (`CONCLUSION.md`, STATUS 3ae). H-261112-01 open. No runs in flight; no raw files to move (`raw/` empty).
* NEXT (owner, 2026-11-13): week item 2, E-261110-02 prep (S6 (10,3); (10,2) formula and foreign-model bridge gates
  first). Week item 1B (Stage B, E-261112-02) deferred until after item 2: Stage A gives no reason for it.
* Checks: run integrity verified at conclusion (unit set = list hash, commit/env identical in all shards, 50/50
  controls); trace.py 0 errors. verify_all --quick last ALL PASS before amendment 2 (gate code: test_stage_a,
  startup check 3); the conclusion changes no code.
* For the lead (unchanged): crease lemma proof/five outside chords; pencil planar lemma vs implemented clauses.
