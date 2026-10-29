#!/usr/bin/env bash
# One-command night run. Usage: ./run_night.sh [HOURS] [WORKERS]
# Phase 1 (45% of the time): sym       - independent verification of all symmetric cases
# Phase 2 (55% of the time): immersion - does a type admit a polyhedral immersion? Each worker spends
#   the whole phase on one type (a 30-min test on type 0 was not enough); re-runs continue with new types.
# Re-running the same command resumes; results are committed to git every 30 min (--git).
set -u
cd "$(dirname "$0")"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
H1=$(python3 -c "print(round($H * 0.45, 2))")
H2=$(python3 -c "print(round($H * 0.55, 2))")
echo "night run: $H h on $W workers (sym $H1 h, immersion $H2 h)"
python3 run_overnight.py sym --hours "$H1" --workers "$W" --git
T2=$(python3 -c "print(int($H2 * 3600) - 120)")   # one type per worker for the whole phase
python3 run_overnight.py immersion --hours "$H2" --workers "$W" --timeout "$T2" --git
python3 run_overnight.py status
