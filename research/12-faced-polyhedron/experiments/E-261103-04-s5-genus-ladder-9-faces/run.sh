#!/usr/bin/env bash
# Bounded representation/surgery audit, one shard. See PLAN.md for stage gates.
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
  *) echo "Unknown audit stage: $STAGE" >&2; exit 2 ;;
esac
OUT="${OUT:-$DEFAULT_OUT}"
exec "$PYTHON" "$HERE/audit.py" --stage "$STAGE" --out "$OUT"
