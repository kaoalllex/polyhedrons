# Prompt to continue this research in a new session

The standing rules are in the root `CLAUDE.md`, which loads automatically. This file holds only the hand-over:
what was in flight when the last session ended. The `session-handover` skill rewrites the block below. Paste the
part under the line into a new Claude Code session on `kaoalllex/polyhedrons`.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

1. Read `STATUS.md` and `ROADMAP.md`.
2. Read the hand-over below.
3. Unless the owner names another task, work on the top `open` row of `ROADMAP.md`, using the `experiment-start`
   skill.

## Hand-over (2026-11-04, autonomous cutoff grid complete)

* Branch: `experiment/E-261103-03-s5-exact-decision-8-2-9-3`, local, not pushed.
* Done: E-261103-03 paired pilot and autonomous 60/300-second follow-through; see CONCLUSION and
  STATUS 3e-3f. Grid pre-registration/source is 8f8132c. The (8,2) stage is unchanged.
* Exact formula decisions, no target SAT or S5 witness. Remaining attempted maps and unrun coverage
  are listed in CONCLUSION; do not turn timeouts into negatives or call the census decided.
* A conditional free-C3 coverage draft now addresses genericity, coorientations, orbit/mirror gauges
  and subgroup coverage. Independent exact determinant/gauge controls pass; only AI review so far.
  Treat all geometric interpretation as PROVED-1 conditional, never CERTIFIED or an S0 result.
* In flight: nothing. E-261103-03 remains running because wider coverage is unfinished.
* Next required compute is the E-261103-05 explore control pilot under the strategy review of
  2026-11-04 and the registered grid continuation rule. Do not execute the proposed coverage tranche
  before that prerequisite is concluded. The tranche is costed in CONCLUSION, not yet an executable
  PLAN activation or permission for a night. Do not overwrite any prior result directory.
* Preserve the immutable census, original CNF/proof provenance, baseline cells and the unresolved
  tail. No new census, completed-formula rerun or unchanged escalation of the hard maps is indicated.
* Completed proofs/CNFs are compressed without loss and versioned. Large partial timeout proofs
  remain local with hashes in packing.json; no authorized external upload. Launcher could not lower
  nice priority; the actual grid ran at inherited priority, as recorded in launcher.log.
* Owner actions: human/external review of encoder and C3 coverage; integration via a PR with verify
  green when ready. No push, PR, release or long-run launch was performed.
* Not checked: full (9,3)/(10,4) realizability, nonuniform extension, human review, full archive or
  GitHub CI. No launch command is applicable to these completed stages.
* Final local verification: `verify_all.py --quick` ALL PASS (18 checks, archive skipped), including
  new grid CNF reconstruction, fresh DRAT replay and exact C3 determinant/gauge controls. Seven
  runner regressions pass. Source/document diff checks pass; raw transcript whitespace is retained.
