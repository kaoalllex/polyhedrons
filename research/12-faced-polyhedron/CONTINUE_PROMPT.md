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
* NEXT: owner launches the E-261103-07 (10,4) cost probe (pre-registered `bf1a756`, pilot passed), from the repo root on AC
  power: `bash research/12-faced-polyhedron/overnight/launch.sh 03-07 start` (then `status`, `stop`); 10 shards, <= 1.3 h,
  <= 6.5 core-h, results in `experiments/E-261103-07-*/results/probe/`. Then `experiment-conclude`, then the lead review
  (`/strategy-review`) on review 2026-11-08c §4. Pattern census done (E-261103-07 README).
* For the lead: the whole (9,3) claim rests on one encoder; review 2026-11-08c §7 idea 1 (second encoder on five maps) is
  unscheduled.
* Verification: runner extended for the probe (case, control file, per-map caps): `test_tranche` + `test_pilot` 37 OK,
  `control_f9.py --check` OK; 158 item-5a CNFs rebuilt to recorded hashes; no DRAT replay, no verify_all.
