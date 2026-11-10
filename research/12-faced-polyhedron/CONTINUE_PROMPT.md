# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-10, after the owner approved the lead session's four items)

* Branch `lab/2026-11-09`. No active process, no result, no candidate. Compute is laptop-only (owner, 2026-11-10).
* Focus (`STRATEGY.md` §1, owner 2026-11-10): S6 at (10, 3) first; S1 with the genus free at 9, 10, 12 faces, gated
  by the 8-plane family scoring; S5 at (10, 4) only under the rule of E-261110-06. `SPEC.md` has S6.
* Week plan in `ROADMAP.md` (owner-approved 2026-11-10): 1 filing - done; 2 E-261110-02 (prep, then the owner's
  night, approved, after amendment 1); 3 E-261110-01 then E-261110-03; 4 cube-and-conquer pilot on (10, 4) maps 96,
  85; 5 E-261110-05. Items without a night or an approval may be chained in one session (`PROTOCOL.md` §8b).
* Harness items (ROADMAP Phase 0, owner-approved): one lab session each, between week items, never during a night.
* NEXT: week item 2 prep: `code/lutz_import.py` (Lutz's list of the 20 maps as untrusted data), `--target S6` in
  `verify_candidate.py`, the (7, 1) and (12, 6) controls, the two-map pilot, the smoke test, amendment 1.
* Verification: `trace.py` 0 errors; no solver, no code change. Unverified: the map counts 821 and 751,593 (CLAIMED)
  and the session's wedge tables (E-261110-01 recomputes them). For the lead: none.
