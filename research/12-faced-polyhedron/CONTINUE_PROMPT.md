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

## Hand-over (2026-11-04, E-261103-03 after the (8,2) pilot)

* Branch: `experiment/E-261103-03-s5-exact-decision-8-2-9-3`, local, not pushed.
  Base main f0f677f; pre-registration ac2ad98, computation source c48ab73.
* Done: both plain (8,2) formulas and free-C2 formulas UNSAT-VERIFIED; retained CNFs/DRAT.
  Known eight-face controls reconstructed by both realizers, warm and unseeded; exact rechecks pass.
  See the experiment CONCLUSION and STATUS 3d. Formula decisions EXACT; geometric exclusion is
  conditional PROVED-1 (census/encoder arguments lack human review). No CERTIFIED theorem claim.
* Review hardening: reject realizer fallback unless wrong_signs=0 and exact signs match;
  Python computation alarm added. Original artifacts retain their source provenance and remain valid.
* In flight: nothing. E-261103-03 stays running because (9,3) is not started, not because a process is active.
* Next: strategy review is due after the (8,2) scenario change, in a separate session under strategy-review.
  For subsequent execution, continue E-261103-03 with a committed PLAN amendment for the eight
  free-C3 (9,3) formulas. Reuse census and controls; preserve CNF/proofs. No new census or (8,2) run.
  Fixed-face C2/D3 uniform UNSATs are not geometric exclusions. A nonrealizable model does not decide a map.
* Owner actions: human/external encoder review and integration through PR with verify green when ready.
  No push or PR authorized. No long-run launch command is applicable to the completed (8,2) stage;
  (9,3) launch needs its own pre-registration first.
* Not checked: (9,3)/(10,4) target realizability, nonuniform extension, human review, archive, GitHub CI.
* Final local verification: verify_all.py --quick returned ALL PASS (18 checks, archive skipped);
  five dedicated runner regressions pass. Raw solver/checker whitespace is retained.
