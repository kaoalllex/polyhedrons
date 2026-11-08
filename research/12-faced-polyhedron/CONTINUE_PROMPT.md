# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-08, review 2026-11-08c, item 5a prep done)

* Branch `lab/2026-11-07` (unpushed; old SHAs before the 2026-11-08 rewrite map via
  `reviews/strategy-review-2026-11-08b-commit-map.txt`). Week plan in `ROADMAP.md`: items 1-4 DONE, item 5 amended by
  `reviews/strategy-review-2026-11-08c.md` §2. No active process.
* (9,3) plain: 45/203 UNSAT-VERIFIED, 60 TIMEOUT at 60 s, 98 unattempted, 0 SAT (STATUS 3d).
* NEXT: owner launches item 5a (one night, AC power, lid open), from the repo root:
  `bash research/12-faced-polyhedron/overnight/launch.sh 03-03 start` (then `status`, `stop`; restart resumes). Queue
  `queue_item5a.json` (158 maps, control (c) at the head of each of 10 shards), solver 1800 s, checker 2700 s, <= 8 h per
  shard, 80 core-h; results in `results/item5a/`. Startup check passed (`PLAN.md` amendment 2026-11-08, item 5a). Then
  `experiment-conclude`; all UNSAT -> lead review (review 2026-11-08c §4).
* Local disk: about 7 GB of old gitignored proofs in `experiments/E-261103-03-*/results/` may be deleted (owner's call).
* Verification: `test_pilot` + `test_tranche` 36 OK after the item 5a runner change; no candidates.
