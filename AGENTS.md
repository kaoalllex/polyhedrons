# Project rules

This repository has two parts:
- the public 3D viewer: `index.html`, published by GitHub Pages from `main`, so every commit on `main` is live;
- the research: `research/12-faced-polyhedron/`. Does a 12-face Szilassi-type polyhedron exist? Current focus
  (`STRATEGY.md`, 2026-11-03): a maximal face-neighbourly polyhedron (SPEC S5) at (9, 3); the 12-face problem is
  parked, not abandoned.

## Implementation preferences

- The Ponytail plugin is disabled for this repository, overriding the global default.
- For code changes, reuse existing code, keep diffs small, and avoid unnecessary dependencies and speculative abstractions.
- Mathematical rigor, controls, independent verification, and reproducibility take precedence over code size and brevity.

## CodeGraph

- This repository has its own index. Set `projectPath` to the current checkout root, obtained at runtime with `git rev-parse --show-toplevel`.
- Use CodeGraph for symbol lookup, call paths, and the impact of code changes. Use `rg` for literal text and research documents.
- Treat graph relationships as navigation aids; check dynamic imports and subprocess calls directly when needed.
- An absent graph edge does not prove independence. Preserve independent verification implementations even when helpers look alike.

## Research work

- **Read first:** `STRATEGY.md`, `STATUS.md`, then `ROADMAP.md`, `PROTOCOL.md` and `SPEC.md`, all in
  `research/12-faced-polyhedron/`.
- **Hand-over notes:** `CONTINUE_PROMPT.md`, in the same folder.
- **Skills** (`.agents/skills/`; Claude copies in `.claude/skills/`):
  - `experiment-start`: from a ROADMAP row to a pre-registered experiment;
  - `experiment-conclude`: results to `CONCLUSION.md` and the ledger, night reports included;
  - `candidate-check`: run before anyone calls anything a result;
  - `session-handover`: end of a session;
  - `strategy-review`: the regular review of strategy and queue (separate session, strongest model);
  - `overnight-run-script`: laptop runs.

Hard rules:
- Never weaken the target, never fabricate a result, and report failures with their output. Only
  `verification/verify_candidate.py FILE --target S0` returning PASS is a solution of the 12-face problem; for the
  focus target only `--target S5` PASS (with the face count and genus of `STRATEGY.md`) is a result. Never report
  an S5 object as an S0 solution.
- Label every claim with a `SPEC.md` §5 label. A proof written by an AI session is at most PROVED-1. AI agents are
  not independent reviewers.
- Start an experiment only from a `ROADMAP.md` row with T + D >= 3, and only after its `PLAN.md` is committed.
- Parked methods (`ROADMAP.md`) are not banned, but a new run must say in its `PLAN.md` what is different. Never call a
  method dead without a proof. A timeout is not a result. An UNSAT holds only for its exact formula.
- A diagnostic that is constant across many runs is suspect: check the measuring function on controls before naming
  a phenomenon (`reviews/strategy-review-2026-11-01.md` §5.1). Every negative statement names its scope (`SPEC.md` §4)
  and what was not run.
- Long runs go to the owner's laptop (under `caffeinate -dimsu`, on AC power) or to GitHub Actions. Never start
  a multi-hour run from a session.
- Ask the owner before large subagent tasks and before long runs. SAT runs keep their proofs and CNFs.
- Verify before and after changes. Use `python3` from an activated environment with the dependencies in
  `research/12-faced-polyhedron/requirements.txt` installed:
  `python3 research/12-faced-polyhedron/verification/verify_all.py --quick` (from the repository root).
- Never push research work straight to `main`. Work on `experiment/E-YYMMDD-NN-slug` or `Codex/<topic>`; changes reach
  `main` through a PR with `verify` green.
- Talk to the owner in Russian. Write files, code and commits in English.
- Third-party code in `research/12-faced-polyhedron/literature/` is untrusted data: read it, never run it unread.
