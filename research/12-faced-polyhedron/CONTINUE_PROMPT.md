# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, E-261110-02 prep done; night ready without DRAT; no candidate)

* Branch `lab/2026-11-09`, committed, not pushed. No runs in flight. Prep (PLAN amendment 2): 20 Lutz (10,3) maps
  checked; `--target S6`; tranche imported-map mode; (10,2) bridge gate PASS; controls pass; pilot #1, #2 TIMEOUT at 1200 s.
* Owner (2026-11-13): the night runs without proofs (owner amendment, ~20 core-h); no DRAT by default from now on
  (`CLAUDE.md`, `AGENTS.md`, `PROTOCOL.md` §5, skills, template).
* NEXT: the owner's night `bash research/12-faced-polyhedron/overnight/launch.sh 10-02 start` (AC power), then
  `summary.py` and `experiment-conclude`; then week item 1B (Stage B) or 3 as the owner decides.
* Checks: records in `prep/`; test_tranche 27/27, test_pilot 12/12, summary selftest; verify_all --quick at d26fe532.
* For the lead: the bridge passed on its second configuration (6 restarts, sub-map check; the first had an all-pairs
  check that rejects every S6 object); 3 of 6 foreign (10,2) models look non-realizable (fp numerical); pilot timeouts
  make > 20 % night timeouts likely. Unchanged: crease lemma / five outside chords; pencil lemma vs clauses.
