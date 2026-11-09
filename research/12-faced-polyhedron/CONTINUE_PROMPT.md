# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-09, lead review 2026-11-09 approved and applied)

* Focus: S5 at (10, 4). Gate decided (E-261108-03, STATUS 3x): kissat, about 475 core-h for all 1117 maps without DRAT
  (scenario); route = stratified first-witness sweep, fastest patterns first (`STRATEGY.md` §1, owner 2026-11-09).
* The note is deferred (owner, 2026-11-09): no session time on it unless a worthwhile result is found.
* Week plan in `ROADMAP.md` (lead review 2026-11-09, owner-approved): 1 stratum C first-witness night (360 maps,
  kissat, no DRAT, <= 80 core-h, owner launch); 2 Actions calibration (read GitHub's Actions terms first, record the
  finding in the PLAN; no job if not allowed); 3 cube-and-conquer pilot on maps 96, 85 (explore).
* NEXT: week item 1 is pre-registered as E-261109-06 (`dc4666b`: PLAN, frozen `queue.json` of 358 maps, smoke test
  passed); the owner launches the night (`launch.sh 09-06 start`), the next lab session concludes it
  (`summary.py`, `experiment-conclude`). Meanwhile: week item 2 prep (Actions terms first).
* Branch `lab/2026-11-09` (from `main` after the merge of `lab/2026-11-08`): the week plan's only branch. No active process.
* Done on the owner's request (not a week item): E-261109-05, the owner's "obstruction radar" (I-261108-06 power test):
  0 of 203 (9,3) maps killed, sieve parked (STATUS 3ac). Week plan unchanged; NEXT is still item 1 prep.
