#!/usr/bin/env bash
# E-261112-01 Stage A, one shard of SHARDS (default 10, driven by overnight/launch.sh): bash run.sh SHARD
# Every start runs the C0/C1/C2 controls first; recorded units are skipped. The shard's share of 12 core-h covers
# controls, its two pilot units (one per source), the automatic pilot gate and the rest. PILOT=1: pilot units only.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHARDS="${SHARDS:-10}"; SHARD="${1:-0}"
if [[ ! "$SHARDS" =~ ^([1-9]|10)$ || ! "$SHARD" =~ ^[0-9]+$ || "$SHARD" -ge "$SHARDS" ]]; then
  echo 'Requires SHARDS=1..10 and 0 <= SHARD < SHARDS.' >&2; exit 2
fi
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
OUT="${OUT:-$HERE/results/$SHARD}"
mkdir -p "$OUT"
rc=0
nice -n 10 "$PYTHON" "$HERE/stage_a.py" --out "$OUT" --shard "$SHARD" --shards "$SHARDS" ${CAP:+--cap "$CAP"} \
  ${BUDGET:+--budget "$BUDGET"} ${PILOT:+--pilot} || rc=$?
echo "exit_status $rc" >> "$OUT/manifest.txt"
exit "$rc"
