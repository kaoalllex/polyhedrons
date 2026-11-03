---
name: strategy-review
description: Use when the owner asks for a strategy review, a re-ranking or re-scoring of the ideas, hypotheses, experiments and ROADMAP of the 12-face research, or when STRATEGY.md says a review is due (every 3-4 nights, or after a result that moves a scenario by 0.1 or more). Runs in its own session with the strongest model.
---

# Strategy review of the research

Paths are relative to `research/12-faced-polyhedron/`. The review advises; it changes no ledger file. Its output is
one report and one proposed queue, which the owner approves before any session applies them.

## Setup

* A separate session, not a subagent of a working session: the review needs a clean context and may ask the owner
  questions. Strongest model available, effort high or above.
* If a dated prompt exists (`reviews/REVIEW_PROMPT_YYYY-MM-DD.md`), it holds this review's specific questions;
  follow it together with this skill.
* Small checks are welcome (code, data, `verification/verify_all.py --quick`); no computation longer than ~10 min,
  no night runs, no edits outside `reviews/`.

## Read

`STRATEGY.md` (the current stance and targets; the review may recommend changing it, never changes it), `STATUS.md`,
`ROADMAP.md`, `SPEC.md`, `PROTOCOL.md` §2, §8a; the last two night reports in `reports/`; the `CONCLUSION.md` of
every experiment concluded since the previous review (`experiment-log.md` tells which); the previous
`reviews/strategy-review-*.md`; `map/graph.json` for the full list of ideas, hypotheses and experiments with their
status and links (read the files themselves only for the candidates you rank).

## Do

1. **Verdict on the strategy.** Does the evidence since the last review support `STRATEGY.md`? Name what would
   change it.
2. **Re-score every open candidate** (ideas with status open, hypotheses open, experiments planned or open) on
   T D F G R (ROADMAP "Scoring") under the current strategy, plus two columns the strategy adds: **jump** (2 = reaches
   the focus target's genus without a ladder, 0 = a ladder step) and **cost to first kill** (sessions or core-h to
   the first result that could park it). Candidates that serve the parked target only are listed separately, not
   dropped.
3. **Propose the queue**: the top 5-8 items in order, each with its hypothesis, the cheapest falsifying test, what
   each outcome changes, the budget and the stop rule; mark which are "explore". Name the single first item.
4. **Missing ideas**: at most 5 new ones, concrete enough for an idea file (statement, why, cheapest test). Prefer
   ideas from neighbouring fields; label each CONJECTURE.
5. **Audit**: claims stronger than their evidence, underpowered verdicts, follow-up chains that should stop
   (STRATEGY.md §2 follow-up rule), with file:line.
6. **Scenario credences**: propose new values with one line of evidence each, or say why they stay.

## Output

`reviews/strategy-review-YYYY-MM-DD.md`: a 10-line verdict; the answers above; the scored table; the proposed queue;
new ideas; audit findings; the 3 things to do first. Label every factual statement VERIFIED (checked in code or
data), PLAUSIBLE or CONJECTURE. Commit the report on the current branch; do not push. Then tell the owner, in
Russian, the verdict and the proposed first item; the owner decides, and a working session applies the approved
changes to `ROADMAP.md`, `STATUS.md` and the idea files.
