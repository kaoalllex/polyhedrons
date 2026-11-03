#!/usr/bin/env bash
# Bounded interactive pilot; no unattended long run is registered yet.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-pilot}" == paired ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
  exec "$PYTHON" "$HERE/pilot.py" --paired --resume "$HERE/results/paired_9_3" --out "$HERE/results/paired_9_3_continued"
fi
if [[ "${1:-pilot}" != pilot ]]; then
  echo 'Only the preregistered pilot is available.' >&2
  exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/pilot.py" --out "$HERE/results/pilot"
