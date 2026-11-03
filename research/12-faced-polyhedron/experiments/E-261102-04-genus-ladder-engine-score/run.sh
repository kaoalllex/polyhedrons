#!/usr/bin/env bash
# Runner for one shard of E-261102-04 (the E-261101-26 ladder, genus-ladder engine; a grid of budgets): SHARDS=N bash run.sh SHARD
# Laptop: bash overnight/launch.sh start experiments/E-261102-04-genus-ladder-engine-score CORES   (sets SHARDS=CORES)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SHARD="${1:-0}"
SHARDS="${SHARDS:-10}"
WORKERS=1
PY="${PY:-$HOME/.venvs/polyhedra/bin/python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1   # one core per process on the M4 Pro
export PYTHONHASHSEED=0   # the engine seeds its realizer from hash(tag); fixed so that a unit is reproducible
LADDER="$ROOT/experiments/E-261101-26-engine-benchmark-ladder"   # the harness and tasks.json of E-261101-26
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
T0=$(date +%s)
if [ -f "$OUT/manifest.txt" ]; then
  echo "restarted_utc: $(date -u +%FT%TZ) commit: $(git -C "$ROOT" rev-parse --short HEAD) shards: $SHARDS" >> "$OUT/manifest.txt"   # resume: recorded units are skipped
else
  {
    echo "experiment: $(basename "$HERE")"; echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
    echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"; echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
    echo "shard: $SHARD of $SHARDS"; echo "workers: $WORKERS"; echo "host: $(uname -srm)"; echo "python: $($PY --version 2>&1)"
    echo "tasks_sha256: $(shasum -a 256 "$LADDER/tasks.json" | cut -d' ' -f1)"; echo "started_utc: $(date -u +%FT%TZ)"
  } > "$OUT/manifest.txt"
fi
$PY -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
finish() {
  rc=$?; T1=$(date +%s)
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $((T1 - T0))"
    echo "core_hours: $($PY -c "print(round($((T1 - T0)) * $WORKERS / 3600, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT
cd "$LADDER"
# PLAN: one cell after another, each split over all shards (shard s takes every SHARDS-th unit of the cell)
L() { nice -n 10 $PY ladder.py run --engine genus-ladder --shard "$SHARD" --shards "$SHARDS" --out "$OUT" "$@"; }
L --only R1-szilassi --minutes 5
L --only R5-type15-genus3-from-parent --minutes 6
L --only R5-type15-genus3-from-parent --minutes 40 --seeds 5
L --only R4-type15-genus3 R4-type0-genus3 --minutes 40 --seeds 5
L --only R4-type15-genus3 R4-type0-genus3 --minutes 120 --seeds 2
$PY ladder.py score "$OUT" --to "$OUT/scores.json"   # per shard; the experiment's scores.json is scored over all shards at conclusion
