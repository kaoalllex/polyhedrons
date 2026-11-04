# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-04, authorized conditional grid running)

* Stay on `Codex/s5-coverage-tranche`. E-261103-04's completed pilot remains
  UNDERPOWERED (STATUS 3l). The owner explicitly authorized the conditional grid
  after startup acceptance. Do not ask for that launch authorization again.
* The actual `STAGE=calibration caffeinate -dimsu nice -n 10 bash
  research/12-faced-polyhedron/experiments/E-261103-04-s5-genus-ladder-9-faces/run.sh 0`
  is running in exec session 88085 on AC power, one worker and one thread per
  numeric library. Manifest implementation HEAD is `281881d`, plan `b851f8c`,
  executable implementation `3f3aeda`. Default OUT is `results/recovery-grid`.
  All deterministic controls pass; the first 180-second Roest-Vigh cell started.
* Next collect the existing run, not another launch. Poll its existing exec handle
  or read OUT/recovery.json and OUT/stdout.txt; finalized manifest.json records exit
  status, output hashes and resources. Four cells use frozen accepted parents,
  paired RNG seeds and independent 3/10-minute budgets; PLAN owns decisions.
  Two earlier launch attempts stopped before Python/OUT creation (sandbox nice
  denial; background shell lifetime); no optimization was repeated.
* Apply experiment-conclude on completion; any accepted cell needs candidate-check
  and independent two-scale checks before a result claim. Full eight-face recovery,
  focus geometry and night remain gated even if a cell passes. Keep rejected outputs.
* Reuse startup input/output hashes, labelled round trips, source-bound independent
  parent acceptance, surgery acceptance and the prior shared-code quick-suite PASS.
  No new integrated suite, CI, solver/proof replay or human review. E-261103-03's
  tranche remains complete (STATUS 3i); review/publication remain owner actions.
