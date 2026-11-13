# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, week item 4 prepared)

* Branch `lab/2026-11-09`, committed, not pushed. Nothing in flight.
* E-261113-04 (week item 4, cube pilot on (10, 4) maps 96, 85): PLAN committed, pilot passed (amendment 1).
  march_cu could not be built in the session, so segment-order cubes (512 per map), as the row allows.
  Owner launch pending: `launch.sh 13-04 start` (10 shards, <= 3 core-h, about 15-30 min wall).
* NEXT: after the run, `experiment-conclude` E-261113-04 with `summary.py results` (reading PARK / BETWEEN /
  CUBES-WIN, E-261110-06 row by its rule); (a) CHEAP branch of E-261113-02 (full 865 x 3 seeds, owner launch);
  item 5 prep only.
* Checks: E-261113-04 controls pass, `summary.py --selftest` OK; no shared code changed since `verify_all --quick`.
* For the lead: (1) the pilot's four map-96 cubes average 4.5 s unloaded (x 512 ~ 2.2x monolithic): PARK likely
  for these cubes; march_cu stays untried. (2)-(3) of the previous hand-over stand: bridge ~10 % at (10, 2); LOCAL
  at (8, 2) core mining; does S6 (10, 3) keep first place.
