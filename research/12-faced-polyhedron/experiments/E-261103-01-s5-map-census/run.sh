#!/usr/bin/env bash
# Bounded census shard; results include their own provenance manifest.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHARD="${1:-0}"
case "$SHARD" in
  0) F=7; G=1 ;;
  1) F=8; G=2 ;;
  2) F=9; G=3 ;;
  3) F=10; G=4 ;;
  4) F=12; G=6 ;;
  *) echo "shard must be 0..4" >&2; exit 2 ;;
esac
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
exec "$PYTHON" "$HERE/census.py" "$F" "$G" --seconds 60 --out "$HERE/results/$SHARD"
