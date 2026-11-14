#!/usr/bin/env bash
# E-261110-02 shard runner (PLAN.md): the E-261103-03 runner in its imported-map mode (submap=True, every SAT model
# through the bridge and `verify_candidate.py --target S6`, no first-SAT stop) with kissat on queue.json, no proof
# (owner, 2026-11-13: UNSATs are UNSAT-SOLVER); results in $(cat launch.results)/SHARD. Budget 80 core-h over 10 shards, at most 10 h per invocation.
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 10-02 start|status|stop
# Prep pilot / startup check: RESULTS=<dir> QUEUE=<queue> BUDGET=<seconds> SHARDS=<queue shards> bash run.sh SHARD
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
Q="${QUEUE:-$HERE/queue.json}"
SHARDS="${SHARDS:-10}"
SHARD="${1:-}"
WANT="$("$PYTHON" -c 'import json, sys; print(json.load(open(sys.argv[1]))["shards"])' "$Q")"
if [[ ! "$SHARD" =~ ^[0-9]$ || "$SHARDS" != "$WANT" || "$SHARD" -ge "$SHARDS" ]]; then
  echo "Usage: SHARDS=$WANT run.sh SHARD (0 <= SHARD < $WANT; the queue places each map on a fixed shard)" >&2
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
# Per-unit caps are in the queue; the budget gives each shard BUDGET / SHARDS seconds over all restarts.
SAT_SOLVER="$HOME/bin/kissat" SOLVER_OPTS="" nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 \
  --shard "$SHARD" --shards "$SHARDS" --results-dir "$R/$SHARD" --s5-queue "$Q" \
  --timeout 3600 --s5-checker-timeout 60 --s5-budget-seconds "${BUDGET:-288000}" --hours 10 || rc=$?
exit $rc
