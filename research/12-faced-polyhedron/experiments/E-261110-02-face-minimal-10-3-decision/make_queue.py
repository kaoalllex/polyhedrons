"""Build the queues of PLAN.md: queue.json (night: in each of 10 shards a positive and a negative pinned convex 10-face
control, then the 20 imported (10,3) maps in Lutz order, shard s runs entries s, 10 + s, ...; solver cap 3600 s, no
proof, so the checker cap is unused) and queue_pilot.json (the recorded prep pilot with DRAT: 2 shards, the controls,
then Lutz #1 and #2 at a 1200 s cap).
Usage: python3 make_queue.py [--check]"""
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNNER = HERE.parent / 'E-261103-03-s5-exact-decision-8-2-9-3'
MAPS = HERE / 'maps/maps_10_3.json'
SOLVER_CAP, CHECKER_CAP = 3600, 60  # no proof (owner, 2026-11-13)
PILOT_SOLVER_CAP, PILOT_CHECKER_CAP = 1200, 2400


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def queue(shards, maps, solver_cap, checker_cap, target):
    records = json.loads(MAPS.read_text())['maps']
    assert len(records) == 20 and [r['lutz'] for r in records] == list(range(1, 21))
    control = dict(control_sha256=sha(RUNNER / 'control_f10.json'), solver_cap=60, checker_cap=120)
    rows = [dict(index=f'control-f10{neg}-s{s}', control=kind, **control)
            for neg, kind in [('', 'positive'), ('-neg', 'negative')] for s in range(shards)]
    rows += [dict(index=i, lutz=records[i]['lutz'], solver_cap=solver_cap, checker_cap=checker_cap,
                  canonical_sha256=records[i]['canonical_sha256']) for i in maps]
    return dict(target=target, target_check='S6', case=[10, 3], maps_file=str(MAPS.relative_to(ROOT)),
                maps_sha256=sha(MAPS), control_file='control_f10.json', shards=shards, maps=rows)


def main():
    built = {'queue.json': queue(10, range(20), SOLVER_CAP, CHECKER_CAP,
                                 'S6 (10,3) E-261110-02 PLAN.md, 20 maps, kissat, no proof, submap=True'),
             'queue_pilot.json': queue(2, [0, 1], PILOT_SOLVER_CAP, PILOT_CHECKER_CAP,
                                       'S6 (10,3) E-261110-02 prep pilot, Lutz #1 and #2 at 1200 s')}
    for name, data in built.items():
        path, text = HERE / name, json.dumps(data, indent=1) + '\n'
        if '--check' in sys.argv:
            assert path.read_text() == text, path
        else:
            path.write_text(text)
        n = [len([e for e in data['maps'][s::data['shards']] if isinstance(e['index'], int)]) for s in range(data['shards'])]
        print(name, 'sha256', sha(path), 'maps', sum(n), 'per shard', n)


if __name__ == '__main__':
    main()
