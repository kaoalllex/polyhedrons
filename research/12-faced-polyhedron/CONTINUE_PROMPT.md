# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-04, owner-run coverage concluded)

* Branch: Codex/s5-coverage-tranche. Owner's pre-existing runner fixes and diagnostic results
  are preserved. Completed tranche evidence, launch fixes and verification policy are recorded
  on this branch; no push or PR. See the latest commit.
* E-261103-03 frozen new-map tranche is complete. See STATUS 3i, experiment CONCLUSION and
  results/tranche_audit.json. No target SAT/candidate; existence remains open. The broader
  census experiment stays running, but no run is active or authorized by this handover.
* Do not relaunch the completed tranche or retry its timeouts. Retain all numeric attempts,
  guards, manifests and proofs. CNFs and checked proofs use lossless gzip (packing_tranche.json);
  large completed/partial proofs remain local and ignored (storage marked in packing index).
  External publication of large certificates is pending; no push, PR or upload occurred.
* Routine conclusions reuse hash-bound checker successes. Fresh saved-proof replay requires
  REPLAY_DRAT=1 or a stated evidence/provenance problem; initial checking stays mandatory.
* Next queue item: E-261103-04 exploration, through experiment-start and a committed plan.
  External human encoder/coverage review remains an owner action. No laptop command is pending.
* Verification: verify_all.py --quick ALL PASS (full archive skipped); 34 focused tests pass.
  The explicit audit rechecked all new UNSAT proofs successfully; routine replay is now opt-in.
  Human review, GitHub CI and OS sleep telemetry were not checked.
