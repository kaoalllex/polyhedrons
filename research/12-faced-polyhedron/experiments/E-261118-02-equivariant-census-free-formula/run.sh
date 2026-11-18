#!/usr/bin/env bash
# E-261118-02 (PLAN.md). Controls (session): bash run.sh controls -> results/controls/.
# Rung (owner, laptop, <= 5.6 core-h, about 45 min wall): bash research/12-faced-polyhedron/overnight/launch.sh 261118-02 start
#   shard 0: D2 2 x 4 (5 workers, 30 min), shard 1: S4 2 x 4 (5 workers, 30 min), shard 2: plain cube 5 (8 workers,
#   <= 15 min, after both, within the budget); other shards idle. Pilot: PILOT=1 bash run.sh 0 (and 1) -> results/pilot/.
#   Then: python3 p3sym.py summary results
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARD="${1:?controls or a numeric shard}"
SHARDS="${SHARDS:-10}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cd "$HERE"
if [[ "$SHARD" == controls ]]; then
  exec "$PYTHON" p3sym.py controls "$HERE/results/controls"
fi
[[ "$SHARDS" -ge 3 && "$SHARD" =~ ^[0-9]+$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
UNITS=(D2_8_36 S4_8_36 plain_cube5_8_36)
[[ "$SHARD" -lt 3 ]] || { echo "shard $SHARD idle (three units on shards 0-2)"; exit 0; }
grep -q '"PASS": true' "$HERE/results/controls/controls.json" 2>/dev/null || { echo "controls missing or failed" >&2; exit 2; }
if [[ -n "${PILOT:-}" ]]; then OUT="$HERE/results/pilot/$SHARD"; export P3SYM_CAP="${PILOT_CAP:-120}"; else OUT="$HERE/results/$SHARD"; fi
mkdir -p "$OUT"
{
  echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS unit ${UNITS[$SHARD]}"
  echo "commit: $(git -C "$ROOT" rev-parse HEAD) dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
  echo "host: $(uname -srm) python: $("$PYTHON" --version 2>&1)"
} >> "$OUT/manifest.txt"
rc=0
trap 'echo "finished_utc: $(date -u +%FT%TZ) exit_status: $rc" >> "$OUT/manifest.txt"' EXIT
nice -n 10 "$PYTHON" p3sym.py unit "${UNITS[$SHARD]}" "$OUT" || rc=$?
exit $rc
