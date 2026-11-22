# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, week item 1 done, item 2 skipped)

* Branch `lab/2026-11-22`. Week plan: `ROADMAP.md` "Week plan". Item 1 (E-261117-04 stage A, STATUS 3bk) done: the
  (8, 3) rung passed, only the two known maps SAT and realized; item 2 has no input (skipped).
* Next: **item 3, P6 stage B** (the (9, 4) equivelar census): a PLAN amendment in E-261117-04 with its unit tests
  first; raise the guards (`census.py` `run`: k <= 8, `enum_multi.c` `main`: extras > 8) to 9 and re-read the coverage
  argument; eight partitions of 9 through `p6.cycle_union` (`p6.py` is (8, 3)-specific: generalise F, G and the census
  directory); controls as in the week plan (111 symmetric equivelar codes, both 3au (9, 4) classes, a completion flag
  per pattern); 10-min probe, root-stride shards if it projects > 50 min wall; lab-run after a one-line permission.
* Item 5 (E-261119-02 close-out, untracked `results/stageB5-pass1*`) needs no compute; any order.
* Stage-A tooling to reuse: `run.sh` (`Q=` queue), `p6.py summary|followup`; the pinned control file `control_rv8.json`.
