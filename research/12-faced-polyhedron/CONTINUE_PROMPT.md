# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-17, week item 3 stage B awaiting launch)

* Branch `lab/2026-11-16`. Week item 3, E-261116-07 (P3 v2, CP-SAT host `p3.py`): pre-registered `55f26432`; unit
  tests pass; stage A all PASS (L0 240/240 K13, controls, gauge reachability, L1 (7, 21) OPTIMAL in 8 s and bridged);
  pilot: all five units at the 60 s cap (PLAN amendment of 2026-11-17). Results of stage A and pilot are uncommitted
  in `results/` (commit them with the conclusion).
* In flight: owner launches stage B: `bash research/12-faced-polyhedron/overnight/launch.sh 16-07 start` (AC power;
  48 units, 5.5 core-h, about 35 min wall; then `status`). Next session: `python3 p3.py summary results`, then
  `experiment-conclude` against the PLAN's outcomes and tree; any `--all-pairs` PASS goes through `candidate-check`.
* `verify_all --quick` not rerun since item 2 (no shared code changed); run it once at the conclusion.
* Item 4 starts with `candidate-check` of the 16 S6 (10, 2) files of E-261113-02 (13 maps); it does not need stage B.
* Item 5's PLAN now includes the C2 4 x 2 + 1 arm with a far plane as infinity (reuse `n2.draw` / `n2.chart` at nine
  planes); it states its own power (the seven-plane rate is a rung-below number).
* For the lead: plane-only formulas for the 20 (11, 5) Aut+ = 2 maps and the (9, 4) one-face-involution maps are
  possible only as a new registration; their speed at 12 elements was not measured.
