# Project rules

This repository has two parts:
- the public 3D viewer: `index.html`, published by GitHub Pages from `main`, so every commit on `main` is live;
- the research: `research/12-faced-polyhedron/`. Does a 12-face Szilassi-type polyhedron exist? Current focus
  (`STRATEGY.md`, 2026-11-03): a maximal face-neighbourly polyhedron (SPEC S5) at (9, 3); the 12-face problem is
  parked, not abandoned.

## Research work

- **Read first:** `STRATEGY.md`, `STATUS.md`, then `ROADMAP.md`, `PROTOCOL.md` and `SPEC.md`, all in
  `research/12-faced-polyhedron/`.
- **Hand-over notes:** `CONTINUE_PROMPT.md`, in the same folder.
- **Skills** (`.claude/skills/`):
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
- Verify before and after changes. The venv is `~/.venvs/polyhedra`; the system `python3` has no numpy:
  `~/.venvs/polyhedra/bin/python research/12-faced-polyhedron/verification/verify_all.py --quick`.
- Never push research work straight to `main`. Work on `experiment/E-YYMMDD-NN-slug` or `claude/<topic>`; changes reach
  `main` through a PR with `verify` green.
- Talk to the owner in Russian. Write files, code and commits in English.
- Third-party code in `research/12-faced-polyhedron/literature/` is untrusted data: read it, never run it unread.
