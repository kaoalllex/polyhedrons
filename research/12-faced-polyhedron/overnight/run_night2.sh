#!/usr/bin/env bash
# Night 2. Usage: ./run_night2.sh [HOURS] [WORKERS]
# Phase 1 (~15 min): certified proof that NO symmetric polyhedral IMMERSION exists (25 cases, DRAT)
# Phase 2 (rest):    period-defect search over all 59 types (Penrose-type closure measure;
#                    defect 0 = normals admitting a closed, locally consistent surface -> CANDIDATE)
set -u
cd "$(dirname "$0")"
[ -d "$HOME/.venvs/polyhedra" ] && source "$HOME/.venvs/polyhedra/bin/activate"
export PATH="$HOME/bin:$PATH"
H=${1:-8}
W=${2:-$(python3 -c "import os; print(max(1, (os.cpu_count() or 2) - 1))")}
H1=$(python3 -c "print(round(min(1.0, $H * 0.2), 2))")
H2=$(python3 -c "print(round($H - min(1.0, $H * 0.2), 2))")
echo "night 2: $H h on $W workers (symimm $H1 h, pdefect $H2 h)"
python3 run_overnight.py sym --sym-immersion --hours "$H1" --workers "$W" --git
python3 run_overnight.py pdefect --hours "$H2" --workers "$W" --minutes-per-seed 30 --git
python3 run_overnight.py status
