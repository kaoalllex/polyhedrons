#!/usr/bin/env bash
# Stage A (session pilot, minutes): bash run.sh stage_a   -> results/census/ (both enumerations, kill checks,
#   formula controls). Stage B (owner): bash overnight/launch.sh 17-01 start|status|stop -> results/<shard>/.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARDS="${SHARDS:-10}"
SHARD="${1:?stage_a or a numeric shard}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export SAT_SOLVER="${SAT_SOLVER:-$HOME/bin/kissat}" NO_PROOF=1
provenance() {
  { echo "commit: $(git -C "$ROOT" rev-parse HEAD)"; echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
    echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"; echo "host: $(uname -srm)"; echo "python: $("$PYTHON" --version 2>&1)"
    echo "solver: $SAT_SOLVER $(shasum -a 256 "$SAT_SOLVER" | cut -d' ' -f1)"; echo "started_utc: $(date -u +%FT%TZ)"; } >> "$1/manifest.txt"
  "$PYTHON" -m pip freeze > "$1/pip-freeze.txt" 2>/dev/null || true
}
if [[ "$SHARD" == stage_a ]]; then
  OUT="$HERE/results/census"
  [[ ! -e "$OUT" ]] || { echo "$OUT exists; never overwritten" >&2; exit 2; }
  cd "$HERE"
  "$PYTHON" -m unittest test_cayley
  T0=$(date +%s)
  "$PYTHON" cayley.py stage_a "$OUT" "$SHARDS"
  provenance "$OUT"
  "$PYTHON" formulas.py --controls --out "$OUT/controls"
  echo "wall_seconds: $(( $(date +%s) - T0 ))" >> "$OUT/manifest.txt"
  exit 0
fi
[[ "$SHARDS" =~ ^(8|9|10)$ && "$SHARD" =~ ^[0-9]$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
[[ -f "$HERE/results/census/census.json" ]] && grep -q '"PASS": true' "$HERE/results/census/census.json" || { echo "stage A missing or failed" >&2; exit 2; }
OUT="$HERE/results/$SHARD"; mkdir -p "$OUT"; provenance "$OUT"
cd "$HERE"
nice -n 10 "$PYTHON" formulas.py --out "$OUT" --shard "$SHARD" --shards "$SHARDS" --budget "${BUDGET:-280}" --cap "${CAP:-120}"
echo "finished_utc: $(date -u +%FT%TZ)" >> "$OUT/manifest.txt"
