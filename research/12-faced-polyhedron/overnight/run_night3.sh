#!/usr/bin/env bash
# Night 3 (revised 2026-10-30). Usage: ./run_night3.sh [HOURS] [WORKERS]
# Genus ladder over all 59 neighbourly types: each type's map = simple 12-faced polyhedron + 6 handles;
# remove tubes down to the sphere, then climb back realizing genus 0, 1, 2, ... (annealing + CMA-ES on
# the honest pair energy, each level seeded from the level below, every zero checked exactly).
# Result per type: the highest exactly realized genus (genus 6 = a solution, saved as CANDIDATE).
# (The older phases - 8-face ladder GA, simple-defect - remain available as jobs 'ladder' / 'sdefect'.)
# Merge origin only AFTER the previous night job has exited (it re-imports run_overnight.py from disk).
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
# budgets count awake time only (time.monotonic stops while the Mac sleeps), so closing the lid costs nothing
echo "night 3: genus ladder, $H h on $W workers"
nice -n 10 python3 run_overnight.py glad --reps 2 --minutes-per-seed 8 --hours "$H" --workers "$W" --git
python3 run_overnight.py status
