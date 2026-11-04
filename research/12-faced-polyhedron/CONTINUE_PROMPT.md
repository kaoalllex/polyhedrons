# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-04, conditional grid ready; launch awaits owner)

* Stay on `Codex/s5-coverage-tranche`; no new branch. E-261103-04 remains running
  without an active process. The completed pilot remains UNDERPOWERED (STATUS 3l).
* Conditional failed-level grid pre-registration `b851f8c`, implementation
  `3f3aeda`. Actual `STARTUP_ONLY=1 STAGE=calibration .../run.sh 0` returned
  STARTUP-PASS (STATUS 3m). No optimization ran. Four cells use the frozen accepted
  parents, original paired RNG seeds and independent 3/10-minute budgets.
* Next obtain the owner's explicit long-run authorization, unless already given
  later in this conversation. No full grid has been launched. Then, from the
  repository root with the research environment activated, on AC power, lid open:
  `STAGE=calibration caffeinate -dimsu nice -n 10 bash research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0`.
  Default OUT `results/recovery-grid` refuses overwrite. See PLAN for the cap,
  power limits and outcome decisions. Do not repeat startup or the old pilot.
* Reuse startup input/output hashes, exact deterministic controls, labelled round
  trips, saved source-bound independent parent acceptance and surgery acceptance.
  Static checks, invalid dispatch checks and graph/diff metadata pass. No new
  independent replay, integrated suite, CI, solver/proof replay or human review.
  Full eight-face recovery, focus geometry and night remain gated even if a cell
  passes. Accepted cells need candidate-check before a result claim.
* E-261103-03's tranche remains complete (STATUS 3i). Human encoder/coverage review
  and publication of large local certificates remain owner actions.
