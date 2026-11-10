# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-10, after the E-261109-06 night)

* Focus: S5 at (10, 4) (`STRATEGY.md` §1); route = stratified first-witness sweep with kissat, no DRAT.
* The note is deferred (owner, 2026-11-09): no session time on it unless a worthwhile result is found.
* Week plan in `ROADMAP.md` (lead review 2026-11-09, owner-approved): 1 stratum C night - **done** (E-261109-06, STATUS
  3ad: 360/360 UNSAT-SOLVER, 0 SAT, 63.84 core-h; f = 7.16 prices A + B at 6.06 laptop nights > 4, so the tree sends
  A and B to Actions after item 2, no stratum A night proposal); 2 Actions calibration (read GitHub's Actions terms
  first, record the finding in the PLAN; no job if not allowed); 3 cube-and-conquer pilot on maps 96, 85 (explore).
* Owner, 2026-11-10: GitHub Actions parked, out of the near-term plan (item 2 and I-261108-07); the route is laptop-only.
* NEXT: week item 3 (cube-and-conquer pilot on maps 96, 85, day run <= 3 core-h); its result sets the design of the
  laptop A/B nights, which need the owner's approval (about 6 nights at f = 7.16, fewer with cubes).
* Branch `lab/2026-11-09`: the week plan's only branch. No active process. Verification: no SAT, no candidate; the
  conclusion reused the run's records (solver logs, model-checked controls, hashes); `trace.py` 0 errors.
