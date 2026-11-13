# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, lead review applied: new week plan, S6 (10,3) first by symmetric realizations)

* Branch `lab/2026-11-09`, committed, not pushed. No runs in flight. Raw `attempt_*/` output of E-261110-02 still to
  be moved by `overnight/move_raw.py` (it refused once on a stale PID file of E-261108-01).
* Owner approved `reviews/strategy-review-2026-11-13.md`: week plan (`ROADMAP.md`), `STRATEGY.md` order and two
  rules; proofs declined: no DRAT in item 1, every UNSAT is UNSAT-SOLVER.
* NEXT: week item 1, E-261113-01 (Opus, high): `experiment-start`, PLAN first; (a) tetrahedral family of Lutz #15,
  (b) ten symmetric formulas; day run <= 10 core-h launched by the owner. Then items 2 and 3 (Opus, medium, one
  chained session), item 4, item 5 (prep only).
* Checks: `reviews/strategy-review-2026-11-13-symmetry.py` (group orders equal `maps_10_3.json`); trace.py 0 errors;
  no solver run, no code changed outside `reviews/`.
* For the lead: nothing open. Answered in the review: S6 (10,3) set-up; crease and pencil lemmas earn no session;
  the (10,2) non-realized models are measured by item 2.
