# Prompt: make dispatched dialogues cheaper, observable and harder to waste

## How to run

Open a coding session in the repository on the current lab branch with a strong coding model at high effort (the
task touches the dispatcher, the stream parsers, the page and the contract). Paste everything below the line. The
session asks the owner before any change that the list below does not cover.

-----

Improve the dispatched mode of `research/12-faced-polyhedron/dialogue/chat.py` and its page. **Read
`dialogue/TRANSPORT.md`, `dialogue/README.md` and `dialogue/HOWTO_RU.md` first.** Every behaviour change is written
into `TRANSPORT.md` (contract) and `README.md` (owner's guide) in the same commit; also update the owner's local
Russian guide `HOWTO_RU.md`, which is excluded from git and stays untracked.

## Why (evidence from thread `2026-11-16-strategy`, 2026-11-16/17)

* The lead ran in mode `resume`. Its session grew to about 370,000 tokens of context; every tool call of a turn
  re-reads all of it from the prompt cache, which is cheap per token but still counts against the usage limit. One
  turn that wrote a 37-line message read about 2.0 M cached tokens, wrote 0.35 M to the cache and generated 57,000
  tokens (49,000 of them thinking), about 8 USD at list price.
* The cache was lost twice: a turn started four hours after the previous request (cache TTL one hour: 387,000
  tokens written again), and a turn ran under another account ("Claude can't use thinking from another organization":
  284,000 written again). Nothing on the page showed either.
* The laptop slept during a turn: "Connection lost while your computer was asleep" and ECONNRESET for about an hour,
  CLI-internal `api_retry` events, then the 5-hour usage limit. The console hides `system` events other than `init`,
  so the owner saw nothing but a silent agent and asked "?".
* The owner's "stop!" was a message; the running turn kept spending until its post was refused (exit 5).
* The first response of one turn took 375 s of thinking before the first token; the owner had no way to see or cap it.
* The owner closed the thread with `close` right after approving the synthesis. Closing starts no agent, so the
  brief's post-approval step (copy `SYNTHESIS.md` to `reviews/`, commit) never ran; `threads/` is git-ignored, so the
  approved text existed only on the laptop.

## Changes, in priority order

1. **Context and cost meter per agent.**
   * Parse usage from both runners: Claude `assistant` events (`message.usage`: `input_tokens`,
     `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`), its `result` event (`modelUsage`
     with `contextWindow`, `total_cost_usd`), and Codex `turn.completed.usage`. Context size of a request = input +
     cache read + cache creation. Keep, per agent and per turn, in `dispatch.json`: last context size, context window,
     peak, cumulative cache reads, cache writes, output and thinking tokens, cost when the runner reports it, the time
     of the last request.
   * Show it on the page next to each agent: a fill bar "context 370k / 1M (37 %)", this turn's and the thread's
     totals, and the time since the last request.
   * Each turn appends one line to `work/NAME/usage.jsonl` (turn, attempt, context, reads, writes, output, cost,
     wall time, exit reason), so a thread can be audited after the fact.

2. **Warnings before waste.** Shown on the page (agent chip and console), never silently acted on unless the owner
   enabled the action:
   * *cold cache*: the next turn of a `resume` agent starts more than the runner's cache TTL (runner field, default
     60 min for Claude; check Codex's) after its last request and its context is above a threshold (default 150k):
     "next turn re-writes about N tokens; consider fresh";
   * *large context*: context above a threshold (default 40 % of the window or 250k): suggest switching to `fresh`;
   * *account or model change* detected in the stream (the "another organization" notice, a different model in
     `init`): the cache is gone;
   * *runaway turn*: thinking or output of the running turn above a threshold (default 30k tokens or 10 minutes
     without a tool call or a post), using the streamed `thinking_tokens` estimates where present.

3. **Automatic `fresh` with a handover.** An optional per-agent setting `auto_fresh_at` (tokens). When the last
   context exceeds it, the next turn runs `fresh`. The turn prompt of every `resume` turn then also asks the agent to
   keep `work/NAME/HANDOVER.md` (at most 40 lines: position, open objections, promised items) current, and the
   `fresh` prompt reads it. Keep the existing `fresh` mode semantics otherwise.

4. **Per-turn budgets.** Optional per-agent caps passed to the runner where it supports them (Claude `-p` has
   `--max-budget-usd`; check `--help` of both installed CLIs and use only flags that exist) plus a dispatcher cap on
   wall time per turn, default 20 minutes instead of 60. The turn prompt states the budget and tells the agent to
   write its draft early and post before the cap. A turn stopped by a cap is a failure with reason "budget", visible
   on the page.

5. **Keep the laptop awake.** `serve` starts `caffeinate -dimsu -w <its own pid>` on macOS when the binary exists
   (skip silently elsewhere; a flag `--no-caffeinate` turns it off), and the page header says "awake" or warns
   "may sleep". Document "on AC power" in the guides.

6. **Do not retry blindly.** Show `api_retry` and `api_error` system events in the console (today they render as
   nothing). Classify a failed turn: connection or sleep, usage limit, budget, timeout, no post. After a connection
   failure of a `resume` agent with a context above the cold-cache threshold, do not retry automatically: mark it
   "waiting for owner" with the reason; the owner wakes it or switches it to `fresh`. Usage-limit handling stays.

7. **Stop a running turn.** A page button "stop turn" per running agent (SIGTERM to its process group, SIGKILL after
   10 s, as the timeout path does), and an option on the composer: "send and stop running turns". The stopped turn's
   draft, if any, stays in `work/NAME/`.

8. **Closing with a final step.** The brief may name a post-approval task. Add an owner choice next to `close`:
   "approve and close", which hands the floor to the lead once with a finish prompt (the brief's post-approval step:
   copy the synthesis, commit, no push) and closes the thread after that post. Plain `close` on a thread whose brief
   names such a step asks for confirmation on the page. The CLI keeps `close` unchanged.

## Constraints

* Standard library only; one file `chat.py` plus `page.html`; tests in `test_chat.py` (fake runners emitting
  recorded stream-json lines for both vendors, a fake clock; no network, no real model). Do not test with a
  pseudo-terminal (`pty`, `script`) and do not add the tests to `verification/verify_all.py`.
* Thresholds live in the thread's `agents.json` entry or in `runners.json`, with the defaults above; no new config
  file.
* Root `AGENTS.md` / `CLAUDE.md` apply: English in code and commits, small diff, no speculative features. Commit on
  the current lab branch; do not push.
* Run only `python3 research/12-faced-polyhedron/dialogue/test_chat.py` (and any focused tests you add); report the
  output.

## Also change the brief template (text only, next brief)

* Allow the 10-minute checks of §5.8 again, but under the per-turn budget of item 4; the owner may forbid them for a
  round.
* `SYNTHESIS.md` gets a technical appendix (specifications, kill rules, file and line references) that a lab
  session can build from, because the thread itself is not in git; the 140-line cap applies to the main part only.
* Ideas first raised in the last round get at least one critique turn before they can rank above items that went
  through R2-R3, or the synthesis marks them "one critique round".

When done, delete this file in a separate commit, as was done with the previous build and improvement prompts.
