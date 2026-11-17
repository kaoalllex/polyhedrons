#!/usr/bin/env bash
# Session run (eight processes, <= 1 core-h): bash run.sh pilot -> results/pilot/ (caps 3 s / 10 s);
#   bash run.sh session -> results/session/ (caps 12 s / 120 s). C0, capacity, C1 and C2 in one call (PLAN.md).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
MODE="${1:?pilot or session}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 WORKERS=8
case "$MODE" in
  pilot) export P4_C1_CAP=3 P4_C2_CAP=10 ;;
  session) export P4_C1_CAP=12 P4_C2_CAP=120 ;;
  *) exit 2 ;;
esac
OUT="$HERE/results/$MODE"
[[ ! -e "$OUT" ]] || { echo "$OUT exists; never overwritten" >&2; exit 2; }
cd "$HERE"
"$PYTHON" -m unittest -q test_p4
T0=$(date +%s)
"$PYTHON" p4.py all "$OUT"
"$PYTHON" -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
echo "wall_seconds: $(( $(date +%s) - T0 ))" > "$OUT/wall.txt"
