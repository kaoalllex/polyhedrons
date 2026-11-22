#!/usr/bin/env bash
# Progress of the (9, 5) pass-1 launch (amendment 6): records and statuses per chunk; called by overnight/launch.sh status.
HERE="$(cd "$(dirname "$0")" && pwd)"
PYTHON="${PYTHON:-$HOME/.venvs/polyhedra/bin/python}"
"$PYTHON" - "$HERE" "${CHUNKS:-0-9}" <<'PY'
import json, sys
from collections import Counter
from pathlib import Path
here, (a, b) = Path(sys.argv[1]), sys.argv[2].split('-')
man = json.loads((here / 'pass1_9_5.json').read_text())['chunks']
total, planned = Counter(), 0
for k in range(int(a), int(b) + 1):
    n = man[str(k)]['records']; planned += n; c = Counter()
    for p in (here / 'results' / ('stageB5-pass1-c%03d' % k)).glob('[0-9]/results.jsonl'):
        for line in p.read_text().splitlines():
            r = json.loads(line)
            c['control' if str(r['map_index']).startswith('control') else r['status']] += 1
    total += c
    print('chunk %3d: %5d of %d maps %s' % (k, sum(v for s, v in c.items() if s != 'control'), n, dict(c)))
done = sum(v for s, v in total.items() if s != 'control')
print('all: %d of %d maps (%.1f%%) %s' % (done, planned, 100 * done / planned, dict(total)))
PY
