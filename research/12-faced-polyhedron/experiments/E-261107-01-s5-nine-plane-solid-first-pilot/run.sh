#!/usr/bin/env bash
# Bounded pilot (<= 2 core-hours). Usage: bash run.sh 0   (one shard; WORKERS <= 10 on the laptop)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-0}" != 0 ]]; then echo 'One shard (0).' >&2; exit 2; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/nine.py" --out "${OUT:-$HERE/results/0}" --workers "${WORKERS:-10}" ${SEEDS:+--seeds "$SEEDS"} ${CAP:+--cap "$CAP"}
