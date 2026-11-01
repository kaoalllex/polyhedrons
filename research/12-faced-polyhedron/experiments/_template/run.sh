#!/usr/bin/env bash
# Runner for one shard of this experiment: bash run.sh [SHARD]
# Laptop: caffeinate -dimsu bash run.sh 0      GitHub Actions: .github/workflows/experiment.yml calls it per shard.
# Writes results/<SHARD>/ next to this file, starting with the provenance manifest (PROTOCOL.md section 5).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"                 # research/12-faced-polyhedron
SHARD="${1:-0}"
WORKERS="${WORKERS:-$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)}"
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
T0=$(date +%s)
{
  echo "experiment: $(basename "$HERE")"
  echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
  echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
  echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  echo "shard: $SHARD"
  echo "workers: $WORKERS"
  echo "host: $(uname -srm)"
  echo "python: $(python3 --version 2>&1)"
  echo "started_utc: $(date -u +%FT%TZ)"
} > "$OUT/manifest.txt"
python3 -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
finish() {
  rc=$?; T1=$(date +%s)
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $((T1 - T0))"
    echo "core_hours: $(python3 -c "print(round($((T1 - T0)) * $WORKERS / 3600, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT

# ---- the experiment: bounded, checkpointing into $OUT (EDIT) ----
cd "$ROOT/code"
echo "replace this line with the experiment command, e.g. python3 my_script.py --seed $SHARD --out $OUT/result.json or python3 ../../overnight/run_overnight.py JOB --results-dir $OUT ..."
exit 1

# ---- exact verification of anything found (EDIT) ----
# python3 "$ROOT/verification/verify_candidate.py" "$OUT/result.json"
