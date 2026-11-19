#!/usr/bin/env bash
# E-261119-01 (PLAN.md). Controls (session): bash run.sh controls -> results/controls/.
# Owner run (<= 17.5 core-h, about 2.0 h wall): bash research/12-faced-polyhedron/overnight/launch.sh 261119-01 start
#   shard 0: free C2 at (8, 36) with map blocking (5 workers, 1.5 h) and shard 1: free C2 at (8, 30) (1 h) together;
#   shard 2: C3 3+3+3 at (9, 39) after shard 1 (<= 1 h, what the budget leaves); other shards idle. Then:
#   python3 ladder.py summary results. U4 (D2, S4 with blocking) was decided in the pilot (amendment 2): UNITSET=u4.
# Pilots: PILOT=1 [PILOT_DIR=..] [PILOT_CAP=s] bash run.sh SHARD -> results/<PILOT_DIR or pilot>/SHARD.
#   UNITSET=blockctl maps shards 0, 1 to the unpinned blocking controls (one known map blocked from the start);
#   UNITSET=u4 maps shards 0, 1 to D2 and S4 at (8, 36) with blocking.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARD="${1:?controls or a numeric shard}"
SHARDS="${SHARDS:-10}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
cd "$HERE"
if [[ "$SHARD" == controls ]]; then
  exec "$PYTHON" ladder.py controls "$HERE/results/controls"
fi
case "${UNITSET:-run}" in
  blockctl) UNITS=(C2_8_36_pre_rv C2_8_36_pre_mz) ;;
  u4) UNITS=(D2_8_36_block S4_8_36_block) ;;
  *) UNITS=(C2_8_36_block C2_8_30 C3_9_39) ;;
esac
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
nice -n 10 "$PYTHON" ladder.py unit "${UNITS[$SHARD]}" "$OUT" || rc=$?
exit $rc
