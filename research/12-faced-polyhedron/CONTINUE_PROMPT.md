# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-08, lead review applied)

* Branch `lab/2026-11-07`. Lead review `reviews/strategy-review-2026-11-08.md`, approved by the owner; its week plan
  is in `ROADMAP.md`, its wording fixes are applied (M1, M2, L1-L3; M5 left as is: E-261103-03 is active again).
  No active process.
* DONE (2026-11-08): runner parameters (`--s5-queue`, `--timeout`, `--s5-checker-timeout`, `--s5-budget-seconds`) and
  PLAN.md amendment; `test_tranche.py` 22 OK. Unit (a) ran via the real entry point (`results/item1a/`, 822 s wall, one core,
  controls passed): 9/13 UNSAT-VERIFIED (94, 100, 102, 111, 123, 171, 177, 184, 199), 4 TIMEOUT at 60 s (174, 176, 181, 200),
  no SAT. Prediction (>= 10/13) missed; (a) >= 7/13, so item 3 is not dropped. Scope: these plain formulas at 60/120 s.
  Not yet written to STATUS/ledger (use `experiment-conclude`).
* NEXT: F = 9 positive control (c) from an E-261107-01 Phase B solid; then the owner launches (b) + map 74 + (c) on 8
  workers (needs its own queue file; the 4 new timeouts may join (b) by owner decision). Map selection:
  `reviews/strategy-review-2026-11-08-runtime-patterns.py`.
* STATUS sections 3d-3s compacted (review M4, wording only); STRATEGY §1 C3 wording updated at the owner's request.
* Verification: no candidates, no run; `trace.py --check` run after the ledger edit.
