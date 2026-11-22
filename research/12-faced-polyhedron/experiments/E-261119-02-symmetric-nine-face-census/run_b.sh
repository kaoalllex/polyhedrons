#!/usr/bin/env bash
# E-261119-02 stage-B shard runner (PLAN amendment 2): the E-261103-03 runner in its imported-map mode on the per-map
# symmetric formula records of a stageb.py queue (C3 uniform standard chart, C2 4 x 2 + 1 plane-only moved chart, free
# C2 uniform); kissat seed 0, no proof (UNSATs are UNSAT-SOLVER); every SAT model through the bridge and
# `verify_candidate.py --all-pairs`. Per-unit caps are in the queue; BUDGET is the runner's reservation ceiling.
# Usage: QUEUE=<queue json> RESULTS=<dir> [BUDGET=<seconds>] bash run_b.sh SHARD
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
Q="${QUEUE:?QUEUE=<queue json> is required}"
R="${RESULTS:?RESULTS=<dir> is required}"
SHARDS="${SHARDS:-10}"
SHARD="${1:-}"
WANT="$("$PYTHON" -c 'import json, sys; print(json.load(open(sys.argv[1]))["shards"])' "$Q")"
if [[ ! "$SHARD" =~ ^[0-9]$ || "$SHARDS" != "$WANT" || "$SHARD" -ge "$SHARDS" ]]; then
  echo "Usage: QUEUE=<queue> RESULTS=<dir> run_b.sh SHARD (0 <= SHARD < $WANT)" >&2
  exit 2
fi
mkdir -p "$R/$SHARD"
rc=0
echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS queue $(basename "$Q")" >> "$R/$SHARD/manifest.txt"
trap 'echo "finished_utc: $(date -u +%FT%TZ) exit_status: $rc" >> "$R/$SHARD/manifest.txt"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"   # recorded in the identity only; no proof is produced
export NO_PROOF=1
SAT_SOLVER="$HOME/bin/kissat" SOLVER_OPTS="" nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 \
  --shard "$SHARD" --shards "$SHARDS" --results-dir "$R/$SHARD" --s5-queue "$Q" \
  --timeout 600 --s5-checker-timeout 360 --s5-budget-seconds "${BUDGET:-72000}" --hours 2 || rc=$?
exit $rc
