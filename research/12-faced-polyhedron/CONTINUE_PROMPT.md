# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-07, lab: E-261107-01 pre-registered)

* Branch `lab/2026-11-07`. E-261107-01 (week plan item 1, nine-plane solid-first pilot) is pre-registered
  (`PLAN.md`, commit f77d897 plus the amendment commit after it); status running, no process active.
* Startup check passed from `run.sh` (scratch output, cap 10 s): controls OK, runner defects fixed (PLAN Amendments).
* NEXT, owner launch (<= 2 core-h, about 15 min on 10 cores, AC power):
  `cd research/12-faced-polyhedron && caffeinate -dimsu bash experiments/E-261107-01-s5-nine-plane-solid-first-pilot/run.sh 0`
  (venv `~/.venvs/polyhedra`; output in `results/0`). Then `experiment-conclude`. After it: week plan items 2, 3.
* For the lead: (none yet).
* Verification: startup check only; trace.py 0 errors. No verify_all run (no shared-code change).
