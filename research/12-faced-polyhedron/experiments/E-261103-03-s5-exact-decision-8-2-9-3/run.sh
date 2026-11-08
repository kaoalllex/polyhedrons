#!/usr/bin/env bash
# Week item 5a shards (the launch.sh entry), bounded registered pilots and the concluded tranche coverage shards.
#   run.sh SHARD            item 5a: queue_item5a.json, results in $(cat launch.results)/SHARD; owner launch from the
#                           repo root: bash research/12-faced-polyhedron/overnight/launch.sh 03-03 start|status|stop
#   run.sh coverage SHARD   the frozen tranche queue in results/SHARD (concluded)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-1}"
if [[ "${1:-pilot}" =~ ^[0-9]+$ ]]; then
  SHARD="$1"
  if [[ ! "$SHARDS" =~ ^([1-9]|10)$ || "$SHARD" -ge "$SHARDS" ]]; then
    echo 'Item 5a requires SHARDS=1..10 and 0 <= SHARD < SHARDS.' >&2
    exit 2
  fi
  OUT="${S5A_RESULTS:-$HERE/$(cat "$HERE/launch.results")}/$SHARD"  # S5A_RESULTS: tests only
  mkdir -p "$OUT"
  echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS" >> "$OUT/manifest.txt"
  trap 'echo "exit_status: $?" >> "$OUT/manifest.txt"' EXIT
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
  export CADICAL="${CADICAL:-$HOME/bin/cadical}" DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"
  # 80 core-h = 10 shards x 8 h; S5A_* overrides exist for the bounded startup check only.
  nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 --shard "$SHARD" --shards "$SHARDS" \
    --results-dir "$OUT" --s5-queue "$HERE/queue_item5a.json" --timeout "${S5A_SOLVER_CAP:-1800}" \
    --s5-checker-timeout "${S5A_CHECKER_CAP:-2700}" --s5-budget-seconds 288000 --hours "${S5A_HOURS:-8}"
  exit 0
fi
if [[ "${1:-pilot}" == coverage-pilot || "${1:-pilot}" == coverage ]]; then
  [[ "$1" == coverage ]] && { [[ "${2:-}" =~ ^[0-9]+$ ]] || { echo 'Usage: run.sh coverage SHARD' >&2; exit 2; }; }
  SHARD="${2:-0}"
  PILOT=()
  if [[ "$1" == coverage-pilot ]]; then
    SHARD=0
    SHARDS=1
    PILOT=(--s5-pilot)
    OUT="$HERE/results/coverage_pilot/0"
  else
    OUT="$HERE/results/$SHARD"
  fi
  if [[ ! "$SHARDS" =~ ^([1-9]|10)$ || "$SHARD" -ge "$SHARDS" ]]; then
    echo 'Coverage requires SHARDS=1..10 and 0 <= SHARD < SHARDS.' >&2
    exit 2
  fi
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
  export CADICAL="${CADICAL:-cadical}" DRAT_TRIM="${DRAT_TRIM:-drat-trim}"
  nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 --shard "$SHARD" --shards "$SHARDS" \
    --results-dir "$OUT" ${PILOT[@]+"${PILOT[@]}"}
  "$PYTHON" "$ROOT/overnight/run_overnight.py" status --results-dir "$(dirname "$OUT")"
  exit 0
fi
if [[ "${1:-pilot}" == grid ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
  PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
  exec nice -n 10 "$PYTHON" "$HERE/pilot.py" --grid --out "$HERE/results/grid_9_3"
fi
if [[ "${1:-pilot}" == paired ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
  exec "$PYTHON" "$HERE/pilot.py" --paired --resume "$HERE/results/paired_9_3" --out "$HERE/results/paired_9_3_continued"
fi
if [[ "${1:-pilot}" != pilot ]]; then
  echo 'Usage: run.sh [SHARD|coverage SHARD|coverage-pilot|pilot|paired|grid]' >&2
  exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/pilot.py" --out "$HERE/results/pilot"
