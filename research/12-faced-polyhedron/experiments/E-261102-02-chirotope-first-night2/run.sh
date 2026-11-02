#!/usr/bin/env bash
# Runner for one shard of this experiment: SHARDS=N bash run.sh SHARD   (shard s takes every N-th class seed; default N = 10)
# Laptop: bash overnight/launch.sh start experiments/E-261102-02-chirotope-first-night2 CORES   (sets SHARDS=CORES)      GitHub Actions: .github/workflows/experiment.yml calls it per shard.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SHARD="${1:-0}"
SHARDS="${SHARDS:-10}"
WORKERS="${WORKERS:-1}"
PY="${PY:-$HOME/.venvs/polyhedra/bin/python}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1   # one core per process on the M4 Pro
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
T0=$(date +%s)
if [ -f "$OUT/manifest.txt" ]; then
  echo "restarted_utc: $(date -u +%FT%TZ) commit: $(git -C "$ROOT" rev-parse --short HEAD) shards: $SHARDS" >> "$OUT/manifest.txt"   # resume: finished units are skipped
else
  {
    echo "experiment: $(basename "$HERE")"; echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
    echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"; echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
    echo "shard: $SHARD of $SHARDS"; echo "workers: $WORKERS"; echo "host: $(uname -srm)"; echo "python: $($PY --version 2>&1)"
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
# ---- the experiment: shard = a slice of the class seeds (type taken from each seed file) ----
cd "$ROOT/experiments/E-261101-25-chirotope-first"   # the E-261101-25 engine
SEEDS=$(ls "$ROOT"/experiments/E-261030-11-normals-first-night-runs/results/n5/class_seeds/*.json | awk -v s="$SHARD" -v n="$SHARDS" 'NR % n == s')
for f in $SEEDS; do
  T=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['type_id'])" "$f")
  # a seed recorded by any shard (also under another shard count) is not run again
  if grep -qsF "\"tag\": \"type$T-$(basename "$f")\"" "$HERE"/results/*/results.jsonl; then echo "skip $(basename "$f"): recorded"; continue; fi
  nice -n 10 $PY chirotope_first.py run --type "$T" --seeds "$f" --ladder 7 --alt 20 --timeout 60 --rounds 40 --readd 1000 --realize-restarts 6 --block 1 --realizer two-stage --simple 1 --fp 1 --seed-minutes 40 --progress "$OUT/progress.jsonl" --out "$OUT/results.jsonl" || true
done
# ---- exact verification of anything found: every record with result EMBEDDED carries its planes ----
$PY - "$OUT/results.jsonl" <<'PYEOF'
import json, sys
n = emb = 0
for line in open(sys.argv[1]):
    r = json.loads(line); n += 1; emb += r.get('result') == 'EMBEDDED'
print('records', n, 'EMBEDDED', emb, '(run verify_candidate.py --target S0 on each EMBEDDED record before calling it anything)')
PYEOF
