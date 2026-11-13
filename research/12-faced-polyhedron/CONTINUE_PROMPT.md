# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, E-261110-02 concluded: 20/20 TIMEOUT, OPEN, escalated; no candidate)

* Branch `lab/2026-11-09`, committed, not pushed. No runs in flight. Raw `attempt_*/` output to be moved by
  `overnight/move_raw.py` after this commit (owner or next session, if not done here).
* E-261110-02 night: 20.03 core-h, 2.0 h wall, controls pass; all 20 (10,3) maps TIMEOUT at 3600 s (kissat, no proofs);
  OPEN@20.03 core-h, solver-limited (`CONCLUSION.md`, STATUS 3af). "> 20 % timeouts" rule -> escalated.
* NEXT: the owner decides: week item 1B (Stage B, gated PLAN first) or 3 (thin wedges, PLAN first); items 4, 5 are lab
  items. No further S6 (10,3) compute without a new PLAN amendment saying what is different.
* Checks: summary.py on the night (20 TIMEOUT, verdict escalate); trace.py 0 errors; no code changed.
* For the lead: S6 (10,3) after 0/20 at 3600 s: changed set-up (symmetry breaking via map automorphisms, cube-and-conquer
  as in item 5, another solver/options, longer cap on 1-2 maps) or drop to backup? Unchanged: crease lemma / five outside
  chords; pencil lemma vs clauses; 3 of 6 foreign (10,2) models look non-realizable (fp numerical).
