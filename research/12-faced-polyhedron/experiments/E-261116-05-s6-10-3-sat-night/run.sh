#!/usr/bin/env bash
# Owner entry point: overnight/launch.sh 16-05 start|status|stop
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-10}"
SHARD="${1:?numeric shard required}"
[[ "$SHARDS" =~ ^(8|9|10)$ && "$SHARD" =~ ^[0-9]$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
OUT="$HERE/$(cat "$HERE/launch.results")/$SHARD"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export SAT_SOLVER="${SAT_SOLVER:-kissat}" NO_PROOF=1
nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5ab --workers 1 \
  --shard "$SHARD" --shards "$SHARDS" --results-dir "$OUT" \
  --s5-queue "${S5AB_QUEUE:-$HERE/queue.json}" --s5-budget-seconds "${BUDGET:-284400}" --hours "${HOURS:-8}"
"$PYTHON" "$ROOT/overnight/run_overnight.py" status --results-dir "$OUT"
