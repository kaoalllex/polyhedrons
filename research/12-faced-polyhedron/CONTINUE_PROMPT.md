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

* **Research graph.** Every idea, hypothesis and experiment is one file with a dated ID (`PROTOCOL.md` §4).
  * 108 ideas in `ideas/`, 24 hypotheses in `hypotheses/`.
  * 46 experiments in `experiments/E-*`: 33 past ones reconstructed with their data, 13 planned (the queue).
  * The interactive map is `map/index.html`; `verification/trace.py` checks the links (part of `verify_all`).
  * To add work, use the skills `experiment-start` and `experiment-conclude`. New ideas and hypotheses get their
    own files.
* **State of `main`.** Everything is on `main` once PR #1 is merged (the owner merges). Tag `state-2026-11-01` holds
  the release with the DRAT certificates of FD5/FD6 and the documents that were split or removed (archive,
  old idea notes, reviews, night scripts).
* **Optional for the owner.** A strategic review by a strong model (`reviews/REVIEW_PROMPT_2026-11-01.md`).
* **Infrastructure TODOs.** Listed in `ROADMAP.md` Phase 0: `lint_docs.py`, mutation tests, CNF re-encode
  check, README numbers, Actions pilot.
* **Next research item.** E-261101-03 (type-0 genus-3 dossier). Side line: E-261101-12 (maximal face-neighbourly
  polyhedra).
