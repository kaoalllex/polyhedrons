# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, week items 2 and 3 prepared; one owner launch pending)

* Branch `lab/2026-11-09`, committed, not pushed. Nothing in flight.
* OWNER: `bash research/12-faced-polyhedron/overnight/launch.sh 13-02 10-05 start` (on AC; then `status`). Expected:
  E-261113-02 ~0.3 core-h (153 (10, 2) units), then E-261110-05 <= 3 core-h (twelve (9, 3) units, cap 900 s).
* E-261113-02 pilot (PLAN amendment 1): controls pass, SAT in 0.2-3.6 s, seeds diversify; bridge realized 0 of 6.
* E-261110-05 stage 1 (amendment 1): controls pass; (8, 2) V2 and V1 all UNSAT-SOLVER -> reading LOCAL.
* NEXT after the run: `experiment-conclude` for both (Opus, medium); 13-02 under 0.3 core-h -> the full 865 (tree).
  Then item 4, item 5 (prep only).
* Checks: `verify_all.py --quick` ALL PASS after the encoder option and tranche seed; `test_tranche` 27 OK.
* For the lead: (1) LOCAL at (8, 2) asks for one core-mining session: not in the week plan, schedule it?
  (2) the bridge's hinge stage returns one loss from all 6 random starts (one attractor), so its restarts add nothing.
  (3) symmetric (10, 3) route: only fixed-face C2 and improper symmetries left; does S6 (10, 3) keep first place?
