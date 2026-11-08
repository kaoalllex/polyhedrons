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
* NEXT: item 1 prep: `queue_item1b.json` ((b) 12 maps + 74, 174, 176, 181, 200), F = 9 positive control (c), bounded
  startup check on 10 shards, launch command for the owner. Map selection: `reviews/strategy-review-2026-11-08-runtime-patterns.py`.
* Local disk: about 7 GB of old gitignored proofs in `experiments/E-261103-03-*/results/` may be deleted (owner's call).
* Verification: `test_pilot` + `test_tranche` 34 OK and `verify_all.py --quick` (two git-only checks not applicable)
  on the rewritten tree; no candidates.
