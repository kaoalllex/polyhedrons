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

## Hand-over (2026-11-04, solid-first explore pilot complete)

* Current branch: `experiment/E-261103-05-s5-symmetric-solid-first`, local, not pushed. It inherits
  the completed E-261103-03 cutoff-grid state at 7509f39; pilot pre-registration/source f9b9744.
* Done: E-261103-05's registered R2/R3 explore pilot (CONCLUSION / STATUS 3g). Known-plane controls
  and random D2 recovery pass. This is an auxiliary (8,3) known-map reconstruction, not S5 (9,3).
  E-261103-05 is marked done for that bounded pilot; no target/night phase was activated.
* Raw pilot artifacts remain unchanged. Canonical exports and exact rechecks are separate;
  legacy solid-parser failure and post-run strict error-path fixes are documented. A standalone
  standard-library Fraction checker and REVIEW.md recheck the one random recovery. AI review is
  not an independent human referee. No CERTIFIED statement or novelty claim.
* In flight: nothing. E-261103-03 remains running with partial plain coverage. Its explore
  prerequisite is now concluded; its costed tranche proposal can be activated only after a
  committed PLAN and a bounded same-path pilot. Preserve its hard unresolved tail and all
  previous source/proof provenance. Use this tip as the dependency base, not stale main.
* For the constructive engine, a small separately registered nine-plane target pilot is now
  justified; no automatic night. Do not reopen the census or repeat completed decisions.
* Original S0 scope and hypotheses are unchanged. No focus geometric candidate is known.
* Owner actions: external/human encoder and symmetry-coverage review; integrate via PR with
  verify green when ready. No push, PR, release, mail or external proof upload was performed.
* Large E-261103-03 timeout proofs remain local and untracked with recorded hashes; keep them.
* Not checked: nine-plane construction, full census realizability, nonuniform extension,
  external human review, full archive or GitHub CI. No launch command applies to this completed pilot.
* Final local verification: `verify_all.py --quick` ALL PASS (19 checks, archive skipped), including
  all nine explore-pilot regressions, fresh saved-model replay and the standalone exact checker.
  Research graph and source/document diff checks pass; raw parser-failure output is retained.
