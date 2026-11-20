# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-02 amendment 4: C3 (9, 5) empty, C2 (9, 5) census night pending)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2: stage A 3be; stage B pass 1 3bf (all 12562 (9, 4) records
  UNSAT-SOLVER). Genus 5, amendment 4 (`8b5bc10e`): the C3 3+3+3 (9, 5) census is complete and empty (3bg).
* Next: the owner launches the C2 4 x 2 + 1 (9, 5) census, `launch.sh 261119-02 start` (`run.sh` default `STAGE=A5c2`,
  10 x 14400 s, 40 core-h cap; priced ~12 core-h, ~1.3 h wall, ~1.1M maps, ~1.6 GB records). Then the session:
  `symcensus.py summary results/stageA5c2 A5c2`, the gate, raw records to `../polyhedrons-data` (not git; keep the
  SHA-256 per shard), and amendment 5 (per-stratum pricing; the pass-1 price, ~170 core-h at the (9, 4) rate, to the
  owner). The summary of ~1.1M maps may need a streaming rewrite (memory); its checks must not change.
* Pilots of amendment 4 used ~0.85 core-h, booked to the A5c2 budget.
* For the lead: one status across all 12562 (9, 4) symmetric formulas, each decided in < 1 s; controls hold on both signs
  at formula level, but no map-level nine-face positive exists in the moved chart. A common obstruction may be worth a
  lemma (item 4) before spending ~170 core-h on the (9, 5) C2 formulas.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
