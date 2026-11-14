#!/usr/bin/env bash
# E-261113-03 rung-below cell census, one shard of SHARDS (default 10, driven by overnight/launch.sh): bash run.sh SHARD
# Every start runs the C0/C2/P controls first; recorded units are skipped. The shard's share of 20 core-h covers
# controls and units of every start. PILOT=1: the shard's first five units (the 50 timed cells), 0.5 core-h in all.
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
nice -n 10 "$PYTHON" "$HERE/census.py" --out "$OUT" --shard "$SHARD" --shards "$SHARDS" ${CAP:+--cap "$CAP"} \
  ${BUDGET:+--budget "$BUDGET"} ${PILOT:+--pilot} || rc=$?
echo "exit_status $rc" >> "$OUT/manifest.txt"
exit "$rc"
