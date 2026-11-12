#!/usr/bin/env bash
# Units recorded / queued, per-status counts and the running units; called by overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
R="${RESULTS:-$HERE/$(cat "$HERE/launch.results")}"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
"$PYTHON" - "$R" "$HERE" <<'PY'
import collections, json, sys
from pathlib import Path
R, here = Path(sys.argv[1]), Path(sys.argv[2])
queue = json.loads((here / 'queue.json').read_text())['maps']
recs = [json.loads(l) for p in sorted(R.glob('[0-9]*/results.jsonl')) for l in p.read_text().splitlines()]
started = [json.loads(l) for p in sorted(R.glob('[0-9]*/progress.jsonl')) for l in p.read_text().splitlines()]
done = {r['map_index'] for r in recs}
running = sorted({e['map_index'] for e in started} - done, key=str)
maps = collections.Counter(r['status'] for r in recs if isinstance(r['map_index'], int))
ctrl = collections.Counter(r['status'] for r in recs if not isinstance(r['map_index'], int))
flags = ''.join(f' {n.upper()}' for n in ('first_sat.json', 'stop.json') if (R / n).exists())
print(f'{len(recs)}/{len(queue)} units; maps {dict(maps)}; controls {dict(ctrl)}; running {running}{flags}')
PY
