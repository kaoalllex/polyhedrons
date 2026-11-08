"""Build queue_probe.json for the (10,4) cost probe (PLAN.md): one random map per fast pattern at 300/450 s, two per slow
pattern at 1800/2700 s, and a positive and a negative control-f10 copy for each of the 10 shards (shard s runs the
entries s, 10 + s, 20 + s of the list).  Usage: python3 make_queue.py [--check]"""
import hashlib
import json
from pathlib import Path
import random
import sys

from pattern_census import CENSUS, pattern

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
SEED = 2611080701
FAST = ['(1, 1, 2, 2) (2, 2, 2)', '(1, 1, 2, 2) (2, 3)', '(1, 1, 1, 3) (2, 2, 2)', '(1, 2, 3) (2, 3)',
        '(2, 2, 2) (2, 2, 2)', '(3, 3) (4,)']
SLOW = ['(1, 1, 1, 1, 2) (2, 2, 2)', '(1, 1, 1, 1, 1, 1) (2, 2, 2)']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    census = CENSUS / 'maps_10_4.json'
    maps = json.loads(census.read_text())['maps']
    rng = random.Random(SEED)
    picks = []
    for p, k, caps in [(p, 1, (300, 450)) for p in FAST] + [(p, 2, (1800, 2700)) for p in SLOW]:
        pool = [i for i, m in enumerate(maps) if m['admissible'] and pattern(m) == p]
        for i in sorted(rng.sample(pool, k)):
            picks.append(dict(index=i, pattern=p, solver_cap=caps[0], checker_cap=caps[1],
                              canonical_sha256=hashlib.sha256(json.dumps(maps[i]['code'], separators=(',', ':')).encode()).hexdigest()))
    assert len(picks) == 10
    control = sha(RUNNER / 'control_f10.json')
    controls = [dict(index=f'control-f10{neg}-s{s}', control=kind, control_sha256=control, solver_cap=60, checker_cap=120)
                for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(10)]
    data = dict(target='S5 (10,4) cost probe, E-261103-07 PLAN.md', case=[10, 4], census_sha256=sha(census),
                control_file='control_f10.json', seed=SEED, maps=controls + picks)
    path = HERE / 'queue_probe.json'
    text = json.dumps(data, indent=1) + '\n'
    if '--check' in sys.argv:
        assert path.read_text() == text
    else:
        path.write_text(text)
    for p in picks:
        print(p['index'], p['pattern'], p['solver_cap'])


if __name__ == '__main__':
    main()
