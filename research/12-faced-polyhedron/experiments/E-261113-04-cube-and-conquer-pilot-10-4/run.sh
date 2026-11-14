#!/usr/bin/env bash
# E-261113-04 shard runner (PLAN.md): controls, then this shard's units: the map 845 monolithic speed calibration and
# the 2 x 512 segment-order cubes of (10, 4) maps 96 and 85 (kissat, no proof, cube cap 0.1x monolithic, arm cap 0.7x).
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 13-04 start|status|stop
# Pilot: OUT_DIR=<dir> LIMIT=<units> SHARDS=10 bash run.sh SHARD
# Writes results/<SHARD>/ next to this file, starting with the provenance manifest (PROTOCOL.md section 5).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"                 # research/12-faced-polyhedron
SHARD="${1:-0}"
SHARDS="${SHARDS:-1}"
WORKERS=1   # one solver process per shard
OUT="${OUT_DIR:-$HERE/results}/$SHARD"
mkdir -p "$OUT"
T0=$(python3 -c 'import time; print(time.monotonic_ns())')
if [[ -f "$OUT/manifest.txt" ]]; then
  echo "restarted_utc: $(date -u +%FT%TZ)" >> "$OUT/manifest.txt"
else
  {
  echo "experiment: $(basename "$HERE")"
  echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
  echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
  echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  echo "shard: $SHARD"
  echo "shards: $SHARDS"
  echo "workers: $WORKERS"
  echo "host: $(uname -srm)"
  echo "python: $(python3 --version 2>&1)"
  echo "started_utc: $(date -u +%FT%TZ)"
  } > "$OUT/manifest.txt"
  python3 -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
fi
finish() {
  rc=$?; T1=$(python3 -c 'import time; print(time.monotonic_ns())')
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $(((T1 - T0) / 1000000000))"
    echo "core_hours: $(python3 -c "print(round($((T1 - T0)) * $WORKERS / 3600000000000, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT

# ---- the experiment: controls, then this shard's units (resumes: recorded units are skipped) ----
export NO_PROOF=1   # no DRAT (owner, 2026-11-13): UNSATs are UNSAT-SOLVER
export SAT_SOLVER="$HOME/bin/kissat" SOLVER_OPTS=""
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
PY="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
nice -n 10 "$PY" "$HERE/cubes.py" "$SHARD" "$SHARDS" "$OUT" ${LIMIT:-}
