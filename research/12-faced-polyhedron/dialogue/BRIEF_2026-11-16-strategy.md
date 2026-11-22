# Brief: strategy and new-ideas dialogue of 2026-11-16 (thread `2026-11-16-strategy`)

## How to start

1. Owner: `python3 research/12-faced-polyhedron/dialogue/chat.py serve`, open the page, ＋ a dialogue named
   `2026-11-16-strategy`.
2. Connect two agents (dispatched, memory `resume`):
   * `claude`: Claude Code, `claude-fable-5-2`, effort `high` (`xhigh` for R1 and R4 if the owner wants more depth);
     the **lead**;
   * `astra`: Codex, `gpt-6-astra`, effort `high`; the **critic**.
3. Owner: post the agenda (or "default agenda") with "who answers" = all agents. That opens R1.

No lab session runs in this checkout during the dialogue, and no dialogue runs during an owner night.

## 1. Purpose, roles and output

Two parts, one thread:

* **Part A, strategy.** The strategy of 2026-11-16b (`STRATEGY.md` §1, `reviews/strategy-review-2026-11-16b.md`)
  came from a single-model lead review with no second opinion. Stress-test it: are its premises right, is the order
  right, what is the shortest route on one laptop to a new face-neighbourly polyhedron that passes the significance
  filter, and what would make S0 more tractable?
* **Part B, the owner's ideas** (§2b): can projective geometry, algebraic geometry (complex projective varieties,
  the Hodge conjecture) or differential geometry give the project a construction method or an obstruction?

Roles are deliberately unequal.

* `claude` (lead) proposes, develops, drafts the shortlist and writes `SYNTHESIS.md`.
* `astra` (critic) does not need to propose routes. Its job is to break the lead's claims: wrong or unchecked
  assumptions, a hidden restriction of scope, prior work (an existing id, a parked method, a known theorem), a broken
  project rule, an infeasible cost. It may add at most one alternative per message, and only when it argues that the
  alternative beats a route of the lead.
* The lead answers every numbered objection of the critic: accept (`CHANGED: ...`), rebut with a reason or a check,
  or mark it disputed. An objection may not be dropped silently.

Output: `SYNTHESIS.md` in the thread (§6), approved by the owner. Nothing in the dialogue is evidence: both models
are AI sessions, which the project does not count as independent reviewers (`SPEC.md` §5).

## 2. Before R1

Read, and no more than this: root `CLAUDE.md` / `AGENTS.md` (hard rules); `STRATEGY.md`; `STATUS.md` §0, §1, 3aq to
3at, §4, §6; `ROADMAP.md` week plan, the constructive queue, "Parked methods" and "Decision point"; `SPEC.md` §1,
§2, §4, §5; `PROTOCOL.md` §2 (scores); `reviews/strategy-review-2026-11-16b.md`; `reviews/dialogue-2026-11-10-strategy.md`
(what the last dialogue decided). Later, read a file only when an argument needs it.

The project holds about 170 ideas. **Before proposing one, search the titles in `map/graph.json`.** If it exists,
cite its id and say what is new; if its method is parked, say what is different (project rule).

### 2a. Default agenda, part A

* A1. Premises of 16b: the (8, 3) census bound (>= 34,402 classes after 551 of 1806 patterns, a session check), the
  (11, 5) price (>= 41 nights), the reading of the S6 (10, 3) and (10, 4) UNSAT-SOLVER sets. Which conclusion of 16b
  would change if one of them is wrong, and what cheap check would show it?
* A2. Order: is S1 with nine faces by map-free methods the right first target? Does the census-free OM-SAT ladder
  ((7, 1), (8, 2), (8, 3), then (9, 4), (9, 5)) have a price and a kill rule before its first night?
* A3. Is the significance filter (owner, 2026-11-12) applied correctly, or does it hide a cheaper significant target?
* A4. Blind spots: a wrong assumption in the model or an encoder, a method from another field.

### 2b. Default agenda, part B (the owner's notes, translated)

* B1. Projective geometry, including the Hodge conjecture: can a solution polyhedron be built in projective space?
  Or, conversely: take projections of polyhedra in projective space, study them, and find features that only
  solution polyhedra have.
* B2. Algebraic geometry, and complex projective algebraic varieties.
* B3. Differential geometry.

These are directions, not claims. For each, first translate it into at most three precise mathematical questions
about this problem (what object, which space, which statement would help, and how). Then map each question to
what the project already has; starting points in `map/graph.json` include the projective charting ideas
(I-261029-15, I-261030-12, I-261030-30, I-261116-01 and E-261116-04), the oriented-matroid and final-polynomial line
(I-261029-41, I-261029-45, I-261101-12), complex and tropical methods (I-261029-10, I-261029-19) and the Gauss-map and
curvature line (I-261029-02, I-261101-13, I-261101-14, H-261101-03). Say plainly when a direction does not apply
(for example, which part of the Hodge conjecture would touch a real semialgebraic realization problem, if any), and
when it applies only as a restatement of something already done.

## 3. The four axes (owner's requirement)

Every route, idea or strategy item that a model evaluates gets four marks, each 0 to 3 with one line of reason:

1. **Mathematical validity**: no errors, no unchecked assumptions, no hidden restrictions.
2. **Scientific novelty**: is the approach new, or has it been studied (in the project: an id; in the literature: a
   reference, CLAIMED if from memory)?
3. **Research leverage**: could it open a whole class of new approaches or of mathematical obstructions?
4. **Computational feasibility**: can it give a meaningful result without large-scale brute force, on <= 10 cores
   and nights of <= 80 core-h?

The marks are planning weights (CONJECTURE), not evidence. The critic gives its own marks to every item of the lead
and names the axis it disputes most.

## 4. Rounds

Line caps are per message (the transport refuses more than 60). Use the `--round` labels given here. In an
alternating round each post names the other model as `next`, and the last post of the round names `owner`.

| Round | Mode | `next` | Content |
|---|---|---|---|
| R0 | owner | `all` | the agenda |
| R1 positions | sealed, 60 lines | `owner` (the owner then gives the floor to `astra`) | **claude**: (a) the strongest objection to 16b; (b) three routes, ranked: idea in two lines, why it might work, cheapest test (<= 3 core-h or one night), kill rule, what a success changes, four marks; (c) B1-B3: the precise questions of §2b, each with four marks and keep / park / drop; (d) one wild idea; (e) the weakest claim of the message. **astra**: (a) the three weakest premises of 16b with a check each; (b) B1-B3, independently: the precise questions and four marks; (c) the weakest claim of the message |
| R2 critique | alternating, 2 turns from astra, 60 lines | claude ends with `owner` | **astra**: numbered objections to claude's R1 (each: the claim in its strongest form, the failure mode, a check, ideally 10 minutes; four marks of its own). **claude**: answers every number; adopts what is right; ends with **For the owner** |
| C1 | owner | `claude` | answers, a steer, what survives |
| R3 develop | alternating, 5 turns from claude, 50 lines | claude ends with `owner` | **claude** makes each surviving item concrete: parameters, encoding, the repository code it reuses, cost, kill rule; reports any check it ran. **astra** checks each against the project rules, prior ids and the cost, and attacks the kill rules. The last turn (claude) ends with **For the owner** |
| C2 | owner | `claude` | answers, which items go to the shortlist |
| R4 converge | alternating, at most 5 turns from claude, 60 lines | claude ends with `owner` | **claude** drafts the tables of §6; **astra** accepts or amends each row with a reason; anything still disputed after two exchanges goes to "Disagreements" unchanged. claude writes `SYNTHESIS.md` and posts the owner digest |
| C3 | owner | `close` | approves, edits or rejects |

## 5. Conduct

**Constructive and critical at once.**

1. State the other's idea in its strongest form before attacking it.
2. A critique names a failure mode and a check that would expose it. "I doubt it" is not a critique.
3. No empty agreement: "agreed" comes with a consequence, an extension or a sharper test. The critic that finds
   nothing wrong with an item says what it checked.
4. In R1 propose without self-censorship; R2 is where ideas are judged.
5. Each message names its own weakest claim. When you change your mind, write `CHANGED: from X to Y because Z`.
6. Disagree with the owner too, plainly, including about the owner's own ideas in part B.

**Honest about evidence.**

7. Every factual claim carries a `SPEC.md` §5 label and a source: a file of the repository, a computation of this
   thread, or "memory". A literature claim from memory is CLAIMED and cannot carry a decision until someone looks it
   up. A theorem quoted for part B is quoted with its exact hypotheses.
8. **Settle by computing, not by arguing.** A dispute that a script can decide in 10 minutes is decided by the
   script: saved in `work/<you>/`, at most 10 minutes of wall time and 8 processes, reported with the command, the
   run time, the numbers and a label (NUMERICAL or EXACT). Such a number is a session check, not a result. Never
   start a longer run. If anything looks like a candidate object, stop, tell the owner in the chat and follow the
   `candidate-check` skill; nobody calls it a result before that.
9. Never weaken a target and never describe an S1, S5 or S6 object as a step solved towards S0 (root hard rules).
   A timeout is not a result; an UNSAT holds only for its exact formula; an UNSAT-SOLVER is no negative result.

**The owner in the room.**

10. An owner message is answered first, in the next message of whoever holds the floor.
11. Every **For the owner** block is at most 5 lines of plain language, a term explained where it is not everyday:
    what survived, what died and why, where the models disagree, and one to three questions only the owner can
    answer (priorities, risk, laptop nights, what counts as success).
12. Language: the models write to each other in English, with the project's terms. **For the owner** blocks and
    direct answers to the owner are in the owner's language.

## 6. `SYNTHESIS.md` (English, at most 140 lines; the only part of the thread that is committed)

1. **Owner digest**, 10 lines: verdict on the 16b strategy, the top three routes, the verdict on B1-B3, what needs
   approval.
2. **Strategy shortlist**, at most 7 rows, ranked: idea (existing id or NEW), target, cheapest test, cost in core-h
   or nights, kill rule, the four marks (lead / critic), proposed T D F G R scores (`PROTOCOL.md` §2), who objected
   and why.
3. **Owner's ideas**: per precise question of B1-B3: the question, the existing ids it maps to, the four marks
   (lead / critic), keep / park / drop, and the cheapest next step if kept.
4. **Drop or demote**: items of the current week plan or queue that the dialogue argues against, with the reason.
5. **Disagreements**: both positions, three lines each, and the check that would decide.
6. **Computed in this thread**: script, command, numbers, label. **Not checked**: the claims that rest on memory.

After the owner approves in C3, the `claude` session copies `SYNTHESIS.md` to
`reviews/dialogue-2026-11-16-strategy.md`, commits it on the lab branch and does not push. Filing the approved
ideas, hypotheses and ROADMAP rows, and any change of `STRATEGY.md`, is a separate lead session.
