#!/usr/bin/env bash
# Bounded representation audit, one shard. Geometric search requires an amendment.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
if [[ "${1:-0}" != 0 || "${SHARDS:-1}" != 1 ]]; then
  echo 'The registered representation audit requires shard 0 of 1.' >&2
  exit 2
fi
PYTHON="${PYTHON:-python3}"
exec "$PYTHON" "$HERE/audit.py" --out "$HERE/results/representation-audit"
