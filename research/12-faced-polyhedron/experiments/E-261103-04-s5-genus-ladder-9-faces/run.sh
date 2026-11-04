#!/usr/bin/env bash
# Bounded representation/surgery audits and geometric recovery, one shard. See PLAN.md for stage gates.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-0}" != 0 || "${SHARDS:-1}" != 1 ]]; then
  echo 'The registered representation audit requires shard 0 of 1.' >&2
  exit 2
fi
PYTHON="${PYTHON:-python3}"
STAGE="${STAGE:-representation}"
case "$STAGE" in
  representation) DEFAULT_OUT="$HERE/results/representation-audit" ;;
  surgery) DEFAULT_OUT="$HERE/results/surgery-audit" ;;
  recovery) DEFAULT_OUT="$HERE/results/recovery-pilot" ;;
  *) echo "Unknown audit stage: $STAGE" >&2; exit 2 ;;
esac
OUT="${OUT:-$DEFAULT_OUT}"
if [[ "$STAGE" == recovery ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
  export VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONUNBUFFERED=1
  exec "$PYTHON" "$HERE/recovery.py" --out "$OUT"
fi
exec "$PYTHON" "$HERE/audit.py" --stage "$STAGE" --out "$OUT"
