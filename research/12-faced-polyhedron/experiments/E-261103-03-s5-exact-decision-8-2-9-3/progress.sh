#!/usr/bin/env bash
# Progress of the item 1 launch (done / left / time left per shard); called by item1.sh status and overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
R="${RESULTS:-$HERE/results/item1b}"
SOLVER="${SOLVER_CAP:-1800}" CHECKER="${CHECKER_CAP:-2700}"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
ALIVE="$(for k in 0 1 2 3 4 5 6 7 8 9; do pgrep -f "run_overnight.py s5 .*--results-dir $R/$k " >/dev/null && echo -n "$k,"; done)" \
  "$PYTHON" - "$R" "$HERE/queue_item1b.json" "$SOLVER" "$CHECKER" <<'PY'
import json, os, sys, time
from collections import Counter
from pathlib import Path
R, queue, solver, checker = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())['maps'], float(sys.argv[3]), float(sys.argv[4])
done = {}
for p in R.glob('[0-9]*/results.jsonl'):
    for line in p.read_text().splitlines():
        r = json.loads(line); done[r['map_index']] = r
unit = solver + checker
alive = {int(x) for x in os.environ['ALIVE'].split(',') if x}
now = time.time(); rows = []; left_worst = left_cap = 0.0
for k in range(10):
    mine = [e['index'] for e in queue[k::10]]
    todo = [i for i in mine if i not in done]
    cur = None
    prog = R / str(k) / 'progress.jsonl'
    if todo and prog.exists():
        events = [json.loads(l) for l in prog.read_text().splitlines()]
        last = events[-1]['map_index'] if events else None
        if last == todo[0]:
            cur = (last, now - prog.stat().st_mtime)
    elapsed = cur[1] if cur else 0
    worst = len(todo) * unit - elapsed
    capped = len(todo) * solver - min(elapsed, solver)
    left_worst = max(left_worst, worst); left_cap = max(left_cap, capped)
    rows.append(f"shard {k}: {len(mine) - len(todo)}/{len(mine)} done" +
                (f", now map {cur[0]} for {cur[1] / 60:.0f} min" if cur else (", finished" if not todo else ", running" if k in alive else ", !! NOT RUNNING (run start)")) +
                (f", then {todo[1:]}" if len(todo) > 1 else ""))
print('\n'.join(rows))
c = Counter(r['status'] for r in done.values())
print(f"total: {len(done)}/{len(queue)} done {dict(c)}; {len(queue) - len(done)} left")
print(f"time left (busiest shard): at most {left_worst / 3600:.1f} h (every unit hits solver + checker caps), "
      f"about {left_cap / 3600:.1f} h if the remaining units all end at the solver cap")
print('decided:', ', '.join(f"{i}={r['status'][:5]}" for i, r in sorted(done.items(), key=lambda x: str(x[0]))))
PY
