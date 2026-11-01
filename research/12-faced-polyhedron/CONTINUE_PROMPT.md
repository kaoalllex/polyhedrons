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

## Hand-over (2026-11-01, evening)

* **Branch to open:** `claude/strategy-review-2026-11-01` (on top of `main` after PR #1). It holds the strategy
  review (`reviews/strategy-review-2026-11-01.md`), the ledger corrections it required, ten new ideas
  (I-261101-08..17), seven new hypotheses (H-261101-08..14), seven planned experiments (E-261101-16..22), the
  re-ordered `ROADMAP.md` queue with a three-scenario decision table, and process rules in the agent prompts and
  skills. `verify_all --quick`: ALL PASS. Owner action: review and merge via PR (`verify` must be green).
* **Read first, in this order:** `STATUS.md` (FD6 and FD11 changed; DR18 new), `ROADMAP.md` (new order and
  decision table), `reviews/strategy-review-2026-11-01.md` sections 1, 5 and 9, then the README of the experiment
  you take.
* **Two lemmas await a human reader** (`theory/theory-notes.md`, addendum 2026-11-01): Lemma A closes the FD6 gap
  for mirrors and point reflections; Lemma B says tight trivalent polyhedra are convex. Both are PROVED-1 at most.
  Until Lemma A is reviewed, say "no immersion with a rotational symmetry".
* **In-flight runs:** none. No compute was started by the review session.
* **Open owner actions:** merge the branch; send the first external e-mail (E-261101-11: the `polyhedraproof`
  author, three shared instances with CNF hashes, one question); Zenodo DOI for the certificates (Phase 0 TODO).
* **Next ROADMAP items, in order:** E-261101-06 (rank-3 SAT per type; the cheapest decisive experiment),
  E-261101-09 (predicate equality of the two encoders), E-261101-18 (face-grouped MUS), E-261101-16 (arrangement
  first). Each README has a "Starting point" written so that a smaller model can execute it; the `PLAN.md` must be
  filled and committed before any compute (skill `experiment-start`), including the new counter-calibration and
  scenario-move lines.
* **Do not** use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (it floors at 0, E-261101-07).
