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

## Hand-over (2026-11-04, after the paired (9,3) pilot)

* Branch: `experiment/E-261103-03-s5-exact-decision-8-2-9-3`, local, not pushed.
* Read the completed strategy review `reviews/strategy-review-2026-11-04.md`; the older hand-over
  incorrectly said a review was still due. This session did not repeat it.
* Done: the owner-requested paired C3/plain pilot; see E-261103-03 CONCLUSION and STATUS 3e.
  Pre-registrations bc0ae0e and 0db8d8e. The initial panel correction/interruption and both attempt
  manifests are retained. No formula was retried. The (8,2) stage is unchanged.
* Evidence: checked exact formula decisions, no target SAT or S5 witness. C3 ansatz negatives do
  not decide asymmetric existence or geometric C3-family coverage. Geometric interpretation of
  plain decisions remains conditional PROVED-1; no CERTIFIED theorem or S0 solution.
* In flight: nothing. E-261103-03 remains running because wider plain coverage is unfinished.
* Next decision: separately pre-register the review's small 60/300-second paired grid on at most
  four unresolved plain maps, or the queued exploration pilot. No automatic night/full sweep.
  Do not rerun the census or completed (8,2) solves. Prior 30-second and interrupted calls remain
  distinct from 60-second timeouts. Do not overwrite either paired result directory.
* CNFs and completed proofs are retained with hashes. Large partial timeout/interruption proofs
  stay local (packing.json), with no negative claim and no authorized external upload.
* Owner actions: external/human encoder and symmetry-coverage review; integrate via PR with verify
  green when ready. No push, PR, release or long-run launch is authorized here.
* Not checked: remaining (9,3)/(10,4) realizability, nonuniform extension, human review, archive,
  GitHub CI. No launch command is applicable to this completed pilot.
* Final local verification: `verify_all.py --quick` returned ALL PASS (18 checks, archive skipped),
  including paired CNF reconstruction and fresh completed-proof replay. Six runner regressions
  and the dedicated paired evidence test pass. Raw transcripts retain their original whitespace.
