#!/usr/bin/env bash
# E-261118-04 shard runner (PLAN.md): 1827 deleted-face formulas, kissat, no proof, cap CAP s per formula, BUDGET solver
# seconds per shard over all restarts; results/<SHARD>/results.jsonl (a restart skips the recorded units of every shard).
# Owner launch from the repo root: bash research/12-faced-polyhedron/overnight/launch.sh 261118-04 start|status|stop
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
SHARD="${1:-0}"
SHARDS="${SHARDS:-10}"
OUT="$HERE/results/$SHARD"
mkdir -p "$OUT"
{
  echo "started_utc: $(date -u +%FT%TZ) shard $SHARD of $SHARDS"
  echo "commit: $(git -C "$ROOT" rev-parse HEAD) dirty_files: $(git -C "$ROOT" status --porcelain | wc -l | tr -d ' ')"
  echo "host: $(uname -srm) python: $("$PYTHON" --version 2>&1)"
  echo "solver: ${SAT_SOLVER:-$HOME/bin/kissat} sha256: $(shasum -a 256 "${SAT_SOLVER:-$HOME/bin/kissat}" | cut -d' ' -f1)"
} >> "$OUT/manifest.txt"
rc=0
trap 'echo "finished_utc: $(date -u +%FT%TZ) exit_status: $rc" >> "$OUT/manifest.txt"' EXIT
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export NO_PROOF=1 SAT_SOLVER="${SAT_SOLVER:-$HOME/bin/kissat}" SOLVER_OPTS=""
nice -n 10 "$PYTHON" "$HERE/sieve.py" --shard "$SHARD" --shards "$SHARDS" --cap "${CAP:-300}" \
  --budget "${BUDGET:-360}" --out "$OUT" || rc=$?
exit $rc
