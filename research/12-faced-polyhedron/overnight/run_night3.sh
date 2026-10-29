#!/usr/bin/env bash
# Night 3. Usage: ./run_night3.sh [HOURS] [WORKERS]
# Phase 1 (<= 35 %): own "ladder" path - closed polyhedra with 8 mutually adjacent faces (genus 2),
#                    maps generated from scratch, genetic algorithm (island model) on the honest pair
#                    energy, every float zero re-checked in exact rational arithmetic -> CANDIDATE.
#                    (7 faces = Szilassi is found in seconds by the same code; 8 is open.)
# Phase 2 (rest):    "simple faces first" for 12 faces - anneal admissible normals: first drive the
#                    closure defect to 0, then minimise the number of faces that must be non-simple
#                    (exact MILP); 0 -> planes reconstructed and checked exactly -> CANDIDATE.
# Merge origin only AFTER the previous night job has exited (it re-imports run_overnight.py from disk).
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
H1=$(python3 -c "print(round($H * 0.35, 2))")
# budgets count awake time only (time.monotonic stops while the Mac sleeps), so closing the lid costs nothing
T0=$(python3 -c "import time; print(time.monotonic())")
echo "night 3: $H h on $W workers (ladder <= $H1 h, sdefect gets the rest)"
nice -n 10 python3 run_overnight.py ladder --ladder-n 8 --reps 400 --minutes-per-seed 10 --hours "$H1" --workers "$W" --git
H2=$(python3 -c "import time; print(round($H - (time.monotonic() - $T0) / 3600, 2))")
echo "phase 2: $H2 h"
nice -n 10 python3 run_overnight.py sdefect --reps 3 --minutes-per-seed 30 --milp-seconds 45 --hours "$H2" --workers "$W" --git
python3 run_overnight.py status
