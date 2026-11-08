# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-08, E-261103-03 concluded after item 5a)

* Branch `lab/2026-11-07` (unpushed; old SHAs before the 2026-11-08 rewrite map via
  `reviews/strategy-review-2026-11-08b-commit-map.txt`). Week plan in `ROADMAP.md`: items 1-5 DONE. No active process.
* Item 5a: 158/158 UNSAT-VERIFIED, 0 SAT, controls passed, 18.51 core-h. Every admissible (9,3) plain formula (203/203)
  is UNSAT-VERIFIED (EXACT); geometric reading conditional PROVED-1 (STATUS 3d, E-261103-03 CONCLUSION last section).
* NEXT: owner calls the lead review (`/strategy-review`, separate session) on review 2026-11-08c §4: note / (10,4) exact
  route / S0 transfer. Allowed before it (ROADMAP item 5 follow-up): (10,4) pattern census (minutes) and the E-261103-07
  cost probe (<= 1 core-h, 10 shards).
* For the lead: the whole (9,3) claim rests on one encoder; review 2026-11-08c §7 idea 1 (second encoder on five maps) is
  unscheduled.
* Local disk: about 7 GB of old gitignored proofs in `experiments/E-261103-03-*/results/` may be deleted (owner's call).
* Verification: no code change since the 5a prep (36 tests OK); 158 CNFs rebuilt to recorded hashes; no DRAT replay, no verify_all.
