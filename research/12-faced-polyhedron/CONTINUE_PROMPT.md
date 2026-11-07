# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-07, lab: E-261107-01 and E-261103-06 concluded)

* Branch `lab/2026-11-07`. Week plan items 1 and 2 done: E-261107-01 (30 nine-plane arrangements INFEASIBLE,
  STATUS 3t); E-261103-06 R1 (4 valid torus starts blocked by the barrier, UNDERPOWERED, parked, STATUS 3u).
  No active process.
* Week plan item 3 done: `map/index.html` colours nodes by state, shows the CONCLUSION verdict paragraph on click
  (`conclusion` field from `verification/trace.py`), traces ancestors (blue) and descendants (orange), witnesses are
  big stars in their own band. Syntax checked with `node --check` and `trace.py --check`; not opened in a browser.
* NEXT: week plan exhausted; ask the owner to open `map/index.html` and call the lead review.
* For the lead: (1) nine-plane engine is cheap (about 13 s per exact decision): coverage is limited by the
  arrangement source, not solve time. (2) embedded-first R1 blocks on local mesh folds at ring <= 1 after about
  5 steps; decide whether to fund a repaired flattening (tangential regularisation, contact-sliding barrier,
  finer mesh) before R2'. Open defect: start construction fails for j = 4.
* Verification: no candidates; no shared-code change, no verify_all run; trace.py run after the ledger edit.
