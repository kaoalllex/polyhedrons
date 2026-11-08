"""Strategy review 2026-11-08: (9,3) plain-formula outcomes by multiple-adjacency pattern.

Reads only committed data: the (9,3) census and the E-261103-03 tranche queue.  The solved
times are the UNSAT-VERIFIED plain cells recorded in E-261103-03 (CONCLUSION, STATUS 3e-3i);
every other attempted map timed out at 60 s (maps 0 and 1 also at 300 s).

Run from research/12-faced-polyhedron:  python3 reviews/strategy-review-2026-11-08-runtime-patterns.py
"""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3'
maps = json.loads((ROOT / 'experiments/E-261103-01-s5-map-census/results/maps_9_3.json').read_text())['maps']

SOLVED = {5: 22.5, 6: 27.0, 30: 30.4, 40: 75.7, 48: 62.5, 29: 29.3, 66: 29.6, 20: 30.5, 60: 32.1,
          58: 33.2, 59: 38.5, 52: 39.6, 90: 42.3, 83: 43.5, 43: 43.7, 67: 49.1, 31: 53.6, 75: 56.6, 19: 58.3}
queue = [m['index'] for m in json.loads((EXP / 'tranche_queue.json').read_text())['maps']]
attempted = set(queue) | {0, 1, 2, 3, 4, 5, 6, 7, 10, 30, 40, 48}

table = collections.defaultdict(lambda: [0, 0, 0])
for i, m in enumerate(maps):
    if not m['admissible']:
        continue
    key = (tuple(m['extra_pattern']), tuple(sorted(e[2] for e in m['extra_edges'])))
    table[key][0 if i in SOLVED else 1 if i in attempted else 2] += 1

print('face-excess pattern, pair multiplicities | solved | unresolved | unattempted')
for key, row in sorted(table.items()):
    print(key, row)
assert sum(r[0] for r in table.values()) == 19
assert sum(r[1] for r in table.values()) == 73
assert sum(r[2] for r in table.values()) == 111
print('admissible maps with a tripled pair:',
      sum(any(e[2] >= 3 for e in m['extra_edges']) for m in maps if m['admissible']))
