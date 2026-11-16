#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
"${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}" - "$HERE" <<'PYTHON'
import collections,json,sys
from pathlib import Path
here=Path(sys.argv[1]); root=here/(here/'launch.results').read_text().strip()
queue=json.loads((here/'queue.json').read_text())
rows=[json.loads(l) for p in root.glob('[0-9]*/results.jsonl') for l in p.read_text().splitlines()]
print(f"{len(rows)}/{len(queue['maps'])} fresh maps; {dict(collections.Counter(r['status'] for r in rows))}; pilot #1/#2 reused")
if (root/'budget.json').exists():
    spent=sum(json.loads((root/'budget.json').read_text()).values())/3600
    print(f'charged/reserved worker-h: {spent:.3f}/79 production; remaining: {max(0,79-spent):.3f}')
for path in root.glob('[0-9]*/progress.jsonl'):
    progress=[json.loads(l) for l in path.read_text().splitlines()]
    done={r['map_index'] for r in rows}
    pending=[r['map_index']+1 for r in progress if r['map_index'] not in done]
    if pending: print(f'shard {path.parent.name}: Lutz #{pending[-1]} started, not yet recorded')
if (root/'first_sat.json').exists(): print('SAT saved; coverage stopped, thirty-model bridge pending')
if (root/'stop.json').exists(): print('ERROR stop; review required')
PYTHON
