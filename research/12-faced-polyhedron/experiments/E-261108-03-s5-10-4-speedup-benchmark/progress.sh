#!/usr/bin/env bash
# Per root (variant-phase): units recorded / queued and each map record so far; called by overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
R="${RESULTS:-$HERE/$(cat "$HERE/launch.results")}"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
"$PYTHON" - "$R" "$HERE" <<'PY'
import json, sys
from pathlib import Path
R, here = Path(sys.argv[1]), Path(sys.argv[2])
for name in ('kissat-A', 'unsat-A', 'kissat-B', 'unsat-B'):
    queue = json.loads((here / f'queue_{name}.json').read_text())['maps']
    recs = [json.loads(l) for p in sorted((R / name).glob('[0-9]*/results.jsonl')) for l in p.read_text().splitlines()]
    started = [json.loads(l) for p in sorted((R / name).glob('[0-9]*/progress.jsonl')) for l in p.read_text().splitlines()]
    done = {r['map_index'] for r in recs}
    running = sorted({e['map_index'] for e in started} - done, key=str)
    maps = ' '.join(f"{r['map_index']}:{r['status']}@{r['seconds'] + r.get('checker_seconds', 0):.0f}s" for r in recs
                    if isinstance(r['map_index'], int))
    stop = ' STOP: ' + json.loads((R / name / 'stop.json').read_text())['error'][:80] if (R / name / 'stop.json').exists() else ''
    print(f'{name}: {len(recs)}/{len(queue)} units, running {running} | maps {maps or "-"}{stop}')
PY
