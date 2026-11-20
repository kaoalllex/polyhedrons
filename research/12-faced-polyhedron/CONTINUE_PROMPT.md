# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-20, E-261119-02 stage B pass 1 recorded: both families all UNSAT-SOLVER at (9, 4))

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 (E-261119-01) done, STATUS 3bd. Item 2: stage A STATUS 3be; stage B pass 1 STATUS 3bf: all 12562 records
  UNSAT-SOLVER (max 0.63 s), controls and replication pass, 1.83 core-h; no pass 2. Raw output moved by `move_raw.py`.
* Next (item 2 tree): genus 5 (E = 51) for both families, priced the same way: amendment 4 to `PLAN.md` (stage-A census
  at (9, 5) with its controls and gate, then per-stratum pricing) before any run; the owner launches. Stage B has used
  < 2 of its 10 core-h; a (9, 5) census budget beyond the row goes to the owner.
* For the lead: one status across all 12562 (9, 4) symmetric formulas, each decided in < 1 s; controls hold on both signs
  at formula level, but no map-level nine-face positive exists in the moved chart. A common obstruction may be worth a
  lemma (item 4) before spending on genus 5.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
