---
name: overnight-run-script
description: Use when writing or editing a long-running unattended run script (run_night*.sh, overnight/run_overnight.py jobs) for the 12-face polyhedron research, so it runs well on the user's MacBook, survives lid-close/sleep, and does not waste its time budget.
---

# Overnight run scripts (macOS laptop)

Reference implementations: `research/12-faced-polyhedron/overnight/run_night2.sh` and `run_overnight.py`.
Check them first; extend rather than rewrite.

## Shell wrapper checklist

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
- Do not rely on the machine staying awake. Keeping it awake while the lid is closed needs
  `sudo pmset -a disablesleep 1` (+ `caffeinate`), risks overheating in a bag, and must be reverted
  (`disablesleep 0`); only suggest it if the user asks, and never run `sudo` yourself.

## Python job checklist

- Pool via `run_pool` (spawn context, `maxtasksperchild`), results appended per task, `--git` committer
  commits `results/` periodically and forced on important findings (CANDIDATE / UNSAT).
- Long per-task loops take their own `minutes` budget and check `time.monotonic()`.
- Exact re-check before saving anything as a CANDIDATE.
- Verify with `bash -n` and `python3 -m py_compile`; do not run the real night job to test (use `--only` and a
  tiny `--hours`). No pty tricks.
