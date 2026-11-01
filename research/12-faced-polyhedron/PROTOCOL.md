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
| `experiments/E##-slug/` | one experiment: plan, runner, results, conclusion | see section 2 |
| `theory/`, `ideas/`, `reviews/`, `reports/`, `literature/` | supporting material | ideas are a backlog, not a plan |
| `archive/` | superseded documents | read-only history |

## 2. Experiment lifecycle

1. **Idea** -> `ideas/` (one line is enough).
2. **Score and queue** -> a row in `ROADMAP.md` (T D F G R scores, budget, stop rule). T + D < 3: do not run.
3. **Pre-register** -> copy `experiments/_template/` to `experiments/E##-slug/`, fill `PLAN.md` *before* any
   compute: hypothesis, controls, what each outcome (SAT / UNSAT / timeout / near-miss) will mean, budget, stop
   rule, power statement (what effect size the budget can detect).
4. **Pilot** -> the smallest instance that could expose a bug in the idea (minutes). Positive control must pass.
5. **Run** -> on branch `experiment/E##-slug`, on the laptop (`caffeinate -dimsu bash run.sh`) or on GitHub
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
* A new engine must first reproduce a known object (Szilassi, Roest-Vigh, a saved genus-3 witness).
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
output file it claims anything about. Large proof files (DRAT / LRAT) go to a GitHub release or Zenodo; git
keeps the URL, size and SHA-256.

## 6. Compute

**Laptop** (owner's MacBook, 11 workers): always under `caffeinate -dimsu` (night 4 lost 8 h to sleep); jobs
checkpoint and resume (`overnight/run_overnight.py` does). Use the `overnight-run-script` skill to write night
scripts. Long runs belong to the owner's machine, not to a cloud AI session (its background processes die).

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
* One branch per experiment: `experiment/E##-slug`; documentation / infrastructure work: `claude/<topic>`.
* Night results are committed by the runner (`--git`); push them before starting a new session.
* Tags freeze citable states (`state-YYYY-MM-DD`), e.g. before a write-up or an external review.

## 8. AI sessions and agents

* Start from `CONTINUE_PROMPT.md`; read `STATUS.md` and `ROADMAP.md` before acting; the first task is the top
  open `ROADMAP.md` item unless the owner says otherwise.
* Ask the owner before launching large subagent tasks (usage limits). Agents: `.claude/agents/` (7 roles).
* Report to the owner in Russian; write repository files in English. Never weaken the requirements, never
  fabricate results, report failures with their output.
