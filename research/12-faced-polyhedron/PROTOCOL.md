# Protocol: how this project works

Modelled on practices of large computational-mathematics and lab projects: pre-registered experiments with
stop rules, positive and negative controls in every run, exact verification of every claim, provenance
manifests, append-only logs, independent re-implementation before a theorem is announced (bbchallenge, the
Keller / Schur / Pythagorean-triples SAT campaigns, The Turing Way, the Kempner Institute handbook).

## 1. Documents and their roles

| File | Role | Rule |
|---|---|---|
| `README.md` | entry point, folder map | update when the layout changes |
| `SPEC.md` | target, relaxations, counters, evidence labels | frozen; changes only via its change log |
| `STATUS.md` | ledger: foundations, witnesses, directions with verdicts, claims | update in the same commit as any result that changes a row |
| `ROADMAP.md` | the scored experiment queue | an experiment starts only from here |
| `results.md` | evidence up to 2026-11-01 (old labels) | frozen: correct errors only; new evidence goes to `CONCLUSION.md` |
| `experiment-log.md` | chronology | append-only |
| `CONTINUE_PROMPT.md` | hand-over to the next session | short; points to the files above |
| `experiments/E-YYMMDD-NN-slug/` | one experiment: plan, runner, results, conclusion | see section 2 |
| `theory/`, `ideas/`, `reviews/`, `reports/`, `literature/` | supporting material | ideas are a backlog, not a plan |
| `ideas/`, `hypotheses/` | one file per idea / hypothesis (§4) | ideas are a backlog, not a plan |
| `map/` | `graph.json` (built by `verification/trace.py`) and the interactive map | never edit `graph.json` by hand |

## 2. Experiment lifecycle

1. **Idea** -> `ideas/` (one line is enough).
2. **Score and queue** -> a row in `ROADMAP.md` (T D F G R scores, budget, stop rule). T + D < 3: do not run.
3. **Pre-register** -> copy `experiments/_template/` to `experiments/E-YYMMDD-NN-slug/`, fill `PLAN.md` *before* any
   compute: hypothesis, controls, what each outcome (SAT / UNSAT / timeout / near-miss) will mean, budget, stop
   rule, power statement (what effect size the budget can detect).
4. **Pilot** -> the smallest instance that could expose a bug in the idea (minutes). Positive control must pass.
   The pilot is also the gate of the long run (the lesson of E-261101-26, whose units all stopped at an
   alternation cap after 15-39 % of their time). It reports:
   * per unit, which limit ended it (alternations, rounds, time, solver timeout, hard cap) and the fraction of the
     budget it used;
   * a projection of the long run's outcome from these numbers.

   The long run starts only if three things hold:
   * the binding limit is the one the PLAN intends;
   * at least one pre-registered prediction still has a real chance (roughly 30-70 %) of failing;
   * every outcome is tied to a decision written in the PLAN.

   Re-check the ROADMAP D score against the pilot; if T + D drops below 3, the run does not start. Otherwise the
   PLAN gets a dated amendment (another limit, a grid, a sharper question) or the run is dropped.
5. **Run** -> when the outcome depends on a parameter (a cap, a budget, a step count), the long run is a small grid
   over that parameter with fewer seeds per cell, not one setting with many seeds. On the week's `lab/` branch (section 7), on the laptop (`caffeinate -dimsu bash run.sh`) or on GitHub
   Actions (section 6). Every run writes a manifest (section 5).
6. **Verify** -> every candidate through `verification/verify_candidate.py`; every UNSAT that is used as evidence
   keeps its formula (SMT2 / CNF hash) so it can be re-checked.
7. **Conclude** -> `CONCLUSION.md`: prediction vs outcome, what may be claimed (with its SPEC label), what not,
   the verdict for the direction, the next step. In the same commit: the `STATUS.md` row(s), the `ROADMAP.md` State
   (plus any new row that passes the gate) and a 1-3 line `experiment-log.md` entry pointing to `CONCLUSION.md`.
   Numbers live in `STATUS.md` and `CONCLUSION.md` only; other files link to them (skill `experiment-conclude`).
8. **Merge** -> PR into `main` once `verify_all.py` passes; the branch is kept for its run history.

## 3. Interpretation rules

* A timeout is never a negative result. An UNSAT holds only for its exact formula. A float zero is nothing until
  the exact verifier says EMBEDDED. A near-miss is not progress unless its defects are non-degenerate (SPEC §3).
* Name the counter in every table (SPEC §4); claims use exact counters only.
* Verdicts carry their budget: "LOW-YIELD@8 core-h, 2 seeds" - a measurement, not a ban. REFUTED needs a proof.
* Before calling a direction low-yield, check the positive control was able to succeed under the same budget;
  if it was not, the verdict is "underpowered".
* A new engine must first reproduce a known object (Szilassi, Roest-Vigh, a saved genus-3 witness), and is scored
  on the benchmark ladder next to the engines already scored there (`STATUS.md` 3b). A ladder table with one engine
  ranks nothing.
* Theorem-level claims need two independent implementations (encoder / verifier) and a human reviewer outside
  the agent chain; the `adversarial-verifier` agent is a filter, not a referee. Every claim that changes a
  FD / witness row gets a `REVIEW.md` (`experiments/_template/REVIEW.md`) written by someone other than its author.
* Infrastructure work must answer yes to at least one question: does it help find an obstruction, find a
  realization, exclude a class of hypotheses, make a result independently checkable, or choose a better
  direction? If not, do not build it.

## 4. Research graph: IDs, files, links

Every idea, hypothesis and experiment is one file with a small header, so that the path from an idea to a result
can be traced (`verification/trace.py` checks the links; the interactive map `map/index.html` draws them).

**IDs.** `<K>-YYMMDD-NN`: kind letter, creation date, number within that day (`NN` = 01..99, three digits if ever
needed). Unique without a central counter, so parallel sessions rarely collide; `trace.py` rejects duplicates.
IDs are permanent: never renumber, never reuse.

| Kind | ID | File |
|---|---|---|
| idea | `I-261030-04` | `ideas/I-261030-04-<slug>.md` |
| hypothesis | `H-261101-02` | `hypotheses/H-261101-02-<slug>.md` |
| experiment | `E-261031-05` | `experiments/E-261031-05-<slug>/README.md` (+ `PLAN.md`, `run.sh`, `results/`, `CONCLUSION.md`) |

Other node references: `FD#` and `DR#` rows of `STATUS.md`; `W:<id>` witnesses (`witnesses/witnesses.json`);
`C:<folder>` certificates (`verification/certificates/<folder>/`); `L:<key>` sources (`literature/README.md`);
`owner` (an idea or decision of the project owner).

**Header.** Between two `---` lines at the top of the file; only `key: value` and `key: [a, b]` lines.

```
---
id: E-261031-05
title: Normals-first with exact offsets, genus 3 -> 4
date: 2026-10-31
status: done            # idea: open | tried | parked; hypothesis: open | supported | weakened | refuted | proved;
                        # experiment: planned | running | done | killed
direction: [DR2]        # optional
origin: [I-261030-04, H-261101-04, E-261030-07, L:schewe2010]   # where it came from (any node kinds)
tests: [H-261101-04]    # experiments only: hypotheses it can move
produces: [FD7, W:lab_type0_genus3]                              # experiments only: results it established
verdict: LOW-YIELD@150 core-h                                    # experiments only, when done
concluded: 2026-11-01   # experiments only, when done or killed: the date of CONCLUSION.md (omit if equal to date)
preregistered: false    # experiments only; false for work reconstructed after the fact
---
```

**Links are stored once, on the child.** An experiment lists its `origin` and the hypotheses it `tests`; "what grew
out of this idea / hypothesis / experiment" is computed in reverse by `trace.py`, never written by hand. Links are
many-to-many: one hypothesis can be the origin of many experiments, one experiment can test many hypotheses.

**Body.** Idea: the idea, why it might help, the cheapest test. Hypothesis: statement, rival, evidence so far,
what would move it. Experiment: goal, origin in prose, method, results (files in `results/`), conclusions (with
`SPEC.md` labels and scope), next steps. Planned experiments also carry their `ROADMAP.md` scores.

## 5. Provenance manifest (every run, every shard)

`experiments/_template/run.sh` writes it automatically: commit SHA, dirty flag, branch, shard / seed, host and
OS, CPU count, Python version, `pip freeze`, start and end time (UTC), exit status, wall-clock seconds, and
core-hours (seconds x workers). The experiment adds its own parameters and the SHA-256 of every input and
output file it claims anything about. Proofs (DRAT / LRAT) are checked during the run and then deleted; the record
keeps the CNF and proof SHA-256 and the checker transcript, and CNFs are rebuilt from the committed encoder when
needed (hash-checked). Proof and CNF files never go into git. A claim that goes into a note gets one replay run
whose proofs go to a GitHub release or Zenodo; git keeps the URL, size and SHA-256 (owner, 2026-11-08).

## 6. Compute

**Laptop** (owner's MacBook, 11 workers): always under `caffeinate -dimsu` (night 4 lost 8 h to sleep); jobs
checkpoint and resume (`overnight/run_overnight.py` does). Launch with `overnight/launch.sh CODE [CODE ...] start
[CORES]` (CODE: the end of an experiment id, e.g. `02-03`; CORES 8-10 for every run whose units can be split, day runs
and lab test runs included, owner 2026-11-08); `run.sh` splits its units
by `SHARDS = CORES`, and a restart with another CORES re-splits the remaining units. At most 10 cores in total (more
freezes the laptop; the launcher refuses past `MAX_CORES`): several experiments in one night are one queue on the
same cores (`launch.sh 02-03 02-04 start`), never side by side. `stop` lets each shard finish its current unit;
`kill` stops at once, and the units in flight rerun from their start. Every command the owner types by hand is a simple `start`, `status` or
`stop` (owner, 2026-11-08): one launcher, no flags, paths or environment to remember. `stop`, a crash and an emergency
interrupt never lose recorded results: finished units stay in `results.jsonl`, logs are appended, and a restart resumes.
Use the `overnight-run-script` skill to write night scripts. Long runs belong to the owner's machine, not to a cloud AI session (its background processes die).

**GitHub Actions** (public repository, free standard runners): `.github/workflows/experiment.yml` runs
`experiments/<ID>/run.sh <shard>` for every shard listed in `experiments/<ID>/matrix.json` (default one shard)
when a commit whose message contains `[run]` is pushed to `experiment/<ID>`, or by hand (Actions tab ->
experiment -> Run workflow, give the ID; the workflow file must be on `main` for that). Limits (2026-10-31):
4 CPU / 16 GB / 14 GB disk per job, 6 h per job (the workflow stops jobs at 350 min), 20 concurrent jobs on a
free plan, 256 jobs per matrix, artifacts kept 90 days. So: shards shorter than 5 h, checkpoint inside the
shard, download results with `gh run download <run-id>` and commit the summary (not raw bulk) before 90 days.
Cloud CPU is spent only on items that passed the scoring rule; it does not replace choosing hypotheses.

`.github/workflows/verify.yml` runs `verification/verify_all.py` on every push and pull request touching
`research/`. `main` must stay green.

## 7. Git

* `main` is the integrated state: site (`index.html`) + research; always passes `verify_all.py`.
* One working branch per week plan (owner, 2026-11-07): `lab/YYYY-MM-DD` (the week plan's date), created from `main`
  by the first session of the week; every lab session of that week commits there, one item at a time. No branch per
  experiment or per session. The branch is merged into `main` by a PR with `verify` green at the next lead review
  (or earlier on the owner's request).
* Night results are committed by the runner (`--git`); push them before starting a new session.
* Tags freeze citable states (`state-YYYY-MM-DD`), e.g. before a write-up or an external review.

## 8a. Choosing the next experiment

* The default next experiment is the top `open` row of `ROADMAP.md`; the order follows the credence table of the
  decision point and the T D F G R scores, and every `CONCLUSION.md` moves the credences by the line its `PLAN.md`
  pre-registered ("scenario move").
* `STRATEGY.md` sets the focus target and may set another exploration share (2026-11-03: one in two).
* One run in four (or the `STRATEGY.md` share) is an **explore** run drawn from the mutation pool (a parked method with one stated change, a
  below-gate row re-scored with a written reason, or a new idea file); it is logged as "explore" and its PLAN says
  what result would make it the new default.
* A construction engine runs on the 12-face target only after it is scored on the benchmark ladder (E-261101-26);
  a failure on the target is not evidence about the engine, a failure on a rung with a known answer is.
* A night run is part of an experiment: it is launched only from an experiment's `run.sh`, after its `PLAN.md` is
  committed, and it is concluded with the `experiment-conclude` skill. "Go and run this" without a PLAN is not a
  valid hand-over.

## 8b. Roles and lightness (owner decision, 2026-11-07)

* **Roles.** The *lead* is a strongest-model session at high effort, about once a week (skill `strategy-review`):
  it analyses the week's results in depth, updates the plan and writes the **week plan**. *Lab* sessions (cheaper
  models, medium effort) execute week-plan items; the owner launches nights and calls the lead when needed.
* **Week plan** = the "Week plan" block at the top of the `ROADMAP.md` S5 queue: at most five items, each with its
  question, budget, kill rule and **follow-up tree** (the conditional next steps allowed without the lead). A lab
  session works only on week-plan items, in order.
* **One item at a time.** Lab sessions run sequentially on the week branch (section 7), taking the first unfinished
  item unless the owner names one in the prompt. Two sessions in one checkout at once only if the owner asks.
* **Escalate, do not improvise.** If the next step is not in the item's follow-up tree, or an item fails its
  control twice, stop that item: write one line under "For the lead" in `CONTINUE_PROMPT.md` and take the next
  item. A lab session never designs a new audit chain on its own.
* **Amendments.** A registered follow-up branch needs no new amendment; record its outcome in `CONCLUSION.md`. At
  most two new amendments per experiment between lead reviews; a third need is an escalation.
* **Batch cheap steps.** Steps with less than ~5 minutes of compute and no target claim run back to back in one
  session and are concluded together (one CONCLUSION section, one ledger commit), not one commit cycle each.
* **Text budgets.** PLAN <= 80 lines; amendment <= 15 lines; CONCLUSION section <= 25 lines; STATUS section <= 8
  lines; log entry 1-3 lines; handover <= 12 lines. State each number once (CONCLUSION) and link to it. Cite the
  `SPEC.md` scope and label once per section instead of repeating caveats in every paragraph. Rigour lives in
  manifests, hashes and checkers, not in prose.

## 8. AI sessions and agents

* Start from `CONTINUE_PROMPT.md` and read the relevant ledger and protocol sections. Follow the owner's current
  request, then any unfinished work in the handover, then the top open `ROADMAP.md` item. Use the project skill
  for the current stage and reuse its instructions while they are in context. The committed experiment plan
  governs that stage.
* Work on one stage at a time. Start each check or run once per set of relevant inputs and wait on its existing
  handle. For a finite command, use a wait suited to its expected duration and read the final status or a short
  log excerpt. Check sooner when a result can change the next action. Reuse a passing verification for the same
  relevant files and environment, including across handover/session boundaries. Before a rerun, name
  the relevant change, failed check, unresolved concern, missing baseline evidence or explicit audit request.
  A new session, report, conclusion or handover is not itself a reason to rerun. Choose affected checks;
  do not run a standalone suite and then a wrapper that repeats it for the same inputs. Run an integrated
  quick check once only when code/evidence changes leave an integration concern. Wording-only edits to
  docs, ledgers, prompts and skills need diff/link/metadata review, not research tests. Changed mathematical
  claims, executable instructions or evidence references need the checks that substantiate them.
* Routine conclusions validate certificate hashes and saved successful checker transcripts, without
  replaying unchanged DRAT each session. Reuse requires recorded CNF, proof and checker provenance.
  Replay once for missing evidence, changed formula/proof/checker, suspected corruption, or an explicit
  audit request. Report reuse versus fresh replay; initial checking of new certificates is mandatory.
  E-261103-03 evidence tests enable audit replay explicitly with `REPLAY_DRAT=1`.
* For code navigation, query CodeGraph for the specific symbol or call path with a small file limit. Use
  targeted text searches for research documents and log excerpts.
* Before handing over a launch, exercise the owner's actual entry point in a bounded startup check from the
  same working directory with the same shell, environment, and executable selection. Use a bounded budget or
  fixture without bypassing normal dispatch. Confirm that workers reach the intended job and stop cleanly.
  Record the command, outcome, and any substitutions or limits. If that path cannot be exercised, mark
  startup unverified in the handover. Reuse valid baseline/post-change checks under the policy above.
* Keep one short handover block in `CONTINUE_PROMPT.md`: branch or commit, in-flight state, next action and
  exact command if needed, and verification scope. Link to the plan, ledger, and artifacts for details.
* Ask the owner before launching large subagent tasks (usage limits). Agents: `.claude/agents/` (7 roles).
* Report to the owner in Russian; write repository files in English. Never weaken the requirements, never
  fabricate results, report failures with their output.
