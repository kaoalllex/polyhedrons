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

## Hand-over (2026-11-04, exact coverage launch ready)

* Current branch: `Codex/s5-coverage-tranche`, local, not pushed, based on 9f9f898 with the
  completed E-261103-05 dependency. Coverage pre-registration c707bc5, runner/pilot source
  697e3e5. Local TODO.md remains ignored and intentionally uncommitted.
* E-261103-03 remains running. Its new-map tranche is activated; see PLAN, tranche_queue.json,
  CONCLUSION and STATUS 3h. The same-path pilot and no-op resume completed. No target decision
  or candidate was added; timeouts do not exclude maps. S0 and existence hypotheses are unchanged.
* Production imports the pilot checkpoint and its resource charge. It must not repeat either
  pilot unit, the old hard tail, old grid, paired pilot, census or completed explore controls.
  Saved artifacts retain original source hashes; post-pilot changes import the checkpoint/resource charge and make saved failure stops report
  an error. Current-source CNF reconstruction and inheritance regressions pass.
* The runner uses separate solver/checker caps, shared first-SAT stopping at actual solver
  spawn, durable per-unit checkpoints, source/input guards, fresh attempt directories and a
  conservative cumulative budget across restarts. Interrupted SAT stages retain files and
  consume their allocation without retry. Nested process cleanup is regression-tested.
* Next action belongs to the owner: launch the activated E-261103-03 tranche on the laptop,
  on AC power with the lid open, from the repository root:

  ```bash
  source "$HOME/.venvs/polyhedra/bin/activate"
  export PATH="$HOME/bin:$PATH"
  caffeinate -dimsu bash research/12-faced-polyhedron/overnight/launch.sh E-261103-03 start 8
  ```

  Status and graceful stop:

  ```bash
  bash research/12-faced-polyhedron/overnight/launch.sh E-261103-03 status
  bash research/12-faced-polyhedron/overnight/launch.sh E-261103-03 stop
  ```

  The existing launcher is now applicable and detaches each shard under caffeinate. Repeat
  start to resume completed checkpoints; fewer workers are supported. Never remove a saved
  failure stop or source/budget guard to force continuation. No automatic git writes.
* In flight: nothing. No tranche, night, push, PR, release, e-mail or external upload launched.
  Do not start a long run from an AI session. If the owner has run the tranche, collect numeric
  results directories and all attempt manifests, then use experiment-conclude. First SAT
  takes priority over further coverage; a geometric candidate requires candidate-check.
* Large old timeout proofs and the new pilot's partial proofs remain local and untracked,
  with recorded hashes; retain them. Small saved artifacts and manifests are versioned.
  The sandbox denied nice priority for the short pilot; it ran at default priority. The DRAT
  binary is hashed, but its source commit is unknown. Details are in CONCLUSION.
* Verification: verify_all.py --quick ALL PASS (20 checks; full archive skipped); tranche
  scheduling/evidence regressions and the existing pilot runner regressions pass. Research
  graph has no link errors. Not checked: real concurrent multi-shard execution, target-SAT
  realization, full archive, external human review, or GitHub CI. Mathematical scope remains
  EXACT instance decisions and conditional PROVED-1 geometric interpretation.
* Other owner actions: external/human encoder and symmetry-coverage review; integrate through
  a PR with verify green when authorized. Do not return to the generic top-open fallback while
  this activated exact-decision work is awaiting the owner's run/results.
