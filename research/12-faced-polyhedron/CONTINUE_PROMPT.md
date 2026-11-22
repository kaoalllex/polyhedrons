# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, E-261119-02 amendment 5 done: lean runner, (9, 5) pricing; owner's pass-1 decision next)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 1 done (3bd). Item 2: (9, 4) all UNSAT-SOLVER (3bf); C3 (9, 5) empty (3bg); C2 (9, 5) 978228 classes (3bh).
  Amendment 5 (README "Stage B at genus 5"): lean runner, brief-only summary, lean replication exact, 36 of 36 (9, 5)
  pricing records UNSAT-SOLVER in <= 0.23 s, formula controls pass. No run in flight.
* Owner decision: pass 1 on all 978228 records, ~143 core-h, ~14 h wall (two nights, resumable), ~1 GB lean; cap 5 s
  recommended (tail bound ~110 core-h; 30 s ~650). No subset by a guessed predictor without the owner.
* If approved, amendment 6: ~100 chunked maps files and queues built by streaming (one 0.63 GB file would be loaded by
  every unit), a launch that resumes past `run_b.sh`'s `--hours 2`, a 10-shard smoke, then the owner launch.
* For the lead: one status across all 12562 (9, 4) and 36 (9, 5) symmetric formulas, each < 1 s; a common obstruction
  lemma (item 4) may be worth more than ~143 core-h.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
