# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-12, E-261112-01 prep done; no target unit solved)

* Branch `lab/2026-11-09` (recreated from `main` after PR #10); prep committed there, not pushed.
* E-261112-01 amendment 1: exact list 4,024/1,006 (RV) and 3,992/998 (Mizhaev) orbits, all size 4, hashes pinned;
  `best_solid(edges_at_least=True)`; runner `run.sh`/`stage_a.py`; C0/C1/C2 pass at startup (`startup/`).
* NEXT (owner): `PILOT=1 bash overnight/launch.sh 261112-01 start` (10 shards, <= 0.5 core-h).
* NEXT (lab, after the pilot): pilot gate per PLAN; projection = mean unit wall x 2,004 + controls per start.
  Risk: the dialogue's 13.1 s/orbit already gives ~7.3 core-h before process overhead; a projection above the
  cap is an escalation to the owner (budget or cap), not a silent change. Day run only after the gate passes.
* Checks: cells.py list build, test_stage_a (4), E-261103-05 test_pilot, verify_all --quick ALL PASS.
* For the lead (unchanged): crease lemma proof/five outside chords; pencil planar lemma vs implemented clauses.
