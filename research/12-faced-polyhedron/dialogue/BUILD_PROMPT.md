# Prompt: build the dialogue transport and the owner's chat page

## How to run

Open a coding session in the repository on the current lab branch, with a mid-tier coding model at medium effort
(the task is about 300 lines of standard-library Python and one inline HTML page). Paste everything below the line.

-----

Build `research/12-faced-polyhedron/dialogue/chat.py`: a file-based chat between two AI sessions and a human, with a
local browser page for the human. **The contract is `research/12-faced-polyhedron/dialogue/TRANSPORT.md`; read it
first and implement exactly what it says** (thread layout, message header, floor rules, parallel step with sealing,
commands, exit codes). If something in it cannot be implemented as written, change `TRANSPORT.md` in the same commit
and say so in your final message; do not silently deviate.

## Constraints

* One file, `chat.py`, Python 3.9+ standard library only. No packages, no build step, no network access at run time
  (no CDN: the page's CSS and JavaScript are inline strings in `chat.py`).
* Create only `dialogue/chat.py` and `dialogue/test_chat.py` (`dialogue/.gitignore` already ignores `threads/`). Do
  not touch any other file of the repository, except `TRANSPORT.md` under the rule above, and do not add the tests
  to `verification/verify_all.py`.
* Root `AGENTS.md` / `CLAUDE.md` apply: English in code and commits, small diff, no speculative features. Commit on
  the current branch; do not push.
* Do not test with a pseudo-terminal (`pty`, `script`); nothing here needs one.

## Core (shared by the commands and the page)

* **One writer path.** Every post, from the CLI or from the page, goes through one function that takes a lock
  (atomic `mkdir` of a lock directory in the thread; a lock older than 10 s is stale and is broken), recomputes the
  floor from the files, validates, allocates the next number, writes the message to a temporary file and renames it
  into place, then releases the lock. A reader must never see a half-written message.
* **The floor is derived, not stored**: recomputed from the published messages in order plus the contents of
  `sealed/`, by the rules of `TRANSPORT.md` §2. No state file that can go out of sync.
* **Sealing.** A post by a model while both models are on the floor goes to `sealed/<author>.md`. When the second
  arrives, both are published under consecutive numbers, authors in alphabetical order; the floor then becomes the
  union of their `next` fields. An owner message that replaces the floor first publishes whatever is held.
* **Validation**: thread names match `[a-z0-9][a-z0-9-]*`; `--as` is a participant; a model must be on the floor;
  body not empty and at most `max_lines` lines (models only; the owner has no cap); allowed `next` values per
  `TRANSPORT.md`. Refusals write nothing.
* `wait` polls the directory (0.5 to 1 s interval); "since your last post" is computed from the files, so a
  restarted session loses nothing.

## The owner's page (`serve`)

A single page that feels like an ordinary chat:

* messages in order as bubbles, one colour per author, with number, author, round label and time; the owner's on
  the right. Markdown rendered by a small inline renderer: headings, paragraphs, bullet and numbered lists, bold,
  italic, inline code, fenced code blocks, tables, links shown as text. **Escape all message text before rendering**;
  never insert message content as raw HTML. Anything the renderer does not recognise is shown as plain text;
* a status line: who is on the floor ("waiting for: astra"), and a placeholder bubble for each held message
  ("claude has answered; hidden until astra answers") that the owner may expand;
* a composer at the bottom: a multi-line text box (UTF-8, the owner writes in Russian), send on Ctrl+Enter or
  Cmd+Enter, and a "who answers" selector: `keep` (interjection, the default while a model is on the floor),
  `both`, `claude`, `astra`, `pause`, `close`. When the floor is on the owner, `keep` is not offered and the owner
  must choose;
* new messages appear without a reload (polling every 2 s is enough); the view scrolls to the newest message unless
  the owner has scrolled up;
* readable at a normal laptop width, long messages and tables included (a wide table scrolls inside its bubble).

Server: `http.server` bound to `127.0.0.1` only. Endpoints: the page, `GET` messages and status as JSON, `POST` an
owner message. The server posts only as `owner` and only into the thread it was started for. Reject a `POST` whose
`Origin` or `Host` is not the page's own (a foreign web page must not be able to post as the owner).

## Tests (`test_chat.py`, `unittest`, temporary directories)

1. Floor rules: start on the owner; alternation; owner `keep` leaves the floor unchanged; owner override; `pause`;
   `close` (then `wait` exits 3 and `post` is refused).
2. A model that is not on the floor is refused with exit code 4 and nothing is written.
3. Parallel step: the first post is held and invisible to the other model's `wait`; after the second, both are
   published in alphabetical order with consecutive numbers and the floor is the union of their `next`.
4. Concurrency: 20 owner posts from parallel processes give 20 distinct consecutive numbers and 20 complete files.
5. `max_lines` refusal; `wait` returns exactly the messages since the caller's last post, also after a restart.
6. Server: a `POST` with a foreign `Origin` is rejected; a valid one creates an owner message; message text with
   `<script>` comes back escaped in what the page renders.

## Acceptance (do it and report the actual output)

* `python3 -m unittest research/12-faced-polyhedron/dialogue/test_chat.py` passes.
* A scripted end-to-end run in a scratch thread: `new`; owner posts to `both`; two model posts (held, then
  published); three alternating posts; owner `keep` interjection; owner `close`; `status` after each step.
* Start `serve` on a scratch thread, fetch the page and the JSON once with `curl`, stop the server. Say plainly
  that you did not look at the page in a browser if you did not.
* Final message: what was built, the test output, the one command the owner runs to open the chat, and any deviation
  from `TRANSPORT.md`.
