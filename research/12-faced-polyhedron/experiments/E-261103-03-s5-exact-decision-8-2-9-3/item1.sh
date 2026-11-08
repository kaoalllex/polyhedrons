#!/usr/bin/env bash
# Item 1 long-cap launch on 10 shards: item1.sh start | status | stop  (resumable; recorded units are skipped).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
R="${RESULTS:-$HERE/results/item1b}"
SOLVER="${SOLVER_CAP:-1800}" CHECKER="${CHECKER_CAP:-2700}" BUDGET="${BUDGET:-91000}"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
export CADICAL="${CADICAL:-$HOME/bin/cadical}" DRAT_TRIM="${DRAT_TRIM:-$HOME/bin/drat-trim}"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
RUN="$ROOT/overnight/run_overnight.py"
case "${1:-}" in
  start)
    if pgrep -f "run_overnight.py s5 .*--results-dir $R/" >/dev/null; then echo 'already running'; exit 1; fi
    mkdir -p "$R"
    for k in 0 1 2 3 4 5 6 7 8 9; do
      nohup caffeinate -dimsu nice -n 10 "$PYTHON" "$RUN" s5 --workers 1 --shard "$k" --shards 10 \
        --results-dir "$R/$k" --s5-queue "$HERE/queue_item1b.json" --timeout "$SOLVER" \
        --s5-checker-timeout "$CHECKER" --s5-budget-seconds "$BUDGET" >> "$R/run.$k.log" 2>&1 &
    done
    echo "started 10 shards, results in $R" ;;
  status)
    echo "running shards: $(pgrep -f "run_overnight.py s5 .*--results-dir $R/" | wc -l) python procs, $(pgrep -x cadical | wc -l) cadical, $(pgrep -x drat-trim | wc -l) drat-trim"
    for f in stop.json first_sat.json; do [ -e "$R/$f" ] && { echo "!! $f:"; cat "$R/$f"; echo; }; done
    echo '--- decided units (map, status, solver s)'
    cat "$R"/[0-9]*/results.jsonl 2>/dev/null | "$PYTHON" -c "
import sys, json
rows = [json.loads(l) for l in sys.stdin]
for r in sorted(rows, key=lambda r: str(r['map_index'])):
    print(r['map_index'], r['status'], round(r.get('seconds', 0)))
from collections import Counter
print('total', len(rows), dict(Counter(r['status'] for r in rows)))"
    echo '--- last line per shard'
    for k in 0 1 2 3 4 5 6 7 8 9; do echo "$k: $(tail -n1 "$R/run.$k.log" 2>/dev/null)"; done ;;
  stop)
    pkill -TERM -f "run_overnight.py s5 .*--results-dir $R/" || echo 'nothing running'
    echo 'sent SIGTERM; wait ~30 s and check status (units in progress are redone on the next start)' ;;
  *) echo 'Usage: item1.sh start|status|stop' >&2; exit 2 ;;
esac
