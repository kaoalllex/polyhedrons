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
STARTUP_ONLY="${STARTUP_ONLY:-0}"
if [[ "$STARTUP_ONLY" != 0 && ( "$STARTUP_ONLY" != 1 || "$STAGE" != calibration ) ]]; then
  echo 'STARTUP_ONLY=1 requires STAGE=calibration.' >&2
  exit 2
fi
case "$STAGE" in
  representation) DEFAULT_OUT="$HERE/results/representation-audit" ;;
  surgery) DEFAULT_OUT="$HERE/results/surgery-audit" ;;
  recovery) DEFAULT_OUT="$HERE/results/recovery-pilot" ;;
  calibration)
    DEFAULT_OUT="$HERE/results/recovery-grid"
    if [[ "$STARTUP_ONLY" == 1 ]]; then DEFAULT_OUT="$HERE/results/recovery-grid-startup"; fi ;;
  feasibility) DEFAULT_OUT="$HERE/results/submap-feasibility-audit" ;;
  alternatives) DEFAULT_OUT="$HERE/results/mizhaev-first-step-audit" ;;
  descendants) DEFAULT_OUT="$HERE/results/mizhaev-descendant-audit" ;;
  om-realization) DEFAULT_OUT="$HERE/results/intermediate-om-realization" ;;
  om-continuation) DEFAULT_OUT="$HERE/results/mizhaev-om-realization" ;;
  *) echo "Unknown audit stage: $STAGE" >&2; exit 2 ;;
esac
OUT="${OUT:-$DEFAULT_OUT}"
if [[ "$STAGE" == feasibility || "$STAGE" == alternatives || "$STAGE" == descendants || "$STAGE" == om-realization || "$STAGE" == om-continuation ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
  export VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONUNBUFFERED=1
  exec nice -n 10 "$PYTHON" "$HERE/audit.py" --stage "$STAGE" --out "$OUT"
fi
if [[ "$STAGE" == recovery || "$STAGE" == calibration ]]; then
  export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
  export VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1 PYTHONUNBUFFERED=1
  ARGS=(--out "$OUT")
  if [[ "$STAGE" == calibration ]]; then ARGS+=(--calibration); fi
  if [[ "$STARTUP_ONLY" == 1 ]]; then ARGS+=(--startup-only); fi
  exec "$PYTHON" "$HERE/recovery.py" "${ARGS[@]}"
fi
exec "$PYTHON" "$HERE/audit.py" --stage "$STAGE" --out "$OUT"
