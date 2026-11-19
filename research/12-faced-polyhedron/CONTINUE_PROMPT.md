# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-19, lead review 2026-11-19 and its Codex reconcile approved and applied)

* Branch `lab/2026-11-19` (new week branch from `main` after the 2026-11-18 PR); week plan in `ROADMAP.md`
  (owner-approved `reviews/strategy-review-2026-11-19.md` and `-reconcile.md`). No runs in flight. Week 2026-11-18 done (STATUS 3az-3bc); E-261116-08 deferred by the owner; (11, 5) closed for the laptop.
* Next: week item 1, E-261119-01 (P3-sym power ladder): PLAN with unit tests (free C2 action, units U1-U4, map blocking
  by complete paired runs under the normaliser, its synthetic and pinned controls), then the owner's evening run (hard
  <= 20 core-h); no C3 night follows from it. Item 2, E-261119-02 (symmetric nine-face census, stage A: 0 or 3 fixed
  triangles, multiplicity <= 3, 18 C3 demand classes, gate per family), may be prepared while item 1 runs. Item 3 (P6)
  only if neither census family advances.
* Watch: U2 (8, 30) and U3 (9, 39) are predicted INFEASIBLE (3d's proofs are for the map CNFs, not P3); a SAT there
  goes to the clause-level diagnostic of the ROADMAP tree, never a result. Pilots go through `run.sh` with a manifest. Mirror (Cs) families are out of domain; do not schedule them.
* For the lead: none yet.
