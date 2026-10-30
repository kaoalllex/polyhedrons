#!/usr/bin/env bash
# Night 4 (2026-10-30). Usage: ./run_night4.sh [HOURS] [WORKERS]
# Realization archive + bandit climb (code/archive_climb.py): roots = every exactly embedded polyhedron of
# genus >= 2 from night 3 (results/glad) and experiments/genus_ladder/; arms = every next handle after which
# all 66 pairs stay reachable; a quarter of the time searches NEW realizations of the archived maps
# (different oriented matroid). Every float zero is checked exactly; genus 6 = CANDIDATE (committed at once).
# Run AFTER night 3 has finished and its results are committed (it reads results/glad/results.jsonl).
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
# budgets count awake time only (time.monotonic stops while the Mac sleeps), so closing the lid costs nothing
echo "night 4: realization archive + bandit climb, $H h on $W workers"
nice -n 10 python3 run_overnight.py arch --minutes-per-seed 6 --hours "$H" --workers "$W" --git
python3 analyze_glad.py || true
