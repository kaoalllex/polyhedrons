"""Count the (10,4) census maps by multiple-adjacency pattern (no solving).

Pattern = (sorted nonzero extra adjacencies per face, sorted multiplicities of the multiple pairs); the same
definition reproduces every pattern label of E-261103-03's queue_item5a.json for (9,3)."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / 'experiments/E-261103-01-s5-map-census/results'


def pattern(m):
    return '%s %s' % (tuple(sorted(x for x in m['extra_pattern'] if x)), tuple(sorted(e[2] for e in m['extra_edges'])))


def main():
    maps = json.loads((CENSUS / 'maps_10_4.json').read_text())['maps']
    adm = [m for m in maps if m['admissible']]
    q = json.loads((ROOT / 'experiments/E-261103-03-s5-exact-decision-8-2-9-3/queue_item5a.json').read_text())
    m93 = json.loads((CENSUS / 'maps_9_3.json').read_text())['maps']
    assert all(pattern(m93[x['index']]) == x['pattern'] for x in q['maps'] if 'pattern' in x)
    every = collections.Counter(pattern(m) for m in maps)
    print('classes', len(maps), 'admissible', len(adm))
    for p, n in collections.Counter(pattern(m) for m in adm).most_common():
        aut = collections.Counter(m['aut_plus'] for m in adm if pattern(m) == p)
        print(f'{p:30} admissible {n:4}  all {every[p]:4}  aut+ {dict(sorted(aut.items()))}')


if __name__ == '__main__':
    main()
