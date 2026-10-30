#!/usr/bin/env bash
# Night 5 (prepared 2026-10-30 after the independent review, reviews/review-2026-10-30.md).
# Usage: ./run_night5.sh [HOURS] [WORKERS]
# Run AFTER night 4 has finished and its results (results/glad from night 3, results/arch from night 4) are
# committed: the gate reads every realized polyhedron from them.
# Phase 1 (minutes): job `gate` = Gauss gate T1 for every exactly embedded polyhedron (genus >= 2) x every
#                    extendable next handle, and review test 2.2 on the night-3 chains (results/gate/).
# Phase 2 (rest):    job `n5` on WORKERS-1 cores = the Gauss-gated, normals-first ladder:
#                      nfirst  anneal the normals near a realization into the next map's Gauss class, then
#                              decide the offsets EXACTLY (z3, sub-map encoding); SAT = next genus, re-checked
#                      kdrift  drift inside the realization space until the handle degree k_tau = -1 (the
#                              plateau's obstruction is k_tau = 0), then normals first from that seed
#                      g6      genus-6 normals first from random normals (types 0, 11, 58)
#                    every exact realization is saved (results/n5/realized/) and climbed further at once;
#                    genus 6 = CANDIDATE (committed at once)
#                    + job `arch` (night 4) on 1 core as the control.
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
# budgets count awake time only (time.monotonic stops while the Mac sleeps), so closing the lid costs nothing
T0=$(python3 -c "import time; print(time.monotonic())")
H1=$(python3 -c "print(round(min(1.0, $H * 0.15), 2))")
echo "night 5: $H h on $W workers (gate <= $H1 h, then n5 on $((W > 1 ? W - 1 : 1)) + arch control on 1)"
nice -n 10 python3 run_overnight.py gate --hours "$H1" --workers "$W" --git
H2=$(python3 -c "import time; print(round($H - (time.monotonic() - $T0) / 3600, 2))")   # the gate usually ends early
echo "phase 2: $H2 h"
mkdir -p work
if [ "$W" -gt 1 ]; then
  nice -n 10 python3 run_overnight.py arch --minutes-per-seed 6 --hours "$H2" --workers 1 --git > work/arch_control_night5.log 2>&1 &
  ARCH=$!
  nice -n 10 python3 run_overnight.py n5 --minutes-per-seed 20 --timeout 600 --mix 4,4,1 --hours "$H2" --workers $((W - 1)) --git
  wait $ARCH
else
  nice -n 10 python3 run_overnight.py n5 --minutes-per-seed 20 --timeout 600 --mix 4,4,1 --hours "$H2" --workers 1 --git
fi
python3 analyze_n5.py || true
python3 run_overnight.py status
