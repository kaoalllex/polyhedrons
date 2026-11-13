# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, week items 2 and 3 concluded)

* Branch `lab/2026-11-09`, committed, not pushed. Nothing in flight; raw output moved by `overnight/move_raw.py`.
* E-261113-02 done (STATUS 3ah): 153/153 SAT at (10, 2), median 0.83 s; bridge 16/153; readings LIGHT, CHEAP.
* E-261110-05 done (STATUS 3ai): V2 UNSAT-SOLVER on all eight; V1 SAT on five (9, 3) maps; H-261110-01 weakened.
* NEXT: (a) CHEAP branch of E-261113-02: `make_queue.py` gains the full 865 x 3 seeds (registered follow-up, no new
  amendment), then one owner launch; (b) week item 4 (cube-and-conquer, `experiment-start`, Opus, medium);
  item 5 prep only.
* Checks: both runs' controls pass; `summary.py` on the final results; no code changed since `verify_all --quick`.
* For the lead: (1) the bridge realizes ~10 % of (10, 2) models where objects exist: a (10, 3) SAT would stall at
  realization, not at the solver; (2) LOCAL at (8, 2) asks for one core-mining session (outside the week plan);
  (3) symmetric (10, 3) route: only fixed-face C2 and improper symmetries left; does S6 (10, 3) keep first place?
