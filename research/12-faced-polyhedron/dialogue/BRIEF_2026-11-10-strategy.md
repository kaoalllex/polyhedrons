# Brief: strategy dialogue of 2026-11-10 (thread `2026-11-10-strategy`)

## How to start

1. Owner: `python3 research/12-faced-polyhedron/dialogue/chat.py new 2026-11-10-strategy`, then
   `... chat.py serve 2026-11-10-strategy` and open the page.
2. Start two sessions in this checkout, the strongest model of each vendor at high effort, and paste to each, with
   its own name:
   > You are `claude` (or: `astra`) in a research dialogue. Read `research/12-faced-polyhedron/dialogue/TRANSPORT.md`
   > and `research/12-faced-polyhedron/dialogue/BRIEF_2026-11-10-strategy.md` and follow them. Thread:
   > `2026-11-10-strategy`.
3. Owner: post the agenda in the page with "who answers" = `both`. That opens round 1.

No lab session runs in this checkout during the dialogue, and no dialogue runs during an owner night.

## 1. Purpose and output

Two AI sessions of different vendors and the owner stress-test the strategy adopted on 2026-11-10 and look for
better routes. The question: **what is the most promising way, on one laptop, to a new face-neighbourly polyhedron,
and what would make the 12-face problem (S0) itself more tractable?**

Output: `SYNTHESIS.md` in the thread (§5), approved by the owner. Nothing in the dialogue is evidence: both models
are AI sessions, which the project does not count as independent reviewers (`SPEC.md` §5). Approved items are filed
in the project's formats afterwards by a separate Claude session, not during the dialogue.

## 2. Before round 1

Read, and no more than this: root `CLAUDE.md` / `AGENTS.md` (hard rules); `STRATEGY.md`; `STATUS.md` §0, §2, 3d,
3ad, §4; `ROADMAP.md` week plan, the constructive queue and "Decision point"; `SPEC.md` §1, §2, §5;
`reviews/strategy-review-2026-11-10.md`; `reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §1-§5. Later, read a file
only when an argument needs it.

The project already holds about 150 ideas. **Before proposing one, search the titles in `map/graph.json`.** If it
exists, cite its id and say what is new; if its method is parked, say what is different (project rule).

Default agenda, used where the owner's opening message is silent:

* Q1. Is the target set right (S6 at (10, 3); S1 with the genus free at 9, 10, 12 faces; S5 at (10, 4) under a rule)?
* Q2. The shortest route to any new polyhedron with at most 10 cores and nights of at most 80 core-h.
* Q3. What structural fact or method would make S0 tractable, or show why it is not?
* Q4. What are we blind to: a wrong assumption in the model or encoder, a method from another field?

## 3. Rounds

Line caps are per message. "Sealed" means both models are on the floor and the transport hides each answer until
both are in. Use the `--round` labels given here.

| Round | Mode | `next` | Content |
|---|---|---|---|
| R0 | owner | `both` | the agenda |
| R1 positions | sealed, 60 lines | `both` | (a) your strongest objection to the current strategy; (b) three routes, ranked: the idea in two lines, why it might work, the cheapest test (at most 3 core-h or one night), its kill rule, what a success changes; (c) one wild idea: low odds, high payoff; (d) one thing you think the project assumes wrongly; (e) your weakest claim in this message |
| R2 critique | sealed, 60 lines | `owner` | for each route of the other model: its strongest form in two lines, then the most likely way it fails and a check that would show it (computable in 10 minutes if possible), then keep / change / drop; one idea of theirs you adopt and why; where they were right and you were wrong; **For the owner**: at most 5 lines, see §4 |
| C1 | owner | one model | answers, a steer, and which model opens R3 |
| R3 develop | alternating, 6 turns, 50 lines | the other model; the 6th turn `owner` | each turn does at least one of: makes a surviving idea concrete (parameters, encoding, which code of the repository it reuses), merges two ideas, reports a check it ran, sharpens a kill rule. Prefer building on the other model's idea. The 6th turn ends with **For the owner** |
| C2 | owner | one model | answers, and which model drafts the shortlist |
| R4 converge | alternating, at most 4 turns, 60 lines | the other model; the last `owner` | the named model drafts the shortlist table of §5; the other accepts or amends each row with a reason; whatever is still disputed after two exchanges goes to "Disagreements" unchanged. The drafter then writes `SYNTHESIS.md` and posts its owner digest |
| C3 | owner | `close` | approves, edits or rejects the shortlist |

## 4. Conduct

**Constructive and critical at once.**

1. State the other's idea in its strongest form before attacking it.
2. A critique names a failure mode and a check that would expose it. "I doubt it" is not a critique.
3. No empty agreement: "agreed" comes with a consequence, an extension or a sharper test.
4. Generation and evaluation are separate: in R1 propose without self-censorship; R2 is where ideas are judged.
5. Each message names its own weakest claim. When you change your mind, write `CHANGED: from X to Y because Z`.
6. Do not converge early. If both rank the same route first after R2, each spends at least 10 lines of R3 on the
   strongest alternative.
7. Disagree with the owner too, plainly, when the argument calls for it.

**Honest about evidence.**

8. Every factual claim carries a `SPEC.md` §5 label and a source: a file of the repository, a computation of this
   thread, or "memory". A literature claim from memory is CLAIMED and cannot carry a decision until someone looks it
   up. A credence is a number and a planning weight (CONJECTURE), never evidence.
9. **Settle by computing, not by arguing.** A dispute that a script can decide in 10 minutes is decided by the
   script: saved in `work/<you>/`, at most 10 minutes of wall time and 8 processes, reported with the command, the
   run time, the numbers and a label (NUMERICAL or EXACT). Such a number is a session check, not a result; the other
   model may rerun it. Never start a longer run. If anything looks like a candidate object, stop, tell the owner in
   the chat and in your terminal, and follow the `candidate-check` skill; nobody calls it a result before that.
10. Never weaken a target and never describe an S1, S5 or S6 object as a step solved towards S0 (root hard rules).

**The owner in the room.**

11. An owner message is answered first, in the next message of whoever holds the floor, before anything else.
12. Every **For the owner** block is at most 5 lines of plain language, a term explained where it is not everyday:
    what survived, what died and why, where the models disagree, and one to three questions only the owner can
    answer (priorities, risk, compute nights, what counts as success).
13. Language: the models write to each other in English, with the project's terms. **For the owner** blocks and
    direct answers to the owner are in Russian.

## 5. `SYNTHESIS.md` (English, at most 120 lines; the only part of the thread that is committed)

1. **Owner digest**, 10 lines: verdict on the current strategy, the top three routes, what needs approval.
2. **Shortlist**, at most 7 rows, ranked: idea (existing id or NEW), target, cheapest test, cost in core-h or
   nights, kill rule, proposed T D F G R scores (`PROTOCOL.md` §2), who proposed it, who objected and why.
3. **Drop or demote**: items of the current week plan or queue that the dialogue argues against, with the reason.
4. **Disagreements**: both positions, three lines each, and the check that would decide.
5. **Computed in this thread**: script, command, numbers, label. **Not checked**: the claims that rest on memory.

After the owner approves in C3, the `claude` session copies `SYNTHESIS.md` to
`reviews/dialogue-2026-11-10-strategy.md`, commits it on the lab branch and does not push. Filing the approved
ideas, hypotheses and ROADMAP rows is a separate lead session.
