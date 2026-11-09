#!/usr/bin/env bash
# E-261108-03 shard runner (PLAN.md): per shard the roots kissat-A, unsat-A, kissat-B, unsat-B, default-B in this order, each by the
# E-261103-03 runner on its queue; results in $(cat launch.results)/<root>/SHARD. A failed root does not stop the others.
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 08-03 start|status|stop
# Smoke test only: RESULTS=<scratch dir> QDIR=<dir with test queues> PHASES="A" (or "B") SHARDS=10 bash run.sh SHARD
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-10}"
SHARD="${1:-}"
if [[ ! "$SHARD" =~ ^[0-9]$ || "$SHARDS" != 10 ]]; then
  echo 'Usage: SHARDS=10 run.sh SHARD (0 <= SHARD < 10; the queues place each map on a fixed shard of 10)' >&2
  exit 2
fi
R="${RESULTS:-$HERE/$(cat "$HERE/launch.results")}"
mkdir -p "$R/$SHARD"
rc_all=0
echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS" >> "$R/$SHARD/manifest.txt"
trap 'echo "exit_status: $rc_all" >> "$R/$SHARD/manifest.txt"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"
export NO_PROOF=1   # amendment 2 of PLAN.md (owner 2026-11-08): no DRAT, UNSATs are UNSAT-SOLVER
for PHASE in ${PHASES:-A B}; do
  VARIANTS="kissat unsat"; [ "$PHASE" = B ] && VARIANTS="kissat unsat default"
  for V in $VARIANTS; do
    case "$V" in
      kissat) SOLVER="$HOME/bin/kissat"; OPTS="" ;;
      unsat) SOLVER="$HOME/bin/cadical"; OPTS="--unsat" ;;
      default) SOLVER="$HOME/bin/cadical"; OPTS="" ;;
    esac
    # Per-unit caps are in the queue; the budget only sizes each shard's reservation (A 3180 s, B 15780 s per shard).
    case "$PHASE" in A) BUDGET=31800 ;; B) BUDGET=157800 ;; esac
    D="$R/$V-$PHASE"; mkdir -p "$D/$SHARD"
    ln -sfn ../stop.requested "$D/stop.requested" 2>/dev/null   # launch.sh stop touches $R/stop.requested; shards race here
    if [ -e "$R/stop.requested" ]; then echo "stop requested: $V-$PHASE not started"; continue; fi
    echo "=== $(date '+%F %T') $V-$PHASE shard $SHARD"
    SAT_SOLVER="$SOLVER" SOLVER_OPTS="$OPTS" nice -n 10 "$PYTHON" "$ROOT/overnight/run_overnight.py" s5 --workers 1 \
      --shard "$SHARD" --shards "$SHARDS" --results-dir "$D/$SHARD" --s5-queue "${QDIR:-$HERE}/queue_$V-$PHASE.json" \
      --timeout 60 --s5-checker-timeout 120 --s5-budget-seconds "$BUDGET" --hours 8 \
      || { rc=$?; rc_all=$rc; echo "$V-$PHASE shard $SHARD ended rc=$rc"; }
  done
done
