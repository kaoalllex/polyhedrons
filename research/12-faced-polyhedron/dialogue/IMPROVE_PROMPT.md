# Prompt: make the dialogue chat event-driven (no waiting models, automatic resume after limits)

## How to run

Open a coding session in the repository on the current lab branch, with a mid-tier coding model at medium effort
(about 300 added lines of standard-library Python, a few page elements, tests). No dialogue thread may be running
in this checkout. Paste everything below the line.

-----

Extend `research/12-faced-polyhedron/dialogue/chat.py` so that **a model spends tokens only when it has something
new to read and something to say**. Read `dialogue/TRANSPORT.md` (the contract), `dialogue/chat.py` and
`dialogue/test_chat.py` first. Keep everything that works today: files as the only state of a thread, the derived
floor, sealing, the single writer path, the owner's page.

## Why (observed in the thread `2026-11-10-strategy`, 2026-11-10 to 2026-11-12)

1. **Waiting costs tokens.** A model session calls `wait` in a loop; every timeout (540 s) is one more model turn
   over its whole context. Thirty minutes of waiting are four paid turns that carry no information.
2. **Checking costs tokens and still misses messages.** Sessions run `status` before a post; one owner message
   arrived while a model was computing and was not answered in its next post.
3. **Nobody resumes a model after its usage limit resets.** A session that hits the limit stops; the thread stalls
   until the owner notices.
4. **The ad-hoc fix failed.** A per-model watcher resumed a vendor session once, got "thread already has an active
   writer" (the same session was still open in a terminal) and stopped by design, with no retry.

## Design: the chat server is the dispatcher

`chat.py serve <thread>` is already the one long-lived process, in the owner's terminal. It gains a dispatcher: when
a model has to speak, the server starts that model's command, hands it the unseen messages, and waits for the
process to exit. Between turns no model process exists. Models never call `wait` or `status` in this mode.

**Agent commands are local configuration, never chat content.**

* `chat.py agent <thread> --as NAME [--mode resume|fresh] [--limit-pattern REGEX] -- ARGV...` writes
  `threads/<thread>/agents.json`; `chat.py agent <thread> --as NAME --off` removes the entry. `ARGV` is a list;
  the placeholders `{prompt_file}`, `{thread}` and `{name}` are substituted per element. Nothing received over
  HTTP and nothing written in a message can create or change a command.
* Start with `subprocess.Popen(argv, shell=False, stdin=DEVNULL, cwd=<repository root>)`, output appended to
  `work/<name>/wake-<n>-<attempt>.log`. No shell, no pseudo-terminal. Message text reaches the model only inside
  the prompt file.
* The vendor commands are the owner's business. Give two examples in `HOWTO` wording, each marked "check against
  the installed CLI's `--help`": a headless resume of a Claude Code session, and
  `codex exec ... resume SESSION PROMPT` as used in `threads/2026-11-10-strategy/work/astra/watch_dialogue.py`.
  Do not hard-code either in `chat.py`.

**When to wake.** Derived from the files, like the floor: a model needs a turn when the thread is open, the model is
on the floor and has no held message. Per model the dispatcher is in one of: `idle`, `running` (pid, since),
`backoff` (attempt, next try, last error line), `stalled`, `off`. Retry bookkeeping lives in
`threads/<thread>/dispatch.json`, safe to delete; after a server restart a recorded pid is probed before anything is
started. **Never two processes for one model.** In a parallel step both models are started at once.

**The turn prompt** (`work/<name>/turn-<n>.md`, written by the dispatcher): who you are, the thread, the paths of
the contract and the brief ("read them only if they are not in your context"), the path of your notes file, then
every unseen message in full (the selection `wait` prints today, so a held answer of the other model is never
included), then the fixed instruction: do the step the brief prescribes; post once with
`chat.py post <thread> --as NAME --next WHO --seen <n> --file PATH`; append at most 30 lines to
`work/<name>/NOTES.md` (decisions, open items, files); end your turn. Do not call `wait` or `status`, do not poll.

**`post --seen N`.** If a message by another author with a number above N is published, refuse with exit code 5,
print those messages, write nothing: the model amends its answer in the same turn. Without `--seen` the command
behaves as today. This replaces "run `status` before every post".

**After the process exits.**

* The model posted (the floor moved, or its answer is held): `idle`; wake whoever is on the floor now.
* Non-zero exit, or exit 0 without a post: a failed attempt. Retry after 1, 5, 15, 30 minutes, then every 30
  minutes. If `--limit-pattern` matches the log and its named group `reset` (clock time) or `seconds` parses, the
  next attempt is at that time plus 60 s instead. After 24 hours or 3 consecutive exits without a post: `stalled`,
  shown to the owner, no further attempts until "wake now".
* A turn longer than `--turn-timeout` (default 60 minutes) is terminated (SIGTERM, SIGKILL after 10 s) and counted
  as a failed attempt.
* `--mode fresh` starts a new session each turn; its prompt additionally says to read the contract, the brief,
  `NOTES.md` and the thread's `HANDOVER.md` first. `resume` keeps the model's private context but pays for the whole
  context again after a long pause; `fresh` has a bounded cost per turn and relies on `NOTES.md`. Document the
  trade-off; the owner chooses per model.

**Spending guards.** After `max_auto_turns` consecutive model turns without an owner message (default 12, in
`thread.json`), the dispatcher pauses and the page says so; any owner message resets the count. `serve --no-dispatch`
runs the page alone.

**The page.** One chip per model: state, running time or next attempt, last error line. Buttons: "wake now",
"pause auto", "resume auto". Their `POST` endpoints use the existing `Origin` / `Host` check and can only start
commands that `agents.json` already holds.

**Interactive mode stays.** `wait` and a model session in its own terminal work as today (`TRANSPORT.md` §4). State
in the contract that a dispatched model must not be open interactively at the same time, and why.

## Constraints

* Python 3.9+ standard library only, still one file `chat.py`; no network access. Tests in `test_chat.py`.
* Update `TRANSPORT.md` (§3 commands and exit code 5, §4 the two modes, §5 "commands are configuration") in the same
  commit. `HOWTO_RU.md` is the owner's local untracked note: propose its new section in your final message, do not
  commit it.
* Root `AGENTS.md` / `CLAUDE.md` apply: English, small diff, no speculative features, no pseudo-terminal in code or
  tests. Commit on the current branch; do not push.
* **Tests must not start a real model session.** A real smoke test costs tokens and needs the owner's word.

## Tests (`unittest`, temporary directories, an injected clock: no real sleeping)

Fake agents are small Python scripts that read `{prompt_file}` and then post, fail, or do nothing.

1. Alternation: owner posts to `claude`; the fake `claude` posts to `astra`; the fake `astra` posts to `owner`; no
   `wait` or `status` call anywhere; each prompt file contains exactly the unseen messages.
2. Parallel step: both agents are started; neither prompt contains the other's held answer; both are published.
3. An agent that fails twice and then posts: attempts at +1 and +5 minutes by the injected clock, one message.
4. A log matching the limit pattern with a reset time: the next attempt is at that time plus 60 s.
5. Exit 0 without a post, three times: `stalled`; "wake now" starts one more attempt.
6. A second start for a running model is impossible, also after a server restart with a live pid in
   `dispatch.json`; a dead pid is cleared.
7. `post --seen` refuses with exit code 5 and writes nothing when an unseen message exists; passes otherwise.
8. `max_auto_turns` pauses the dispatcher; an owner message resumes it.
9. A message body containing `$(touch X)` and `; touch Y` creates neither file; a foreign `Origin` cannot trigger
   "wake now"; no endpoint changes `agents.json`.
10. Turn timeout: a sleeping fake agent is terminated and the attempt counts as failed.

## Acceptance (do it and report the actual output)

* `python3 -m unittest research/12-faced-polyhedron/dialogue/test_chat.py` passes.
* A scripted end-to-end run in a scratch thread with two fake agents: a sealed step, three alternating turns, one
  simulated limit with recovery, the owner's `close`; print `status` and the dispatcher states after each step.
* Final message: what was built, the test output, the commands the owner runs to register the two agents and start
  the server, any deviation from `TRANSPORT.md`, and what was not tried (real vendor CLIs, the page in a browser).
