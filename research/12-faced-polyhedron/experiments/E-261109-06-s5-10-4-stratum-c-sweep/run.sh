#!/usr/bin/env bash
# E-261109-06 shard runner (PLAN.md): the E-261103-03 runner with kissat on queue.json, no proof; results in
# $(cat launch.results)/SHARD. Budget 80 core-h over 10 shards (8 h per shard), first-SAT stop across shards.
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 09-06 start|status|stop
# Smoke test only: RESULTS=<scratch dir> QUEUE=<test queue> BUDGET=<seconds> SHARDS=10 bash run.sh SHARD
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-10}"
SHARD="${1:-}"
if [[ ! "$SHARD" =~ ^[0-9]$ || "$SHARDS" != 10 ]]; then
  echo 'Usage: SHARDS=10 run.sh SHARD (0 <= SHARD < 10; the queue places each map on a fixed shard of 10)' >&2
  exit 2
fi
R="${RESULTS:-$HERE/$(cat "$HERE/launch.results")}"
mkdir -p "$R/$SHARD"
rc=0
echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS" >> "$R/$SHARD/manifest.txt"
trap 'echo "exit_status: $rc" >> "$R/$SHARD/manifest.txt"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"   # recorded in the identity only; no proof is produced
export NO_PROOF=1
# Per-unit caps are in the queue; the budget gives each shard 28800 s over all restarts.
SAT_SOLVER="$HOME/bin/kissat" SOLVER_OPTS="" nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 \
  --shard "$SHARD" --shards "$SHARDS" --results-dir "$R/$SHARD" --s5-queue "${QUEUE:-$HERE/queue.json}" \
  --timeout 3600 --s5-checker-timeout 60 --s5-budget-seconds "${BUDGET:-288000}" --hours 10 || rc=$?
exit $rc
