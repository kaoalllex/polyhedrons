# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-18, week items 1 and 2 done)

* Week branch `lab/2026-11-18`. Week plan: `ROADMAP.md` -> Week plan (`reviews/strategy-review-2026-11-18.md` §1).
* Item 1 done: E-261118-04 concluded on its pilot by the owner (STATUS 3az, OPEN-LOW; formula option (a), plane S kept).
* Item 2 done: E-261118-01 (STATUS 3ba): face-transitive (8, 3) classes 1-5 all UNSAT-SOLVER; Roest-Vigh's class SAT and
  realized by the bridge in < 1 s (a cheap rung control for item 3).
* Next: item 3, P3-sym (E-261118-02; Opus high). Its prep adds the dirty-tree refusal to `overnight/launch.sh`; it needs
  its `PLAN.md` first, with the unit tests run in that commit.
* For the lead: (1) the owner's curved face as stated (free vertices on the lines L_XY) needs a new, non-uniform encoder
  with a soundness note: worth it? (2) Two unrealized SAT models of map 29 (faces 5, 8; 1 and 4 wrong signs): a
  final-polynomial test or drop?
