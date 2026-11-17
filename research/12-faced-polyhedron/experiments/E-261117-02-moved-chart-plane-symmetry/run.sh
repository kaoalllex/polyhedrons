#!/usr/bin/env bash
# Stage A (session, seconds): bash run.sh stage_a -> results/controls/ (Szilassi control chain K1-K5, negatives).
# Stage B (<= 1 core-h, about 6 min wall on 10 shards): bash overnight/launch.sh 17-02 start|status|stop
#   -> results/<shard>/results.jsonl; then: python3 n2.py summary results
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
  "$PYTHON" n2.py controls "$OUT"
  provenance "$OUT"
  echo "wall_seconds: $(( $(date +%s) - T0 ))" >> "$OUT/manifest.txt"
  exit 0
fi
[[ "$SHARDS" =~ ^(8|9|10)$ && "$SHARD" =~ ^[0-9]$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
grep -q '"PASS": true' "$HERE/results/controls/controls.json" 2>/dev/null || { echo "stage A missing or failed" >&2; exit 2; }
OUT="$HERE/results/$SHARD"; mkdir -p "$OUT"; provenance "$OUT"
# N units per arm, per-unit CP-SAT cap CAP s, shard wall DEADLINE s (10 x 330 s < 1 core-h).
nice -n 10 "$PYTHON" n2.py sample "$SHARD" "$SHARDS" "${N:-5000}" "${CAP:-10}" "${DEADLINE:-330}" "$OUT"
echo "finished_utc: $(date -u +%FT%TZ)" >> "$OUT/manifest.txt"
