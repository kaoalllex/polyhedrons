#!/usr/bin/env bash
HERE="$(cd "$(dirname "$0")" && pwd)"
"${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}" - "$HERE" <<'PY'
import collections, json, sys
from pathlib import Path
here=Path(sys.argv[1]); root=here/(here/'launch.results').read_text().strip()
rows=[json.loads(l) for p in root.glob('[0-9]*/results.jsonl') for l in p.read_text().splitlines()]
print(f"{len(rows)}/{len(json.loads((here/'queue.json').read_text())['maps'])} maps; {dict(collections.Counter(r['status'] for r in rows))}")
PY
