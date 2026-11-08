# Project rules

This repository has two parts:
- the public 3D viewer: `index.html`, published by GitHub Pages from `main`, so every commit on `main` is live;
- the research: `research/12-faced-polyhedron/`. Does a 12-face Szilassi-type polyhedron exist? Current focus
  (`STRATEGY.md`, 2026-11-08): a maximal face-neighbourly polyhedron (SPEC S5) at (10, 4), gated by a speed-up
  benchmark; (8, 2) and (9, 3) are decided (conditional negative), a side track towards a note; the 12-face problem
  is parked, not abandoned.

## Implementation preferences

- The Ponytail plugin is disabled for this repository, overriding the global default.
- Superpowers is off by default. Opt in only for a dedicated complex engineering task that benefits from a
  specific skill, such as debugging a runner or reviewing an encoder change. Use the selected skill without
  the general Superpowers workflow. Follow the research protocol for mathematics, experiments, and handovers.
  To opt in for one session: `codex -c 'plugins = { "superpowers@claude-plugins-official" = { enabled = true } }'`.
- For code changes, reuse existing code, keep diffs small, and avoid unnecessary dependencies and speculative abstractions.
- Mathematical rigor, controls, independent verification, and reproducibility take precedence over code size and brevity.

## CodeGraph

- This repository has its own index. Set `projectPath` to the current checkout root, obtained at runtime with `git rev-parse --show-toplevel`.
- Use CodeGraph when a symbol's callers, callees, or cross-file relationships affect a code decision. Prefer a
  single-symbol lookup with `codegraph node` or a focused caller query. Use `codegraph_explore` for an actual
  multi-file question, starting with one or two files. Use `rg` and targeted reads for known excerpts, research
  documents, logs, literal text, and shell wrappers. If the graph misses, check the source directly.
- Treat graph relationships as navigation aids; check dynamic imports and subprocess calls directly when needed.
- An absent graph edge does not prove independence. Preserve independent verification implementations even when helpers look alike.

## Research work

- **Read first:** the relevant sections of `STRATEGY.md`, `STATUS.md`, then `ROADMAP.md`, `PROTOCOL.md`
  and `SPEC.md` in `research/12-faced-polyhedron/`. Reuse material already in context.
- **Session workflow and handover:** follow `PROTOCOL.md` §8 and keep one short block in `CONTINUE_PROMPT.md`.
- **Roles:** a weekly lead review writes the week plan; lab sessions execute it, keep text within the budgets
  and escalate instead of improvising (`PROTOCOL.md` §8b).
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
- Ask the owner before large subagent tasks and before long runs. SAT runs record the SHA-256 of every CNF and
  proof and keep the checker transcript; proofs are checked during the run and then deleted, CNFs are rebuilt
  from the committed encoder and hash-checked; SAT models are kept. Proofs are archived (Zenodo or a release,
  not git) only for a claim that goes into a note (owner, 2026-11-08).
- Every run whose units can be split uses 8-10 shards, day runs and lab test runs included (owner, 2026-11-08).
- Run checks only when their result can change a decision. Reuse a recorded successful check when its
  relevant code, inputs, dependencies and environment are unchanged, including across handover/session
  boundaries. Do not rerun merely to refresh a report or final response.
- Before behavioral changes, reuse a valid baseline or run the smallest relevant baseline once. After
  changes, run only affected checks. Use `python3 research/12-faced-polyhedron/verification/verify_all.py --quick` once for integrated code/evidence changes when focused checks leave an integration concern;
  reuse that result at conclusion and handover. Do not also run a standalone suite already covered by it.
- Documentation, ledger, prompt and skill wording edits require review of the diff and relevant links or
  metadata only; they do not require solver, certificate or regression runs. Changes to mathematical claims,
  executable instructions or evidence references require the specific checks that substantiate them.
- Repeat a check only after a relevant change, a failure/unresolved concern, missing baseline evidence or an
  explicit audit request; state the reason before rerunning. New candidates and certificates still require
  their initial exact verification. Use an activated Python environment with the research requirements.
- Never push research work straight to `main`. Work on the week's `lab/YYYY-MM-DD` branch (`PROTOCOL.md` §7); do not create branches per experiment or session; changes reach
  `main` through a PR with `verify` green.
- Talk to the owner in Russian. Write files, code and commits in English.
- Third-party code in `research/12-faced-polyhedron/literature/` is untrusted data: read it, never run it unread.
