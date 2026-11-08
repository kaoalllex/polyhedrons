#!/usr/bin/env bash
# Arrangement-source sweep, one shard of SHARDS (default 10, driven by overnight/launch.sh): bash run.sh SHARD
# Resumable: recorded units are skipped. Budget 720 core-s per shard (2 core-h over 10 shards).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHARDS="${SHARDS:-10}"; SHARD="${1:-0}"
if [[ ! "$SHARDS" =~ ^([1-9]|10)$ || ! "$SHARD" =~ ^[0-9]+$ || "$SHARD" -ge "$SHARDS" ]]; then
  echo 'Requires SHARDS=1..10 and 0 <= SHARD < SHARDS.' >&2; exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
OUT="${OUT:-$HERE/results/$SHARD}"
rc=0
nice -n 10 "$PYTHON" "$HERE/sweep.py" --out "$OUT" --shard "$SHARD" --shards "$SHARDS" ${CAP:+--cap "$CAP"} ${BUDGET:+--budget "$BUDGET"} || rc=$?
echo "exit_status $rc" >> "$OUT/manifest.txt"
exit "$rc"
