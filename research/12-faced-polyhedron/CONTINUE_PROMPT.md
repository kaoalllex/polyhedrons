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
* Week item 2 = E-261108-03, launched and concluded 2026-11-09 (CONCLUSION, STATUS 3x): kissat wins, decides (10,4) maps 96, 85,
  146, 845 as UNSAT-SOLVER in 189-2749 s, best ratio 2.35x (no 10x), P(4) = P(16) = 475 core-h without DRAT; follow-up tree:
  Actions calibration (I-261108-07), no holdout; cube-and-conquer still open. The lead review decides.
* Week item 1 = E-261109-01, concluded 2026-11-09: m = 3, 4 grooved-box controls pass (STATUS 3y); the item 1 caveat is lifted.
* Week item 3 = E-261109-02, concluded 2026-11-09: independent growth enumerator agrees with E-261103-01 at (7,1), (8,2), (9,3) (240 / 203, STATUS 3z); (10,4) not run.
* NEXT: week item 4 (second encoder on six (9,3) maps, I-261031-03; <= 2 sessions + 1 core-h, 8 shards), then item 5.
* Branch `lab/2026-11-08` (from `main` 49e2a5c after PR #6; pushed): the week plan's only branch. No active process.
* For the lead: after week item 5 concludes, decide the next stages of I-261108-11 (owner 2026-11-08): if the
  mechanism works, general genus-0 pieces (e.g. Szilassi + a cube on 3 planes), the (9, 4) sources, the rigid (9, 3)
  cross-check and the 12-face filter on the 59 types; if it fails, record why and do not move to harder pieces.
