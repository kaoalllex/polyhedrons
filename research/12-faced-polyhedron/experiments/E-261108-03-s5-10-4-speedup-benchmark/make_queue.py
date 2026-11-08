"""Build the five queues of PLAN.md (queue_{kissat,unsat}-{A,B}.json, queue_default-B.json) for exactly 10 shards: in every shard a positive and
a negative pinned-plane control, then at most one map on the shard PLAN.md assigns (shard s runs entries s, 10 + s, ...;
a filler positive control keeps a map on its shard).  Usage: python3 make_queue.py [--check]"""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
CENSUS = HERE.parent / 'E-261103-01-s5-map-census/results'
SHARDS = 10
CAPS_A, CAPS_B = (1800, 60), (14400, 60)  # amendment 2 of PLAN.md: solver caps, no proof (checker cap unused)
PHASES = {'A': dict(case=[9, 3], control='control_f9.json', tag='f9', caps=CAPS_A, maps=[7, 165, 87, 130, 29, 184]),
          'B': dict(case=[10, 4], control='control_f10.json', tag='f10', caps=CAPS_B, maps=[96, 85, 146, 845])}
ON_SHARDS = {('kissat', 'A'): [4, 5, 6, 7, 8, 9], ('unsat', 'A'): [0, 1, 2, 3, 8, 9], ('kissat', 'B'): [0, 1, 2, 3],
             ('unsat', 'B'): [4, 5, 6, 7], ('default', 'B'): [8, 9]}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def queue(variant, phase):
    p = PHASES[phase]
    census = CENSUS / f'maps_{p["case"][0]}_{p["case"][1]}.json'
    records = json.loads(census.read_text())['maps']
    control = dict(control_sha256=sha(RUNNER / p['control']), solver_cap=60, checker_cap=120)
    rows = [[dict(index=f'control-{p["tag"]}{neg}-s{s}', control=kind, **control) for s in range(SHARDS)]
            for neg, kind in [('', 'positive'), ('-neg', 'negative')]]
    on = ON_SHARDS[variant, phase]
    maps = dict(zip(on, p['maps']))
    row = []
    for s in range(max(on) + 1):
        if s not in maps:
            row.append(dict(index=f'control-{p["tag"]}-x-s{s}', control='positive', **control)); continue
        i = maps[s]
        assert records[i]['admissible']
        row.append(dict(index=i, solver_cap=p['caps'][0], checker_cap=p['caps'][1],
                        canonical_sha256=hashlib.sha256(json.dumps(records[i]['code'], separators=(',', ':')).encode()).hexdigest()))
    return dict(target=f'S5 E-261108-03 PLAN.md, variant {variant}, phase {phase}', case=p['case'],
                census_sha256=sha(census), control_file=p['control'], shards=SHARDS, maps=rows[0] + rows[1] + row)


def main():
    for variant, phase in ON_SHARDS:
        path = HERE / f'queue_{variant}-{phase}.json'
        text = json.dumps(queue(variant, phase), indent=1) + '\n'
        if '--check' in sys.argv:
            assert path.read_text() == text, path
        else:
            path.write_text(text)
        maps = json.loads(text)['maps']
        print(path.name, {s: [e['index'] for e in maps[s::SHARDS] if isinstance(e['index'], int)] for s in range(SHARDS)})


if __name__ == '__main__':
    main()
