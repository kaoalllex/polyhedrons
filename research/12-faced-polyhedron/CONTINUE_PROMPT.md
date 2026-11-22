# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, lead review approved and applied; new week starts)

* Branch `lab/2026-11-22` (from `main` after the `lab/2026-11-19` PR). Week plan: `ROADMAP.md` "Week plan" (source
  `reviews/strategy-review-2026-11-22-final.md`, owner-approved). Next: **item 1, P6 stage A** (E-261117-04): write
  and commit `PLAN.md` (skill `experiment-start`; stages A-C, coverage argument, controls), then the (8, 3) rung and the
  enrichment control on the 790 free-C2 (8, 3) maps after a one-line permission (<= 1 core-h, <= 50 min wall).
* Item 2 (E-261119-02 amendment 7, 862 actions) runs only on maps item 1 leaves UNKNOWN or SAT-unrealized.
  Item 5 (close-out of the random 10 %, 97830 of 97830 UNSAT-SOLVER in untracked `results/stageB5-pass1*`) needs no compute.
* Session checks of the final review (K1-K3, scratch, not ledger) give the expected counts for the PLAN: 862 free
  half-turns on 790 maps; 45 equivelar (8, 3) and 111 equivelar (9, 4) symmetric codes; plain (9, 4) 1.4-23.4 s per map.
