#!/usr/bin/env bash
# Progress of the sweep (done / left / verdicts); called by overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
"$PYTHON" - "$HERE/results" <<'PY'
import json, sys
from collections import Counter
from pathlib import Path
rows = [json.loads(l) for p in sorted(Path(sys.argv[1]).glob('[0-9]*/results.jsonl')) for l in p.read_text().splitlines()]
ctl = [json.loads(l) for p in sorted(Path(sys.argv[1]).glob('[0-9]*/controls.jsonl')) for l in p.read_text().splitlines()]
print(f"units: {len(rows)}/300 done; verdicts {dict(Counter(r['verdict'] for r in rows))}; SOLID {sum(r['solid'] for r in rows)}")
print('by family:', dict(Counter(r['unit'].split('_')[0] for r in rows)))
print(f"core-h so far: {sum(r['wall_seconds'] for r in rows + ctl) / 3600:.2f} of 2.0; controls failed: {sum(not c['passed'] for c in ctl)}")
PY
