---
name: session-handover
description: Use at the end of a 12-face research session, before the owner closes it, when the context is about to run out, or when asked to prepare or update the continue prompt.
---

# Hand over a research session

Paths and commands are relative to `research/12-faced-polyhedron/`. Use `python3` from an activated environment
with `requirements.txt` installed.

1. **Uncommitted work.** Run `git status`.
   - Commit your own work on the session branch.
   - Never commit the owner's untracked notes (the root `TODO.md`).
   - Never push to `main`. Push the session branch only when the owner says so.
2. **Log.** Add a dated entry to `experiment-log.md`: what was done, the commits, the outcomes, with pointers to
   the files. Keep the log append-only.
3. **Hand-over block.** Rewrite only the "Hand-over" block of `CONTINUE_PROMPT.md`. It names:
   - the branch to open;
   - in-flight runs: where they run and how to collect them;
   - open owner actions (merge, publish a release, send an e-mail);
   - the next ROADMAP item.

   Standing rules live in the root `CLAUDE.md`; do not copy them into the prompt.
4. **Ledger.** Check that `STATUS.md` "As of" and the ROADMAP State column match reality.
5. **Verify.** Run `python3 verification/verify_all.py --quick` and report its last line.
6. **Tell the owner,** in Russian:
   - the exact commands left for them (push, merge, launch with `caffeinate -dimsu`);
   - what was not checked.
