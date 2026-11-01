---
name: overnight-run-script
description: Use when writing or editing a long-running unattended run script (an experiment's run.sh, run_night*.sh, overnight/run_overnight.py jobs) for the 12-face polyhedron research, so it runs well on the user's MacBook, survives lid-close/sleep, and does not waste its time budget.
---

# Overnight run scripts (macOS laptop)

Reference implementations: `research/12-faced-polyhedron/experiments/_template/run.sh` (manifest) and
`research/12-faced-polyhedron/overnight/run_overnight.py` (jobs, resume, `--results-dir`). The old night wrappers
`run_night*.sh` are in git tag `state-2026-11-01`. Check these first; extend rather than rewrite.

## Before writing anything

- A night is an experiment. It needs a `ROADMAP.md` row with T + D >= 3 and a committed
  `experiments/E-YYMMDD-NN-slug/PLAN.md` (skill `experiment-start`). A parked method (`ROADMAP.md`) needs a
  `PLAN.md` that says what is different this time.
- The wrapper is `experiments/E-YYMMDD-NN-slug/run.sh` (from `experiments/_template/`). It writes the provenance
  manifest and calls `run_overnight.py <job> ... --results-dir "$OUT"`, so a night gets both the manifest and
  resume. Do not build a third framework.
- `--git` commits go to the experiment branch, never to `main`.
- SAT jobs keep proofs and CNFs (the default since 2026-11-01). Record `cadical --version` and the drat-trim
  commit in the manifest.

## Shell wrapper checklist

0. The owner launches it as `caffeinate -dimsu bash run.sh ...`, on AC power, lid open. Print that line in the
   hand-over. Without it, idle sleep stops the night (night 4 lost 8 h).
1. `cd "$(dirname "$0")"`, activate `~/.venvs/polyhedra` if present, `export PATH="$HOME/bin:$PATH"` (cadical, drat-trim).
2. Usage line `[HOURS] [WORKERS]`; default workers = `ncpu - 1`.
3. Pin BLAS/numba to one thread per worker, otherwise N workers x M BLAS threads oversubscribe the cores:
   `export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1`
4. Run every phase as `nice -n 10 python3 run_overnight.py <job> ... --git` so the laptop stays usable.
5. Phases run sequentially; each phase's `--hours` is a ceiling, not a reservation. Phases often finish early
   (everything done), so compute the next phase's budget from the time actually spent, not from a fixed split.
6. Measure elapsed time with `time.monotonic()`, never `$SECONDS` or `date` (see below).
7. End with `python3 run_overnight.py status`.

## Sleep / lid-close semantics

- Closing the lid sleeps the Mac and freezes all processes; nothing is killed.
- `time.time()` keeps running during sleep and would burn the `--hours` budget, task timeouts and
  `minutes-per-seed` loops. On macOS `time.monotonic()` (mach_absolute_time) does not advance during sleep,
  so use it for every deadline, timeout and duration. `time.time()` is only for filenames/timestamps.
  This must be consistent within a measurement (do not mix the two clocks).
- Across processes `time.monotonic()` shares one base on macOS, so bash can do `T0=$(python3 -c "import time;print(time.monotonic())")`
  and later subtract in another python call.
- Resume: all jobs record per-task results and skip finished tasks on re-run, so after sleep, a crash or
  a power cut re-running the same command continues. New jobs must keep this property
  (`load_results` / `append_result` / `jobdir`; task ids stable and deterministic).
- `caffeinate` keeps the Mac awake with the lid open, but not with the lid closed. Keeping it awake with the
  lid closed needs
  `sudo pmset -a disablesleep 1` (+ `caffeinate`), risks overheating in a bag, and must be reverted
  (`disablesleep 0`); only suggest it if the user asks, and never run `sudo` yourself.

## Lessons of night 6 (2026-11-01): a night the owner can restart blindly

- **Resume at unit granularity.** Every runner appends one JSON record per finished unit (a seed, a (type, k)
  pair) to `results.jsonl` and, on start, reads that file and skips the units already recorded. The owner's rule
  is then "if it died, run the same command again"; only the unit in flight is recomputed. Derived skips too: a
  type with a recorded UNSAT skips its larger k.
- **Progress inside a unit.** A unit that can run for an hour appends one line per step to `progress.jsonl`, so a
  killed run still leaves data; and it has its own wall-clock cap (`--seed-minutes`), recorded as TIME-CAP, so one
  hard unit cannot eat the shard's night.
- **Manifest survives restarts.** `run.sh` writes the manifest header only if it is absent and appends a
  `restarted_utc` line otherwise; the `finish` trap appends `finished_utc`, `exit_status`, `wall_seconds` and
  `core_hours` every time, so the core-hours of a restarted shard are the sum of its lines.
- **One command for the whole night** (`overnight/run_night6.sh`): starts N detached processes (`nohup ... &`, each
  under its own `caffeinate -dimsu` and `nice -n 10`), one per performance core (M4 Pro: 10), with `status` and
  `stop` modes. Detached means Ctrl+C or closing the terminal does not kill them; only `stop` does.
- **Pilot through the same code path** as the night: a positive control (expected SAT / found) and a negative
  control (expected UNSAT with a VERIFIED proof; rebuild a certified instance and compare its CNF SHA-256 with the
  record) before the first full run.
- **Flush, do not buffer.** A pilot piped through `grep | tail` shows nothing until the end; log with `flush=True`
  and read the raw log, or use `grep --line-buffered` without `tail`.
- **Keep only what certifies.** CNF and proof files are kept for UNSATs (with SHA-256 in the record); SAT and
  timeout CNFs are deleted after the hash is recorded, or a 59-type sweep fills the disk.
- **Forked SAT children.** When a SAT call runs in a forked child with `p.join(timeout)`, the timeout is monotonic
  and the child is terminated on expiry; solver binaries (`cadical -t`) use wall time, which is fine while
  `caffeinate` holds the machine awake.

## Python job checklist

- Pool via `run_pool` (spawn context, `maxtasksperchild`), results appended per task, `--git` committer
  commits `results/` periodically and forced on important findings (CANDIDATE / UNSAT).
- Long per-task loops take their own `minutes` budget and check `time.monotonic()`.
- Exact re-check before saving anything as a CANDIDATE.
- Verify with `bash -n` and `python3 -m py_compile`; do not run the real night job to test (use `--only` and a
  tiny `--hours`). No pty tricks.
