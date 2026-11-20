#!/usr/bin/env bash
# E-261119-02 (PLAN.md). Default (amendment 4): STAGE=A5c2, the C2 4 x 2 + 1 census at (9, 5) with the C2 controls,
#   10 shards x BUDGET 14400 s (40 core-h hard cap) -> results/stageA5c2/<s>/ with night.log (launch.results).
#   Owner launch: bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start
#   Then: python3 symcensus.py summary results/stageA5c2 A5c2
# STAGE=A5c3: the C3 3+3+3 census at (9, 5) with the C3 (9, 3) control (session, BUDGET=300) -> results/stageA5c3/<s>/.
# STAGE=B1: amendment 3, stage-B pass 1, queue_pass1.json (every (9, 4) map, cap 30 s, BUDGET 36000 s) through run_b.sh
#   -> results/stageB-pass1/<s>/ (launch.results back to results/stageB-pass1). maps/pass1.json is not committed:
#   `python stageb.py` rebuilds it; the runner checks it against the queue's SHA-256.
# STAGE=B: amendment 2, the rung (9, 3), the rung (8, 3) and the pricing in turn -> results/stageB-<queue>/<s>/, launch
#   log in results/stageB/<s>/night.log (launch.results back to results/stageB).
# STAGE=A: stage A, one shard of the symmetric census; shards claim units in order (C3 first) until BUDGET seconds.
#   Rerun: STAGE=A with launch.results set back to results/stageA (10 shards x 360 s = 1 core-h)
#   -> results/stageA/<s>/results.jsonl (launch.results). Shard 0 first runs test_symcensus.py (single process, the other
#   shards wait); a failure stops every shard before any census unit. Then: python3 symcensus.py summary results/stageA
#   The census stages A, A5c3 and A5c2 share this path (results/stage<STAGE>/).
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
STAGE="${STAGE:-A5c2}"
[[ "$STAGE" == A5c2 && -z "${PILOT:-}" ]] && BUDGET="${BUDGET_A5C2:-14400}"
if [[ "$STAGE" == B1 ]]; then   # amendment 3: pass 1
  [[ -f "$HERE/maps/pass1.json" ]] || { echo "maps/pass1.json missing: run python stageb.py first" >&2; exit 2; }
  BUDGET=36000 QUEUE="$HERE/queue_pass1.json" RESULTS="$HERE/results/stageB-pass1" bash "$HERE/run_b.sh" "$SHARD"
  exit $?
fi
if [[ "${STAGE}" == B ]]; then   # amendment 2: the rung (9, 3), the rung (8, 3), then the pricing, in turn per shard
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
[[ "$STAGE" =~ ^(A|A5c3|A5c2)$ ]] || { echo "unknown STAGE $STAGE" >&2; exit 2; }
if [[ -n "${PILOT:-}" ]]; then OUT="$HERE/results/${PILOT_DIR:-pilot}"; else OUT="$HERE/results/stage$STAGE"; fi
mkdir -p "$OUT/$SHARD"
{
  echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS seconds $BUDGET stage $STAGE"
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
nice -n 10 "$PYTHON" symcensus.py shard "$SHARD" "$SHARDS" "$OUT" "$BUDGET" "$STAGE" || rc=$?
exit $rc
