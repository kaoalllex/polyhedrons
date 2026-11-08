# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-08, lead review 2026-11-08d approved and applied)

* Focus moved to S5 at (10, 4), gated by a speed-up benchmark (`STRATEGY.md` §1, owner 2026-11-08). The (8,2)/(9,3)
  negative result (all admissible plain formulas UNSAT-VERIFIED, geometry PROVED-1 conditional) is a side track towards
  a note that must say no independent review took place. GitHub Actions trial approved.
* Week plan in `ROADMAP.md` (lead review 2026-11-08d, items 1, 2, 5 amended by review 2026-11-08e, owner-approved):
  1 grooved-box multiplicity control with a valid geometric negative (I-261108-04), 2 (10,4) speed-up benchmark
  (kissat and cube-and-conquer; Phase A correctness screen on six (9,3) maps, Phase B on (10,4) maps 96, 85, 146, 845
  incl. both slow strata, censored projection, holdout; owner launch <= 2 h), 3 independent census (I-261108-08),
  4 second encoder on six maps, 5 union of two matched solids (explore, I-261108-11 stage 1). The contraction sieve
  moved out of the week; the note package starts with the soundness chain of review 08e Follow-up Q3.
* NEXT: week item 1 in a lab session (no night). Item 2 needs `experiment-start` (new experiment, kissat pinned, cube
  format, projection formula in `PLAN.md`); items 1 and 2 may be prepared in either order, but a (10,4) UNSAT carries the
  item 1 caveat until item 1 passes.
* Branch `lab/2026-11-08` (from `main` 49e2a5c after PR #6; pushed): the week plan's only branch. No active process.
* For the lead: after week item 5 concludes, decide the next stages of I-261108-11 (owner 2026-11-08): if the
  mechanism works, general genus-0 pieces (e.g. Szilassi + a cube on 3 planes), the (9, 4) sources, the rigid (9, 3)
  cross-check and the 12-face filter on the 59 types; if it fails, record why and do not move to harder pieces.
