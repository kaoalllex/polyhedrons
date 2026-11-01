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

## Hand-over (2026-11-01)

* `main` holds everything: the restructure, the audit fixes, `witnesses/` with the site's "Lab ·" models. It is
  tagged `state-2026-11-01`, and the GitHub release on that tag carries the DRAT certificates of FD5/FD6
  (`verification/certificates/symmetric_drat/`). Start new work on a new branch.
* Owner actions:
  * Zenodo DOI (enable the GitHub-Zenodo integration; it archives the next release).
  * Confirm the licence holder name in `LICENSE` and `CITATION.cff` (currently `kaoalllex`).
* Open audit actions (`reviews/fresh-audit-2026-11-01.md`):
  * 9: `lint_docs.py` in `verify_all`, and an id regex in `experiment.yml`.
  * 10: `test_mutants.py` and a re-encode-and-hash check of 2-3 symmetric CNFs.
  * 12: READMEs link to STATUS instead of restating numbers.
  * 13: archive `run_night*.sh`.
  * 14: Actions pilot on E02.
* Next research item: E01 (type-0 genus-3 dossier).
