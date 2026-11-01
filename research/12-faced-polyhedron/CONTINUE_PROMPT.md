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

## Hand-over (2026-11-01, night)

* **Branches.** `claude/strategy-review-2026-11-01` (pushed): the strategy review, ledger corrections, new ideas /
  hypotheses / experiments E-261101-16..24, primary reads, process rules. `experiment/E-261101-25-chirotope-first`
  (on top of it): algorithm v2 and its pre-registered experiment. Owner: review and merge both via PR (`verify` green).
* **Algorithm v2 = E-261101-25 (`experiments/E-261101-25-chirotope-first/chirotope_first.py`).** Search in the space of
  chirotopes: the signs of a geometric seed are SAT assumptions, UNSAT cores release the conflicting signs, a greedy
  re-add pass leaves a minimal correction set, the model is realized by hinge-loss descent with analytic gradients,
  rounded, re-checked exactly; alternating projections between SAT models and realizations; heuristic no-good
  blocking of models that do not realize; optional face ladder (k-face sub-instances, monotone). Controls pass:
  n = 7 from random planes -> exact EMBEDDED; known 12-plane chirotopes realized from random starts in 0.3 s.
  Pilot state at n = 12 (type 0, k = 7 sub-instance): solves take seconds, the minimal correction set is 8-9 signs,
  but the nearest embedding models did not realize (8 wrong signs); blocking pilot K in `PLAN.md` Amendments.
* **Night 6 = two pre-registered experiments, one command** (owner, laptop on AC power, lid open):
  `cd research/12-faced-polyhedron && bash overnight/run_night6.sh` starts 10 single-core worker processes under
  `caffeinate -dimsu` (6 shards of E-261101-23, k-face sub-instances with DRAT, types mod 6; 4 shards of E-261101-25,
  chirotope-first ladder on the class seeds, 75-minute cap per seed) for the 10 performance cores of the M4 Pro.
  `bash overnight/run_night6.sh status` shows records and progress per shard; `... stop` kills everything.
  Results: `experiments/<ID>/results/<shard>/results.jsonl`, `progress.jsonl` (E-25), `night.log`, `manifest.txt`.
  Predictions P1-P4 for each experiment are in its `PLAN.md`; the morning session compares against them.
* **Morning (new session):** paste the prompt from the top of this file; the session runs `experiment-conclude` for
  E-261101-23 and E-261101-25 (core-hours from the manifests, controls, predictions vs outcomes, SPEC labels, STATUS
  rows, ROADMAP states, log entries), runs `candidate-check` on every record with result EMBEDDED or a realized k-face
  model before calling it anything, and keeps every UNSAT's CNF, proof and hashes. Then the decision table in
  `ROADMAP.md` is updated from the pre-registered scenario moves, and the queue follows it.
* **What the night measures** (`PLAN.md`): fraction of seeds whose k-face models realize at each k, the size of the
  minimal correction sets, and whether any seed climbs the face ladder to k = 12. The engine's open weaknesses are
  listed in the Amendments: no realizability constraints in the SAT instance (final polynomials would be the exact
  cut), the RC2/LSU projections are too slow or not interruptible at n = 12, the realizer uses 5-6 restarts.
* **Open owner actions:** merge the branches; send the first external e-mail (E-261101-11 README "Why and whom");
  Zenodo DOI (Phase 0 TODO).
* **Next ROADMAP items after the night:** E-261101-23 (k-face sub-instances with DRAT, the UNSAT side of the same
  encoder), E-261101-06 (rank-3), E-261101-21, E-261101-22, E-261101-18, E-261101-09, E-261101-11, E-261101-16.
* **How the next step is chosen** (`PROTOCOL.md` 8a, idea I-261101-22): top open ROADMAP row by credences and
  scores; one run in four from the mutation pool, logged as "explore"; construction engines go to the target only
  after the benchmark ladder (E-261101-26).
* **Do not** use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (floors at 0, E-261101-07).
