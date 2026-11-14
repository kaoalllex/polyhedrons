#!/usr/bin/env bash
# Bounded interactive experiment: run pilot first, then the remaining nine shards.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
"$PY" "$HERE/core.py" "${OUT_DIR:-$HERE/results}" "$@"
