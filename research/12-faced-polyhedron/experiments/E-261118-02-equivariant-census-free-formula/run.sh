#!/usr/bin/env bash
# E-261118-02 (PLAN.md). Controls (session): bash run.sh controls -> results/controls/.
# Owner run (amendment 1; <= 17 core-h, <= 2.3 h wall): bash research/12-faced-polyhedron/overnight/launch.sh 261118-02 start
#   shards 0, 1: C3 3+3+3 at nine faces, E = 45, 51 (5 workers, 1 h); shard 2: E = 57 after E = 45; shard 3: plain
#   cube 5 at eight faces (8 workers, <= 15 min) after the three; other shards idle. Then: python3 p3sym.py summary results
# STAGE=rung maps shards 0-2 to the registered rung (D2, S4, plain cube 5). Pilots: PILOT=1 [PILOT_DIR=..] [PILOT_CAP=s]
#   bash run.sh SHARD -> results/<PILOT_DIR or pilot>/SHARD (the rung pilot: STAGE=rung PILOT=1, shards 0 and 1).
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
if [[ "${STAGE:-nine}" == rung ]]; then UNITS=(D2_8_36 S4_8_36 plain_cube5_8_36); else UNITS=(C3_9_45 C3_9_51 C3_9_57 plain_cube5_8_36); fi
[[ "$SHARDS" -ge ${#UNITS[@]} && "$SHARD" =~ ^[0-9]+$ && "$SHARD" -lt "$SHARDS" ]] || exit 2
[[ "$SHARD" -lt ${#UNITS[@]} ]] || { echo "shard $SHARD idle (${#UNITS[@]} units on the first shards)"; exit 0; }
grep -q '"PASS": true' "$HERE/results/controls/controls.json" 2>/dev/null || { echo "controls missing or failed" >&2; exit 2; }
if [[ -n "${PILOT:-}" ]]; then OUT="$HERE/results/${PILOT_DIR:-pilot}/$SHARD"; export P3SYM_CAP="${PILOT_CAP:-120}"; else OUT="$HERE/results/$SHARD"; fi
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
