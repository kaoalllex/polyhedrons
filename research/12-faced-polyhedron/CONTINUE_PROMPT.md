# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, week item 4 concluded)

* Branch `lab/2026-11-09`, committed, not pushed. Nothing in flight; raw output moved by `overnight/move_raw.py`.
* E-261113-04 done (STATUS 3aj): segment-order cubes PARK (r >= 1.07 on 96, >= 0.92 on 85), 1.08 core-h;
  E-261110-06 -> at most one explore night, only by a lead review.
* NEXT: week item 5 prep only (E-261113-03, Opus, high). The CHEAP branch of E-261113-02 (full 865 x 3 seeds) is held
  by the owner (2026-11-13) for the lead: it changes no current decision and is priced at ~3.3 core-h.
* Checks: controls and calibration pass, `summary.py` on the final results; no shared code changed since
  `verify_all --quick`.
* For the lead: (1) march_cu is now built by the owner (`~/bin/march_cu`, CnC `705b60c6`, SHA-256 `f3554726...`):
  a march_cu cube pilot on 96 / 85 would be a changed set-up; decide whether it earns a row. (2) bridge ~10 % at
  (10, 2); (3) LOCAL at (8, 2) core mining; (4) does S6 (10, 3) keep first place; (5) run the full 865 of
  E-261113-02 (it could only show a heavy tail, unlikely at max 5.2 s on 150 units, or refine the 10 % bridge rate) or drop it.
