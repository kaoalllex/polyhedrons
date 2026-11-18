#!/usr/bin/env bash
# Progress of the night (units per arm and E, statuses, hits, core-h); called by overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-${VIRTUAL_ENV:-$HOME/.venvs/polyhedra}/bin/python}"
"$PYTHON" - "$HERE/results" <<'PY'
import json, sys
from collections import Counter
from pathlib import Path
rows = []
for p in sorted(Path(sys.argv[1]).glob('[0-9]*/results.jsonl')):
    for l in p.read_text().splitlines():
        try:
            rows.append(json.loads(l))
        except json.JSONDecodeError:
            pass
for k in sorted({(r['arm'], r['edges']) for r in rows}):
    rs = [r for r in rows if (r['arm'], r['edges']) == k]
    print('%-5s E=%d: %5d units %s, nine-face hits %d' % (k[0], k[1], len(rs), dict(Counter(r['status'] for r in rs)),
          sum(bool(r.get('EMBEDDED') and r.get('all_pairs') and len(r['planes']) == 9) for r in rs)))
print('core-h so far: %.2f of 80; engine errors: %d; stop requested: %s' % (
    sum(r['seconds'] for r in rows) / 3600, sum(r['status'] == 'ENGINE_ERROR' for r in rows),
    (Path(sys.argv[1]) / 'stop.requested').exists()))
PY
