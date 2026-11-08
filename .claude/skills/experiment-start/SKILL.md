---
name: experiment-start
description: Use when starting work on a ROADMAP item (E-YYMMDD-NN) of the 12-face polyhedron research, or when asked to run, launch, plan or pre-register an experiment, a night run or a GitHub Actions run for it.
---

# Start a pre-registered experiment

Paths are relative to `research/12-faced-polyhedron/`. Rules: `PROTOCOL.md` §2, §5, §6. Read `STRATEGY.md` for the
focus target. Use `python3` from an activated environment with `requirements.txt` installed.

1. **Gate.** Read the `ROADMAP.md` row, the experiment's `README.md` (its header names its origin and the
   hypotheses it tests) and `STATUS.md` §3.
   - Refuse, and say why, if T + D < 3, if the row is neither `planned` nor `open`, or if the method is a parked method in
     `ROADMAP.md` and the plan does not say what is different this time (an unchanged re-run scores D = 0).
   - If there is no row yet, create the experiment: ID `E-<today YYMMDD>-NN` with the next free NN (check
     `experiments/`), folder `experiments/<ID>-<slug>/` with `README.md` from `experiments/_template/README.md`
     (`status: planned`, `origin` = the ideas / hypotheses / experiments / sources it grew from, `tests` = the
     hypotheses it can move). New ideas or hypotheses get their own files first (`PROTOCOL.md` §4). Then add the
     ROADMAP row with its scores and ask the owner.
2. **Branch.** Stay on the week's `lab/YYYY-MM-DD` branch (`PROTOCOL.md` §7); create it from `main` only if it does
   not exist yet. Never create a branch per experiment.
3. **Folder.** Copy the template files you need (`PLAN.md`, `run.sh`, `matrix.json`) from `experiments/_template/` into
   the experiment folder; keep its `README.md`.
4. **Plan.** Fill in `PLAN.md` from the row and its ROADMAP section:
   - the hypotheses it moves (the `tests` of its header) and H1/H0 for this run;
   - the target (S0-S5), including (F, g) for S5, and the counters by their `SPEC.md` §4 names;
   - a positive control that must succeed and a negative control that must fail;
   - a power statement;
   - **counter calibration**: for every float diagnostic that may appear in the verdict, one control input on each
     side of its threshold (a clamped or saturating measure is not a measurement; `gauss_gate.hemisphere_margin`
     floors at 0, E-261101-07);
   - the meaning of every outcome (SAT / UNSAT / timeout / near-miss);
   - budget and stop rule, both from the row.
5. **Runner.** Replace the placeholder in `run.sh` with one bounded command that writes into `$OUT`.
   - For a laptop night, call `python3 "$ROOT/overnight/run_overnight.py" JOB ... --results-dir "$OUT"`, where the
     template derives `ROOT` as the research directory. Follow
     the `overnight-run-script` skill.
   - Set the shards in `matrix.json`. Each Actions shard must stay under 5 h.
6. **Pre-register.** Commit `PLAN.md` before any pilot or full run; that commit is the pre-registration. In the same
   commit set the ROADMAP State and the README `status` to `running`, and run `verification/trace.py`.
7. **Pilot.** Run shard 0 with a budget of a few minutes. The positive and negative controls must give their
   expected outcomes. Apply the long-run gates of `PROTOCOL.md` §2 and re-check T + D. Record the pilot under
   `## Amendments`; commit any plan changes before running the amended experiment.
8. **Hand over the launch.** Give the owner the exact command:
   - laptop: `bash research/12-faced-polyhedron/overnight/launch.sh CODE start` (then `status`, `stop`), on AC power. Only
     these three words reach the owner; stop and interrupt keep every recorded result (`PROTOCOL.md` §6). If `run.sh`
     cannot be driven by `launch.sh` (custom queue, caps), add a mode to `run.sh` or extend `launch.sh`; do not write a
     separate launcher script;
   - Actions: push the branch with `[run]` in the commit message.

   Do not start a multi-hour run from a session.
