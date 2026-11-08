# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-08, review 2026-11-08b applied)

* Branch `lab/2026-11-07` (unpushed; history rewritten 2026-11-08 without CNF/proof files, old SHAs map via
  `reviews/strategy-review-2026-11-08b-commit-map.txt`). Week plan in `ROADMAP.md`; item 1 amended by
  `reviews/strategy-review-2026-11-08b.md`. No active process.
* DONE (2026-11-08): unit (a) recorded (STATUS 3d, CONCLUSION, log): 9/13 UNSAT-VERIFIED, 4 TIMEOUT, 0 SAT. Evidence
  policy (owner): proofs checked in the run, then deleted; hashes and transcripts kept (`PROTOCOL.md` §5, `pilot.solve`,
  `tranche.pending`, evidence tests); every splittable run uses 8-10 shards, `run.sh` accepts up to 10.
* NEXT: owner launches item 1 (prep done, startup checked on 10 shards with 8 s / 10 s caps, scratch dir: control SAT, 17 maps
  TIMEOUT as expected, no stop file). Queue `queue_item1b.json` (control `control-f9` first, 17 maps), `PLAN.md` amendment
  2026-11-08. Command per shard k=0..9 from the repo root, venv active, `CADICAL`/`DRAT_TRIM` set, under `caffeinate -dimsu`:
  `python research/12-faced-polyhedron/overnight/run_overnight.py s5 --workers 1 --shard k --shards 10 --results-dir
  research/12-faced-polyhedron/experiments/E-261103-03-s5-exact-decision-8-2-9-3/results/item1b/k --s5-queue
  research/12-faced-polyhedron/experiments/E-261103-03-s5-exact-decision-8-2-9-3/queue_item1b.json --timeout 1800
  --s5-checker-timeout 2700 --s5-budget-seconds 91000`. Control (c) is a genus-0 convex 9-face map (no Phase B output is a solid).
* Local disk: about 7 GB of old gitignored proofs in `experiments/E-261103-03-*/results/` may be deleted (owner's call).
* Verification: `test_pilot` + `test_tranche` 34 OK and `verify_all.py --quick` (two git-only checks not applicable)
  on the rewritten tree; no candidates.
