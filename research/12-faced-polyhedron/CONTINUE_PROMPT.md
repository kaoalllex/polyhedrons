# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, E-261110-02 prep done; night ready; no candidate)

* Branch `lab/2026-11-09`; prep committed there (PLAN amendment 2), not pushed. No runs in flight.
* Prep: 20 Lutz (10,3) maps imported and checked; `--target S6`; tranche imported-map mode; (10,2) bridge gate PASS
  after fixing the all-pairs exact check; controls (a)-(d) pass; pilot Lutz #1, #2 TIMEOUT at 1200 s; startup check clean.
* NEXT: the owner's night `bash research/12-faced-polyhedron/overnight/launch.sh 10-02 start` (AC power), then
  `summary.py` and `experiment-conclude`. Then week item 1B (Stage B) or 3 as the owner decides.
* Checks: bridge gate, controls, pilot and startup recorded in `prep/`; test_tranche 27/27, test_pilot 12/12,
  summary selftest; verify_all --quick and trace.py at the prep commit.
* For the lead: (1) the bridge passed on its second configuration (6 restarts, sub-map check), decided before the recorded
  gate run; 3 of 6 foreign (10,2) models look non-realizable (fp numerical). (2) Pilot timeouts make > 20 % night timeouts
  likely; DRAT check time and memory of ~8 GB proofs are unmeasured (7200 s checker cap).
* Unchanged: crease lemma proof/five outside chords; pencil planar lemma vs implemented clauses.
