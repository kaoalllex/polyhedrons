#!/usr/bin/env bash
# Runner for one shard of the benchmark ladder: SHARDS=N bash run.sh SHARD   (shard s takes every N-th (task, seed) unit)
# Laptop: bash overnight/launch.sh start experiments/E-261101-26-engine-benchmark-ladder CORES   (sets SHARDS=CORES)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SHARD="${1:-0}"
SHARDS="${SHARDS:-10}"
WORKERS=1
PY="${PY:-$HOME/.venvs/polyhedra/bin/python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1   # one core per process on the M4 Pro
export PYTHONHASHSEED=0   # the engine seeds its realizer from hash(tag); fixed so that a unit is reproducible
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
    echo "tasks_sha256: $(shasum -a 256 "$HERE/tasks.json" | cut -d' ' -f1)"; echo "started_utc: $(date -u +%FT%TZ)"
  } > "$OUT/manifest.txt"
fi
$PY -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
finish() {
  rc=$?; T1=$(date +%s)
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $((T1 - T0))"
    echo "core_hours: $($PY -c "print(round($((T1 - T0)) * $WORKERS / 3600, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT
cd "$HERE"
nice -n 10 $PY ladder.py run --shard "$SHARD" --shards "$SHARDS" --out "$OUT"
$PY ladder.py score "$OUT" --to "$OUT/scores.json"   # per shard; the experiment's scores.json is scored over all shards at conclusion
