#!/usr/bin/env bash
# E-261119-02 (PLAN.md). Default (amendment 2): stage-B rung and pricing, the three stageb.py queues in turn through
#   run_b.sh -> results/stageB-<queue>/<s>/; launch log in results/stageB/<s>/night.log (launch.results).
#   Owner launch: bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start
# STAGE=A: stage A, one shard of the symmetric census; shards claim units in order (C3 first) until BUDGET seconds.
#   Rerun: STAGE=A with launch.results set back to results/stageA (10 shards x 360 s = 1 core-h)
#   -> results/stageA/<s>/results.jsonl (launch.results). Shard 0 first runs test_symcensus.py (single process, the other
#   shards wait); a failure stops every shard before any census unit. Then: python3 symcensus.py summary results/stageA
# Pilots: PILOT=1 [PILOT_DIR=..] BUDGET=s bash run.sh SHARD -> results/<PILOT_DIR or pilot>/.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARD="${1:?numeric shard}"
SHARDS="${SHARDS:-10}"
BUDGET="${BUDGET:-360}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
[[ "$SHARD" =~ ^[0-9]+$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
cd "$HERE"
if [[ "${STAGE:-B}" == B ]]; then   # amendment 2: the rung (9, 3), the rung (8, 3), then the pricing, in turn per shard
  rc=0
  for q in rung_9_3 rung_8_3 pricing; do
    [[ -f "$HERE/results/stageB/stop.requested" ]] && break
    echo "=== $(date -u +%FT%TZ) shard $SHARD queue $q"
    mkdir -p "$HERE/results/stageB-$q" "$HERE/results/stageB"   # launch.sh stop reaches the runner through this link
    ln -sfn ../stageB/stop.requested "$HERE/results/stageB-$q/stop.requested"
    BUDGET=72000 QUEUE="$HERE/queue_$q.json" RESULTS="$HERE/results/stageB-$q" bash "$HERE/run_b.sh" "$SHARD" || rc=$?
  done
  exit $rc
fi
if [[ -n "${PILOT:-}" ]]; then OUT="$HERE/results/${PILOT_DIR:-pilot}"; else OUT="$HERE/results/stageA"; fi
mkdir -p "$OUT/$SHARD"
{
  echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS seconds $BUDGET"
  echo "commit: $(git -C "$ROOT" rev-parse HEAD) dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
  echo "host: $(uname -srm) python: $("$PYTHON" --version 2>&1)"
} >> "$OUT/$SHARD/manifest.txt"
TESTS="$OUT/unit-tests"
if [[ "$SHARD" == 0 && ! -f "$TESTS.ok" ]]; then
  if "$PYTHON" -m unittest -v test_symcensus > "$TESTS.log" 2>&1; then touch "$TESTS.ok"; else touch "$TESTS.failed"; fi
fi
until [[ -f "$TESTS.ok" || -f "$TESTS.failed" ]]; do sleep 5; done
[[ -f "$TESTS.ok" ]] || { echo "unit tests failed: $TESTS.log" >&2; exit 2; }
rc=0
trap 'echo "finished_utc: $(date -u +%FT%TZ) exit_status: $rc" >> "$OUT/$SHARD/manifest.txt"' EXIT
nice -n 10 "$PYTHON" symcensus.py shard "$SHARD" "$SHARDS" "$OUT" "$BUDGET" || rc=$?
exit $rc
