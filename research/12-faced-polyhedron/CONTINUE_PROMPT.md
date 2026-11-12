# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-12, E-261112-01 prep + amendment 2; no target unit solved)

* Branch `lab/2026-11-09` (recreated from `main` after PR #10); prep committed there, not pushed.
* E-261112-01 amendment 1: exact list 4,024/1,006 (RV) and 3,992/998 (Mizhaev) orbits, all size 4, hashes pinned;
  `best_solid(edges_at_least=True)`; runner `run.sh`/`stage_a.py`; C0/C1/C2 pass at startup (`startup/`).
* Amendment 2 (owner): budget 12 core-h; pilot + automatic pilot gate + day run in one launch.
* NEXT (owner): `bash overnight/launch.sh 261112-01 start` (10 shards, ~1-1.5 h). Exit 6 = gate stop, 5 = candidate.
* NEXT (lab): `experiment-conclude` on the results; any SOLID -> `verify_candidate.py --all-pairs`, `candidate-check`.
* Checks: cells.py list build, test_stage_a (5), startup checks 1-3, E-261103-05 test_pilot, verify_all --quick ALL PASS (before amendment 2).
* For the lead (unchanged): crease lemma proof/five outside chords; pencil planar lemma vs implemented clauses.
