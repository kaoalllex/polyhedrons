#!/usr/bin/env bash
# Runner for one shard of this experiment: bash run.sh SHARD   (8 shards; shard s takes every 8th type of TYPES)
# Laptop: caffeinate -dimsu bash run.sh 0      GitHub Actions: .github/workflows/experiment.yml calls it per shard.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SHARD="${1:-0}"
WORKERS="${WORKERS:-1}"
PY="${PY:-$HOME/.venvs/polyhedra/bin/python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1   # one core per process on the M4 Pro
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
T0=$(date +%s)
if [ -f "$OUT/manifest.txt" ]; then
  echo "restarted_utc: $(date -u +%FT%TZ) commit: $(git -C "$ROOT" rev-parse --short HEAD)" >> "$OUT/manifest.txt"   # resume: finished units are skipped
else
  {
    echo "experiment: $(basename "$HERE")"; echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
    echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"; echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
    echo "shard: $SHARD"; echo "workers: $WORKERS"; echo "host: $(uname -srm)"; echo "python: $($PY --version 2>&1)"
    echo "cadical: $(${CADICAL:-$HOME/bin/cadical} --version 2>&1 | head -1)"; echo "started_utc: $(date -u +%FT%TZ)"
  } > "$OUT/manifest.txt"
fi
$PY -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
finish() {
  rc=$?; T1=$(date +%s)
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $((T1 - T0))"
    echo "core_hours: $($PY -c "print(round($((T1 - T0)) * $WORKERS / 3600, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT
TYPES=$(echo "15 16 19 21 22 25 27 28 29 31 33 34 35 36 37 39 40 41 42 43 45 46 47 48 49 51 52 53 54 55 57 58" | tr " " "\n" | awk -v s="$SHARD" "(NR - 1) % 8 == s" | tr "\n" " ")   # the 32 types night 6 did not reach (E-261101-23 CONCLUSION)
cd "$ROOT/experiments/E-261101-23-k-face-subinstances-face-cegar"   # the E-261101-23 runner
nice -n 10 $PY kface_sweep.py --types $TYPES --ks 8 9 --timeouts 300 600 --out "$OUT"
# ---- exact verification: every UNSAT carries drat_trim VERIFIED and both hashes; every realized SAT model its planes ----
$PY - "$OUT/results.jsonl" <<'PYEOF'
import json, sys, collections
c = collections.Counter(); real = 0
for line in open(sys.argv[1]):
    r = json.loads(line); c[(r['k'], r['status'])] += 1; real += r.get('realized_wrong_signs') == 0
print('counts (k, status):', dict(c), '| realized k-face models:', real)
PYEOF
