#!/usr/bin/env bash
# Stage A (session, about a minute): bash run.sh stage_a -> results/controls/ (engine, chart and draw controls).
# Night (<= 80 core-h, one owner night, 10 shards): bash overnight/launch.sh 10-04 start|status|stop
#   -> results/<shard>/results.jsonl; then: python3 night.py summary results
# Pilot: DEADLINE=300 OUTDIR=pilot bash run.sh 0 -> results/pilot/0/ (not counted in the night's tally).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-10}"
SHARD="${1:?stage_a or a numeric shard}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
provenance() {
  { echo "commit: $(git -C "$ROOT" rev-parse HEAD)"; echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
    echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"; echo "host: $(uname -srm)"; echo "python: $("$PYTHON" --version 2>&1)"
    echo "started_utc: $(date -u +%FT%TZ)"; } >> "$1/manifest.txt"
  "$PYTHON" -m pip freeze > "$1/pip-freeze.txt" 2>/dev/null || true
}
cd "$HERE"
if [[ "$SHARD" == stage_a ]]; then
  OUT="$HERE/results/controls"
  [[ ! -e "$OUT" ]] || { echo "$OUT exists; never overwritten" >&2; exit 2; }
  T0=$(date +%s)
  "$PYTHON" night.py controls "$OUT"
  provenance "$OUT"
  echo "wall_seconds: $(( $(date +%s) - T0 ))" >> "$OUT/manifest.txt"
  exit 0
fi
[[ "$SHARDS" =~ ^([1-9]|10)$ && "$SHARD" =~ ^[0-9]$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
grep -q '"PASS": true' "$HERE/results/controls/controls.json" 2>/dev/null || { echo "stage A missing or failed" >&2; exit 2; }
OUT="$HERE/results/${OUTDIR:+$OUTDIR/}$SHARD"; mkdir -p "$OUT"; provenance "$OUT"
T0=$(date +%s)
# Shard wall DEADLINE s, monotonic (10 x 27000 s = 75 core-h, under the 80 core-h cap with the last unit's 40 s).
trap 'echo "finished_utc: $(date -u +%FT%TZ)" >> "$OUT/manifest.txt"; echo "wall_seconds: $(( $(date +%s) - T0 ))" >> "$OUT/manifest.txt"' EXIT
nice -n 10 "$PYTHON" night.py sample "$SHARD" "$SHARDS" "${DEADLINE:-27000}" "$OUT"
