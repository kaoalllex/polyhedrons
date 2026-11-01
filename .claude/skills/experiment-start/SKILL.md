---
name: experiment-start
description: Use when starting work on a ROADMAP item (E##) of the 12-face polyhedron research, or when asked to run, launch, plan or pre-register an experiment, a night run or a GitHub Actions run for it.
---

# Start a pre-registered experiment

Paths are relative to `research/12-faced-polyhedron/`. Rules: `PROTOCOL.md` §2, §5, §6.

1. **Gate.** Read the `ROADMAP.md` row and `STATUS.md` §3.
   - Refuse, and say why, if T + D < 3, if the row is not `open`, or if the method is on the ROADMAP stop list
     and `STATUS.md` has no dated reason to reopen it.
   - If there is no row yet, write one with its scores first and ask the owner.
2. **Branch.** Create `experiment/E##-slug` from an up-to-date `main`. If the owner is still working on another
   branch, ask which base to use.
3. **Folder.** `cp -r experiments/_template experiments/E##-slug`.
4. **Plan.** Fill in `PLAN.md` from the row and its ROADMAP section:
   - H1 and H0;
   - the target (S0-S4) and the counters by their `SPEC.md` §4 names;
   - a positive control that must succeed and a negative control that must fail;
   - a power statement;
   - the meaning of every outcome (SAT / UNSAT / timeout / near-miss);
   - budget and stop rule, both from the row.
5. **Runner.** Replace the placeholder in `run.sh` with one bounded command that writes into `$OUT`.
   - For a laptop night, call `python3 ../../overnight/run_overnight.py JOB ... --results-dir "$OUT"`. Follow
     the `overnight-run-script` skill.
   - Set the shards in `matrix.json`. Each Actions shard must stay under 5 h.
6. **Pilot.** Run shard 0 with a budget of a few minutes. The positive control must pass. Record the pilot under
   `## Amendments`.
7. **Pre-register.** Commit `PLAN.md` before the full run; that commit is the pre-registration. In the same
   commit set the ROADMAP State to `running` and fill in its folder.
8. **Hand over the launch.** Give the owner the exact command:
   - laptop: `caffeinate -dimsu bash experiments/E##-slug/run.sh 0`, on AC power, lid open;
   - Actions: push the branch with `[run]` in the commit message.

   Do not start a multi-hour run from a session.
