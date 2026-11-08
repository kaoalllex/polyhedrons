#!/usr/bin/env bash
# (10,4) cost probe shards (PLAN.md), run by the E-261103-03 runner on queue_probe.json; results in $(cat launch.results)/SHARD.
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 03-07 start|status|stop
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-1}"
SHARD="${1:-}"
if [[ ! "$SHARD" =~ ^[0-9]+$ || ! "$SHARDS" =~ ^([1-9]|10)$ || "$SHARD" -ge "$SHARDS" ]]; then
  echo 'Usage: SHARDS=1..10 run.sh SHARD (0 <= SHARD < SHARDS)' >&2
  exit 2
fi
OUT="${PROBE_RESULTS:-$HERE/$(cat "$HERE/launch.results")}/$SHARD"  # PROBE_RESULTS: startup check only
mkdir -p "$OUT"
echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS" >> "$OUT/manifest.txt"
trap 'echo "exit_status: $?" >> "$OUT/manifest.txt"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export CADICAL="${CADICAL:-$HOME/bin/cadical}" DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"
# Per-map caps are in the queue (300/450 s fast, 1800/2700 s slow, 60/120 s controls); --timeout and
# --s5-checker-timeout are only the defaults. Budget: 10 equal shard shares of 5820 s (2 controls + one slow map + 960 s).
nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 --shard "$SHARD" --shards "$SHARDS" \
  --results-dir "$OUT" --s5-queue "$HERE/queue_probe.json" --timeout 300 --s5-checker-timeout 450 \
  --s5-budget-seconds 58200 --hours "${PROBE_HOURS:-2}"
