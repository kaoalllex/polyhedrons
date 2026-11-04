#!/usr/bin/env bash
# Bounded interactive pilot; no night run is activated.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-0}" != 0 || "${SHARDS:-1}" != 1 ]]; then
  echo 'This registered pilot has one shard (0).' >&2
  exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
PYTHON="${PYTHON:-python3}"
exec "$PYTHON" "$HERE/pilot.py" --out "$HERE/results/pilot"
