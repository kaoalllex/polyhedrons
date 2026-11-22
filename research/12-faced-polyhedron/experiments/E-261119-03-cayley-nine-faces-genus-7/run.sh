#!/usr/bin/env bash
# Session run (minutes): bash run.sh stage_a -> results/census/; bash run.sh stage_b -> results/formulas/ (only on
# admissible classes, PLAN.md). Outputs are never overwritten.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
WORKERS="${WORKERS:-10}"
STAGE="${1:?stage_a or stage_b}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMBA_NUM_THREADS=1
export SAT_SOLVER="${SAT_SOLVER:-$HOME/bin/kissat}" NO_PROOF=1
provenance() {
  { echo "commit: $(git -C "$ROOT" rev-parse HEAD)"; echo "dirty_files: $(git -C "$ROOT" status --porcelain -- "$HERE" | wc -l | tr -d ' ')"
    echo "branch: $(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"; echo "host: $(uname -srm)"; echo "python: $("$PYTHON" --version 2>&1)"
    echo "solver: $SAT_SOLVER $(shasum -a 256 "$SAT_SOLVER" | cut -d' ' -f1)"; echo "started_utc: $(date -u +%FT%TZ)"; } > "$1.manifest.txt"
}
cd "$HERE"
case "$STAGE" in
  stage_a) OUT="$HERE/results/census"; [[ ! -e "$OUT" ]] || { echo "$OUT exists" >&2; exit 2; }
    mkdir -p "$HERE/results"; "$PYTHON" -m unittest test_cayley7; provenance "$OUT"; T0=$(date +%s)
    "$PYTHON" cayley7.py stage_a "$OUT" "$WORKERS" ;;
  stage_b) OUT="$HERE/results/formulas"; [[ ! -e "$OUT" ]] || { echo "$OUT exists" >&2; exit 2; }
    grep -q '"PASS": true' "$HERE/results/census/census.json" || { echo "stage A missing or failed" >&2; exit 2; }
    provenance "$OUT"; T0=$(date +%s)
    nice -n 10 "$PYTHON" cayley7.py stage_b "$OUT" "${CAP:-120}" ;;
  *) exit 2 ;;
esac
echo "wall_seconds: $(( $(date +%s) - T0 ))" >> "$OUT.manifest.txt"
