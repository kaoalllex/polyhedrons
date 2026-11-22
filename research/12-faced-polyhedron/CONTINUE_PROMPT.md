# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, E-261119-02 amendment 4 done: C3 (9, 5) empty, C2 (9, 5) 978228 classes; amendment 5 next)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2: stage A 3be; stage B pass 1 3bf (all 12562 (9, 4) records
  UNSAT-SOLVER). Genus 5, amendment 4: C3 3+3+3 (9, 5) empty (3bg); C2 4 x 2 + 1 (9, 5) complete, gate passed, 978228 map
  classes in 12 strata (3bh; owner night 2026-11-21, ~12.4 of 40 core-h). Records (1.4 GB, uncompressed by the owner's
  choice) are in `../polyhedrons-data/<same path>`, hashes in `results/stageA5c2/SHA256SUMS`; the derived `summary.json`
  and the claim markers were deleted (owner, 2026-11-22).
* Next: amendment 5 (PLAN.md, before any genus-5 solver run): `stageb.py` records for C2f_9_5 read from the data copy
  (hash-checked), 3 maps per stratum (frozen seed), the amendment-3 formula controls on them, a pricing run, then the
  pass-1 price to the owner (~150 core-h and tens of GB raw at the (9, 4) per-record rate; no subset by a guessed
  predictor without the owner). `summary` peaks at 21 GB RSS on these records: anything reading all of them should stream.
* Amendment 5 requirements (owner, 2026-11-22: do not write raw data nobody needs). (1) Lean runner mode for pass 1: an
  UNSAT-SOLVER unit leaves only its line in the shard's `results.jsonl` (status, seconds, sizes, `cnf_sha256`,
  `formula_sha256`) and its unit folder is removed as soon as that line is written; SAT, UNKNOWN, errors and controls keep
  everything. At (9, 4) the per-map folders were 5 files each (63k files, 239 MB on disk for 94 MB of bytes); at (9, 5)
  that would be ~5M files and 20-45 GB. (2) `symcensus.py summary` writes only the brief and the strata, not the full
  code list (already in the records); claim markers are removed at the end of a census run. Check on the controls and
  the pricing queue that statuses and hashes are unchanged before the pass-1 launch.
* For the lead: one status across all 12562 (9, 4) symmetric formulas, each decided in < 1 s; controls hold on both signs
  at formula level, but no map-level nine-face positive exists in the moved chart. A common obstruction may be worth a
  lemma (item 4) before spending ~150 core-h on the (9, 5) C2 formulas.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
