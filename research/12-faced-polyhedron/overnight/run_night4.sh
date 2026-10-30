#!/usr/bin/env bash
# Night 4 (revised 2026-10-30 evening after the night-3 analysis and the independent review).
# Usage: ./run_night4.sh [HOURS] [WORKERS]
# Run AFTER night 3 has finished and its results are committed (it reads results/glad/results.jsonl).
# Why revised: the bandit `arch` ranks arms by target genus, so it would spend the night on the type-0 genus-4
# arms, which the Gauss gate excludes exactly (degree -2 instead of -3 at every saved genus-3 polyhedron).
# Phase 1 (minutes): job `gate` = Gauss gate T1 for every realized polyhedron x next handle + test 2.2 (night-3
#                    data is already gated in results/gate; only new realizations are processed).
# Phase 2 (rest), in parallel:
#   * `arch --gauss-gate` on about 1/3 of the cores: realization archive + bandit (night-4 original), but arms
#     without an admissible orientation for the next genus are never picked;
#   * `n5` on the rest: normals first + exact offsets (nfirst), drift to handle degree -1 then normals first
#     (kdrift), genus-6 normals first (g6); every exact realization is saved and climbed at once.
# Every float zero is checked exactly; genus 6 = CANDIDATE (committed at once).
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
# budgets count awake time only (time.monotonic stops while the Mac sleeps), so closing the lid costs nothing
T0=$(python3 -c "import time; print(time.monotonic())")
H1=$(python3 -c "print(round(min(0.5, $H * 0.1), 2))")
WA=$(( W >= 3 ? W / 3 : 1 ))
WN=$(( W - WA > 0 ? W - WA : 1 ))
echo "night 4 (revised): $H h on $W workers (gate <= $H1 h, then arch --gauss-gate on $WA + n5 on $WN)"
nice -n 10 python3 run_overnight.py gate --hours "$H1" --workers "$W" --git
H2=$(python3 -c "import time; print(round($H - (time.monotonic() - $T0) / 3600, 2))")   # the gate usually ends early
echo "phase 2: $H2 h"
mkdir -p work
nice -n 10 python3 run_overnight.py arch --gauss-gate --minutes-per-seed 6 --hours "$H2" --workers "$WA" --git > work/arch_night4.log 2>&1 &
ARCH=$!
nice -n 10 python3 run_overnight.py n5 --minutes-per-seed 20 --timeout 600 --mix 4,4,1 --hours "$H2" --workers "$WN" --git
wait $ARCH
tail -n 5 work/arch_night4.log
python3 analyze_n5.py || true
python3 analyze_glad.py > /dev/null 2>&1 || true
python3 run_overnight.py status
