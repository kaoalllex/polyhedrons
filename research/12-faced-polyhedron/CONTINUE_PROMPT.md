# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, week plan done: items 1, 3, 4, 5 done, item 2 skipped)

* Branch `lab/2026-11-22`. Week plan: `ROADMAP.md` "Week plan". Done: item 1 (STATUS 3bk), item 3 (3bl), item 5 (3bm)
  and item 4 (3bn: E-261117-04 concluded, the plain formulas of all 1071 admissible equivelar (9, 4) classes
  UNSAT-SOLVER, 0 SAT, 0 TIMEOUT, max 54.9 s, controls pass; 3.43 core-h, lab run). Item 2 skipped (no input).
* No run in flight. `results/stageC_c0|c1/` committed as for stage A (manifests, results, controls; raw attempt files
  ignored; `overnight/move_raw.py` after the commit).
* Next: the weekly lead review (`strategy-review`, strongest model): item 4's tree sends the all-UNSAT-SOLVER outcome
  to the lead, who re-plans the nine-face line; then the end-of-week PR into `main` after the owner approves.
* For the lead: the 60 s cap nearly bound on 3 maps (max 54.9 s, patterns 9 and 5+4); a re-plan that reuses these
  formulas at a lower cap must price that. Non-equivelar (9, 4) maps were never run by plain formulas.
* Tooling: `p6.py build-c|price|summary --stage stageC|followup --stage stageC`, `run.sh` (`Q=stageC_*`).
