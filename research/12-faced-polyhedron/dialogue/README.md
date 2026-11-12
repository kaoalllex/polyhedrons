# Dialogue chat: owner's guide

A local chat in which AI sessions (Claude Code, Codex, any number of them) and the owner discuss a question through
files. The rules for the agents are in `TRANSPORT.md`; what a dialogue is about is in its brief (`BRIEF_*.md`).
Run every command from the repository root. Threads (`dialogue/threads/`) and `runners.json` stay out of git.

Before you start: no night run is going, and no lab session is working in this checkout (the agents run in it).

## 1. Start

One terminal window:

```
python3 research/12-faced-polyhedron/dialogue/chat.py serve
```

Open http://127.0.0.1:8765/ and keep the window open. The page shows every dialogue; `serve <thread>` opens it on
that thread. If the port is taken, add `--port 8766`. Ctrl+C stops the page; nothing is lost: messages are files, and
an agent in the middle of a turn finishes it. Start `serve` again with the same command. `--no-dispatch` gives the
page without starting any agent.

## 2. Runners: how agents are started

`dialogue/runners.json` holds one template per CLI (copy `runners.example.json` the first time). Each has the
commands `new` (a new session) and `resume` (continue the agent's session) and the lists of models and efforts the
page offers. The page can only pick from these lists; it never sends a command of its own.

* Check each command against the installed CLI (`claude --help`, `codex exec --help`) before the first real turn.
* An agent started this way cannot ask for permission. What it may do is decided by the template: Claude Code with
  `--permission-mode auto`, Codex with `--approve-for-me`. Change these flags in `runners.json` if you want more or
  less freedom.
* The Codex model list comes from the local Codex model cache (`~/.codex/models_cache.json`); edit it when new
  models appear. Not every model supports every effort (`ultra` is not available everywhere).

## 3. Dialogues and agents

* **New dialogue**: ＋ next to "Dialogues", a name of lowercase letters, digits and dashes. Put its brief in
  `dialogue/BRIEF_<name>.md` (the turn prompt points the agents to it).
* **Connect an agent**: "＋ connect agent" under the dialogue. Fields:
  * name: the agent's name in this dialogue (`claude`, `astra`, `critic`, …);
  * CLI, model, effort;
  * memory: `resume` keeps the agent's own context between turns, but every turn pays for the whole context again,
    also after a long pause; `fresh` starts a new session each turn, which is cheaper on long dialogues, and the
    agent remembers only what it wrote in `work/<name>/NOTES.md` and the thread's `HANDOVER.md`;
  * existing session (optional): the UUID of a session to continue, for example a session that already took part
    in this dialogue in a terminal. Close it in every terminal first: a session accepts one writer at a time.
    Claude Code keeps sessions as `~/.claude/projects/<project>/<uuid>.jsonl`; Codex lists them with
    `codex resume`.
* **Change** model or effort: ⚙ on the agent. **Remove** it from the dialogue: ✕ (its messages stay).
* An agent added later takes part from the next message on.

## 4. The page

* **Left**: the tree. Level one: dialogues ("your turn" means the floor is yours; "2 working" means two agents are
  busy). Level two: the agents of the dialogue. The dot: green and pulsing, working; yellow, waiting to retry; red,
  stalled; grey, idle; a blue ring, it is that agent's turn. ⏵ wakes an agent now.
* **Centre**: the chat. My messages are on the right; every message has a number (`#7`) to cite. A card under the
  last message shows an agent that is working or failing, with "console" and "wake now". Ctrl+Enter or Cmd+Enter
  sends. "Who answers" after my message:

| Choice | Effect |
|---|---|
| nobody new (interjection) | the floor stays; whoever is due answers me first |
| all agents, in parallel | everyone answers without seeing the others; the answers appear together |
| an agent's name | only that agent speaks next |
| nobody (pause) | everyone waits until I write again and choose who answers |
| nobody (close the dialogue) | the end; no agent is started again |

* A dashed frame "… has answered; hidden until … answer": a sealed answer. I can open it; the other agents cannot.
* **Right**: the console of the agent I clicked: its text, ▶ tool calls and their output (long output folded),
  errors. The list at the top picks a turn ("after #29", "attempt 2"). "follow" keeps the view at the bottom. Drag
  the left edge to resize; ✕ closes it.
* **Automatic turns**: after 12 agent messages in a row without mine, agents stop being started (`auto turn limit`
  in the header) until I write anything. "pause" and "resume" in the header stop and restart automatic turns.

## 5. When something goes wrong

* An agent failed (non-zero exit, no post, usage limit, turn longer than its timeout): it is retried after 1, 5, 15
  and 30 minutes, then every 30 minutes. A usage-limit message with a reset time moves the retry to that time plus a
  minute. After 3 runs that end without a post, or after 24 hours of failures, it is **stalled**: read its console,
  fix the cause, press "wake now" (one more attempt).
* "Another dispatcher serves this thread": a second `serve` is running; stop one of them.
* Turn prompts, logs and drafts: `dialogue/threads/<thread>/work/<agent>/` (`turn-<n>.md`, `wake-<n>-<attempt>.log`).
  Never edit message files, `sealed/`, `thread.json`, `agents.json` or `dispatch.json` by hand.
* State from a terminal: `python3 research/12-faced-polyhedron/dialogue/chat.py status <thread>`.

## 6. Interactive mode (an agent in its own terminal)

An agent without a runner can run in its own terminal window, as before automatic turns existed: create the thread
with `chat.py new <thread>` (it starts with `claude` and `astra`), start the model in the repository root and paste:

> You are `claude` in a research dialogue. Read `research/12-faced-polyhedron/dialogue/TRANSPORT.md` and
> `research/12-faced-polyhedron/dialogue/BRIEF_<thread>.md` and follow them. Thread: `<thread>`.

It waits with `chat.py wait` and posts by itself. Do not connect the same agent on the page at the same time.

## 7. Getting value from a dialogue

* Steer: "I did not understand #5, explain more simply", "this was tried in E-…", "a new polyhedron matters more to
  me than a negative result". Priorities, risk and laptop nights are mine to decide.
* If the agents agree too fast, ask each for the strongest alternative and what it disagrees with in the others.
* If a dispute about a fact lasts more than two messages, ask for a calculation ("compute it, 10 minutes") or a
  "not checked" mark in the summary.
* If the talk drifts: "back to question Q…", or pause.
* Nothing in a dialogue is a result: these are ideas and criticism; numbers from calculations are session checks.
  If anyone claims a candidate: stop, and run `candidate-check`.
* The stages of a dialogue (rounds, who opens them, the synthesis and who commits it) are in its brief.
