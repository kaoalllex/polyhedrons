#!/usr/bin/env bash
# Runner for one shard of this experiment: bash run.sh [SHARD]
# Laptop: caffeinate -dimsu bash run.sh 0      GitHub Actions: .github/workflows/experiment.yml calls it per shard.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
SHARD="${1:-0}"
WORKERS="${WORKERS:-1}"
PY="${PY:-$HOME/.venvs/polyhedra/bin/python}"
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
T0=$(date +%s)
{
  echo "experiment: $(basename "$HERE")"; echo "commit: $(git -C "$ROOT" rev-parse HEAD)"
  echo "dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"; echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  echo "shard: $SHARD"; echo "workers: $WORKERS"; echo "host: $(uname -srm)"; echo "python: $($PY --version 2>&1)"
  echo "started_utc: $(date -u +%FT%TZ)"
} > "$OUT/manifest.txt"
$PY -m pip freeze > "$OUT/pip-freeze.txt" 2>/dev/null || true
finish() {
  rc=$?; T1=$(date +%s)
  { echo "finished_utc: $(date -u +%FT%TZ)"; echo "exit_status: $rc"; echo "wall_seconds: $((T1 - T0))"
    echo "core_hours: $($PY -c "print(round($((T1 - T0)) * $WORKERS / 3600, 3))")"; } >> "$OUT/manifest.txt"
}
trap finish EXIT
# ---- the experiment: shard = a slice of the class seeds (type taken from each seed file) ----
cd "$HERE"
SEEDS=$(ls "$ROOT"/experiments/E-261030-11-normals-first-night-runs/results/n5/class_seeds/*.json | awk -v s="$SHARD" 'NR % 10 == s')
for f in $SEEDS; do
  T=$($PY -c "import json,sys; print(json.load(open(sys.argv[1]))['type_id'])" "$f")
  $PY chirotope_first.py run --type "$T" --seeds "$f" --timeout 120 --rounds 40 --out "$OUT/results.jsonl" || true
done
# ---- exact verification of anything found: every record with result EMBEDDED carries its planes ----
$PY - "$OUT/results.jsonl" <<'PYEOF'
import json, sys
n = emb = 0
for line in open(sys.argv[1]):
    r = json.loads(line); n += 1; emb += r.get('result') == 'EMBEDDED'
print('records', n, 'EMBEDDED', emb, '(run verify_candidate.py --target S0 on each EMBEDDED record before calling it anything)')
PYEOF
