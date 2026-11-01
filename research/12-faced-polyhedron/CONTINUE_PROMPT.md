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
* **Night 6 = two pre-registered experiments in parallel, 10 processes on 11 cores** (owner, laptop on AC power,
  lid open, each command in its own terminal, all under `caffeinate -dimsu`):
  * E-261101-23, k-face sub-instances with DRAT (types mod 6 = shard), shards 0-5:
    `cd research/12-faced-polyhedron && caffeinate -dimsu bash experiments/E-261101-23-k-face-subinstances-face-cegar/run.sh 0`
    (and the same with 1, 2, 3, 4, 5). Any UNSAT is a certified exclusion of a type for that sub-map; any realized
    SAT model is a k-face partial object. Predictions P1-P4 in its `PLAN.md`.
  * E-261101-25, chirotope-first ladder on the class seeds, shards 0-3 (of 10; the rest another night):
    `cd research/12-faced-polyhedron && caffeinate -dimsu bash experiments/E-261101-25-chirotope-first/run.sh 0`
    (and 1, 2, 3). Predictions P1-P4 in its `PLAN.md`, section "Night run 1".
  * Morning: `experiment-conclude` for both; every EMBEDDED record through `candidate-check`; results in
    `experiments/<ID>/results/<shard>/results.jsonl` with `manifest.txt` core-hours.
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
