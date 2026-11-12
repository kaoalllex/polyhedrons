"""Build queue.json of PLAN.md: in every one of the 10 shards a positive and a negative pinned-plane control, then the
358 stratum C maps of (10,4) in the registered pattern order (census index order within a pattern); shard s runs
entries s, 10 + s, ...  Maps 146 and 845 are excluded (E-261108-03 kissat records).  Usage: python3 make_queue.py [--check]"""
import collections
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
CENSUS = HERE.parent / 'E-261103-01-s5-map-census/results/maps_10_4.json'
SHARDS = 10
SOLVER_CAP, CHECKER_CAP = 3600, 60  # no proof: the checker cap is unused
ORDER = ['(1, 2, 3) (2, 3)', '(1, 1, 1, 3) (2, 2, 2)', '(1, 1, 2, 2) (2, 3)', '(1, 1, 2, 2) (2, 2, 2)',
         '(2, 2, 2) (2, 2, 2)', '(3, 3) (4,)']
COUNTS = [38, 58, 70, 186, 7, 1]
REUSED = {146: '(2, 2, 2) (2, 2, 2)', 845: '(1, 2, 3) (2, 3)'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pattern(m):  # the definition of E-261103-07 pattern_census.py
    return '%s %s' % (tuple(sorted(x for x in m['extra_pattern'] if x)), tuple(sorted(e[2] for e in m['extra_edges'])))


def queue():
    records = json.loads(CENSUS.read_text())['maps']
    by = collections.defaultdict(list)
    for i, m in enumerate(records):
        if m['admissible']:
            by[pattern(m)].append(i)
    assert [len(by[p]) for p in ORDER] == COUNTS and sum(COUNTS) == 360
    assert all(i in by[p] for i, p in REUSED.items())
    control = dict(control_sha256=sha(RUNNER / 'control_f10.json'), solver_cap=60, checker_cap=120)
    rows = [dict(index=f'control-f10{neg}-s{s}', control=kind, **control)
            for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(SHARDS)]
    for p in ORDER:
        for i in by[p]:
            if i not in REUSED:
                code = json.dumps(records[i]['code'], separators=(',', ':')).encode()
                rows.append(dict(index=i, pattern=p, solver_cap=SOLVER_CAP, checker_cap=CHECKER_CAP,
                                 canonical_sha256=hashlib.sha256(code).hexdigest()))
    return dict(target='S5 (10,4) E-261109-06 PLAN.md, stratum C, kissat, no proof', case=[10, 4],
                census_sha256=sha(CENSUS), control_file='control_f10.json', shards=SHARDS, maps=rows)


def main():
    path = HERE / 'queue.json'
    text = json.dumps(queue(), indent=1) + '\n'
    if '--check' in sys.argv:
        assert path.read_text() == text, path
    else:
        path.write_text(text)
    maps = json.loads(text)['maps']
    n = [len([e for e in maps[s::SHARDS] if isinstance(e['index'], int)]) for s in range(SHARDS)]
    print(path.name, 'sha256', sha(path), 'maps', sum(n), 'per shard', n)


if __name__ == '__main__':
    main()
