# Prompt to continue this research in a new session

Copy everything below the line into a new Claude Code session on `kaoalllex/polyhedrons`, branch `main` (or the
experiment branch named in `ROADMAP.md`).

---

You are continuing a research project in `research/12-faced-polyhedron/` of `kaoalllex/polyhedrons`: does a
polyhedron embedded in R^3 exist with 12 planar simple faces, every two sharing exactly one edge, three faces per
vertex (V = 44, E = 66, genus 6)? Find and exactly verify one, or prove impossibility (fully or for some
combinatorial types). Never weaken the requirements; never fabricate results; report failures with their output.
Report to the owner in Russian; write repository files in English.

Read, in this order: `README.md` (map), `STATUS.md` (where we are: foundations, witnesses, directions with
verdicts, what may be claimed), `ROADMAP.md` (the scored queue), `PROTOCOL.md` (how experiments are run),
`SPEC.md` (definitions, counters, evidence labels). History is in `experiment-log.md` and `archive/`.

Rules that matter most:
* Start an experiment only from a `ROADMAP.md` row; pre-register it in `experiments/E##-slug/PLAN.md` before any
  compute; one branch `experiment/E##-slug` per experiment; finish with `CONCLUSION.md` and update `STATUS.md`.
* `python3 verification/verify_all.py` must pass before and after your changes; every candidate goes through
  `verification/verify_candidate.py`.
* Do not run anything on the stop list (`ROADMAP.md`). A timeout is not a result; an UNSAT holds only for its
  formula.
* Ask the owner before large subagent tasks (usage limits) and before long runs; long runs go to the owner's
  laptop (`caffeinate`) or to GitHub Actions (`.github/workflows/experiment.yml`).

First task unless the owner says otherwise: the top open item of `ROADMAP.md` (E01, the type-0 genus-3 dossier).
