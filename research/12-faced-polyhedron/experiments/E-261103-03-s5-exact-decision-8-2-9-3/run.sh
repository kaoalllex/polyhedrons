#!/usr/bin/env bash
# Bounded registered pilots and resumable coverage shards.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-1}"
if [[ "${1:-pilot}" == coverage-pilot || "${1:-pilot}" =~ ^[0-9]+$ ]]; then
  SHARD="${1:-0}"
  PILOT=()
  if [[ "$SHARD" == coverage-pilot ]]; then
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
  echo 'Usage: run.sh [SHARD|coverage-pilot|pilot|paired|grid]' >&2
  exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/pilot.py" --out "$HERE/results/pilot"
