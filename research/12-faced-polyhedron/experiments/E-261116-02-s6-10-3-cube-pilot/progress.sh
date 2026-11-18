#!/usr/bin/env bash
HERE="$(cd "$(dirname "$0")" && pwd)"
"${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}" - "$HERE" <<'PYTHON'
import collections,json,sys
from pathlib import Path
root=Path(sys.argv[1])/'results/run'
rows=[json.loads(l) for p in root.glob('[0-9]*/results.jsonl') for l in p.read_text().splitlines()]
print(f"{len(rows)}/258 units; {dict(collections.Counter(r['status'] for r in rows))}")
if (root/'budget.json').exists():
    print('charged/reserved core-h:',sum(json.loads((root/'budget.json').read_text()).values())/3600)
PYTHON
