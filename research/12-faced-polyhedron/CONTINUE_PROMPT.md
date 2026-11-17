# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-17, week item 3 concluded; item 4 next)

* Branch `lab/2026-11-16`. Week item 3, E-261116-07 (P3 v2) concluded: UNDERPOWERED@5.5 core-h, 48/48 stage-B cubes
  UNKNOWN at their caps, no model (also in cube 5 with Roest-Vigh and Mizhaev); gate not passed, method parked
  (STATUS 3aw, ROADMAP parked-methods row). Two unit tests had failed since pre-registration (gauge in the test
  helper); fixed in `test_p3.py` only, now a `verify_all` line; `verify_all.py --quick` ALL PASS at the conclusion.
* No run in flight. Raw output moved with `overnight/move_raw.py` after the conclusion commit.
* Next: week item 4 (P4 probe, E-261117-03), starting with `candidate-check` of the 16 S6 (10, 2) files of
  E-261113-02 (13 maps). Then item 5 (the owner night, E-261110-04), whose PLAN takes the C2 4 x 2 + 1 arm.
* For the lead: does a P3 rerun earn a row, measured first on cube 5 (Roest-Vigh as a solution hint or partly pinned,
  more workers, a longer cap)? The coupled P3 + P4 test is not triggered (no models).
* For the lead: plane-only formulas for the 20 (11, 5) Aut+ = 2 maps and the (9, 4) one-face-involution maps are
  possible only as a new registration; their speed at 12 elements was not measured.
