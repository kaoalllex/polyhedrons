#!/usr/bin/env bash
# Bounded R1 pilot, laptop minutes. Usage: bash run.sh 0   (one shard)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-0}" != 0 ]]; then echo 'One shard (0).' >&2; exit 2; fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/embfirst.py" --out "${OUT:-$HERE/results/0}" "${@:2}"
