#!/usr/bin/env bash
# E-261119-02 (PLAN.md). Default (amendment 6): STAGE=B5p1, pass 1 at (9, 5) on the random 10% (chunks CHUNKS=0-9 of
#   maps/pass1_9_5/, `python stageb.py --g5-pass1` builds them; cap 5 s, lean), the chunks in turn per shard, each
#   through run_b.sh with BUDGET 18000 s -> results/stageB5-pass1-c<k>/<s>/; launch log in results/stageB5-pass1/<s>/
#   (launch.results). A shard stops at the first chunk that ends other than SHARD-COMPLETE (deadline, stop, error), and
#   before a chunk once the chunks' budget ledgers hold CAP_TOTAL (72000 core-s = 20 core-h, reservations included).
#   Owner launch: bash research/12-faced-polyhedron/overnight/launch.sh 261119-02 start (stop: ... stop; resumable)
# STAGE=A5c2: amendment 4, the C2 4 x 2 + 1 census at (9, 5) with the C2 controls, 10 shards x BUDGET 14400 s
#   -> results/stageA5c2/<s>/ (launch.results back to results/stageA5c2). Then: python3 symcensus.py summary
#   results/stageA5c2 A5c2
# STAGE=B5: amendment 5 (session, seconds): per shard in turn the lean replication of the (9, 4) pricing
#   (queue_pricing_lean.json), the (9, 5) C2 4 x 2 + 1 pricing (queue_pricing_9_5.json) and (amendment 6) the lean
#   (8, 3) rung with its SAT units (queue_rung_8_3_lean.json), through run_b.sh -> results/stageB5-<queue>/<s>/;
#   `python stageb.py --g5` builds the queues from the data copy.
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
CHUNKS="${CHUNKS:-0-9}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
[[ "$SHARD" =~ ^[0-9]+$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
cd "$HERE"
STAGE="${STAGE:-B5p1}"
[[ "$STAGE" == A5c2 && -z "${PILOT:-}" ]] && BUDGET="${BUDGET_A5C2:-14400}"
if [[ "$STAGE" == B1 ]]; then   # amendment 3: pass 1
  [[ -f "$HERE/maps/pass1.json" ]] || { echo "maps/pass1.json missing: run python stageb.py first" >&2; exit 2; }
  BUDGET=36000 QUEUE="$HERE/queue_pass1.json" RESULTS="$HERE/results/stageB-pass1" bash "$HERE/run_b.sh" "$SHARD"
  exit $?
fi
if [[ "$STAGE" == B5 ]]; then   # amendment 5: lean replication, then the (9, 5) pricing, in turn per shard
  rc=0
  for q in pricing_lean pricing_9_5 rung_8_3_lean; do
    [[ -f "$HERE/results/stageB5/stop.requested" ]] && break
    mkdir -p "$HERE/results/stageB5-$q" "$HERE/results/stageB5"
    ln -sfn ../stageB5/stop.requested "$HERE/results/stageB5-$q/stop.requested"
    BUDGET=72000 QUEUE="$HERE/queue_$q.json" RESULTS="$HERE/results/stageB5-$q" bash "$HERE/run_b.sh" "$SHARD" || rc=$?
  done
  exit $rc
fi
if [[ "$STAGE" == B5p1 ]]; then   # amendment 6: pass 1 at (9, 5), chunks in turn
  L="$HERE/results/${PILOT_DIR:-stageB5-pass1}"; mkdir -p "$L"
  for k in $(seq "${CHUNKS%-*}" "${CHUNKS#*-}"); do
    [[ -f "$L/stop.requested" ]] && break
    used=$(cat "$L"-c*/budget.json 2>/dev/null | "$PYTHON" -c 'import json, sys
d = json.JSONDecoder(); s = sys.stdin.read().strip(); t = 0
while s:
    o, i = d.raw_decode(s); t += sum(o.values()); s = s[i:].strip()
print(int(t))')
    [[ "$used" -lt "${CAP_TOTAL:-72000}" ]] || { echo "pass-1 cap: ${used} core-s charged; shard $SHARD stops"; break; }
    c=$(printf 'c%03d' "$k"); R="$HERE/results/${PILOT_DIR:-stageB5-pass1}-$c"; Q="$HERE/maps/pass1_9_5/queue_$c.json"
    [[ -f "$Q" ]] || { echo "$Q missing: run python stageb.py --g5-pass1 first" >&2; exit 2; }
    mkdir -p "$R"; ln -sfn "../$(basename "$L")/stop.requested" "$R/stop.requested"
    echo "=== $(date -u +%FT%TZ) shard $SHARD chunk $c"
    BUDGET="${BUDGET_CHUNK:-18000}" QUEUE="$Q" RESULTS="$R" bash "$HERE/run_b.sh" "$SHARD" || exit $?
    st=$(cat "$R/$SHARD"/attempt_*/manifest.json 2>/dev/null | "$PYTHON" -c 'import json, sys
d = json.JSONDecoder(); s = sys.stdin.read().strip(); out = []
while s:
    o, i = d.raw_decode(s); out.append(o); s = s[i:].strip()
print(max(out, key=lambda m: m["started_utc"])["status"] if out else "NONE")')
    [[ "$st" == SHARD-COMPLETE ]] || { echo "chunk $c ended $st: shard $SHARD stops" ; break; }
  done
  exit 0
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
