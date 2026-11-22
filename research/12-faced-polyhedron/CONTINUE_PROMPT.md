# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, item 5 E-261119-03 done; E-261119-02's 10 % run stopped by the owner at 50 %, resumable)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 2, amendment 6: the owner stopped the random 10 % of (9, 5) pass 1 at 49194 of 97830 maps (all UNSAT-SOLVER,
  5 SKIPPED-STOP); `bash overnight/launch.sh 261119-02 start` resumes it. Its reading belongs to the owner's other session.
* Item 5 done on an owner exception to T + D >= 3 (STATUS 3bj): no admissible face-transitive (9, 7) map; the slice
  is empty at genus 4 and 7. Item 4 done (STATUS 3bi). Item 3 only if item 2 does not advance.
* Next: the lead review; the owner decides on chunks 10-99 after the 10 % (amendment 6).
* For the lead: the priced (9, 4) / (9, 5) stage-B UNSATs do not use the symmetry (3bi); a GF(2) parity pass over all
  978228 + 12562 records, then the plain formula, may be worth more than the remaining 90 %; not priced here.
* For the lead: L6 at k = 5, 6 is the open part of I-261108-09; a P3-sym UNKNOWN at nine faces carries no information (3bd).
* For the lead: budget overruns: E-261119-01 by 6.8 core-h; E-261119-03 ~2.0 against <= 0.9 core-h (an aborted launch,
  canonical code ~11 ms per map at valency 14). E-261119-01's normaliser rule under-blocks.
